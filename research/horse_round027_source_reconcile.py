from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from horse_round025_runtime import PERIODS, PERIOD_ORDER, candidate_history, download

OUT = Path("research_outputs/horse_round027")
OUT.mkdir(parents=True, exist_ok=True)
RNG_SEED = 270826
BOOTSTRAP_DRAWS = 5000

EXPECTED_SHA256 = {
    "Kash_Model_Results_2023.csv": "68208577fb67d24057a651db65ff99b526a2b79129f930efde4dc5760f229e2e",
    "Kash_Model_Results_2024.csv": "fe2604156e36fd05af80e125cc0ed5ae088cc57f02d512c03dc9204a8cdadfef",
    "Kash_Model_Results_2025.csv": "a6b51f3f174a44a169fb320b09e34d734f817d378144d733ac25345065feb758",
    "Kash_Model_Results_2026_01.csv": "54c8980ccffbd43efa799569da4e563e5b5c63f16330a287f5978d1f599c6d16",
    "Kash_Model_Results_2026_02.csv": "4efc4513ab58fd91a7769110683f1581759a29669e4e097ed1918a1bf4a77ab2",
    "Kash_Model_Results_2026_03.csv": "6e2900590efd1effc2b6fa834ea0a130df948400985b86fca5f5beddcb6d4aaf",
    "Kash_Model_Results_2026_04.csv": "724f10686d438a886227c6aa9c85efd039e7ada149046d53b88522d312b22882",
    "Kash_Model_Results_2026_05.csv": "c8b5824d0964085fbe147a73fb6c2af0681fadcbdd5b5d04744a3e49158b8c3b",
    "Kash_Model_Results_2026_06.csv": "c689c8586ac28c013cd249a987bed8172e7d197b6dea07bfadbdfa9714211641",
    "Kash_Model_Results_2026_07.csv": "8dbab7c394347e87e6ad55193370d81d19c2690bfb4c7ffce243c1b25ea29c7c",
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_source_vintage() -> list[dict]:
    rows = []
    seen = set()
    for period in PERIOD_ORDER:
        for url in PERIODS[period]:
            p = download(url)
            if p.name in seen:
                continue
            seen.add(p.name)
            got = sha256_file(p)
            expected = EXPECTED_SHA256[p.name]
            ok = got == expected
            rows.append({
                "period": period,
                "file": p.name,
                "bytes": int(p.stat().st_size),
                "sha256": got,
                "expected_sha256": expected,
                "match_round026_vintage": ok,
            })
            if not ok:
                raise RuntimeError(f"SOURCE_VINTAGE_CHANGED {p.name}: expected={expected} got={got}")
    return rows


def market_net_pnl(x: pd.DataFrame, commission: float) -> pd.DataFrame:
    gross = np.where(x.win.eq(1), -(x.bsp - 1.0), 1.0)
    z = pd.DataFrame({
        "date": x.date.to_numpy(),
        "market_id": x.market_id.to_numpy(),
        "gross": gross,
        "liability": (x.bsp - 1.0).to_numpy(),
    })
    # Candidate is one R2 selection per market, but retain market aggregation for contract consistency.
    z = z.groupby(["date", "market_id"], as_index=False).agg(gross=("gross", "sum"), liability=("liability", "sum"))
    z["net"] = z.gross - np.where(z.gross > 0, commission * z.gross, 0.0)
    return z.sort_values(["date", "market_id"]).reset_index(drop=True)


def max_drawdown(z: pd.DataFrame) -> float:
    if z.empty:
        return 0.0
    eq = z.net.cumsum().to_numpy(float)
    peak = np.maximum.accumulate(np.r_[0.0, eq])[:-1]
    dd = peak - eq
    return float(np.max(dd)) if len(dd) else 0.0


def bootstrap_pot(x: pd.DataFrame, commission: float, draws: int = BOOTSTRAP_DRAWS) -> dict:
    if x.empty:
        return {"ci95": [None, None], "p_nonpositive": None}
    # One candidate per market after rank/dedup, resample markets to preserve market atomicity.
    markets = list(x.market_id.unique())
    groups = {m: x[x.market_id.eq(m)] for m in markets}
    rng = np.random.default_rng(RNG_SEED + int(round(commission * 1000)))
    vals = np.empty(draws)
    for i in range(draws):
        sampled = rng.choice(markets, size=len(markets), replace=True)
        pieces = []
        # Re-label duplicated market draws so duplicated samples remain distinct settlement units.
        for j, m in enumerate(sampled):
            g = groups[m].copy()
            g["market_id"] = f"{m}__boot{j}"
            pieces.append(g)
        s = pd.concat(pieces, ignore_index=True)
        z = market_net_pnl(s, commission)
        vals[i] = float(z.net.sum() / len(s))
    q = np.quantile(vals, [0.025, 0.975])
    return {"ci95": [float(q[0]), float(q[1])], "p_nonpositive": float((vals <= 0).mean())}


def period_metrics(x: pd.DataFrame, period: str) -> dict:
    p = x[x.period.eq(period)].sort_values(["date", "market_id", "selection_id"]).copy()
    if p.empty:
        raise RuntimeError(f"no candidates for {period}")
    out = {
        "period": period,
        "date_min": str(p.date.min().date()),
        "date_max": str(p.date.max().date()),
        "n": int(len(p)),
        "markets": int(p.market_id.nunique()),
        "horse_wins": int(p.win.sum()),
        "horse_win_rate": float(p.win.mean()),
        "lay_success_rate": float(1.0 - p.win.mean()),
        "avg_bsp": float(p.bsp.mean()),
        "median_bsp": float(p.bsp.median()),
        "avg_model_odds": float(p.model_odds.mean()),
        "avg_model_prob": float(p.model_prob.mean()),
        "avg_market_prob": float(p.market_prob.mean()),
        "avg_value_calc": float(p.value_calc.mean()),
    }
    cs = {}
    for c in [0.02, 0.03, 0.04, 0.05, 0.06, 0.07]:
        z = market_net_pnl(p, c)
        key = f"{int(c*100)}pct"
        cs[key] = {
            "net_pl": float(z.net.sum()),
            "pot": float(z.net.sum() / len(p)),
            "return_on_liability": float(z.net.sum() / z.liability.sum()),
        }
        if c == 0.05:
            out["max_drawdown_5pct"] = max_drawdown(z)
    out["commission_sensitivity"] = cs
    out["bootstrap_5pct"] = bootstrap_pot(p, 0.05)
    return out


def monthly_metrics(x: pd.DataFrame) -> list[dict]:
    rows = []
    y = x.copy()
    y["month"] = y.date.dt.to_period("M").astype(str)
    for month, g in y.groupby("month", sort=True):
        z5 = market_net_pnl(g, 0.05)
        z7 = market_net_pnl(g, 0.07)
        rows.append({
            "month": month,
            "period": str(g.period.iloc[0]),
            "n": int(len(g)),
            "horse_win_rate": float(g.win.mean()),
            "pot_5pct": float(z5.net.sum() / len(g)),
            "pot_7pct": float(z7.net.sum() / len(g)),
        })
    return rows


def aggregate_metrics(x: pd.DataFrame) -> dict:
    z5 = market_net_pnl(x, 0.05)
    z7 = market_net_pnl(x, 0.07)
    return {
        "n": int(len(x)),
        "markets": int(x.market_id.nunique()),
        "date_min": str(x.date.min().date()),
        "date_max": str(x.date.max().date()),
        "net_pl_5pct": float(z5.net.sum()),
        "pot_5pct": float(z5.net.sum() / len(x)),
        "pot_7pct": float(z7.net.sum() / len(x)),
        "max_drawdown_5pct": max_drawdown(z5),
        "bootstrap_5pct": bootstrap_pot(x, 0.05),
    }


def main() -> None:
    fingerprints = verify_source_vintage()
    x, integrity = candidate_history()
    periods = [period_metrics(x, p) for p in PERIOD_ORDER]
    months = monthly_metrics(x)
    aggregate = aggregate_metrics(x)

    # A reconciliation round must report the current-vintage baseline only; older-vintage values remain historical receipts.
    status = {
        "round": 27,
        "capability": "HorseRacing.SourceVersionReconciliation",
        "status": "COMPLETE",
        "source_vintage": "ROUND026_SHA256_FROZEN_VINTAGE",
        "all_source_hashes_match_round026": bool(all(r["match_round026_vintage"] for r in fingerprints)),
        "frozen_signal": "SA × model rank 2 × continuous value_calc < -7% × LAY",
        "commission_contract": "market-net-winnings commission; flat nominal lay stake=1; liability=BSP-1",
        "source_fingerprints": fingerprints,
        "integrity": integrity,
        "period_metrics": periods,
        "aggregate_metrics": aggregate,
        "monthly_metrics": months,
        "governance": {
            "round020_2026_old_vintage": "SUPERSEDED_FOR_CROSS_ROUND_COMPARISON",
            "rule": "All future comparisons must either match these SHA256 hashes or declare a new source vintage before computing strategy deltas.",
            "betting_ready": False,
        },
    }
    (OUT / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    pd.DataFrame(periods).to_json(OUT / "period_metrics.json", orient="records", indent=2)
    pd.DataFrame(months).to_csv(OUT / "monthly_metrics.csv", index=False)
    pd.DataFrame(fingerprints).to_csv(OUT / "source_fingerprints.csv", index=False)
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
