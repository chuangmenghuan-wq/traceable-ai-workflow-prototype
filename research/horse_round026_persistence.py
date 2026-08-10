from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from horse_round025_runtime import candidate_history

PAST_WINDOW = 50
PRIMARY_FUTURE = 20
FUTURE_HORIZONS = [20, 30, 50]
BOOTSTRAP_DRAWS = 10000
RNG_SEED = 260826
OUT = Path("research_outputs/horse_round026")
OUT.mkdir(parents=True, exist_ok=True)


def build_nonoverlap_blocks(x: pd.DataFrame, future_horizon: int) -> pd.DataFrame:
    """Build chronology-safe non-overlapping forward blocks.

    Each block's past window uses only rows with date < anchor date.
    The future block begins at anchor date and never splits a date; if the
    horizon boundary lands inside a date, all candidate rows on that date are
    included. The next block starts on the next available date, preventing
    overlap between forward outcomes.
    """
    y = x.sort_values(["date", "market_id", "selection_id"]).reset_index(drop=True).copy()
    dates = pd.Index(sorted(y.date.unique()))
    rows: list[dict] = []
    pos = 0

    while pos < len(dates):
        anchor = pd.Timestamp(dates[pos])
        prior = y[y.date < anchor]
        if len(prior) < PAST_WINDOW:
            pos += 1
            continue

        future_all = y[y.date >= anchor]
        if len(future_all) < future_horizon:
            break

        first_h = future_all.iloc[:future_horizon]
        end_date = pd.Timestamp(first_h.date.iloc[-1])
        future = y[(y.date >= anchor) & (y.date <= end_date)]
        if len(future) < future_horizon:
            raise AssertionError("future block shorter than requested horizon")

        past = prior.tail(PAST_WINDOW)
        past_market_brier = float(past.market_sqerr.mean())
        past_model_brier = float(past.model_sqerr.mean())
        future_market_brier = float(future.market_sqerr.mean())
        future_model_brier = float(future.model_sqerr.mean())
        past_adv = past_market_brier - past_model_brier
        future_adv = future_market_brier - future_model_brier

        rows.append({
            "future_horizon": future_horizon,
            "anchor_date": str(anchor.date()),
            "end_date": str(end_date.date()),
            "start_period": str(future.period.iloc[0]),
            "end_period": str(future.period.iloc[-1]),
            "past_n": int(len(past)),
            "future_n": int(len(future)),
            "past_market_brier": past_market_brier,
            "past_model_brier": past_model_brier,
            "past_adv": past_adv,
            "past_trusted": bool(past_adv > 0),
            "future_market_brier": future_market_brier,
            "future_model_brier": future_model_brier,
            "future_adv": future_adv,
            "future_model_better": bool(future_adv > 0),
            "sign_correct": bool((past_adv > 0) == (future_adv > 0)),
        })

        # Advance to the first date strictly after this completed future block.
        pos = int(dates.searchsorted(np.datetime64(end_date), side="right"))

    return pd.DataFrame(rows)


def ci(vals: np.ndarray, q=(0.025, 0.975)) -> list[float | None]:
    vals = vals[np.isfinite(vals)]
    if len(vals) == 0:
        return [None, None]
    a, b = np.quantile(vals, q)
    return [float(a), float(b)]


def bootstrap(blocks: pd.DataFrame) -> dict:
    rng = np.random.default_rng(RNG_SEED + int(blocks.future_horizon.iloc[0]))
    n = len(blocks)
    if n == 0:
        return {}

    direction = np.empty(BOOTSTRAP_DRAWS)
    trusted_mean = np.full(BOOTSTRAP_DRAWS, np.nan)
    diff_mean = np.full(BOOTSTRAP_DRAWS, np.nan)
    trusted_rate = np.full(BOOTSTRAP_DRAWS, np.nan)

    for i in range(BOOTSTRAP_DRAWS):
        s = blocks.iloc[rng.integers(0, n, size=n)]
        direction[i] = float(s.sign_correct.mean())
        t = s[s.past_trusted]
        u = s[~s.past_trusted]
        if len(t):
            trusted_mean[i] = float(t.future_adv.mean())
            trusted_rate[i] = float(t.future_model_better.mean())
        if len(t) and len(u):
            diff_mean[i] = float(t.future_adv.mean() - u.future_adv.mean())

    return {
        "directional_accuracy_ci95": ci(direction),
        "trusted_future_adv_mean_ci95": ci(trusted_mean),
        "trusted_future_positive_rate_ci95": ci(trusted_rate),
        "trusted_minus_untrusted_future_adv_ci95": ci(diff_mean),
    }


def summarize(blocks: pd.DataFrame) -> dict:
    t = blocks[blocks.past_trusted]
    u = blocks[~blocks.past_trusted]
    pearson = None
    spearman = None
    if len(blocks) >= 3 and blocks.past_adv.std(ddof=0) > 0 and blocks.future_adv.std(ddof=0) > 0:
        pearson = float(blocks[["past_adv", "future_adv"]].corr(method="pearson").iloc[0, 1])
        spearman = float(blocks[["past_adv", "future_adv"]].corr(method="spearman").iloc[0, 1])

    out = {
        "future_horizon": int(blocks.future_horizon.iloc[0]),
        "blocks": int(len(blocks)),
        "trusted_blocks": int(len(t)),
        "untrusted_blocks": int(len(u)),
        "directional_accuracy": float(blocks.sign_correct.mean()),
        "trusted_future_positive_rate": float(t.future_model_better.mean()) if len(t) else None,
        "untrusted_future_positive_rate": float(u.future_model_better.mean()) if len(u) else None,
        "trusted_future_adv_mean": float(t.future_adv.mean()) if len(t) else None,
        "untrusted_future_adv_mean": float(u.future_adv.mean()) if len(u) else None,
        "trusted_minus_untrusted_future_adv": float(t.future_adv.mean() - u.future_adv.mean()) if len(t) and len(u) else None,
        "pearson_past_future_adv": pearson,
        "spearman_past_future_adv": spearman,
        "confusion": {
            "past_trusted_future_positive": int(((blocks.past_trusted) & (blocks.future_model_better)).sum()),
            "past_trusted_future_negative": int(((blocks.past_trusted) & (~blocks.future_model_better)).sum()),
            "past_untrusted_future_positive": int(((~blocks.past_trusted) & (blocks.future_model_better)).sum()),
            "past_untrusted_future_negative": int(((~blocks.past_trusted) & (~blocks.future_model_better)).sum()),
        },
    }
    out.update(bootstrap(blocks))
    return out


def by_period(blocks: pd.DataFrame) -> list[dict]:
    rows = []
    for period, g in blocks.groupby("start_period", sort=False):
        t = g[g.past_trusted]
        rows.append({
            "future_horizon": int(g.future_horizon.iloc[0]),
            "period": str(period),
            "blocks": int(len(g)),
            "trusted_blocks": int(len(t)),
            "directional_accuracy": float(g.sign_correct.mean()),
            "trusted_future_positive_rate": float(t.future_model_better.mean()) if len(t) else None,
            "trusted_future_adv_mean": float(t.future_adv.mean()) if len(t) else None,
            "false_positive_trusted_blocks": int(((g.past_trusted) & (~g.future_model_better)).sum()),
        })
    return rows


def classify(primary: dict) -> dict:
    ci_low = primary["trusted_future_adv_mean_ci95"][0]
    tests = {
        "at_least_20_nonoverlap_blocks": primary["blocks"] >= 20,
        "at_least_5_trusted_blocks": primary["trusted_blocks"] >= 5,
        "directional_accuracy_at_least_60pct": primary["directional_accuracy"] >= 0.60,
        "trusted_future_positive_rate_at_least_65pct": (
            primary["trusted_future_positive_rate"] is not None
            and primary["trusted_future_positive_rate"] >= 0.65
        ),
        "trusted_future_adv_mean_positive": (
            primary["trusted_future_adv_mean"] is not None
            and primary["trusted_future_adv_mean"] > 0
        ),
        "trusted_future_adv_bootstrap_ci_low_positive": ci_low is not None and ci_low > 0,
    }
    if all(tests.values()):
        label = "PERSISTENCE_SUPPORTED"
    elif (
        tests["at_least_20_nonoverlap_blocks"]
        and tests["at_least_5_trusted_blocks"]
        and primary["directional_accuracy"] >= 0.55
        and primary["trusted_future_adv_mean"] is not None
        and primary["trusted_future_adv_mean"] > 0
    ):
        label = "WEAK_PERSISTENCE_ONLY"
    else:
        label = "NO_PERSISTENCE_EVIDENCE"
    return {
        "classification": label,
        "tests": tests,
        "guardrail": (
            "Primary test frozen as past 50 candidate outcomes -> next 20 candidate outcomes, "
            "chronological non-overlapping forward blocks with date boundaries. Horizons 30/50 "
            "are sensitivity only and cannot replace the primary horizon 20 in Round 026."
        ),
    }


def main() -> None:
    x, integrity = candidate_history()
    all_blocks = []
    summaries = []
    period_rows = []

    for h in FUTURE_HORIZONS:
        b = build_nonoverlap_blocks(x, h)
        if b.empty:
            raise RuntimeError(f"no blocks for future horizon {h}")
        all_blocks.append(b)
        summaries.append(summarize(b))
        period_rows.extend(by_period(b))

    blocks = pd.concat(all_blocks, ignore_index=True)
    blocks.to_csv(OUT / "persistence_blocks.csv", index=False)
    pd.DataFrame(period_rows).to_csv(OUT / "period_summary.csv", index=False)
    (OUT / "summary.json").write_text(json.dumps(summaries, indent=2), encoding="utf-8")

    primary = next(s for s in summaries if s["future_horizon"] == PRIMARY_FUTURE)
    decision = classify(primary)

    false_pos_2024 = blocks[
        (blocks.future_horizon == PRIMARY_FUTURE)
        & (blocks.start_period == "2024")
        & (blocks.past_trusted)
        & (~blocks.future_model_better)
    ][["anchor_date", "end_date", "past_adv", "future_adv", "future_n"]].to_dict("records")

    status = {
        "round": 26,
        "capability": "HorseRacing.RegimePersistenceAudit",
        "status": "COMPLETE",
        "frozen_signal": "SA × model rank 2 × continuous value_calc < -7% × LAY",
        "primary_test": "past 50 candidate Brier advantage predicts next 20 candidate Brier advantage",
        "same_day_guard": "past window uses dates strictly before anchor; future block never splits a date",
        "nonoverlap_guard": "primary future outcome blocks are chronological and non-overlapping",
        "sensitivity_future_horizons": [30, 50],
        "integrity": integrity,
        "summaries": summaries,
        "period_summary": period_rows,
        "primary_2024_false_positive_blocks": false_pos_2024,
        "decision": decision,
    }
    (OUT / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
