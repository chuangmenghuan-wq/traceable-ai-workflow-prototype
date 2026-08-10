from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

SOURCE = Path('research_outputs/horse_round031/candidate_audit.csv')
OUT = Path('research_outputs/horse_round032')
OUT.mkdir(parents=True, exist_ok=True)
COMMISSION = 0.07
EXPECTED_RECENT_N = 101
EXPECTED_ALL_N = 511


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def pnl_rows(x: pd.DataFrame) -> pd.DataFrame:
    y = x.sort_values(['date', 'market_key', 'selection_key']).copy()
    y['gross'] = np.where(y.win.eq(1), -(y.preoff_lay - 1.0), 1.0)
    z = (y.groupby(['date', 'period', 'market_key', 'track_kash'], as_index=False)
           .agg(gross=('gross', 'sum'),
                liability=('preoff_lay', lambda s: float((s - 1.0).sum())),
                bets=('selection_key', 'size')))
    z['net'] = z.gross - np.where(z.gross > 0, COMMISSION * z.gross, 0.0)
    z['month'] = pd.to_datetime(z.date).dt.to_period('M').astype(str)
    z['quarter'] = pd.to_datetime(z.date).dt.to_period('Q').astype(str)
    return z.sort_values(['date', 'market_key']).reset_index(drop=True)


def metrics(z: pd.DataFrame) -> dict:
    n = int(z.bets.sum()) if len(z) else 0
    net = float(z.net.sum()) if len(z) else 0.0
    liab = float(z.liability.sum()) if len(z) else 0.0
    if len(z):
        eq = z.net.cumsum().to_numpy(float)
        peak = np.maximum.accumulate(np.r_[0.0, eq])[:-1]
        dd = float(np.max(peak - eq)) if len(eq) else 0.0
    else:
        dd = 0.0
    return {'n': n, 'markets': int(len(z)), 'net_pl': net,
            'pot': net / n if n else None,
            'rol': net / liab if liab else None,
            'maxdd': dd}


def streaks(z: pd.DataFrame) -> dict:
    vals = z.sort_values(['date', 'market_key']).net.to_numpy(float)
    max_loss = max_win = cur_loss = cur_win = 0
    for v in vals:
        if v < 0:
            cur_loss += 1; cur_win = 0; max_loss = max(max_loss, cur_loss)
        elif v > 0:
            cur_win += 1; cur_loss = 0; max_win = max(max_win, cur_win)
        else:
            cur_loss = cur_win = 0
    return {'max_consecutive_losing_markets': int(max_loss),
            'max_consecutive_winning_markets': int(max_win)}


def leave_one_out(z: pd.DataFrame, col: str) -> list[dict]:
    out = []
    for key in sorted(z[col].dropna().unique()):
        g = z[z[col] != key]
        out.append({'removed': str(key), **metrics(g)})
    return out


def summarize_group(z: pd.DataFrame, col: str) -> list[dict]:
    rows = []
    for key, g in z.groupby(col, sort=True):
        rows.append({col: str(key), **metrics(g)})
    return rows


def main() -> None:
    if not SOURCE.exists():
        raise RuntimeError('ROUND031_SOURCE_MISSING')
    x = pd.read_csv(SOURCE)
    required = {'date','period','market_key','selection_key','track_kash','preoff_lay','preoff_value','gate_on','win'}
    missing = sorted(required - set(x.columns))
    if missing:
        raise RuntimeError(f'ROUND031_SCHEMA_MISSING {missing}')
    if len(x) != EXPECTED_ALL_N:
        raise RuntimeError(f'ROUND031_ROW_DRIFT {len(x)} != {EXPECTED_ALL_N}')
    x['date'] = pd.to_datetime(x.date, format='%Y-%m-%d', errors='raise')
    if x.gate_on.dtype == object:
        x['gate_on'] = x.gate_on.astype(str).str.lower().eq('true')
    else:
        x['gate_on'] = x.gate_on.astype(bool)
    if not x.preoff_value.lt(-0.07).all():
        raise RuntimeError('ROUND031_CANDIDATE_SCOPE_DRIFT')

    recent = x[x.period.astype(str).isin(['2025','2026_JAN_JUL']) & x.gate_on].copy()
    if len(recent) != EXPECTED_RECENT_N:
        raise RuntimeError(f'ROUND031_RECENT_DRIFT {len(recent)} != {EXPECTED_RECENT_N}')
    z = pnl_rows(recent)

    base = metrics(z)
    by_year = summarize_group(z, 'period')
    by_month = summarize_group(z, 'month')
    by_quarter = summarize_group(z, 'quarter')
    by_track = summarize_group(z, 'track_kash')
    lomo = leave_one_out(z, 'month')
    loqo = leave_one_out(z, 'quarter')
    loto = leave_one_out(z, 'track_kash')

    positive_months = sum(1 for r in by_month if r['pot'] is not None and r['pot'] > 0)
    month_count = len(by_month)
    worst_lomo = min(lomo, key=lambda r: r['pot']) if lomo else None
    worst_loqo = min(loqo, key=lambda r: r['pot']) if loqo else None
    worst_loto = min(loto, key=lambda r: r['pot']) if loto else None
    best_month = max(by_month, key=lambda r: r['net_pl']) if by_month else None
    best_track = max(by_track, key=lambda r: r['net_pl']) if by_track else None
    largest_track = max(by_track, key=lambda r: r['n']) if by_track else None
    largest_track_share = largest_track['n'] / base['n'] if largest_track and base['n'] else None

    remove_best_month = metrics(z[z.month != best_month['month']]) if best_month else None
    remove_best_track = metrics(z[z.track_kash != best_track['track_kash']]) if best_track else None

    years = {r['period']: r for r in by_year}
    tests = {
        'both_2025_2026_positive': bool(years.get('2025', {}).get('pot', -1) > 0 and years.get('2026_JAN_JUL', {}).get('pot', -1) > 0),
        'positive_month_share_at_least_60pct': bool(month_count > 0 and positive_months / month_count >= 0.60),
        'leave_one_month_out_worst_positive': bool(worst_lomo and worst_lomo['pot'] > 0),
        'leave_one_track_out_worst_positive': bool(worst_loto and worst_loto['pot'] > 0),
        'largest_track_sample_share_at_most_35pct': bool(largest_track_share is not None and largest_track_share <= 0.35),
        'remove_best_month_still_positive': bool(remove_best_month and remove_best_month['pot'] > 0),
    }
    if all(tests.values()):
        classification = 'HYBRID_PREOFF_STABILITY_SUPPORTED'
    elif tests['both_2025_2026_positive'] and tests['leave_one_track_out_worst_positive'] and tests['remove_best_month_still_positive']:
        classification = 'HYBRID_PREOFF_STABILITY_PARTIAL'
    else:
        classification = 'HYBRID_PREOFF_STABILITY_FAIL'

    status = {
        'round': 32,
        'capability': 'HorseRacing.HybridPreOffStabilityAudit',
        'status': 'COMPLETE',
        'source': 'Round031 candidate_audit.csv',
        'source_sha256': sha256_file(SOURCE),
        'frozen_scope': '2025 + 2026_JAN_JUL Round031 gate_on candidates only',
        'commission': COMMISSION,
        'threshold_tuning': False,
        'window_tuning': False,
        'base': base,
        'streaks': streaks(z),
        'by_year': by_year,
        'by_month': by_month,
        'by_quarter': by_quarter,
        'by_track': by_track,
        'positive_months': positive_months,
        'month_count': month_count,
        'positive_month_share': positive_months / month_count if month_count else None,
        'worst_leave_one_month_out': worst_lomo,
        'worst_leave_one_quarter_out': worst_loqo,
        'worst_leave_one_track_out': worst_loto,
        'largest_track': largest_track,
        'largest_track_sample_share': largest_track_share,
        'best_month': best_month,
        'remove_best_month': remove_best_month,
        'best_track_by_net_pl': best_track,
        'remove_best_track': remove_best_track,
        'tests': tests,
        'classification': classification,
        'governance': {
            'betting_ready': False,
            'guardrail': 'No signal, threshold, rank, state, window, or price-source tuning in Round032. Stability only.',
            'next_if_supported': 'Freeze paper-forward execution contract; do not optimize further.'
        }
    }
    (OUT / 'status.json').write_text(json.dumps(status, indent=2), encoding='utf-8')
    pd.DataFrame(by_month).to_csv(OUT / 'monthly.csv', index=False)
    pd.DataFrame(by_track).to_csv(OUT / 'tracks.csv', index=False)
    pd.DataFrame(lomo).to_csv(OUT / 'leave_one_month_out.csv', index=False)
    pd.DataFrame(loto).to_csv(OUT / 'leave_one_track_out.csv', index=False)
    print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
