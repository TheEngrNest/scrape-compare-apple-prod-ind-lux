"""Amazon India scraper — placeholder.

TODO: implement search-result + product-page scraping for amazon.in.
Note: Amazon serves frequent CAPTCHAs/bot pages to automated browsers;
expect to need request pacing, stealth tweaks, and CAPTCHA detection.
"""

from __future__ import annotations

from .base import BaseScraper
from .models import Offer


class AmazonIndiaScraper(BaseScraper):
    source = "amazon_in"

    def scrape(self, models: list[dict]) -> list[Offer]:
        raise NotImplementedError(
            "Amazon India scraper not implemented yet."
        )
