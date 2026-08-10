from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from horse_round025_runtime import SA_TRACKS, candidate_history
from horse_round027_source_reconcile import verify_source_vintage

OUT = Path("research_outputs/horse_round029")
OUT.mkdir(parents=True, exist_ok=True)

HOLDOUT_START = pd.Timestamp("2026-08-01")
HOLDOUT_END = pd.Timestamp("2026-08-10")
PAST_WINDOW = 50
PRIMARY_COMMISSION = 0.07
KASH_DAILY = (
    "https://betfair-data-supplier-prod.herokuapp.com/api/widgets/"
    "kash-ratings-model/datasets?date={date}&presenter=RatingsPresenter&csv=true"
)
MONTHLY_URL = "https://betfair-datascientists.github.io/data/assets/Kash_Model_Results_2026_08.csv"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def get_bytes(url: str) -> tuple[int, bytes, str]:
    r = requests.get(url, timeout=(20, 120))
    return r.status_code, r.content, r.headers.get("content-type", "")


def norm_colmap(cols) -> dict[str, str]:
    return {str(c).strip().upper(): str(c) for c in cols}


def pick(cm: dict[str, str], *names: str) -> str | None:
    for n in names:
        if n.upper() in cm:
            return cm[n.upper()]
    return None


def parse_daily(raw: bytes, date: pd.Timestamp, source_name: str) -> tuple[pd.DataFrame, dict]:
    text = raw.decode("utf-8-sig", errors="replace")
    if not text.strip():
        return pd.DataFrame(), {"date": str(date.date()), "source": source_name, "status": "EMPTY"}
    try:
        d = pd.read_csv(io.StringIO(text), low_memory=False)
    except Exception as e:
        return pd.DataFrame(), {
            "date": str(date.date()), "source": source_name,
            "status": "CSV_PARSE_FAIL", "error": str(e), "prefix": text[:200],
        }
    cm = norm_colmap(d.columns)
    mapped = {
        "track": pick(cm, "Track", "Venue"),
        "market_id": pick(cm, "Market", "MarketId", "MARKET_ID"),
        "selection_id": pick(cm, "Selection", "SelectionId", "SELECTION_ID"),
        "model_odds": pick(cm, "RP", "Model Odds", "MODEL_ODDS"),
        "bsp": pick(cm, "WIN_BSP", "BSP", "Win BSP"),
        "win": pick(cm, "WIN_RESULT", "RESULT", "Win Result"),
    }
    qa = {
        "date": str(date.date()), "source": source_name, "status": "PARSED",
        "rows": int(len(d)), "columns": [str(c) for c in d.columns], "mapped": mapped,
    }
    required = ["track", "market_id", "selection_id", "model_odds", "bsp", "win"]
    missing = [k for k in required if mapped[k] is None]
    if missing:
        qa["status"] = "MISSING_SETTLEMENT_COLUMNS"
        qa["missing"] = missing
        return pd.DataFrame(), qa

    x = pd.DataFrame({
        "date": date,
        "track": d[mapped["track"]].astype(str).str.strip(),
        "market_id": d[mapped["market_id"]].astype(str),
        "selection_id": d[mapped["selection_id"]].astype(str),
        "model_odds": pd.to_numeric(d[mapped["model_odds"]], errors="coerce"),
        "bsp": pd.to_numeric(d[mapped["bsp"]], errors="coerce"),
        "win": pd.to_numeric(d[mapped["win"]], errors="coerce"),
    })
    x = x.replace([np.inf, -np.inf], np.nan).dropna(
        subset=["model_odds", "bsp", "win", "market_id", "selection_id"]
    )
    x = x[(x.model_odds > 1) & (x.bsp > 1) & x.win.isin([0, 1])].copy()
    x = x.sort_values(["market_id", "selection_id"]).drop_duplicates(
        ["market_id", "selection_id"], keep="last"
    )
    x["model_rank"] = x.groupby("market_id").model_odds.rank(method="first", ascending=True)
    x["model_prob"] = 1.0 / x.model_odds
    x["market_prob"] = 1.0 / x.bsp
    x["value_calc"] = x.model_prob - x.market_prob
    x["model_sqerr"] = (x.win - x.model_prob) ** 2
    x["market_sqerr"] = (x.win - x.market_prob) ** 2
    qa["usable_rows"] = int(len(x))
    qa["markets"] = int(x.market_id.nunique())
    return x, qa


def candidate_rows(d: pd.DataFrame) -> pd.DataFrame:
    if d.empty:
        return d
    return d[
        d.track.isin(SA_TRACKS)
        & d.model_rank.eq(2)
        & d.value_calc.lt(-0.07)
    ].copy()


def pnl(candidate: pd.DataFrame, commission: float) -> dict:
    if candidate.empty:
        return {"n": 0, "net_pl": 0.0, "pot": None, "rol": None, "horse_win_rate": None}
    gross = np.where(candidate.win.eq(1), -(candidate.bsp - 1.0), 1.0)
    net = gross - np.where(gross > 0, commission * gross, 0.0)
    liability = candidate.bsp.to_numpy(float) - 1.0
    return {
        "n": int(len(candidate)),
        "net_pl": float(net.sum()),
        "pot": float(net.sum() / len(candidate)),
        "rol": float(net.sum() / liability.sum()),
        "horse_win_rate": float(candidate.win.mean()),
    }


def main() -> None:
    # Freeze/re-verify the exact pre-August historical vintage before evaluating unseen dates.
    historical_fingerprints = verify_source_vintage()
    history, integrity = candidate_history()
    history = history[history.date < HOLDOUT_START].sort_values(["date", "market_id", "selection_id"]).copy()
    if len(history) < PAST_WINDOW:
        raise RuntimeError("insufficient pre-holdout history")

    monthly_status, monthly_bytes, monthly_ct = get_bytes(MONTHLY_URL)
    source_probe = {
        "monthly_url": MONTHLY_URL,
        "monthly_http_status": monthly_status,
        "monthly_content_type": monthly_ct,
        "monthly_bytes": int(len(monthly_bytes)),
        "monthly_sha256": sha256_bytes(monthly_bytes) if monthly_status == 200 else None,
    }

    daily_qa = []
    all_aug_candidates = []
    gate_days = []
    working_history = history.copy()
    settlement_available_days = 0

    for date in pd.date_range(HOLDOUT_START, HOLDOUT_END, freq="D"):
        prior = working_history[working_history.date < date].tail(PAST_WINDOW)
        mb = float(prior.market_sqerr.mean())
        rb = float(prior.model_sqerr.mean())
        adv = mb - rb
        gate_on = bool(adv > 0)

        url = KASH_DAILY.format(date=str(date.date()))
        status, raw, ct = get_bytes(url)
        qa = {
            "date": str(date.date()), "url": url, "http_status": status,
            "content_type": ct, "bytes": int(len(raw)),
            "sha256": sha256_bytes(raw) if status == 200 else None,
        }
        if status != 200:
            qa["status"] = "HTTP_UNAVAILABLE"
            daily_qa.append(qa)
            gate_days.append({
                "date": str(date.date()), "gate_on": gate_on, "past_n": int(len(prior)),
                "past_brier_adv": adv, "candidate_n": None, "settled": False,
            })
            continue

        parsed, pqa = parse_daily(raw, date, f"daily:{date.date()}")
        qa.update(pqa)
        daily_qa.append(qa)
        if parsed.empty and pqa.get("status") != "PARSED":
            gate_days.append({
                "date": str(date.date()), "gate_on": gate_on, "past_n": int(len(prior)),
                "past_brier_adv": adv, "candidate_n": None, "settled": False,
            })
            continue

        settlement_available_days += 1
        cand = candidate_rows(parsed)
        if not cand.empty:
            cand["gate_on"] = gate_on
            cand["past_brier_adv"] = adv
            all_aug_candidates.append(cand)
        gate_days.append({
            "date": str(date.date()), "gate_on": gate_on, "past_n": int(len(prior)),
            "past_brier_adv": adv, "candidate_n": int(len(cand)), "settled": True,
        })
        # Only after date D is settled may D outcomes enter the history for D+1.
        if not cand.empty:
            working_history = pd.concat([working_history, cand], ignore_index=True).sort_values(
                ["date", "market_id", "selection_id"]
            )

    aug = pd.concat(all_aug_candidates, ignore_index=True) if all_aug_candidates else pd.DataFrame()
    gated = aug[aug.gate_on].copy() if not aug.empty else aug
    blocked = aug[~aug.gate_on].copy() if not aug.empty else aug
    gated7 = pnl(gated, PRIMARY_COMMISSION)
    gated5 = pnl(gated, 0.05)
    blocked7 = pnl(blocked, PRIMARY_COMMISSION)

    if settlement_available_days == 0:
        classification = "HOLDOUT_DATA_UNAVAILABLE"
    elif len(gated) == 0:
        classification = "HOLDOUT_STARTED_NO_GATED_SIGNALS"
    elif len(gated) < 5:
        classification = "INSUFFICIENT_HOLDOUT_SAMPLE"
    elif gated7["pot"] is not None and gated7["pot"] > 0:
        classification = "EARLY_HOLDOUT_POSITIVE"
    else:
        classification = "EARLY_HOLDOUT_NEGATIVE"

    status = {
        "round": 29,
        "capability": "HorseRacing.UntouchedForwardHoldout",
        "status": "COMPLETE",
        "holdout_window": [str(HOLDOUT_START.date()), str(HOLDOUT_END.date())],
        "freeze_timestamp_semantics": "Rules frozen before any August outcome/result inspection in Round029.",
        "source_vintage": "ROUND026_SHA256_FROZEN_VINTAGE for pre-Aug history",
        "historical_source_hashes_match": bool(all(r["match_round026_vintage"] for r in historical_fingerprints)),
        "frozen_signal": "SA × model rank 2 × continuous value_calc < -7% × LAY",
        "frozen_gate": "past 50 candidate outcomes, date-safe; MODEL_TRUSTED iff RP Brier < BSP Brier",
        "primary_commission": PRIMARY_COMMISSION,
        "source_probe": source_probe,
        "settlement_available_days": settlement_available_days,
        "daily_qa": daily_qa,
        "gate_days": gate_days,
        "candidate_n": int(len(aug)) if not aug.empty else 0,
        "gated_n": int(len(gated)) if not gated.empty else 0,
        "blocked_n": int(len(blocked)) if not blocked.empty else 0,
        "gated_metrics_5pct": gated5,
        "gated_metrics_7pct": gated7,
        "blocked_metrics_7pct": blocked7,
        "classification": classification,
        "governance": {
            "betting_ready": False,
            "promotion_forbidden_this_round": True,
            "reason": "Initial untouched batch is deliberately small; no tuning or strategy promotion from Round029 alone.",
        },
        "history_integrity": integrity,
    }
    (OUT / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    pd.DataFrame(daily_qa).to_json(OUT / "daily_source_qa.json", orient="records", indent=2)
    pd.DataFrame(gate_days).to_csv(OUT / "gate_days.csv", index=False)
    if not aug.empty:
        aug[[
            "date", "track", "market_id", "selection_id", "model_odds", "bsp", "win",
            "model_rank", "value_calc", "gate_on", "past_brier_adv"
        ]].to_csv(OUT / "holdout_candidates.csv", index=False)
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
