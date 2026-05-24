# scrape-compare-apple-prod-ind-lux

Scrape and compare Apple MacBook prices across India and Luxembourg.

Phase 1 (current) targets **India** sources with Playwright:

| Site            | Key        | Status        |
| --------------- | ---------- | ------------- |
| Apple India     | `apple`    | implemented   |
| iDestiny        | `idestiny` | placeholder¹  |
| Amazon India    | `amazon`   | placeholder   |
| Flipkart India  | `flipkart` | placeholder   |

¹ Confirm the exact iDestiny store URL before implementing.

## Layout

```
macbook_models.json     Seed list of MacBook models + variants to price
run.py                  CLI entry point
scrapers/
  base.py               Playwright lifecycle + shared helpers
  models.py             Offer dataclass + INR price parsing
  storage.py            CSV + JSON output writers
  apple_in.py           Apple India scraper (template)
  idestiny_in.py        placeholder
  amazon_in.py          placeholder
  flipkart_in.py        placeholder
output/                 Timestamped run results (gitignored)
```

## Setup

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## Usage

```bash
python run.py --sites apple                 # one site
python run.py --sites apple,amazon          # several
python run.py --sites all                   # everything wired up
python run.py --sites apple --no-headless   # watch the browser
python run.py --sites apple --debug         # dump page HTML to output/debug/
```

Each run writes `output/prices-india-<timestamp>.csv` and `.json`.

## Notes / caveats

- **Network access required.** Live scraping needs outbound access to the
  target sites and to the Playwright browser CDN. Some sandboxed/cloud
  environments block these (the Apple Cloud session this was built in does),
  so run it locally or in an environment whose network policy allows them.
- **Bot detection.** Amazon and Flipkart frequently serve CAPTCHAs/bot pages
  to automated browsers; expect to need pacing, stealth tweaks, and CAPTCHA
  handling when those scrapers are implemented.
- **Selectors drift.** Site DOMs change. `apple_in.py` falls back to a regex
  price sweep if its tile selectors stop matching; use `--debug` to capture
  HTML for re-tuning.
