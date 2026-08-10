from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from horse_round025_runtime import candidate_history
from horse_round027_source_reconcile import verify_source_vintage

PAST_WINDOW = 50
FUTURE_HORIZON = 20
BOOTSTRAP_DRAWS = 10000
RNG_SEED = 280826
OUT = Path("research_outputs/horse_round028")
OUT.mkdir(parents=True, exist_ok=True)


def net_for_rows(x: pd.DataFrame, commission: float) -> np.ndarray:
    gross = np.where(x.win.eq(1), -(x.bsp.to_numpy(float) - 1.0), 1.0)
    return gross - np.where(gross > 0, commission * gross, 0.0)


def max_drawdown(net: np.ndarray) -> float:
    if len(net) == 0:
        return 0.0
    eq = np.cumsum(net.astype(float))
    peak = np.maximum.accumulate(np.r_[0.0, eq])[:-1]
    return float(np.max(peak - eq)) if len(eq) else 0.0


def build_blocks(x: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    y = x.sort_values(["date", "market_id", "selection_id"]).reset_index(drop=True).copy()
    dates = pd.Index(sorted(y.date.unique()))
    block_rows: list[dict] = []
    bet_parts: list[pd.DataFrame] = []
    pos = 0
    block_id = 0

    while pos < len(dates):
        anchor = pd.Timestamp(dates[pos])
        prior = y[y.date < anchor]
        if len(prior) < PAST_WINDOW:
            pos += 1
            continue

        future_all = y[y.date >= anchor]
        if len(future_all) < FUTURE_HORIZON:
            break

        first_h = future_all.iloc[:FUTURE_HORIZON]
        end_date = pd.Timestamp(first_h.date.iloc[-1])
        future = y[(y.date >= anchor) & (y.date <= end_date)].copy()
        if len(future) < FUTURE_HORIZON:
            raise AssertionError("future block shorter than frozen horizon")

        past = prior.tail(PAST_WINDOW)
        past_market_brier = float(past.market_sqerr.mean())
        past_model_brier = float(past.model_sqerr.mean())
        past_adv = past_market_brier - past_model_brier
        trusted = bool(past_adv > 0)

        n5 = net_for_rows(future, 0.05)
        n7 = net_for_rows(future, 0.07)
        liability = future.bsp.to_numpy(float) - 1.0

        block_rows.append({
            "block_id": block_id,
            "anchor_date": str(anchor.date()),
            "end_date": str(end_date.date()),
            "start_period": str(future.period.iloc[0]),
            "end_period": str(future.period.iloc[-1]),
            "past_n": int(len(past)),
            "future_n": int(len(future)),
            "past_market_brier": past_market_brier,
            "past_model_brier": past_model_brier,
            "past_adv": past_adv,
            "past_trusted": trusted,
            "future_horse_win_rate": float(future.win.mean()),
            "future_net_pl_5pct": float(n5.sum()),
            "future_pot_5pct": float(n5.sum() / len(future)),
            "future_rol_5pct": float(n5.sum() / liability.sum()),
            "future_maxdd_5pct": max_drawdown(n5),
            "future_net_pl_7pct": float(n7.sum()),
            "future_pot_7pct": float(n7.sum() / len(future)),
            "future_rol_7pct": float(n7.sum() / liability.sum()),
            "future_maxdd_7pct": max_drawdown(n7),
            "future_profitable_5pct": bool(n5.sum() > 0),
            "future_profitable_7pct": bool(n7.sum() > 0),
        })

        z = future[["date", "period", "market_id", "selection_id", "track", "bsp", "win"]].copy()
        z["block_id"] = block_id
        z["past_trusted"] = trusted
        z["net_5pct"] = n5
        z["net_7pct"] = n7
        z["liability"] = liability
        bet_parts.append(z)

        block_id += 1
        pos = int(dates.searchsorted(np.datetime64(end_date), side="right"))

    blocks = pd.DataFrame(block_rows)
    bets = pd.concat(bet_parts, ignore_index=True) if bet_parts else pd.DataFrame()
    return blocks, bets


def aggregate_bets(bets: pd.DataFrame, trusted: bool | None) -> dict:
    g = bets if trusted is None else bets[bets.past_trusted.eq(trusted)]
    if g.empty:
        return {
            "n": 0, "blocks": 0, "net_pl_5pct": 0.0, "pot_5pct": None,
            "rol_5pct": None, "maxdd_5pct": None, "net_pl_7pct": 0.0,
            "pot_7pct": None, "rol_7pct": None, "maxdd_7pct": None,
        }
    return {
        "n": int(len(g)),
        "blocks": int(g.block_id.nunique()),
        "net_pl_5pct": float(g.net_5pct.sum()),
        "pot_5pct": float(g.net_5pct.sum() / len(g)),
        "rol_5pct": float(g.net_5pct.sum() / g.liability.sum()),
        "maxdd_5pct": max_drawdown(g.sort_values(["date", "market_id"]).net_5pct.to_numpy(float)),
        "net_pl_7pct": float(g.net_7pct.sum()),
        "pot_7pct": float(g.net_7pct.sum() / len(g)),
        "rol_7pct": float(g.net_7pct.sum() / g.liability.sum()),
        "maxdd_7pct": max_drawdown(g.sort_values(["date", "market_id"]).net_7pct.to_numpy(float)),
    }


def bootstrap_blocks(blocks: pd.DataFrame) -> dict:
    t = blocks[blocks.past_trusted].reset_index(drop=True)
    u = blocks[~blocks.past_trusted].reset_index(drop=True)
    rng = np.random.default_rng(RNG_SEED)

    trusted_pot = np.full(BOOTSTRAP_DRAWS, np.nan)
    untrusted_pot = np.full(BOOTSTRAP_DRAWS, np.nan)
    diff = np.full(BOOTSTRAP_DRAWS, np.nan)
    trusted_positive_rate = np.full(BOOTSTRAP_DRAWS, np.nan)

    for i in range(BOOTSTRAP_DRAWS):
        if len(t):
            st = t.iloc[rng.integers(0, len(t), size=len(t))]
            tp = float(st.future_net_pl_7pct.sum() / st.future_n.sum())
            trusted_pot[i] = tp
            trusted_positive_rate[i] = float(st.future_profitable_7pct.mean())
        if len(u):
            su = u.iloc[rng.integers(0, len(u), size=len(u))]
            up = float(su.future_net_pl_7pct.sum() / su.future_n.sum())
            untrusted_pot[i] = up
        if np.isfinite(trusted_pot[i]) and np.isfinite(untrusted_pot[i]):
            diff[i] = trusted_pot[i] - untrusted_pot[i]

    def ci(a: np.ndarray) -> list[float | None]:
        q = a[np.isfinite(a)]
        if not len(q):
            return [None, None]
        z = np.quantile(q, [0.025, 0.975])
        return [float(z[0]), float(z[1])]

    return {
        "draws": BOOTSTRAP_DRAWS,
        "trusted_pot_7pct_ci95": ci(trusted_pot),
        "untrusted_pot_7pct_ci95": ci(untrusted_pot),
        "trusted_minus_untrusted_pot_7pct_ci95": ci(diff),
        "trusted_positive_block_rate_ci95": ci(trusted_positive_rate),
        "p_trusted_pot_nonpositive": float(np.nanmean(trusted_pot <= 0)),
        "p_trusted_not_better_than_untrusted": float(np.nanmean(diff <= 0)),
    }


def period_summary(blocks: pd.DataFrame, bets: pd.DataFrame) -> list[dict]:
    rows = []
    for period in ["2023", "2024", "2025", "2026_JAN_JUL"]:
        b = blocks[blocks.start_period.eq(period)]
        # Keep only bets from blocks anchored in this period; a rare cross-boundary block remains with its anchor period.
        ids = set(b.block_id.tolist())
        g = bets[bets.block_id.isin(ids)]
        t = g[g.past_trusted]
        u = g[~g.past_trusted]
        rows.append({
            "period": period,
            "blocks": int(len(b)),
            "trusted_blocks": int(b.past_trusted.sum()) if len(b) else 0,
            "untrusted_blocks": int((~b.past_trusted).sum()) if len(b) else 0,
            "trusted_positive_block_rate_7pct": float(b.loc[b.past_trusted, "future_profitable_7pct"].mean()) if b.past_trusted.any() else None,
            "trusted_n": int(len(t)),
            "trusted_pot_7pct": float(t.net_7pct.sum() / len(t)) if len(t) else None,
            "untrusted_n": int(len(u)),
            "untrusted_pot_7pct": float(u.net_7pct.sum() / len(u)) if len(u) else None,
        })
    return rows


def classify(blocks: pd.DataFrame, trusted: dict, untrusted: dict, boot: dict) -> dict:
    trusted_blocks = blocks[blocks.past_trusted]
    tests = {
        "at_least_20_forward_blocks": len(blocks) >= 20,
        "at_least_5_trusted_blocks": len(trusted_blocks) >= 5,
        "trusted_pot_7pct_positive": trusted["pot_7pct"] is not None and trusted["pot_7pct"] > 0,
        "trusted_rol_7pct_positive": trusted["rol_7pct"] is not None and trusted["rol_7pct"] > 0,
        "trusted_positive_block_rate_at_least_60pct": len(trusted_blocks) > 0 and float(trusted_blocks.future_profitable_7pct.mean()) >= 0.60,
        "trusted_minus_untrusted_ci_low_positive": boot["trusted_minus_untrusted_pot_7pct_ci95"][0] is not None and boot["trusted_minus_untrusted_pot_7pct_ci95"][0] > 0,
        "trusted_pot_ci_low_positive": boot["trusted_pot_7pct_ci95"][0] is not None and boot["trusted_pot_7pct_ci95"][0] > 0,
    }
    if all(tests.values()):
        label = "ECONOMIC_VALUE_SUPPORTED"
    elif (
        tests["at_least_20_forward_blocks"]
        and tests["at_least_5_trusted_blocks"]
        and tests["trusted_pot_7pct_positive"]
        and tests["trusted_rol_7pct_positive"]
        and trusted["pot_7pct"] > (untrusted["pot_7pct"] if untrusted["pot_7pct"] is not None else -999)
    ):
        label = "WEAK_ECONOMIC_VALUE"
    else:
        label = "NO_ECONOMIC_VALUE_EVIDENCE"
    return {
        "classification": label,
        "tests": tests,
        "guardrail": "Frozen Round026 gate: past 50 candidates by Brier advantage; primary future horizon=20 candidates, non-overlapping and date-safe. No parameter tuning in Round028.",
    }


def main() -> None:
    source_fingerprints = verify_source_vintage()
    x, integrity = candidate_history()
    blocks, bets = build_blocks(x)
    if len(blocks) < 20:
        raise RuntimeError(f"insufficient forward blocks: {len(blocks)}")

    all_metrics = aggregate_bets(bets, None)
    trusted_metrics = aggregate_bets(bets, True)
    untrusted_metrics = aggregate_bets(bets, False)
    boot = bootstrap_blocks(blocks)
    periods = period_summary(blocks, bets)
    decision = classify(blocks, trusted_metrics, untrusted_metrics, boot)

    status = {
        "round": 28,
        "capability": "HorseRacing.ForwardEconomicValueAudit",
        "status": "COMPLETE",
        "source_vintage": "ROUND026_SHA256_FROZEN_VINTAGE",
        "all_source_hashes_match": bool(all(r["match_round026_vintage"] for r in source_fingerprints)),
        "frozen_signal": "SA × model rank 2 × continuous value_calc < -7% × LAY",
        "frozen_gate": "past 50 candidate outcomes; MODEL_TRUSTED iff RP Brier < BSP Brier",
        "primary_forward_horizon": 20,
        "same_day_guard": "past window uses outcomes strictly before anchor date; future block never splits a date",
        "nonoverlap_guard": "future economic blocks are chronological and non-overlapping",
        "commission_contract": "market-net-winnings; flat nominal lay stake=1; primary economic stress uses 7% commission",
        "integrity": integrity,
        "block_count": int(len(blocks)),
        "trusted_block_count": int(blocks.past_trusted.sum()),
        "untrusted_block_count": int((~blocks.past_trusted).sum()),
        "trusted_positive_block_rate_7pct": float(blocks.loc[blocks.past_trusted, "future_profitable_7pct"].mean()),
        "untrusted_positive_block_rate_7pct": float(blocks.loc[~blocks.past_trusted, "future_profitable_7pct"].mean()),
        "all_forward_metrics": all_metrics,
        "trusted_metrics": trusted_metrics,
        "untrusted_metrics": untrusted_metrics,
        "bootstrap": boot,
        "period_summary": periods,
        "decision": decision,
        "governance": {
            "betting_ready": False,
            "note": "Retrospective leakage-safe forward-block audit on already-inspected historical years; not untouched live OOS."
        },
    }

    blocks.to_csv(OUT / "economic_blocks.csv", index=False)
    bets.to_csv(OUT / "economic_block_bets.csv", index=False)
    pd.DataFrame(periods).to_csv(OUT / "period_summary.csv", index=False)
    (OUT / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
