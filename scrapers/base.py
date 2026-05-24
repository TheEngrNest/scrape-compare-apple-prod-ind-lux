"""Base scraper: shared Playwright browser lifecycle and helpers."""

from __future__ import annotations

import random
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from .models import Offer

# A realistic desktop UA reduces the odds of being served a bot page.
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

DEBUG_DIR = Path(__file__).resolve().parent.parent / "output" / "debug"


class BaseScraper:
    """Subclass and implement ``scrape``.

    Provides a ready-to-use Playwright page via ``self.page`` inside the
    ``browser()`` context manager, plus small anti-bot conveniences.
    """

    source = "base"
    region = "india"
    currency = "INR"

    def __init__(
        self,
        headless: bool = True,
        timeout_ms: int = 30000,
        debug: bool = False,
    ) -> None:
        self.headless = headless
        self.timeout_ms = timeout_ms
        self.debug = debug
        self.page: Page | None = None

    @contextmanager
    def browser(self) -> Iterator[Page]:
        with sync_playwright() as p:
            browser: Browser = p.chromium.launch(headless=self.headless)
            context: BrowserContext = browser.new_context(
                user_agent=DEFAULT_UA,
                locale="en-IN",
                viewport={"width": 1366, "height": 900},
            )
            context.set_default_timeout(self.timeout_ms)
            page = context.new_page()
            self.page = page
            try:
                yield page
            finally:
                self.page = None
                context.close()
                browser.close()

    # --- helpers ---------------------------------------------------------

    def goto(self, url: str, wait_until: str = "domcontentloaded") -> None:
        assert self.page is not None, "Call within the browser() context."
        self.page.goto(url, wait_until=wait_until)

    def polite_pause(self, lo: float = 1.0, hi: float = 2.5) -> None:
        """Randomised delay between requests to look less robotic."""
        time.sleep(random.uniform(lo, hi))

    def dump_html(self, label: str) -> None:
        """Save the current page HTML for offline selector tuning."""
        if not self.debug or self.page is None:
            return
        DEBUG_DIR.mkdir(parents=True, exist_ok=True)
        path = DEBUG_DIR / f"{self.source}-{label}.debug.html"
        path.write_text(self.page.content(), encoding="utf-8")
        print(f"  [debug] wrote {path}")

    # --- contract --------------------------------------------------------

    def scrape(self, models: list[dict]) -> list[Offer]:
        """Return offers for the given seed models. Must be implemented."""
        raise NotImplementedError
