from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

from horse_round025_runtime import PERIODS, PERIOD_ORDER, SA_TRACKS, download, load_file

OUT = Path("research_outputs/horse_round026")
OUT.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    files = []
    for period in PERIOD_ORDER:
        for url in PERIODS[period]:
            p = download(url)
            d = load_file(url, period)
            usable_before_dedup = int(len(d))
            dup_rows = int(d.duplicated(["market_id", "selection_id"], keep=False).sum())
            d = d.sort_values(["market_id", "selection_id", "date"]).drop_duplicates(
                ["market_id", "selection_id"], keep="last"
            ).copy()
            d["model_rank"] = d.groupby("market_id").model_odds.rank(method="first", ascending=True)
            candidate = d[
                d.track.isin(SA_TRACKS)
                & d.model_rank.eq(2)
                & d.value_calc.lt(-0.07)
            ]
            files.append({
                "period": period,
                "file": p.name,
                "url": url,
                "bytes": int(p.stat().st_size),
                "sha256": sha256_file(p),
                "usable_rows_before_dedup": usable_before_dedup,
                "dedup_rows": int(len(d)),
                "duplicate_rows": dup_rows,
                "unique_markets": int(d.market_id.nunique()),
                "candidate_rows": int(len(candidate)),
                "date_min": str(d.date.min().date()),
                "date_max": str(d.date.max().date()),
            })

    payload = {
        "purpose": "Freeze exact official CSV assets used by Round 026; detect publisher-side historical data revisions across rounds.",
        "files": files,
        "period_totals": pd.DataFrame(files).groupby("period").agg(
            usable_rows_before_dedup=("usable_rows_before_dedup", "sum"),
            dedup_rows=("dedup_rows", "sum"),
            candidate_rows=("candidate_rows", "sum"),
        ).reset_index().to_dict("records"),
        "qa_note": "No prior raw-file hashes were stored in Round 020, so exact byte-level revision timing cannot be proven retrospectively. Current hashes freeze the Round 026 source version going forward.",
    }
    (OUT / "source_fingerprint.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
