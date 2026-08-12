from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = "https://bff.senservices.betfair.com.au/api/v1"
TZ = ZoneInfo("Australia/Adelaide")
OUT = Path("research_outputs/horse_round048")
OUT.mkdir(parents=True, exist_ok=True)


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "FutureAbility-HorseResearch/round048-readonly", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        raw = e.read(100000)
        try:
            body = json.loads(raw)
        except Exception:
            body = {"raw": raw[:500].decode("utf-8", "replace")}
        return e.code, body


def main():
    now = datetime.now(timezone.utc)
    local = now.astimezone(TZ)
    target = (local.date() + timedelta(days=1)).isoformat()
    url = f"{BASE}/hub/thoroughbred-model?date={target}"
    http, body = get_json(url)
    events = body.get("events") or [] if isinstance(body, dict) else []
    markets = []
    for event in events:
        for m in event.get("markets") or []:
            markets.append({"event_name": event.get("name"), "market_id": m.get("id"), "market_name": m.get("name"), "startTime": m.get("startTime"), "status": m.get("status")})
    result = {
        "round": 48,
        "capability": "HorseRacing.NextDayModelPublicationPreflight",
        "checked_at_utc": now.isoformat(),
        "checked_at_adelaide": local.isoformat(),
        "target_date": target,
        "http_status": http,
        "model_published": http == 200,
        "event_count": len(events),
        "market_count": len(markets),
        "markets": markets,
        "detail": body.get("detail") if isinstance(body, dict) else None,
        "paper_only": True,
        "real_betting_allowed": False,
        "strategy_tuning": False,
    }
    (OUT / "status.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["target_date", "http_status", "model_published", "event_count", "market_count", "detail"]}, indent=2))


if __name__ == "__main__":
    main()
