from __future__ import annotations

import json
import math
import time
from collections import defaultdict
from pathlib import Path

import requests

R45 = Path('research_outputs/horse_round045')
OUT = Path('research_outputs/horse_round046')
OUT.mkdir(parents=True, exist_ok=True)
SIGNALS = R45 / 'state_parallel_signals.jsonl'
RESULTS_API = 'https://betfair-data-supplier-prod.herokuapp.com/api/race_results/'
COMMISSION = 0.07

S = requests.Session()
S.headers.update({'User-Agent': 'FutureAbilityResearch/round046 paper-only settlement'})


def norm_id(v) -> str:
    if v is None:
        return ''
    s = str(v).strip()
    if s.endswith('.0') and s[:-2].isdigit():
        s = s[:-2]
    return s


def get_result(market_id: str):
    last = None
    for i in range(3):
        try:
            last = S.get(RESULTS_API, params={'market_id': market_id, 'nz_tote_event_id': ''}, timeout=45)
            if last.status_code == 200:
                break
        except requests.RequestException:
            last = None
        time.sleep(0.5 * (i + 1))
    if last is None or last.status_code != 200:
        return None, {'http_status': None if last is None else last.status_code, 'status': 'HTTP_UNAVAILABLE'}
    try:
        j = last.json()
    except Exception as e:
        return None, {'http_status': last.status_code, 'status': 'JSON_PARSE_FAIL', 'error': str(e)}
    qa = {'http_status': last.status_code, 'status': str(j.get('raceEventStatus')), 'venue': j.get('venueName'), 'day': j.get('day')}
    if str(j.get('raceEventStatus')).upper() != 'RESULT':
        return None, qa
    runners = {}
    for r in j.get('runners') or []:
        sid = norm_id(r.get('selectionId'))
        if not sid:
            continue
        bsp = None
        for m in r.get('markets') or []:
            if str(m.get('productType')).upper() == 'WIN_ODDS_BSP':
                try:
                    p = float(m.get('price'))
                except (TypeError, ValueError):
                    p = math.nan
                if math.isfinite(p) and p > 1:
                    bsp = p
                    break
        placed = r.get('placedResult')
        try:
            win = float(placed) == 1.0
        except (TypeError, ValueError):
            win = False
        runners[sid] = {'runner_name': r.get('runnerName'), 'placed_result': placed, 'win': win, 'bsp': bsp}
    return runners, qa


def lay_profit(lay_price: float, horse_won: bool) -> float:
    # Unit lay stake: if selection loses, win 1 unit less commission; if selection wins, lose liability (lay-1).
    return -(lay_price - 1.0) if horse_won else (1.0 - COMMISSION)


def main():
    if not SIGNALS.exists():
        print('ROUND045_SIGNALS_MISSING=true')
        return
    candidates = []
    for line in SIGNALS.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get('raw_paper_lay_candidate'):
            candidates.append(r)

    settlements = []
    by_state = defaultdict(lambda: {'candidates': 0, 'settled': 0, 'wins': 0, 'losses': 0, 'profit_units': 0.0, 'liability_units': 0.0})
    cache = {}
    for c in candidates:
        state = str(c.get('state') or 'UNKNOWN')
        by_state[state]['candidates'] += 1
        mid = str(c.get('market_id') or '')
        sid = norm_id(c.get('selection_id'))
        if mid not in cache:
            cache[mid] = get_result(mid)
        runners, qa = cache[mid]
        row = dict(c)
        row['settlement_source'] = RESULTS_API
        row['settlement_http_status'] = qa.get('http_status')
        row['race_event_status'] = qa.get('status')
        row['settled'] = False
        if runners and sid in runners:
            rr = runners[sid]
            lay = float(c['lay_price'])
            horse_won = bool(rr['win'])
            profit = lay_profit(lay, horse_won)
            liability = lay - 1.0
            row.update({
                'settled': True,
                'official_runner_name': rr.get('runner_name'),
                'placed_result': rr.get('placed_result'),
                'horse_won': horse_won,
                'bsp': rr.get('bsp'),
                'paper_lay_result': 'LOSS' if horse_won else 'WIN',
                'paper_profit_units': profit,
                'lay_liability_units': liability,
            })
            s = by_state[state]
            s['settled'] += 1
            s['wins'] += 0 if horse_won else 1
            s['losses'] += 1 if horse_won else 0
            s['profit_units'] += profit
            s['liability_units'] += liability
        settlements.append(row)

    for state, s in by_state.items():
        s['pot_on_lay_stake_pct'] = (100.0 * s['profit_units'] / s['settled']) if s['settled'] else None
        s['roi_on_liability_pct'] = (100.0 * s['profit_units'] / s['liability_units']) if s['liability_units'] else None

    (OUT / 'settlements.jsonl').write_text(''.join(json.dumps(x, separators=(',', ':')) + '\n' for x in settlements), encoding='utf-8')
    status = {
        'round': 46,
        'capability': 'HorseRacing.ProspectivePaperSettlementEvaluator',
        'status': 'SETTLEMENT_EVALUATED',
        'paper_only': True,
        'real_betting_allowed': False,
        'commission': COMMISSION,
        'candidate_count': len(candidates),
        'settled_count': sum(1 for x in settlements if x.get('settled')),
        'pending_count': sum(1 for x in settlements if not x.get('settled')),
        'per_state': dict(sorted(by_state.items())),
        'governance': {
            'sa_remains_frozen_benchmark': True,
            'non_sa_results_are_exploratory_only': True,
            'cross_state_pooling_for_promotion_forbidden': True,
            'strategy_tuning': False,
        },
        'next_gate': 'continue per-state forward accumulation; refresh state-specific evidence without pooling states',
    }
    (OUT / 'status.json').write_text(json.dumps(status, indent=2), encoding='utf-8')
    print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
