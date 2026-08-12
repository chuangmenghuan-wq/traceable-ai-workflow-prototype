from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

R43 = Path("research_outputs/horse_round043")
R45 = Path("research_outputs/horse_round045")
STATUS43 = R43 / "status.json"
SNAPS = R43 / "snapshots"
R45.mkdir(parents=True, exist_ok=True)

VALUE_THRESHOLD = -0.07
MODEL_RANK = 2
COMMISSION = 0.07

# Venue → Australian state. Unknown venues are preserved as UNKNOWN instead of guessed.
TRACK_STATE = {
    # South Australia
    "BALAKLAVA": "SA", "BORDERTOWN": "SA", "CLARE": "SA", "GAWLER": "SA",
    "HALIDON": "SA", "KANGAROO ISLAND": "SA", "MORPHETTVILLE": "SA",
    "MORPHETTVILLE PARKS": "SA", "MOUNT GAMBIER": "SA", "MURRAY BRIDGE": "SA",
    "NARACOORTE": "SA", "OAKBANK": "SA", "PENOLA": "SA", "PORT AUGUSTA": "SA",
    "PORT LINCOLN": "SA", "STRATHALBYN": "SA",
    # Victoria
    "BALLARAT": "VIC", "BENDIGO": "VIC", "CAULFIELD": "VIC", "CRANBOURNE": "VIC",
    "FLEMINGTON": "VIC", "GEELONG": "VIC", "HAMILTON": "VIC", "KYNETON": "VIC",
    "MOE": "VIC", "MOONEE VALLEY": "VIC", "MORNINGTON": "VIC", "PAKENHAM": "VIC",
    "SALE": "VIC", "SANDOWN": "VIC", "SEYMOUR": "VIC", "SWAN HILL": "VIC",
    "WANGARATTA": "VIC", "WARRNAMBOOL": "VIC", "WERRIBEE": "VIC",
    # New South Wales / ACT
    "CANTERBURY": "NSW", "KENSINGTON": "NSW", "RANDWICK": "NSW", "ROSEHILL": "NSW",
    "WARWICK FARM": "NSW", "NEWCASTLE": "NSW", "KEMBLA GRANGE": "NSW",
    "HAWKESBURY": "NSW", "GOSFORD": "NSW", "WYONG": "NSW", "SCONE": "NSW",
    "TAMWORTH": "NSW", "DUBBO": "NSW", "WAGGA": "NSW", "GOULBURN": "NSW",
    "CANBERRA": "ACT",
    # Queensland
    "DOOMBEN": "QLD", "EAGLE FARM": "QLD", "GOLD COAST": "QLD", "IPSWICH": "QLD",
    "SUNSHINE COAST": "QLD", "TOOWOOMBA": "QLD", "ROCKHAMPTON": "QLD",
    "TOWNSVILLE": "QLD", "CAIRNS": "QLD", "MACKAY": "QLD",
    # Tasmania
    "DEVONPORT": "TAS", "HOBART": "TAS", "LAUNCESTON": "TAS",
    # Western Australia
    "ASCOT": "WA", "BELMONT": "WA", "BUNBURY": "WA", "PINJARRA": "WA",
    "NORTHAM": "WA", "GERALDTON": "WA", "ALBANY": "WA",
    # Northern Territory
    "DARWIN": "NT", "ALICE SPRINGS": "NT",
}


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    if not STATUS43.exists():
        print("ROUND043_STATUS_MISSING=true")
        return 0

    s43 = json.loads(STATUS43.read_text(encoding="utf-8"))
    if s43.get("status") != "VALIDATED":
        print("ROUND043_VALIDATED=false")
        return 0

    active_date = str(s43.get("active_date") or s43.get("target_date") or "")
    if not active_date:
        print("ROUND043_ACTIVE_DATE_MISSING=true")
        return 0

    records = []
    for p in sorted(SNAPS.glob("*.json")):
        try:
            r = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if str(r.get("target_date") or "") != active_date:
            continue
        r["_snapshot_path"] = str(p)
        records.append(r)

    # One evaluation row per market, using the closest preserved pre-off snapshot.
    by_market: dict[str, dict] = {}
    for r in records:
        market = r.get("market") or {}
        market_id = str(market.get("id") or "")
        if not market_id:
            continue
        try:
            mins = float(r.get("minutes_to_start"))
        except Exception:
            continue
        if mins < 0:
            continue
        cur = by_market.get(market_id)
        if cur is None or mins < float(cur.get("minutes_to_start")):
            by_market[market_id] = r

    rows = []
    for market_id, r in sorted(by_market.items()):
        event_name = str((r.get("event") or {}).get("name") or "").upper().strip()
        state = TRACK_STATE.get(event_name, "UNKNOWN")
        market = r.get("market") or {}

        ranked = []
        for runner in market.get("runners") or []:
            try:
                rp = float(runner.get("ratedPrice"))
            except Exception:
                continue
            if rp <= 1:
                continue
            runner_status = str(runner.get("status") or "").upper()
            if runner_status in {"REMOVED", "SCRATCHED"}:
                continue
            ranked.append((rp, runner))
        ranked.sort(key=lambda z: (z[0], str(z[1].get("id"))))
        if len(ranked) < MODEL_RANK:
            continue

        rated_price, runner = ranked[MODEL_RANK - 1]
        try:
            lay_price = float(runner.get("layPrice"))
        except Exception:
            lay_price = None

        value_calc = None
        raw_candidate = False
        if lay_price is not None and lay_price > 1:
            value_calc = 1.0 / rated_price - 1.0 / lay_price
            raw_candidate = value_calc < VALUE_THRESHOLD

        lane = "SA_BENCHMARK" if state == "SA" else "PARALLEL_EXPLORATORY"
        historical_gate_authority = (
            "round035-last-verified-through-2026-08-08"
            if state == "SA" else "NONE_STATE_SPECIFIC_YET"
        )

        rows.append({
            "active_date": active_date,
            "state": state,
            "lane": lane,
            "event_name": event_name,
            "market_id": market_id,
            "market_name": market.get("name"),
            "scheduled_start": market.get("startTime"),
            "snapshot_path": r.get("_snapshot_path"),
            "minutes_to_start": r.get("minutes_to_start"),
            "target_label": r.get("target_label"),
            "selection_id": runner.get("id"),
            "runner_name": runner.get("name"),
            "model_rank": MODEL_RANK,
            "rated_price": rated_price,
            "lay_price": lay_price,
            "value_calc": value_calc,
            "threshold": VALUE_THRESHOLD,
            "raw_paper_lay_candidate": raw_candidate,
            "historical_gate_authority": historical_gate_authority,
            "state_validated_strategy": state == "SA",
            "paper_only": True,
            "real_betting_allowed": False,
        })

    signals_path = R45 / "state_parallel_signals.jsonl"
    signals_path.write_text(
        "".join(json.dumps(x, separators=(",", ":")) + "\n" for x in rows),
        encoding="utf-8",
    )

    evaluated = Counter(r["state"] for r in rows)
    candidates = Counter(r["state"] for r in rows if r["raw_paper_lay_candidate"])
    unknown_venues = sorted({r["event_name"] for r in rows if r["state"] == "UNKNOWN"})

    per_state = {}
    for state in sorted(set(evaluated) | set(candidates)):
        state_rows = [r for r in rows if r["state"] == state]
        state_candidates = [r for r in state_rows if r["raw_paper_lay_candidate"]]
        per_state[state] = {
            "evaluated_markets": len(state_rows),
            "raw_paper_lay_candidates": len(state_candidates),
            "candidate_selection_ids": [r["selection_id"] for r in state_candidates],
            "lane": "SA_BENCHMARK" if state == "SA" else "PARALLEL_EXPLORATORY",
        }

    status = {
        "round": 45,
        "capability": "HorseRacing.StateParallelPaperValidator",
        "status": "PARALLEL_PAPER_EVALUATED",
        "active_date": active_date,
        "rule": "all mapped states × model_rank_2 × (1/ratedPrice - 1/layPrice) < -0.07",
        "model_rank": MODEL_RANK,
        "value_threshold": VALUE_THRESHOLD,
        "commission_reference": COMMISSION,
        "governance": {
            "paper_only": True,
            "real_betting_allowed": False,
            "strategy_tuning": False,
            "sa_remains_frozen_benchmark": True,
            "non_sa_results_are_exploratory_only": True,
            "cross_state_pooling_for_promotion_forbidden": True,
        },
        "snapshot_records_considered": len(records),
        "evaluated_markets_total": len(rows),
        "raw_paper_lay_candidates_total": sum(candidates.values()),
        "per_state": per_state,
        "unknown_venues": unknown_venues,
        "next_gate": "settle each state independently; compare forward hit-rate/POT and only then consider state-specific promotion",
    }
    write_json(R45 / "status.json", status)
    print("ROUND045_STATUS=PARALLEL_PAPER_EVALUATED")
    print("PER_STATE=" + json.dumps(per_state, sort_keys=True))
    print("UNKNOWN_VENUES=" + json.dumps(unknown_venues))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
