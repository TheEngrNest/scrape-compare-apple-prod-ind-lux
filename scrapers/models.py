"""Shared data structures and helpers for all scrapers."""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional

# Columns used for CSV output, in order.
OFFER_FIELDS = [
    "scraped_at",
    "source",
    "region",
    "currency",
    "family",
    "config",
    "chip",
    "screen_size_in",
    "memory_gb",
    "storage_gb",
    "color",
    "price",
    "price_raw",
    "in_stock",
    "url",
    "sku",
]


@dataclass
class Offer:
    """A single priced product configuration scraped from one source."""

    source: str
    family: str
    config: str
    price: Optional[float]
    price_raw: str
    url: str
    region: str = "india"
    currency: str = "INR"
    chip: Optional[str] = None
    screen_size_in: Optional[float] = None
    memory_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    color: Optional[str] = None
    in_stock: Optional[bool] = None
    sku: Optional[str] = None
    scraped_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


def parse_inr(text: str) -> Optional[float]:
    """Extract a numeric price from Indian-formatted rupee text.

    Handles Indian digit grouping (e.g. "₹1,69,900.00" -> 169900.0).
    Returns None when no rupee amount is found.
    """
    if not text:
        return None
    match = re.search(r"₹\s*([\d,]+(?:\.\d+)?)", text)
    if not match:
        # Fall back to a bare number if the symbol was stripped upstream.
        match = re.search(r"([\d,]{4,}(?:\.\d+)?)", text)
        if not match:
            return None
    try:
        return float(match.group(1).replace(",", ""))
    except ValueError:
        return None
