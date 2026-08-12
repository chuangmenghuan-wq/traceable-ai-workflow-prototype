from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

R46 = Path('research_outputs/horse_round046')
OUT = Path('research_outputs/horse_round047')
OUT.mkdir(parents=True, exist_ok=True)
CURRENT = R46 / 'settlements.jsonl'
LEDGER = OUT / 'forward_settlement_ledger.jsonl'
SUMMARY = OUT / 'status.json'


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def key(r: dict) -> tuple[str, str, str]:
    return (
        str(r.get('active_date') or ''),
        str(r.get('market_id') or ''),
        str(r.get('selection_id') or ''),
    )


def main():
    previous = read_jsonl(LEDGER)
    current = read_jsonl(CURRENT)

    # Upsert so a previously pending candidate can later become settled without duplication.
    merged = {key(r): r for r in previous if all(key(r))}
    for r in current:
        k = key(r)
        if all(k):
            merged[k] = r

    rows = sorted(merged.values(), key=lambda r: (str(r.get('active_date') or ''), str(r.get('state') or ''), str(r.get('scheduled_start') or ''), str(r.get('market_id') or '')))
    LEDGER.write_text(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in rows), encoding='utf-8')

    by_state = defaultdict(lambda: {
        'candidates': 0,
        'settled': 0,
        'pending': 0,
        'lay_wins': 0,
        'lay_losses': 0,
        'profit_units': 0.0,
        'liability_units': 0.0,
        'first_date': None,
        'last_date': None,
    })

    for r in rows:
        state = str(r.get('state') or 'UNKNOWN')
        s = by_state[state]
        s['candidates'] += 1
        d = str(r.get('active_date') or '') or None
        if d:
            s['first_date'] = d if s['first_date'] is None else min(s['first_date'], d)
            s['last_date'] = d if s['last_date'] is None else max(s['last_date'], d)
        if not r.get('settled'):
            s['pending'] += 1
            continue
        s['settled'] += 1
        result = str(r.get('paper_lay_result') or '')
        s['lay_wins'] += 1 if result == 'WIN' else 0
        s['lay_losses'] += 1 if result == 'LOSS' else 0
        s['profit_units'] += float(r.get('paper_profit_units') or 0.0)
        s['liability_units'] += float(r.get('lay_liability_units') or 0.0)

    for state, s in by_state.items():
        settled = s['settled']
        s['lay_win_rate_pct'] = 100.0 * s['lay_wins'] / settled if settled else None
        s['pot_on_lay_stake_pct'] = 100.0 * s['profit_units'] / settled if settled else None
        s['roi_on_liability_pct'] = 100.0 * s['profit_units'] / s['liability_units'] if s['liability_units'] else None

    status = {
        'round': 47,
        'capability': 'HorseRacing.StateForwardPerformanceLedger',
        'status': 'FORWARD_LEDGER_UPDATED',
        'paper_only': True,
        'real_betting_allowed': False,
        'strategy_tuning': False,
        'ledger_rows': len(rows),
        'settled_rows': sum(1 for r in rows if r.get('settled')),
        'pending_rows': sum(1 for r in rows if not r.get('settled')),
        'dates_observed': sorted({str(r.get('active_date')) for r in rows if r.get('active_date')}),
        'per_state': dict(sorted(by_state.items())),
        'governance': {
            'sa_remains_frozen_benchmark': True,
            'non_sa_results_are_exploratory_only': True,
            'cross_state_pooling_for_promotion_forbidden': True,
            'append_only_forward_history': True,
            'dedupe_key': ['active_date', 'market_id', 'selection_id'],
        },
        'next_gate': 'accumulate genuine future candidates by state; assess sample size and stability before any state-specific promotion',
    }
    SUMMARY.write_text(json.dumps(status, indent=2), encoding='utf-8')
    print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
