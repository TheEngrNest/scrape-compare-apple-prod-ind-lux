"""Flipkart India scraper — placeholder.

TODO: implement search-result + product-page scraping for flipkart.com.
Note: Flipkart shows a login modal and uses obfuscated CSS class names that
change often; selectors will need regular maintenance.
"""

from __future__ import annotations

from .base import BaseScraper
from .models import Offer


class FlipkartIndiaScraper(BaseScraper):
    source = "flipkart_in"

    def scrape(self, models: list[dict]) -> list[Offer]:
        raise NotImplementedError(
            "Flipkart India scraper not implemented yet."
        )
