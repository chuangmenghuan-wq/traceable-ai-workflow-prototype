from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import requests

OUT = Path("research_outputs/horse_round034")
OUT.mkdir(parents=True, exist_ok=True)
CONTRACT_PATH = Path("research/horse_round033_contract.json")
EXPECTED_CONTRACT_SHA = "e446a15ebc40bd4ad7ccc820e60ec829d623311f22d71b425c98c01fc13724e3"

KASH_DAILY = (
    "https://betfair-data-supplier-prod.herokuapp.com/api/widgets/"
    "kash-ratings-model/datasets?date={date}&presenter=RatingsPresenter&csv=true"
)
KASH_MONTHLY = "https://betfair-datascientists.github.io/data/assets/Kash_Model_Results_2026_08.csv"
ANZ_MONTHLY = "https://betfair-datascientists.github.io/data/assets/ANZ_Thoroughbreds_2026_08.csv"
BSP_DAILY = "https://promo.betfair.com/betfairsp/prices/dwbfpricesauswin{ddmmyyyy}.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/150 Safari/537.36",
    "Accept": "text/csv,text/plain,*/*",
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def probe(url: str, headers=None, attempts: int = 3) -> dict:
    last = None
    for attempt in range(1, attempts + 1):
        try:
            r = requests.get(url, headers=headers, timeout=(15, 90))
            last = {
                "url": url,
                "http_status": int(r.status_code),
                "content_type": r.headers.get("content-type", ""),
                "bytes": int(len(r.content)),
                "sha256": sha256_bytes(r.content) if r.status_code == 200 else None,
                "attempt": attempt,
            }
            if r.status_code == 200:
                return last
        except Exception as e:
            last = {"url": url, "http_status": None, "error": repr(e), "attempt": attempt}
        if attempt < attempts:
            time.sleep(1.0 * attempt)
    return last or {"url": url, "http_status": None, "error": "NO_ATTEMPT"}


def main() -> None:
    now_adelaide = datetime.now(ZoneInfo("Australia/Adelaide"))
    paper_date = pd.Timestamp(os.environ.get("PAPER_DATE", now_adelaide.date().isoformat()))
    start = pd.Timestamp("2026-08-01")
    prior_day = paper_date - pd.Timedelta(days=1)

    contract_bytes = CONTRACT_PATH.read_bytes()
    contract_sha = sha256_bytes(contract_bytes)
    contract_ok = contract_sha == EXPECTED_CONTRACT_SHA

    daily_rows = []
    for d in pd.date_range(start, paper_date, freq="D"):
        q = probe(KASH_DAILY.format(date=str(d.date())), attempts=3)
        daily_rows.append({
            "date": str(d.date()),
            "kind": "KASH_DAILY_RATINGS",
            **q,
        })
    ratings_df = pd.DataFrame(daily_rows)
    today_row = ratings_df[ratings_df.date.eq(str(paper_date.date()))].iloc[0].to_dict()
    prior_rows = ratings_df[ratings_df.date.le(str(prior_day.date()))]
    ratings_prior_coverage = float((prior_rows.http_status == 200).mean()) if len(prior_rows) else 0.0

    kash_month = probe(KASH_MONTHLY, attempts=2)
    anz_month = probe(ANZ_MONTHLY, attempts=2)

    bsp_rows = []
    if prior_day >= start:
        for d in pd.date_range(start, prior_day, freq="D"):
            q = probe(BSP_DAILY.format(ddmmyyyy=d.strftime("%d%m%Y")), headers=HEADERS, attempts=2)
            bsp_rows.append({
                "date": str(d.date()),
                "kind": "BETFAIR_DAILY_BSP",
                **q,
            })
    bsp_df = pd.DataFrame(bsp_rows)
    bsp_coverage = float((bsp_df.http_status == 200).mean()) if len(bsp_df) else 0.0

    # A settlement ledger can be refreshed by either a complete official August result file,
    # or a complete daily ratings + daily BSP/result path through yesterday.
    monthly_settlement_ready = bool(kash_month.get("http_status") == 200)
    daily_settlement_ready = bool(
        len(prior_rows) > 0
        and ratings_prior_coverage == 1.0
        and len(bsp_df) == len(prior_rows)
        and bsp_coverage == 1.0
    )
    settlement_ready = monthly_settlement_ready or daily_settlement_ready

    ratings_today_ready = bool(today_row.get("http_status") == 200)
    app_key = bool(os.environ.get("BETFAIR_APP_KEY"))
    session = bool(os.environ.get("BETFAIR_SESSION_TOKEN"))
    live_price_ready = app_key and session

    blockers = []
    if not contract_ok:
        blockers.append("CONTRACT_HASH_MISMATCH")
    if not ratings_today_ready:
        blockers.append("TODAY_RATINGS_UNAVAILABLE")
    if not settlement_ready:
        blockers.append("SETTLEMENT_LEDGER_REFRESH_UNAVAILABLE")
    if not live_price_ready:
        blockers.append("LIVE_PREOFF_PRICE_ADAPTER_NOT_READY")

    if not contract_ok:
        classification = "CONTRACT_INTEGRITY_FAIL"
    elif not blockers:
        classification = "PAPER_FORWARD_DATA_PLANE_READY"
    elif len(blockers) == 1:
        classification = "PAPER_FORWARD_DATA_PLANE_ONE_BLOCKER"
    else:
        classification = "PAPER_FORWARD_DATA_PLANE_BLOCKED"

    status = {
        "round": 34,
        "capability": "HorseRacing.PaperForwardDataPlaneReadiness",
        "status": "COMPLETE",
        "paper_date_adelaide": str(paper_date.date()),
        "contract": {
            "expected_sha256": EXPECTED_CONTRACT_SHA,
            "actual_sha256": contract_sha,
            "match": contract_ok,
            "tuning_allowed": False,
        },
        "ratings_plane": {
            "today_ready": ratings_today_ready,
            "today_probe": today_row,
            "august_through_yesterday_coverage": ratings_prior_coverage,
            "days_probed": int(len(ratings_df)),
            "days_200": int((ratings_df.http_status == 200).sum()),
        },
        "settlement_plane": {
            "ready": settlement_ready,
            "monthly_kash_probe": kash_month,
            "monthly_anz_probe": anz_month,
            "daily_bsp_days_probed": int(len(bsp_df)),
            "daily_bsp_days_200": int((bsp_df.http_status == 200).sum()) if len(bsp_df) else 0,
            "daily_bsp_coverage": bsp_coverage,
            "monthly_path_ready": monthly_settlement_ready,
            "daily_path_ready": daily_settlement_ready,
        },
        "live_price_plane": {
            "ready": live_price_ready,
            "betfair_app_key_present": app_key,
            "betfair_session_token_present": session,
            "orders_enabled": False,
            "paper_only": True,
        },
        "blockers": blockers,
        "classification": classification,
        "paper_bets_created": 0,
        "governance": {
            "fail_closed": True,
            "final_bsp_entry_forbidden": True,
            "stale_gate_forbidden": True,
            "post_hoc_tuning_forbidden": True,
            "minimum_new_gated_bets_before_review": 30,
        },
    }

    ratings_df.to_csv(OUT / "ratings_probe.csv", index=False)
    bsp_df.to_csv(OUT / "bsp_probe.csv", index=False)
    (OUT / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
