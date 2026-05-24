"""Write scraped offers to timestamped CSV and JSON files."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

from .models import OFFER_FIELDS, Offer

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def write_outputs(offers: list[Offer], run_tag: str | None = None) -> dict[str, Path]:
    """Write offers to both CSV and JSON. Returns the paths written."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = run_tag or datetime.now().strftime("%Y%m%d-%H%M%S")
    base = OUTPUT_DIR / f"prices-india-{stamp}"

    rows = [o.to_dict() for o in offers]

    csv_path = base.with_suffix(".csv")
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=OFFER_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k) for k in OFFER_FIELDS})

    json_path = base.with_suffix(".json")
    json_path.write_text(
        json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return {"csv": csv_path, "json": json_path}
