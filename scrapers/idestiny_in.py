"""iDestiny (India Apple reseller) scraper — placeholder.

TODO: confirm the exact store URL (e.g. idestiny.in) and product-listing
structure, then implement like AppleIndiaScraper. Until then this raises so
the runner reports it clearly instead of returning silent empty results.
"""

from __future__ import annotations

from .base import BaseScraper
from .models import Offer


class IDestinyScraper(BaseScraper):
    source = "idestiny_in"

    def scrape(self, models: list[dict]) -> list[Offer]:
        raise NotImplementedError(
            "iDestiny scraper not implemented yet — confirm site URL first."
        )
