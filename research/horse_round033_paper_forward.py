from __future__ import annotations

import hashlib
import io
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import requests

from horse_round025_runtime import SA_TRACKS, candidate_history

OUT = Path("research_outputs/horse_round033")
OUT.mkdir(parents=True, exist_ok=True)
CONTRACT_PATH = Path("research/horse_round033_contract.json")
KASH_DAILY = (
    "https://betfair-data-supplier-prod.herokuapp.com/api/widgets/"
    "kash-ratings-model/datasets?date={date}&presenter=RatingsPresenter&csv=true"
)
MONTHLY_AUG = "https://betfair-datascientists.github.io/data/assets/Kash_Model_Results_2026_08.csv"
PAST_WINDOW = 50


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def get(url: str) -> tuple[int, bytes, str]:
    r = requests.get(url, timeout=(20, 120))
    return r.status_code, r.content, r.headers.get("content-type", "")


def cmap(cols) -> dict[str, str]:
    return {str(c).strip().upper(): str(c) for c in cols}


def pick(cm: dict[str, str], *names: str) -> str | None:
    for n in names:
        if n.upper() in cm:
            return cm[n.upper()]
    return None


def parse_ratings(raw: bytes, date: pd.Timestamp) -> tuple[pd.DataFrame, dict]:
    text = raw.decode("utf-8-sig", errors="replace")
    d = pd.read_csv(io.StringIO(text), low_memory=False)
    cm = cmap(d.columns)
    mapped = {
        "track": pick(cm, "meetings.name", "Track", "Venue"),
        "market_id": pick(cm, "meetings.races.bfExchangeMarketId", "Market", "MarketId", "MARKET_ID"),
        "selection_id": pick(cm, "meetings.races.runners.bfExchangeSelectionId", "Selection", "SelectionId", "SELECTION_ID"),
        "model_odds": pick(cm, "meetings.races.runners.ratedPrice", "RP", "Model Odds", "MODEL_ODDS"),
        "horse": pick(cm, "meetings.races.runners.name", "Horse", "SELECTION_NAME"),
        "scheduled_time": pick(cm, "meetings.races.startTime", "SCHEDULED_RACE_TIME", "startTime"),
    }
    missing = [k for k in ["track", "market_id", "selection_id", "model_odds"] if mapped[k] is None]
    if missing:
        return pd.DataFrame(), {"status": "MISSING_COLUMNS", "missing": missing, "columns": list(map(str, d.columns))}
    x = pd.DataFrame({
        "date": date,
        "track": d[mapped["track"]].astype(str).str.strip(),
        "market_id": d[mapped["market_id"]].astype(str).str.strip(),
        "selection_id": d[mapped["selection_id"]].astype(str).str.strip(),
        "model_odds": pd.to_numeric(d[mapped["model_odds"]], errors="coerce"),
        "horse": d[mapped["horse"]].astype(str).str.strip() if mapped["horse"] else "",
        "scheduled_time": d[mapped["scheduled_time"]].astype(str).str.strip() if mapped["scheduled_time"] else "",
    })
    x = x.replace([np.inf, -np.inf], np.nan).dropna(subset=["model_odds", "market_id", "selection_id"])
    x = x[x.model_odds > 1].copy()
    x = x.sort_values(["market_id", "selection_id"]).drop_duplicates(["market_id", "selection_id"], keep="last")
    x["model_rank"] = x.groupby("market_id").model_odds.rank(method="first", ascending=True)
    sa_r2 = x[x.track.isin(SA_TRACKS) & x.model_rank.eq(2)].copy()
    return x, {
        "status": "PARSED",
        "raw_rows": int(len(d)),
        "usable_rows": int(len(x)),
        "markets": int(x.market_id.nunique()),
        "sa_r2_rows": int(len(sa_r2)),
        "sa_r2_markets": int(sa_r2.market_id.nunique()),
        "mapped": mapped,
    }


def main() -> None:
    contract_bytes = CONTRACT_PATH.read_bytes()
    contract = json.loads(contract_bytes.decode("utf-8"))
    contract_sha256 = sha256_bytes(contract_bytes)

    adelaide_now = datetime.now(ZoneInfo("Australia/Adelaide"))
    paper_date = pd.Timestamp(os.environ.get("PAPER_DATE", adelaide_now.date().isoformat()))

    hist, integrity = candidate_history()
    hist = hist.sort_values(["date", "market_id", "selection_id"]).copy()
    prior = hist[hist.date < paper_date].tail(PAST_WINDOW)
    if len(prior) < PAST_WINDOW:
        raise RuntimeError(f"insufficient historical gate rows: {len(prior)}")
    gate_adv = float(prior.market_sqerr.mean() - prior.model_sqerr.mean())
    gate_on = bool(gate_adv > 0)
    latest_settled_candidate_date = pd.Timestamp(hist.date.max()).normalize()

    # Strict forward governance: if the known settled-candidate ledger does not reach
    # the immediately preceding calendar date, we cannot assert that the Past-50 set
    # is the true current Past-50. This deliberately blocks paper bets rather than
    # silently carrying a stale July gate into August.
    expected_through = paper_date - pd.Timedelta(days=1)
    gate_ledger_current = bool(latest_settled_candidate_date >= expected_through)

    rating_url = KASH_DAILY.format(date=str(paper_date.date()))
    rs, rr, rct = get(rating_url)
    if rs == 200:
        ratings, ratings_qa = parse_ratings(rr, paper_date)
    else:
        ratings, ratings_qa = pd.DataFrame(), {"status": "HTTP_UNAVAILABLE", "http_status": rs}

    ms, mb, mct = get(MONTHLY_AUG)

    app_key_present = bool(os.environ.get("BETFAIR_APP_KEY"))
    session_present = bool(os.environ.get("BETFAIR_SESSION_TOKEN"))
    price_adapter_ready = app_key_present and session_present

    staged = pd.DataFrame()
    if not ratings.empty:
        staged = ratings[ratings.track.isin(SA_TRACKS) & ratings.model_rank.eq(2)].copy()
        if not staged.empty:
            staged["gate_on_snapshot"] = gate_on
            staged["gate_brier_adv_snapshot"] = gate_adv
            staged["paper_eligible"] = False
            staged["block_reason"] = (
                "STALE_SETTLEMENT_LEDGER" if not gate_ledger_current
                else "LIVE_PRICE_ADAPTER_MISSING" if not price_adapter_ready
                else "WAIT_FOR_PREOFF_PRICE_CAPTURE"
            )
            staged.to_csv(OUT / "staged_sa_rank2.csv", index=False)

    if rs != 200 or ratings.empty:
        classification = "RATINGS_UNAVAILABLE"
    elif not gate_ledger_current:
        classification = "PAPER_FORWARD_ARMED_SETTLEMENT_LEDGER_STALE"
    elif not price_adapter_ready:
        classification = "PAPER_FORWARD_ARMED_PRICE_ADAPTER_REQUIRED"
    else:
        classification = "PAPER_FORWARD_ARMED_WAITING_PREOFF_CAPTURE"

    status = {
        "round": 33,
        "capability": "HorseRacing.PaperForwardExecutionContract",
        "status": "COMPLETE",
        "contract_id": contract["contract_id"],
        "contract_sha256": contract_sha256,
        "paper_date_adelaide": str(paper_date.date()),
        "mode": "PAPER_ONLY",
        "real_betting_allowed": False,
        "tuning_allowed": False,
        "historical_gate_snapshot": {
            "past_window": PAST_WINDOW,
            "known_prior_n": int(len(prior)),
            "brier_advantage": gate_adv,
            "gate_on": gate_on,
            "latest_known_settled_candidate_date": str(latest_settled_candidate_date.date()),
            "required_ledger_through": str(expected_through.date()),
            "gate_ledger_current": gate_ledger_current,
        },
        "ratings_source": {
            "url": rating_url,
            "http_status": rs,
            "content_type": rct,
            "bytes": int(len(rr)),
            "sha256": sha256_bytes(rr) if rs == 200 else None,
            "qa": ratings_qa,
            "staged_sa_rank2_n": int(len(staged)),
        },
        "settlement_monthly_probe": {
            "url": MONTHLY_AUG,
            "http_status": ms,
            "content_type": mct,
            "bytes": int(len(mb)),
            "sha256": sha256_bytes(mb) if ms == 200 else None,
        },
        "live_price_adapter": {
            "betfair_app_key_present": app_key_present,
            "betfair_session_token_present": session_present,
            "ready": price_adapter_ready,
            "orders_enabled": False,
        },
        "paper_bets_created": 0,
        "classification": classification,
        "governance": {
            "final_bsp_entry_forbidden": True,
            "stale_gate_forbidden": True,
            "post_hoc_threshold_tuning_forbidden": True,
            "minimum_new_gated_bets_before_review": 30,
            "historical_results_do_not_count_toward_forward_counter": True,
        },
        "history_integrity": integrity,
    }
    (OUT / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (OUT / "contract_snapshot.json").write_text(json.dumps(contract, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
