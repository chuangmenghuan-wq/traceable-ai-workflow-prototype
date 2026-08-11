from __future__ import annotations

import io
import json
import math
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from horse_round025_runtime import SA_TRACKS, candidate_history

OUT = Path('research_outputs/horse_round035')
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'https://betfair-datascientists.github.io/data/assets'
JULY_URL = f'{BASE}/Kash_Model_Results_2026_07.csv'
KASH_DAILY = (
    'https://betfair-data-supplier-prod.herokuapp.com/api/widgets/'
    'kash-ratings-model/datasets?date={date}&presenter=RatingsPresenter&csv=true'
)
RESULTS_API = 'https://betfair-data-supplier-prod.herokuapp.com/api/race_results/'
AUG_START = pd.Timestamp('2026-08-01')
AUG_END = pd.Timestamp('2026-08-10')
PAPER_DATE = pd.Timestamp('2026-08-11')
PAST_WINDOW = 50
VALUE_CUTOFF = -0.07
VALIDATION_SAMPLE = 30

S = requests.Session()
S.headers.update({'User-Agent': 'FutureAbilityResearch/1.0 (+paper-only validation)'})


def norm_id(v) -> str:
    if pd.isna(v):
        return ''
    s = str(v).strip()
    if re.fullmatch(r'\d+\.0', s):
        s = s[:-2]
    return s


def request(url: str, *, params=None, attempts: int = 3, timeout: int = 45):
    last = None
    for i in range(attempts):
        try:
            r = S.get(url, params=params, timeout=timeout)
            last = r
            if r.status_code == 200:
                return r
        except requests.RequestException:
            pass
        time.sleep(0.5 * (i + 1))
    return last


def parse_daily_ratings(raw: bytes, date: pd.Timestamp) -> tuple[pd.DataFrame, dict]:
    d = pd.read_csv(io.BytesIO(raw), dtype=str, low_memory=False)
    cols = {str(c).strip().upper(): str(c) for c in d.columns}

    def pick(*names):
        for n in names:
            if n.upper() in cols:
                return cols[n.upper()]
        return None

    mapped = {
        'track': pick('meetings.name', 'Track', 'Venue'),
        'market_id': pick('meetings.races.bfExchangeMarketId', 'Market', 'MarketId', 'MARKET_ID'),
        'selection_id': pick('meetings.races.runners.bfExchangeSelectionId', 'Selection', 'SelectionId', 'SELECTION_ID'),
        'model_odds': pick('meetings.races.runners.ratedPrice', 'RP', 'Model Odds', 'MODEL_ODDS'),
        'horse': pick('meetings.races.runners.name', 'Horse', 'SELECTION_NAME'),
    }
    required = ['track', 'market_id', 'selection_id', 'model_odds']
    missing = [k for k in required if mapped[k] is None]
    if missing:
        raise RuntimeError(f'daily ratings missing columns {missing}; columns={list(d.columns)}')

    x = pd.DataFrame({
        'date': date,
        'track': d[mapped['track']].astype(str).str.strip(),
        'market_id': d[mapped['market_id']].map(norm_id),
        'selection_id': d[mapped['selection_id']].map(norm_id),
        'model_odds': pd.to_numeric(d[mapped['model_odds']], errors='coerce'),
        'horse': d[mapped['horse']].astype(str).str.strip() if mapped['horse'] else '',
    })
    x = x.replace([np.inf, -np.inf], np.nan).dropna(subset=['model_odds'])
    x = x[(x.model_odds > 1) & x.market_id.ne('') & x.selection_id.ne('')].copy()
    x = x.sort_values(['market_id', 'selection_id']).drop_duplicates(['market_id', 'selection_id'], keep='last')
    x['model_rank'] = x.groupby('market_id').model_odds.rank(method='first', ascending=True)
    qa = {
        'date': str(date.date()),
        'raw_rows': int(len(d)),
        'usable_rows': int(len(x)),
        'markets': int(x.market_id.nunique()),
        'sa_markets': int(x[x.track.isin(SA_TRACKS)].market_id.nunique()),
        'sa_r2_rows': int(len(x[x.track.isin(SA_TRACKS) & x.model_rank.eq(2)])),
    }
    return x, qa


def parse_july_official(raw: bytes) -> pd.DataFrame:
    d = pd.read_csv(io.BytesIO(raw), dtype={'Market': str, 'Selection': str}, low_memory=False)
    required = ['Date', 'Track', 'Market', 'Selection', 'RP', 'WIN_BSP', 'WIN_RESULT']
    missing = [c for c in required if c not in d.columns]
    if missing:
        raise RuntimeError(f'July official missing {missing}')
    x = pd.DataFrame({
        'date': pd.to_datetime(d.Date.astype(str).str.strip(), format='%Y-%m-%d', errors='coerce'),
        'track': d.Track.astype(str).str.strip(),
        'market_id': d.Market.map(norm_id),
        'selection_id': d.Selection.map(norm_id),
        'model_odds': pd.to_numeric(d.RP, errors='coerce'),
        'bsp_official': pd.to_numeric(d.WIN_BSP, errors='coerce'),
        'win_official': pd.to_numeric(d.WIN_RESULT, errors='coerce'),
    })
    x = x.replace([np.inf, -np.inf], np.nan).dropna(subset=['date', 'model_odds', 'bsp_official', 'win_official'])
    x = x[(x.model_odds > 1) & (x.bsp_official > 1) & x.win_official.isin([0, 1])]
    x = x.sort_values(['market_id', 'selection_id']).drop_duplicates(['market_id', 'selection_id'], keep='last').copy()
    x['model_rank'] = x.groupby('market_id').model_odds.rank(method='first', ascending=True)
    return x


def get_market_result(market_id: str) -> tuple[dict | None, dict]:
    r = request(RESULTS_API, params={'market_id': market_id, 'nz_tote_event_id': ''}, attempts=3, timeout=45)
    qa = {'market_id': market_id, 'http_status': r.status_code if r is not None else None}
    if r is None or r.status_code != 200:
        qa['status'] = 'HTTP_UNAVAILABLE'
        return None, qa
    try:
        j = r.json()
    except Exception as e:
        qa.update({'status': 'JSON_PARSE_FAIL', 'error': str(e)})
        return None, qa
    qa.update({
        'status': str(j.get('raceEventStatus')),
        'race_type': j.get('raceType'),
        'venue': j.get('venueName'),
        'day': j.get('day'),
        'runner_count': len(j.get('runners') or []),
    })
    if str(j.get('raceEventStatus')).upper() != 'RESULT':
        return None, qa
    rows = {}
    for runner in j.get('runners') or []:
        sid = norm_id(runner.get('selectionId'))
        if not sid:
            continue
        bsp = None
        for m in runner.get('markets') or []:
            if str(m.get('productType')).upper() == 'WIN_ODDS_BSP':
                try:
                    p = float(m.get('price'))
                except (TypeError, ValueError):
                    p = math.nan
                if math.isfinite(p) and p > 1:
                    bsp = p
                    break
        if bsp is None:
            continue
        placed = runner.get('placedResult')
        try:
            win = 1.0 if float(placed) == 1.0 else 0.0
        except (TypeError, ValueError):
            win = 0.0
        rows[sid] = {
            'bsp': bsp,
            'win': win,
            'runner_name': runner.get('runnerName'),
            'placed_result': placed,
        }
    qa['usable_runner_count'] = len(rows)
    return {'meta': j, 'runners': rows}, qa


def validate_against_july() -> tuple[dict, pd.DataFrame]:
    r = request(JULY_URL, attempts=3, timeout=120)
    if r is None or r.status_code != 200:
        raise RuntimeError(f'July official unavailable: {None if r is None else r.status_code}')
    july = parse_july_official(r.content)
    pool = july[july.track.isin(SA_TRACKS) & july.model_rank.eq(2)].sort_values(['date', 'market_id']).copy()
    if len(pool) < VALIDATION_SAMPLE:
        raise RuntimeError(f'insufficient July SA R2 validation pool: {len(pool)}')
    idx = np.linspace(0, len(pool) - 1, VALIDATION_SAMPLE, dtype=int)
    sample = pool.iloc[idx].drop_duplicates('market_id').copy()
    records = []
    for row in sample.itertuples(index=False):
        res, qa = get_market_result(row.market_id)
        rec = {
            'date': str(row.date.date()), 'track': row.track, 'market_id': row.market_id,
            'selection_id': row.selection_id, 'official_bsp': float(row.bsp_official),
            'official_win': float(row.win_official), 'api_http_status': qa.get('http_status'),
            'api_status': qa.get('status'), 'api_race_type': qa.get('race_type'), 'api_day': qa.get('day'),
        }
        if res and row.selection_id in res['runners']:
            rr = res['runners'][row.selection_id]
            rec.update({
                'api_bsp': float(rr['bsp']), 'api_win': float(rr['win']),
                'bsp_abs_diff': abs(float(row.bsp_official) - float(rr['bsp'])),
                'win_match': bool(float(row.win_official) == float(rr['win'])),
                'selection_found': True,
            })
        else:
            rec.update({'api_bsp': None, 'api_win': None, 'bsp_abs_diff': None, 'win_match': False, 'selection_found': False})
        records.append(rec)
        time.sleep(0.03)
    v = pd.DataFrame(records)
    matched = v[v.selection_found].copy()
    summary = {
        'requested_markets': int(len(v)),
        'matched_selections': int(len(matched)),
        'selection_match_rate': float(len(matched) / len(v)) if len(v) else 0.0,
        'winner_match_rate': float(matched.win_match.mean()) if len(matched) else 0.0,
        'bsp_max_abs_diff': float(matched.bsp_abs_diff.max()) if len(matched) else None,
        'bsp_mean_abs_diff': float(matched.bsp_abs_diff.mean()) if len(matched) else None,
        'race_types': sorted(str(x) for x in v.api_race_type.dropna().unique()),
    }
    summary['validated'] = bool(
        summary['matched_selections'] >= 20
        and summary['selection_match_rate'] >= 0.90
        and summary['winner_match_rate'] == 1.0
        and summary['bsp_max_abs_diff'] is not None
        and summary['bsp_max_abs_diff'] <= 0.011
    )
    return summary, v


def recover_august(validation_ok: bool) -> tuple[pd.DataFrame, list[dict], list[dict]]:
    if not validation_ok:
        return pd.DataFrame(), [], []
    all_candidates = []
    day_qa = []
    market_qa = []
    for date in pd.date_range(AUG_START, AUG_END, freq='D'):
        url = KASH_DAILY.format(date=str(date.date()))
        r = request(url, attempts=3, timeout=90)
        if r is None or r.status_code != 200:
            day_qa.append({'date': str(date.date()), 'ratings_status': None if r is None else r.status_code, 'status': 'RATINGS_UNAVAILABLE'})
            continue
        ratings, rqa = parse_daily_ratings(r.content, date)
        sa_r2 = ratings[ratings.track.isin(SA_TRACKS) & ratings.model_rank.eq(2)].copy()
        recovered = []
        for row in sa_r2.itertuples(index=False):
            res, qa = get_market_result(row.market_id)
            qa.update({'date': str(date.date()), 'track': row.track, 'selection_id': row.selection_id})
            market_qa.append(qa)
            if not res:
                continue
            rr = res['runners'].get(row.selection_id)
            if not rr:
                continue
            bsp = float(rr['bsp']); win = float(rr['win'])
            model_prob = 1.0 / float(row.model_odds)
            market_prob = 1.0 / bsp
            value = model_prob - market_prob
            recovered.append({
                'date': date, 'track': row.track, 'horse': row.horse,
                'market_id': row.market_id, 'selection_id': row.selection_id,
                'model_odds': float(row.model_odds), 'bsp': bsp, 'win': win,
                'model_prob': model_prob, 'market_prob': market_prob, 'value_calc': value,
                'model_sqerr': (win - model_prob) ** 2,
                'market_sqerr': (win - market_prob) ** 2,
                'is_candidate': bool(value < VALUE_CUTOFF),
                'source': 'BETFAIR_HUB_RACE_RESULTS_BACKING_API',
            })
            time.sleep(0.03)
        recdf = pd.DataFrame(recovered)
        if not recdf.empty:
            cand = recdf[recdf.is_candidate].copy()
            if not cand.empty:
                all_candidates.append(cand)
        day_qa.append({
            **rqa,
            'ratings_http_status': r.status_code,
            'r2_result_rows_recovered': int(len(recdf)),
            'r2_result_coverage': float(len(recdf) / len(sa_r2)) if len(sa_r2) else 1.0,
            'candidate_n': int(recdf.is_candidate.sum()) if not recdf.empty else 0,
            'status': 'RECOVERED' if len(recdf) == len(sa_r2) and len(sa_r2) > 0 else 'PARTIAL',
        })
    aug = pd.concat(all_candidates, ignore_index=True) if all_candidates else pd.DataFrame()
    return aug, day_qa, market_qa


def rebuild_gate(aug: pd.DataFrame) -> tuple[list[dict], dict]:
    hist, _ = candidate_history()
    hist = hist[hist.date < AUG_START].sort_values(['date', 'market_id', 'selection_id']).copy()
    gate_days = []
    working = hist.copy()
    for date in pd.date_range(AUG_START, AUG_END, freq='D'):
        prior = working[working.date < date].tail(PAST_WINDOW)
        adv = float(prior.market_sqerr.mean() - prior.model_sqerr.mean())
        daycand = aug[aug.date.eq(date)].copy() if not aug.empty else pd.DataFrame()
        gate_days.append({
            'date': str(date.date()), 'past_n': int(len(prior)), 'past_brier_adv': adv,
            'gate_on': bool(adv > 0), 'recovered_candidate_n': int(len(daycand)),
        })
        if not daycand.empty:
            # Match historical candidate schema fields required by future Gate updates.
            working = pd.concat([working, daycand], ignore_index=True, sort=False)
            working = working.sort_values(['date', 'market_id', 'selection_id'])
    prior = working[working.date < PAPER_DATE].tail(PAST_WINDOW)
    final_adv = float(prior.market_sqerr.mean() - prior.model_sqerr.mean())
    snap = {
        'as_of': str(PAPER_DATE.date()),
        'past_n': int(len(prior)),
        'brier_advantage': final_adv,
        'gate_on': bool(final_adv > 0),
        'latest_recovered_candidate_date': str(pd.Timestamp(aug.date.max()).date()) if not aug.empty else None,
        'august_candidate_n': int(len(aug)),
    }
    return gate_days, snap


def main() -> None:
    validation, validation_rows = validate_against_july()
    validation_rows.to_csv(OUT / 'results_api_validation_rows.csv', index=False)
    (OUT / 'results_api_validation.json').write_text(json.dumps(validation, indent=2), encoding='utf-8')

    aug, day_qa, market_qa = recover_august(validation['validated'])
    if not aug.empty:
        aug.to_csv(OUT / 'august_recovered_candidates.csv', index=False)
    pd.DataFrame(day_qa).to_csv(OUT / 'august_recovery_day_qa.csv', index=False)
    pd.DataFrame(market_qa).to_csv(OUT / 'august_recovery_market_qa.csv', index=False)

    complete_days = sum(1 for d in day_qa if d.get('status') == 'RECOVERED')
    min_coverage = min((d.get('r2_result_coverage', 0.0) for d in day_qa), default=0.0)
    ledger_recovered = bool(validation['validated'] and len(day_qa) == 10 and complete_days == 10 and min_coverage >= 0.99)
    if ledger_recovered:
        gate_days, gate_snapshot = rebuild_gate(aug)
        pd.DataFrame(gate_days).to_csv(OUT / 'recovered_gate_days.csv', index=False)
        classification = 'SETTLEMENT_LEDGER_RECOVERED_VIA_BETFAIR_RESULTS_API'
    else:
        gate_days, gate_snapshot = [], None
        classification = 'SETTLEMENT_LEDGER_RECOVERY_INCOMPLETE'

    status = {
        'round': 35,
        'capability': 'HorseRacing.SettlementLedgerRecovery',
        'status': 'COMPLETE',
        'strategy_tuning': False,
        'real_betting_allowed': False,
        'source': {
            'name': 'Betfair Hub backing race_results endpoint',
            'endpoint': RESULTS_API + '?market_id=<MARKET_ID>&nz_tote_event_id=',
            'trust': 'BETFAIR_BACKING_API_VALIDATED_AGAINST_OFFICIAL_KASH_JULY' if validation['validated'] else 'UNVALIDATED',
            'monthly_reconciliation_required': True,
        },
        'validation': validation,
        'august': {
            'days_expected': 10,
            'days_recovered_complete': complete_days,
            'minimum_r2_result_coverage': min_coverage,
            'candidate_n': int(len(aug)),
        },
        'ledger_recovered': ledger_recovered,
        'gate_snapshot_2026_08_11': gate_snapshot,
        'classification': classification,
        'governance': {
            'paper_only': True,
            'betting_ready': False,
            'monthly_official_reconciliation_required': True,
            'no_threshold_or_window_changes': True,
        },
    }
    (OUT / 'status.json').write_text(json.dumps(status, indent=2), encoding='utf-8')
    print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
