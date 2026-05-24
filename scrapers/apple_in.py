"""Apple official India store scraper (https://www.apple.com/in).

Strategy: visit each MacBook family's "buy" page and read the standard
configuration tiles, each of which carries a "From ₹..." price. This gives
one offer per listed chip/size variant without having to drive the full
configurator. Selectors have a regex fallback so a DOM change degrades to a
best-effort price sweep rather than a hard failure.
"""

from __future__ import annotations

from .base import BaseScraper
from .models import Offer, parse_inr

# Buy pages per family. Keys match the "family" field in macbook_models.json.
BUY_URLS = {
    "MacBook Neo": "https://www.apple.com/in/shop/buy-mac/macbook-neo",
    "MacBook Air": "https://www.apple.com/in/shop/buy-mac/macbook-air",
    "MacBook Pro": "https://www.apple.com/in/shop/buy-mac/macbook-pro",
}

# Candidate selectors for the product tiles on a buy page, tried in order.
TILE_SELECTORS = [
    "[data-autom='product-tile']",
    ".rf-bfe-product-tile",
    "li.rf-bfe-collection-item",
]


class AppleIndiaScraper(BaseScraper):
    source = "apple_in"
    region = "india"
    currency = "INR"

    def scrape(self, models: list[dict]) -> list[Offer]:
        families = [m["family"] for m in models if m["family"] in BUY_URLS]
        seen: set[str] = set()
        offers: list[Offer] = []

        with self.browser():
            self._dismiss_cookies()
            for family in dict.fromkeys(families):  # de-dupe, keep order
                url = BUY_URLS[family]
                print(f"[apple_in] {family} -> {url}")
                try:
                    self.goto(url)
                    self.page.wait_for_load_state("networkidle")
                except Exception as exc:  # noqa: BLE001 - report and continue
                    print(f"  ! failed to load {url}: {exc}")
                    continue
                self.dump_html(family.replace(" ", "_"))
                found = self._extract_tiles(family, url)
                if not found:
                    print("  ! no tiles matched; falling back to price sweep")
                    found = self._regex_sweep(family, url)
                offers.extend(found)
                self.polite_pause()

        return offers

    # --- internals -------------------------------------------------------

    def _dismiss_cookies(self) -> None:
        try:
            self.goto("https://www.apple.com/in/")
            btn = self.page.query_selector("#ac-gn-store-cookie-banner-accept")
            if btn:
                btn.click()
        except Exception:  # noqa: BLE001 - non-fatal
            pass

    def _extract_tiles(self, family: str, url: str) -> list[Offer]:
        offers: list[Offer] = []
        tiles = []
        for sel in TILE_SELECTORS:
            tiles = self.page.query_selector_all(sel)
            if tiles:
                break

        for tile in tiles:
            text = (tile.inner_text() or "").strip()
            price = parse_inr(text)
            if price is None:
                continue
            # First non-empty line is typically the variant name.
            config = next(
                (ln.strip() for ln in text.splitlines() if ln.strip()),
                family,
            )
            offers.append(
                Offer(
                    source=self.source,
                    region=self.region,
                    currency=self.currency,
                    family=family,
                    config=config,
                    chip=_guess_chip(text),
                    price=price,
                    price_raw=_first_price_line(text),
                    url=url,
                )
            )
        return offers

    def _regex_sweep(self, family: str, url: str) -> list[Offer]:
        """Last-resort: pull every ₹ amount visible on the page."""
        body = self.page.query_selector("body")
        text = (body.inner_text() if body else "") or ""
        offers: list[Offer] = []
        for line in text.splitlines():
            price = parse_inr(line)
            if price and price > 30000:  # filter out accessory/EMI noise
                offers.append(
                    Offer(
                        source=self.source,
                        region=self.region,
                        currency=self.currency,
                        family=family,
                        config=line.strip()[:120],
                        price=price,
                        price_raw=line.strip(),
                        url=url,
                    )
                )
        return offers


def _first_price_line(text: str) -> str:
    for line in text.splitlines():
        if "₹" in line:
            return line.strip()
    return text.strip()[:120]


def _guess_chip(text: str) -> str | None:
    for chip in ("M5 Max", "M5 Pro", "M5", "A18 Pro"):
        if chip in text:
            return chip
    return None
