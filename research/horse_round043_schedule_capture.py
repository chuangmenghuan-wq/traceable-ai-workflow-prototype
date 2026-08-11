from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

CAPABILITY = "HorseRacing.ScheduleAwarePreoffCapture"
LOCAL_TZ = ZoneInfo("Australia/Adelaide")
BASE = "https://bff.senservices.betfair.com.au/api/v1"
UA = "FutureAbility-HorseResearch/round043 schedule-aware read-only validation"
TARGETS = [("T-30", 30.0), ("T-15", 15.0), ("T-10", 10.0), ("T-5", 5.0), ("T-1", 1.0)]
SAMPLE_LOOPS_NEAR_RACE = 6
SAMPLE_SLEEP_SECONDS = 55

ROOT = Path("research_outputs/horse_round043")
SNAPS = ROOT / "snapshots"
PLANS = ROOT / "schedule_plans"
LEDGER = ROOT / "capture_ledger.jsonl"
STATUS = ROOT / "status.json"
for p in (ROOT, SNAPS, PLANS):
    p.mkdir(parents=True, exist_ok=True)


def get_json(url: str):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        raw = e.read(200000)
        try:
            body = json.loads(raw)
        except Exception:
            body = {"raw": raw[:500].decode("utf-8", "replace")}
        return e.code, body


def parse_start(raw_start: str) -> datetime:
    return datetime.fromisoformat(raw_start.replace("Z", "+00:00"))


def current_target_date(now_utc: datetime) -> str:
    override = os.getenv("HORSE_TARGET_DATE", "").strip()
    return override or now_utc.astimezone(LOCAL_TZ).date().isoformat()


def load_captured_keys() -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    if not LEDGER.exists():
        return keys
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
            market_id = str(row.get("market_id") or "")
            label = str(row.get("target_label") or "")
            if market_id and label:
                keys.add((market_id, label))
        except Exception:
            pass
    return keys


def schedule_rows(model: dict) -> list[dict]:
    rows: list[dict] = []
    for event in model.get("events") or []:
        for market in event.get("markets") or []:
            raw_start = market.get("startTime")
            if not raw_start:
                continue
            start = parse_start(raw_start)
            rows.append(
                {
                    "event_id": event.get("id"),
                    "event_name": event.get("name"),
                    "market_id": str(market.get("id")),
                    "market_name": market.get("name"),
                    "scheduled_start_utc": start.isoformat(),
                    "scheduled_start_adelaide": start.astimezone(LOCAL_TZ).isoformat(),
                    "capture_targets": {
                        label: (start - timedelta(minutes=offset)).isoformat()
                        for label, offset in TARGETS
                    },
                }
            )
    return rows


def persist_schedule_plan(model: dict, target_date: str, now_utc: datetime) -> Path:
    path = PLANS / f"{target_date}.json"
    rows = schedule_rows(model)
    payload = {
        "round": 43,
        "capability": CAPABILITY,
        "mode": "SCHEDULE_AWARE",
        "target_date": target_date,
        "generated_at_utc": now_utc.isoformat(),
        "targets": [label for label, _ in TARGETS],
        "market_count": len(rows),
        "markets": rows,
        "governance": {
            "paper_only": True,
            "real_betting_allowed": False,
            "strategy_tuning": False,
            "credentials_supplied": False,
        },
    }
    changed = True
    if path.exists():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
            changed = old.get("markets") != rows or old.get("targets") != payload["targets"]
        except Exception:
            changed = True
    if changed:
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"SCHEDULE_PLAN_UPDATED=true DATE={target_date} MARKET_COUNT={len(rows)}")
    else:
        print(f"SCHEDULE_PLAN_UNCHANGED=true DATE={target_date} MARKET_COUNT={len(rows)}")
    return path


def has_near_race(model: dict, now_utc: datetime) -> bool:
    for event in model.get("events") or []:
        for market in event.get("markets") or []:
            raw_start = market.get("startTime")
            if not raw_start:
                continue
            mins = (parse_start(raw_start) - now_utc).total_seconds() / 60.0
            status = str(market.get("status") or "").upper()
            if status != "CLOSED" and -1.0 <= mins <= 33.0:
                return True
    return False


def due_targets(model: dict, sample_utc: datetime, captured_keys: set[tuple[str, str]]):
    due = []
    for event in model.get("events") or []:
        for market in event.get("markets") or []:
            raw_start = market.get("startTime")
            if not raw_start:
                continue
            start = parse_start(raw_start)
            mins = (start - sample_utc).total_seconds() / 60.0
            status = str(market.get("status") or "").upper()
            if status == "CLOSED":
                continue
            market_id = str(market.get("id") or "")
            if not market_id:
                continue
            for label, target in TARGETS:
                if (market_id, label) in captured_keys:
                    continue
                if label == "T-1":
                    matched = 0.0 <= mins <= 1.35
                else:
                    matched = (target - 2.25) <= mins <= (target + 0.25)
                if matched:
                    due.append((event, market, mins, label, target))
    return due


def capture_one(
    event: dict,
    market: dict,
    mins: float,
    label: str,
    target: float,
    sample_utc: datetime,
    target_date: str,
):
    market_id = str(market.get("id"))
    mover_http, movers = get_json(f"{BASE}/models/racing-market-movers/{market_id}")
    rating_http, rating = get_json(
        f"{BASE}/models/racing-rating-model/{market_id}?modelName=BFA_THOROUGHBRED"
    )
    header_http, header = get_json(f"{BASE}/bema/race-market-screen/market-header/{market_id}")
    runners_http, runners = get_json(f"{BASE}/bema/race-market-screen/runners-list/{market_id}")

    model_runners = market.get("runners") or []
    live_count = sum(
        1
        for r in model_runners
        if r.get("backPrice") is not None
        or r.get("layPrice") is not None
        or r.get("value") is not None
    )
    mover_sels = (movers.get("selections") or []) if isinstance(movers, dict) else []
    t15_count = sum(1 for s in mover_sels if s.get("fifteenMinPrice") is not None)
    morning_count = sum(1 for s in mover_sels if s.get("morningPrice") is not None)
    sample_local = sample_utc.astimezone(LOCAL_TZ)

    record = {
        "round": 43,
        "capability": CAPABILITY,
        "capture_mode": "SCHEDULE_AWARE",
        "target_label": label,
        "target_minutes_before_start": target,
        "captured_at_utc": sample_utc.isoformat(),
        "captured_at_adelaide": sample_local.isoformat(),
        "target_date": target_date,
        "minutes_to_start": mins,
        "timing_error_minutes": mins - target,
        "event": {"id": event.get("id"), "name": event.get("name")},
        "market": market,
        "model_live_price_runner_count": live_count,
        "endpoints": {
            "market_movers_http": mover_http,
            "rating_http": rating_http,
            "header_http": header_http,
            "runners_http": runners_http,
        },
        "market_movers": movers,
        "rating_model": rating,
        "market_header": header,
        "runners_list": runners,
        "movers_fifteen_min_non_null_count": t15_count,
        "movers_morning_non_null_count": morning_count,
        "governance": {
            "read_only": True,
            "credentials_supplied": False,
            "orders_allowed": False,
            "strategy_tuning": False,
            "paper_only": True,
        },
    }
    stamp = sample_utc.strftime("%Y%m%dT%H%M%SZ")
    safe_market = market_id.replace(".", "_")
    path = SNAPS / f"{stamp}_{safe_market}_{label.replace('-', 'm')}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")

    row = {
        "captured_at_utc": sample_utc.isoformat(),
        "target_date": target_date,
        "market_id": market_id,
        "event_name": event.get("name"),
        "target_label": label,
        "target_minutes_before_start": target,
        "minutes_to_start": mins,
        "timing_error_minutes": mins - target,
        "model_live_price_runner_count": live_count,
        "movers_fifteen_min_non_null_count": t15_count,
        "movers_morning_non_null_count": morning_count,
        "snapshot": str(path),
    }
    print(
        f"CAPTURED TARGET={label} MARKET={market_id} EVENT={event.get('name')} "
        f"MINS={mins:.2f} LIVE_MODEL={live_count} T15={t15_count} MORNING={morning_count}"
    )
    return row


def load_snapshots() -> list[dict]:
    rows = []
    for p in sorted(SNAPS.glob("*.json")):
        try:
            rows.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass
    return rows


def write_status(target_date: str, plan_path: Path):
    all_records = load_snapshots()
    daily_records = [r for r in all_records if str(r.get("target_date") or "") == target_date]
    cumulative_live = any((r.get("model_live_price_runner_count") or 0) > 0 for r in all_records)
    cumulative_t15 = any((r.get("movers_fifteen_min_non_null_count") or 0) > 0 for r in all_records)
    cumulative_validated = cumulative_live and cumulative_t15
    daily_counts = Counter(str(r.get("target_label") or "LEGACY") for r in daily_records)
    all_counts = Counter(str(r.get("target_label") or "LEGACY") for r in all_records)
    daily_market_ids = {
        str((r.get("market") or {}).get("id") or "")
        for r in daily_records
        if (r.get("market") or {}).get("id") is not None
    }
    all_market_ids = {
        str((r.get("market") or {}).get("id") or "")
        for r in all_records
        if (r.get("market") or {}).get("id") is not None
    }
    payload = {
        "round": 43,
        "capability": CAPABILITY,
        "status": "VALIDATED" if cumulative_validated else "CAPTURE_IN_PROGRESS",
        "capture_mode": "SCHEDULE_AWARE_DAILY_ROLLOVER",
        "active_date": target_date,
        "last_run_utc": datetime.now(timezone.utc).isoformat(),
        "schedule_plan": str(plan_path),
        "target_offsets_minutes": [30, 15, 10, 5, 1],
        "today": {
            "snapshot_count": len(daily_records),
            "captured_market_count": len(daily_market_ids),
            "target_capture_counts": dict(sorted(daily_counts.items())),
        },
        "cumulative": {
            "snapshot_count": len(all_records),
            "captured_market_count": len(all_market_ids),
            "target_capture_counts": dict(sorted(all_counts.items())),
            "live_model_price_seen": cumulative_live,
            "fifteen_min_price_seen": cumulative_t15,
        },
        "paper_only": True,
        "real_betting_allowed": False,
        "strategy_tuning": False,
        "next_gate": (
            "compare frozen SA rank2 value<-7% LAY signal using preserved scheduled-off snapshots"
            if cumulative_validated
            else "continue daily T-30/T-15/T-10/T-5/T-1 capture until cumulative validation is satisfied"
        ),
    }
    STATUS.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("ROUND043_STATUS=" + payload["status"])
    print("TODAY_TARGET_CAPTURE_COUNTS=" + json.dumps(payload["today"]["target_capture_counts"], sort_keys=True))


def main() -> None:
    now_utc = datetime.now(timezone.utc)
    target_date = current_target_date(now_utc)
    print(f"ROUND043_START_UTC={now_utc.isoformat()}")
    print(f"ROUND043_START_ADELAIDE={now_utc.astimezone(LOCAL_TZ).isoformat()}")
    print(f"TARGET_DATE={target_date}")

    model_url = f"{BASE}/hub/thoroughbred-model?date={target_date}"
    first_http, first_model = get_json(model_url)
    print(f"MODEL_HTTP_INITIAL={first_http}")
    if first_http != 200:
        detail = first_model.get("detail") if isinstance(first_model, dict) else None
        print(f"MODEL_DETAIL={detail}")
        return

    plan_path = persist_schedule_plan(first_model, target_date, now_utc)
    captured_keys = load_captured_keys()
    sample_loops = SAMPLE_LOOPS_NEAR_RACE if has_near_race(first_model, now_utc) else 1
    print(f"SAMPLE_LOOPS={sample_loops}")
    new_rows: list[dict] = []

    for sample_idx in range(sample_loops):
        sample_utc = datetime.now(timezone.utc)
        if sample_utc.astimezone(LOCAL_TZ).date().isoformat() != target_date:
            break
        model_http, model = get_json(model_url)
        print(f"SAMPLE={sample_idx + 1}/{sample_loops} UTC={sample_utc.isoformat()} MODEL_HTTP={model_http}")
        if model_http != 200:
            break
        due = due_targets(model, sample_utc, captured_keys)
        print(f"DUE_TARGET_COUNT={len(due)}")
        for event, market, mins, label, target in due:
            market_id = str(market.get("id"))
            key = (market_id, label)
            if key in captured_keys:
                continue
            new_rows.append(capture_one(event, market, mins, label, target, sample_utc, target_date))
            captured_keys.add(key)
        if sample_idx < sample_loops - 1:
            time.sleep(SAMPLE_SLEEP_SECONDS)

    if new_rows:
        with LEDGER.open("a", encoding="utf-8") as fh:
            for row in new_rows:
                fh.write(json.dumps(row, separators=(",", ":")) + "\n")

    write_status(target_date, plan_path)


if __name__ == "__main__":
    main()
