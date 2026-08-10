from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import requests

BASE = "https://betfair-datascientists.github.io/data/assets"
PERIODS = {
    "2023": [f"{BASE}/Kash_Model_Results_2023.csv"],
    "2024": [f"{BASE}/Kash_Model_Results_2024.csv"],
    "2025": [f"{BASE}/Kash_Model_Results_2025.csv"],
    "2026_JAN_JUL": [f"{BASE}/Kash_Model_Results_2026_{m:02d}.csv" for m in range(1, 8)],
}
PERIOD_ORDER = ["2023", "2024", "2025", "2026_JAN_JUL"]
WINDOWS = [30, 50, 100]
PRIMARY_WINDOW = 50

SA_TRACKS = {
    "Balaklava", "Bordertown", "Clare", "Gawler", "Halidon", "Kangaroo Island",
    "Morphettville", "Morphettville Parks", "Mount Gambier", "Murray Bridge",
    "Naracoorte", "Oakbank", "Penola", "Port Augusta", "Port Lincoln", "Strathalbyn",
}
DATE_FORMATS = ["%d/%m/%Y", "%Y-%m-%d"]
CACHE = Path(".cache/horse_round025")
OUT = Path("research_outputs/horse_round025")
CACHE.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)


def download(url: str) -> Path:
    p = CACHE / url.rsplit("/", 1)[-1]
    if p.exists() and p.stat().st_size > 1024:
        return p
    with requests.get(url, stream=True, timeout=(20, 300)) as resp:
        resp.raise_for_status()
        with p.open("wb") as fh:
            for chunk in resp.iter_content(1024 * 1024):
                if chunk:
                    fh.write(chunk)
    return p


def parse_dates(raw: pd.Series, filename: str) -> tuple[pd.Series, str]:
    s = raw.astype(str).str.strip()
    m = re.search(r"_(20\d{2})(?:_(\d{2}))?\.csv$", filename)
    expected_year = int(m.group(1))
    expected_month = int(m.group(2)) if m.group(2) else None
    candidates = []
    for fmt in DATE_FORMATS:
        dt = pd.to_datetime(s, format=fmt, errors="coerce")
        valid = dt.notna()
        vr = float(valid.mean())
        yr = float((dt[valid].dt.year == expected_year).mean()) if valid.any() else 0.0
        mr = float((dt[valid].dt.month == expected_month).mean()) if valid.any() and expected_month else 1.0
        score = (mr, yr, vr) if expected_month else (yr, vr)
        candidates.append((score, dt, fmt, vr, yr, mr))
    score, dt, fmt, vr, yr, mr = max(candidates, key=lambda z: z[0])
    if vr < 0.99 or yr < 0.999 or (expected_month and mr < 0.999):
        raise ValueError(f"date parse fail {filename}: fmt={fmt} valid={vr} year={yr} month={mr}")
    return dt, fmt


def load_file(url: str, period: str) -> pd.DataFrame:
    p = download(url)
    cols = ["Date", "Track", "Market", "Selection", "RP", "WIN_BSP", "WIN_RESULT"]
    d = pd.read_csv(p, usecols=cols, low_memory=False)
    d["source_file"] = p.name
    d["period"] = period
    d["date"], d["date_fmt"] = parse_dates(d.Date, p.name)
    d["track"] = d.Track.astype(str).str.strip()
    d["market_id"] = d.Market.astype(str)
    d["selection_id"] = d.Selection.astype(str)
    d["model_odds"] = pd.to_numeric(d.RP, errors="coerce")
    d["bsp"] = pd.to_numeric(d.WIN_BSP, errors="coerce")
    d["win"] = pd.to_numeric(d.WIN_RESULT, errors="coerce")
    d["model_prob"] = 1.0 / d.model_odds
    d["market_prob"] = 1.0 / d.bsp
    d["value_calc"] = d.model_prob - d.market_prob
    d = d.replace([np.inf, -np.inf], np.nan).dropna(
        subset=["date", "market_id", "selection_id", "model_odds", "bsp", "win", "value_calc"]
    )
    return d[(d.model_odds > 1) & (d.bsp > 1) & d.win.isin([0, 1])]


def load_period(period: str, urls: list[str]) -> tuple[pd.DataFrame, dict]:
    d = pd.concat([load_file(u, period) for u in urls], ignore_index=True)
    raw_n = len(d)
    dup_rows = int(d.duplicated(["market_id", "selection_id"], keep=False).sum())
    d = d.sort_values(["market_id", "selection_id", "date"]).drop_duplicates(
        ["market_id", "selection_id"], keep="last"
    ).copy()
    d["model_rank"] = d.groupby("market_id").model_odds.rank(method="first", ascending=True)
    integrity = {
        "period": period,
        "raw_usable_rows": int(raw_n),
        "dedup_rows": int(len(d)),
        "duplicate_rows": dup_rows,
        "date_min": str(d.date.min().date()),
        "date_max": str(d.date.max().date()),
        "date_parsers": d.groupby("source_file").date_fmt.first().to_dict(),
    }
    return d, integrity


def candidate_history() -> tuple[pd.DataFrame, list[dict]]:
    parts, integrity = [], []
    for period in PERIOD_ORDER:
        d, info = load_period(period, PERIODS[period])
        sa = d[d.track.isin(SA_TRACKS)].copy()
        r2 = sa[sa.model_rank.eq(2)].copy()
        x = r2[r2.value_calc.lt(-0.07)].copy()
        x["period"] = period
        x["market_sqerr"] = (x.win - x.market_prob) ** 2
        x["model_sqerr"] = (x.win - x.model_prob) ** 2
        info.update({
            "sa_markets": int(sa.market_id.nunique()),
            "sa_r2": int(len(r2)),
            "candidate_rows": int(len(x)),
            "candidate_markets": int(x.market_id.nunique()),
        })
        integrity.append(info)
        parts.append(x)
    x = pd.concat(parts, ignore_index=True).sort_values(
        ["date", "market_id", "selection_id"]
    ).reset_index(drop=True)
    return x, integrity


def apply_gate(x: pd.DataFrame, window: int) -> pd.DataFrame:
    y = x.copy()
    fields = [
        f"gate_{window}", f"hist_n_{window}", f"hist_brier_adv_{window}",
        f"hist_market_brier_{window}", f"hist_model_brier_{window}",
    ]
    for f in fields:
        y[f] = np.nan
    history_idx: list[int] = []
    for _, idx in y.groupby("date", sort=True).groups.items():
        idx = list(idx)
        prior = y.loc[history_idx].tail(window) if history_idx else y.iloc[0:0]
        if len(prior) >= window:
            mb = float(prior.market_sqerr.mean())
            rb = float(prior.model_sqerr.mean())
            adv = mb - rb
            vals = [bool(adv > 0), int(len(prior)), adv, mb, rb]
        else:
            vals = [False, int(len(prior)), np.nan, np.nan, np.nan]
        for f, v in zip(fields, vals):
            y.loc[idx, f] = v
        history_idx.extend(idx)
    y[f"gate_{window}"] = y[f"gate_{window}"].astype(bool)
    return y


def pnl(x: pd.DataFrame, commission: float) -> dict:
    if x.empty:
        return {"n": 0, "markets": 0, "pl": 0.0, "pot": None, "win_rate": None}
    gross = np.where(x.win.eq(1), -(x.bsp - 1.0), 1.0)
    z = pd.DataFrame({"market_id": x.market_id.to_numpy(), "gross": gross})
    z = z.groupby("market_id", as_index=False).gross.sum()
    z["net"] = z.gross - np.where(z.gross > 0, commission * z.gross, 0.0)
    return {
        "n": int(len(x)),
        "markets": int(x.market_id.nunique()),
        "pl": float(z.net.sum()),
        "pot": float(z.net.sum() / len(x)),
        "win_rate": float(x.win.mean()),
    }


def evaluate(x: pd.DataFrame, window: int) -> tuple[list[dict], list[dict]]:
    gcol = f"gate_{window}"
    rows = []
    for period in PERIOD_ORDER:
        p = x[x.period.eq(period)]
        b5, b7 = pnl(p, .05), pnl(p, .07)
        on5, on7 = pnl(p[p[gcol]], .05), pnl(p[p[gcol]], .07)
        off5, off7 = pnl(p[~p[gcol]], .05), pnl(p[~p[gcol]], .07)
        rows.append({
            "window": window, "period": period,
            "baseline_n": b5["n"], "baseline_pl_5": b5["pl"], "baseline_pot_5": b5["pot"], "baseline_pot_7": b7["pot"],
            "gated_n": on5["n"], "retention": on5["n"] / b5["n"] if b5["n"] else None,
            "gated_pl_5": on5["pl"], "gated_pot_5": on5["pot"], "gated_pot_7": on7["pot"], "gated_horse_win_rate": on5["win_rate"],
            "blocked_n": off5["n"], "blocked_pl_5": off5["pl"], "blocked_pot_5": off5["pot"], "blocked_pot_7": off7["pot"],
        })
    daily = x.groupby("date", as_index=False).agg(
        period=("period", "first"), gate=(gcol, "first"),
        hist_n=(f"hist_n_{window}", "first"),
        hist_brier_adv=(f"hist_brier_adv_{window}", "first"),
        hist_market_brier=(f"hist_market_brier_{window}", "first"),
        hist_model_brier=(f"hist_model_brier_{window}", "first"),
    ).sort_values("date")
    daily["prev_gate"] = daily.gate.shift(1)
    transitions = []
    for _, r in daily[(daily.hist_n >= window) & daily.prev_gate.notna() & daily.gate.ne(daily.prev_gate)].iterrows():
        transitions.append({
            "window": window, "date": str(r.date.date()), "period": r.period,
            "new_state": "MODEL_TRUSTED" if bool(r.gate) else "MODEL_NOT_TRUSTED",
            "hist_brier_adv": float(r.hist_brier_adv),
            "hist_market_brier": float(r.hist_market_brier),
            "hist_model_brier": float(r.hist_model_brier),
        })
    return rows, transitions


def classify(summary: pd.DataFrame) -> dict:
    s = summary[summary.window.eq(PRIMARY_WINDOW)].set_index("period")
    y23, y25, y26 = s.loc["2023"], s.loc["2025"], s.loc["2026_JAN_JUL"]
    recent_base = y25.baseline_n + y26.baseline_n
    recent_gated = y25.gated_n + y26.gated_n
    tests = {
        "reduces_2023_loss_by_at_least_50pct": bool(y23.gated_pl_5 > 0.5 * y23.baseline_pl_5),
        "2025_positive_at_7pct": bool(pd.notna(y25.gated_pot_7) and y25.gated_pot_7 > 0),
        "2026_positive_at_7pct": bool(pd.notna(y26.gated_pot_7) and y26.gated_pot_7 > 0),
        "recent_gated_n_at_least_50": bool(recent_gated >= 50),
        "recent_retention_at_least_25pct": bool(recent_gated / recent_base >= .25),
    }
    passed = all(tests.values())
    return {
        "classification": "PROMISING_WALK_FORWARD_GATE" if passed else "GATE_NOT_PROVEN",
        "primary_window": PRIMARY_WINDOW,
        "tests": tests,
        "passed_all": passed,
        "guardrail": "Retrospective leakage-safe walk-forward on already-inspected history; not a new untouched OOS. Windows 30/100 are sensitivity only and cannot replace primary window 50 in this round.",
    }


def main() -> None:
    x, integrity = candidate_history()
    for w in WINDOWS:
        x = apply_gate(x, w)
    rows, transitions = [], []
    for w in WINDOWS:
        a, b = evaluate(x, w)
        rows += a
        transitions += b
    summary = pd.DataFrame(rows)
    summary.to_csv(OUT / "rolling_gate_summary.csv", index=False)
    pd.DataFrame(transitions).to_csv(OUT / "gate_transitions.csv", index=False)
    decision = classify(summary)
    status = {
        "round": 25,
        "capability": "HorseRacing.RollingRegimeGate",
        "execution_plane": "isolated public GitHub Actions runtime; no Future_Ability private code copied",
        "status": "COMPLETE",
        "frozen_signal": "SA × model rank 2 × continuous value_calc < -7% × LAY",
        "primary_gate": "trailing 50 candidate bets from strictly earlier dates; trusted iff RP Brier < BSP Brier",
        "same_day_leakage_guard": "date D gate uses only outcomes with date < D",
        "sensitivity_windows": [30, 100],
        "integrity": integrity,
        "summary": rows,
        "transitions": transitions,
        "decision": decision,
    }
    (OUT / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
