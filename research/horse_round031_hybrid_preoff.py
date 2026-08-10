from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

# Import v2 first: this installs the mixed-format, fail-closed ANZ loader onto
# the Round030 module without changing the frozen strategy rules.
import horse_round030_preoff_translation_v2  # noqa: F401
import horse_round030_preoff_translation as r30
from horse_round025_runtime import candidate_history
from horse_round027_source_reconcile import verify_source_vintage

OUT = Path('research_outputs/horse_round031')
OUT.mkdir(parents=True, exist_ok=True)

PAST_WINDOW = 50
PRIMARY_COMMISSION = 0.07
BOOT_DRAWS = 10000
RNG_SEED = 310826


def build_final_gate_history() -> tuple[pd.DataFrame, list[dict]]:
    """Exact original frozen candidate population from Kash/final BSP only."""
    h, integrity = candidate_history()
    h = h.sort_values(['date', 'market_id', 'selection_id']).reset_index(drop=True).copy()
    required = {'date', 'market_sqerr', 'model_sqerr', 'value_calc'}
    missing = required - set(h.columns)
    if missing:
        raise RuntimeError(f'FINAL_GATE_HISTORY_SCHEMA_MISSING: {sorted(missing)}')
    if not h.value_calc.lt(-0.07).all():
        raise RuntimeError('FINAL_GATE_HISTORY_NOT_FROZEN_LT_MINUS_7')
    return h, integrity


def build_preoff_candidates() -> tuple[pd.DataFrame, list[dict], list[dict]]:
    x, join_qa, anz_fps = r30.build_joined()
    r2 = x[(x.state_code.eq('SA')) & x.model_rank.eq(2)].copy()
    r2 = r2[r2.preoff_lay.notna() & r2.preoff_lay.gt(1) & r2.bsp_anz.gt(1)].copy()
    r2['final_value'] = 1.0 / r2.model_odds - 1.0 / r2.bsp_anz
    r2['preoff_value'] = 1.0 / r2.model_odds - 1.0 / r2.preoff_lay
    r2['final_candidate'] = r2.final_value.lt(-0.07)
    r2['preoff_candidate'] = r2.preoff_value.lt(-0.07)
    pre = r2[r2.preoff_candidate].sort_values(['date', 'market_key', 'selection_key']).reset_index(drop=True).copy()
    return pre, join_qa, anz_fps


def attach_hybrid_gate(pre: pd.DataFrame, final_hist: pd.DataFrame) -> pd.DataFrame:
    """For race date D, use only final-BSP candidate outcomes with date < D."""
    y = pre.copy()
    y['gate_on'] = False
    y['hist_n'] = 0
    y['hist_market_brier'] = np.nan
    y['hist_model_brier'] = np.nan
    y['hist_brier_adv'] = np.nan

    for d, idx in y.groupby('date', sort=True).groups.items():
        prior = final_hist[final_hist.date < pd.Timestamp(d)].tail(PAST_WINDOW)
        n = int(len(prior))
        if n >= PAST_WINDOW:
            mb = float(prior.market_sqerr.mean())
            rb = float(prior.model_sqerr.mean())
            adv = mb - rb
            gate = bool(adv > 0)
        else:
            mb = rb = adv = np.nan
            gate = False
        y.loc[list(idx), 'gate_on'] = gate
        y.loc[list(idx), 'hist_n'] = n
        y.loc[list(idx), 'hist_market_brier'] = mb
        y.loc[list(idx), 'hist_model_brier'] = rb
        y.loc[list(idx), 'hist_brier_adv'] = adv

    y['gate_on'] = y.gate_on.astype(bool)
    return y


def market_net_pnl(x: pd.DataFrame, commission: float) -> pd.DataFrame:
    if x.empty:
        return pd.DataFrame(columns=['date', 'market_key', 'gross', 'liability', 'net'])
    gross = np.where(x.win.eq(1), -(x.preoff_lay - 1.0), 1.0)
    z = pd.DataFrame({
        'date': x.date.to_numpy(),
        'market_key': x.market_key.to_numpy(),
        'gross': gross,
        'liability': (x.preoff_lay - 1.0).to_numpy(),
    })
    z = z.groupby(['date', 'market_key'], as_index=False).agg(gross=('gross', 'sum'), liability=('liability', 'sum'))
    z['net'] = z.gross - np.where(z.gross > 0, commission * z.gross, 0.0)
    return z.sort_values(['date', 'market_key']).reset_index(drop=True)


def maxdd(z: pd.DataFrame) -> float:
    if z.empty:
        return 0.0
    eq = z.net.cumsum().to_numpy(float)
    peak = np.maximum.accumulate(np.r_[0.0, eq])[:-1]
    return float(np.max(peak - eq)) if len(eq) else 0.0


def metrics(x: pd.DataFrame, commission: float) -> dict:
    if x.empty:
        return {'n': 0, 'markets': 0, 'net_pl': 0.0, 'pot': None, 'rol': None, 'maxdd': 0.0, 'horse_win_rate': None}
    z = market_net_pnl(x, commission)
    liability = float(z.liability.sum())
    return {
        'n': int(len(x)),
        'markets': int(x.market_key.nunique()),
        'net_pl': float(z.net.sum()),
        'pot': float(z.net.sum() / len(x)),
        'rol': float(z.net.sum() / liability) if liability > 0 else None,
        'maxdd': maxdd(z),
        'horse_win_rate': float(x.win.mean()),
        'avg_preoff_lay': float(x.preoff_lay.mean()),
    }


def month_bootstrap(x: pd.DataFrame, commission: float) -> dict:
    if x.empty:
        return {'months': 0, 'ci95': [None, None], 'p_nonpositive': None}
    y = x.copy()
    y['month'] = y.date.dt.to_period('M').astype(str)
    rows = []
    for month, g in y.groupby('month'):
        z = market_net_pnl(g, commission)
        rows.append((month, float(z.net.sum()), int(len(g))))
    if len(rows) < 2:
        return {'months': len(rows), 'ci95': [None, None], 'p_nonpositive': None}
    pl = np.array([r[1] for r in rows], dtype=float)
    n = np.array([r[2] for r in rows], dtype=int)
    rng = np.random.default_rng(RNG_SEED)
    vals = np.empty(BOOT_DRAWS)
    for i in range(BOOT_DRAWS):
        idx = rng.integers(0, len(rows), size=len(rows))
        vals[i] = pl[idx].sum() / n[idx].sum()
    q = np.quantile(vals, [0.025, 0.975])
    return {
        'months': len(rows),
        'ci95': [float(q[0]), float(q[1])],
        'p_nonpositive': float((vals <= 0).mean()),
    }


def commission_curve(x: pd.DataFrame) -> dict:
    return {f'{c}%': metrics(x, c / 100.0) for c in range(2, 8)}


def gate_transitions(y: pd.DataFrame) -> list[dict]:
    daily = y.groupby('date', as_index=False).agg(
        gate_on=('gate_on', 'first'),
        hist_n=('hist_n', 'first'),
        hist_brier_adv=('hist_brier_adv', 'first'),
    ).sort_values('date')
    daily['prev'] = daily.gate_on.shift(1)
    out = []
    for _, row in daily[(daily.hist_n >= PAST_WINDOW) & daily.prev.notna() & daily.gate_on.ne(daily.prev)].iterrows():
        out.append({
            'date': str(row.date.date()),
            'new_state': 'MODEL_TRUSTED' if bool(row.gate_on) else 'MODEL_NOT_TRUSTED',
            'hist_brier_adv': float(row.hist_brier_adv),
        })
    return out


def main() -> None:
    kash_fps = verify_source_vintage()
    final_hist, final_integrity = build_final_gate_history()
    pre, join_qa, anz_fps = build_preoff_candidates()
    y = attach_hybrid_gate(pre, final_hist)

    period_rows = []
    for period in r30.PERIOD_ORDER:
        g = y[y.period.eq(period)]
        on = g[g.gate_on]
        off = g[~g.gate_on]
        period_rows.append({
            'period': period,
            'preoff_candidate_n': int(len(g)),
            'gate_on_n': int(len(on)),
            'gate_off_n': int(len(off)),
            'gate_on_5pct': metrics(on, 0.05),
            'gate_on_7pct': metrics(on, 0.07),
            'gate_off_7pct': metrics(off, 0.07),
        })

    on_all = y[y.gate_on]
    off_all = y[~y.gate_on]
    recent = y[y.period.isin(['2025', '2026_JAN_JUL'])]
    recent_on = recent[recent.gate_on]

    aggregate = {
        'all_gate_on_7pct': metrics(on_all, 0.07),
        'all_gate_off_7pct': metrics(off_all, 0.07),
        'all_gate_on_bootstrap_7pct': month_bootstrap(on_all, 0.07),
        'recent_2025_2026_gate_on_7pct': metrics(recent_on, 0.07),
        'recent_2025_2026_bootstrap_7pct': month_bootstrap(recent_on, 0.07),
        'recent_2025_2026_commission_curve': commission_curve(recent_on),
    }

    by_period = {r['period']: r for r in period_rows}
    recent_boot = aggregate['recent_2025_2026_bootstrap_7pct']
    tests = {
        'kash_hashes_match_round026': bool(all(x['match_round026_vintage'] for x in kash_fps)),
        '2025_gate_on_positive_at_7pct': bool(by_period['2025']['gate_on_7pct']['pot'] is not None and by_period['2025']['gate_on_7pct']['pot'] > 0),
        '2026_gate_on_positive_at_7pct': bool(by_period['2026_JAN_JUL']['gate_on_7pct']['pot'] is not None and by_period['2026_JAN_JUL']['gate_on_7pct']['pot'] > 0),
        'recent_combined_positive_at_7pct': bool(aggregate['recent_2025_2026_gate_on_7pct']['pot'] is not None and aggregate['recent_2025_2026_gate_on_7pct']['pot'] > 0),
        'recent_gate_on_n_at_least_50': bool(aggregate['recent_2025_2026_gate_on_7pct']['n'] >= 50),
        'recent_bootstrap_ci_low_positive': bool(recent_boot['ci95'][0] is not None and recent_boot['ci95'][0] > 0),
    }

    if all(tests.values()):
        classification = 'HYBRID_PREOFF_SUPPORTED'
    elif (
        tests['2025_gate_on_positive_at_7pct']
        and tests['2026_gate_on_positive_at_7pct']
        and tests['recent_combined_positive_at_7pct']
        and tests['recent_gate_on_n_at_least_50']
    ):
        classification = 'HYBRID_PREOFF_PROMISING_NOT_PROVEN'
    else:
        classification = 'HYBRID_PREOFF_NOT_PROVEN'

    status = {
        'round': 31,
        'capability': 'HorseRacing.HybridPreOffExecutionAudit',
        'status': 'COMPLETE',
        'frozen_historical_gate_population': 'SA × model rank 2 × (1/RP - 1/final BSP) < -7%; settled races only',
        'historical_gate': 'date D uses last 50 frozen final-BSP candidates with date strictly < D; MODEL_TRUSTED iff RP Brier < final-BSP Brier',
        'current_preoff_signal': 'SA × model rank 2 × (1/RP - 1/BEST_AVAIL_LAY_AT_SCHEDULED_OFF) < -7%',
        'entry_price': 'BEST_AVAIL_LAY_AT_SCHEDULED_OFF',
        'threshold_tuning': False,
        'window_tuning': False,
        'primary_commission': PRIMARY_COMMISSION,
        'final_history_integrity': final_integrity,
        'join_qa': join_qa,
        'anz_source_fingerprints': anz_fps,
        'period_economics': period_rows,
        'aggregate_economics': aggregate,
        'gate_transitions': gate_transitions(y),
        'decision': {'classification': classification, 'tests': tests},
        'governance': {
            'betting_ready': False,
            'no_same_day_final_bsp_leakage': True,
            'guardrail': 'No threshold/window/state/rank tuning in Round031. Historical gate may use only outcomes settled before current race date.',
        },
    }

    (OUT / 'status.json').write_text(json.dumps(status, indent=2), encoding='utf-8')
    pd.DataFrame(period_rows).to_json(OUT / 'period_economics.json', orient='records', indent=2)
    y[['date','period','market_key','selection_key','track_kash','model_odds','bsp_anz','preoff_lay','final_value','preoff_value','final_candidate','gate_on','hist_n','hist_brier_adv','win']].to_csv(OUT / 'candidate_audit.csv', index=False)
    print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
