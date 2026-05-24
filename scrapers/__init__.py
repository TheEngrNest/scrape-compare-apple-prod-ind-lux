"""Scraper registry for the India price-comparison project."""

from .amazon_in import AmazonIndiaScraper
from .apple_in import AppleIndiaScraper
from .base import BaseScraper
from .flipkart_in import FlipkartIndiaScraper
from .idestiny_in import IDestinyScraper
from .models import Offer

# Map CLI names -> scraper classes.
SCRAPERS: dict[str, type[BaseScraper]] = {
    "apple": AppleIndiaScraper,
    "idestiny": IDestinyScraper,
    "amazon": AmazonIndiaScraper,
    "flipkart": FlipkartIndiaScraper,
}

__all__ = ["SCRAPERS", "BaseScraper", "Offer"]
