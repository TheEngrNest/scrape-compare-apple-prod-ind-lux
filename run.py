#!/usr/bin/env python3
"""Run India price scrapers and write CSV + JSON output.

Examples:
    python run.py --sites apple
    python run.py --sites apple,amazon --no-headless --debug
    python run.py --sites all
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scrapers import SCRAPERS, Offer
from scrapers.storage import write_outputs

ROOT = Path(__file__).resolve().parent
SEED_FILE = ROOT / "macbook_models.json"


def load_models() -> list[dict]:
    data = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    return data["models"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scrape MacBook prices in India.")
    p.add_argument(
        "--sites",
        default="apple",
        help="Comma-separated site keys or 'all'. "
        f"Available: {', '.join(SCRAPERS)}",
    )
    p.add_argument("--no-headless", action="store_true", help="Show the browser.")
    p.add_argument("--debug", action="store_true", help="Dump page HTML for tuning.")
    p.add_argument("--timeout", type=int, default=30000, help="Per-action ms timeout.")
    return p.parse_args()


def selected_sites(arg: str) -> list[str]:
    if arg.strip().lower() == "all":
        return list(SCRAPERS)
    keys = [s.strip().lower() for s in arg.split(",") if s.strip()]
    unknown = [k for k in keys if k not in SCRAPERS]
    if unknown:
        sys.exit(f"Unknown site(s): {', '.join(unknown)}. Choose from {list(SCRAPERS)}")
    return keys


def main() -> int:
    args = parse_args()
    models = load_models()
    sites = selected_sites(args.sites)

    all_offers: list[Offer] = []
    for key in sites:
        scraper = SCRAPERS[key](
            headless=not args.no_headless,
            timeout_ms=args.timeout,
            debug=args.debug,
        )
        print(f"\n=== Running '{key}' ({scraper.source}) ===")
        try:
            offers = scraper.scrape(models)
            print(f"  -> {len(offers)} offers")
            all_offers.extend(offers)
        except NotImplementedError as exc:
            print(f"  skipped: {exc}")
        except Exception as exc:  # noqa: BLE001 - keep other sites running
            print(f"  ERROR: {exc}")

    if not all_offers:
        print("\nNo offers collected; nothing written.")
        return 1

    paths = write_outputs(all_offers)
    print(f"\nWrote {len(all_offers)} offers:")
    for kind, path in paths.items():
        print(f"  {kind}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
