# Webpage Content Extraction

A simple toolkit for scraping structured data from web pages. Built this to track exchange rates, but the pattern works for any site where you need to click things and grab data.

## What It Does

**Core idea:** Selenium + Pandas = clean CSV data

- Opens a browser (headless or visible)
- Clicks buttons / navigates to find data
- Extracts what you need
- Saves to CSV with timestamps

## Example: FX Rate Tracker

The included script (`fx_tracker.py`) pulls live exchange rates from Travelex UK. I built this as an expat watching for good GBP exchange rates.

```bash
python fx_tracker.py
```

Output goes to `data/rates.csv`:

| Date | Day | Month | Year | Currency | Rate | Source | Query_Amount |
|------|-----|-------|------|----------|------|--------|--------------|
| 2026-02-22 | 22 | 2 | 2026 | EUR | 1.18 | Travelex | 1000_GBP |
| 2026-02-22 | 22 | 2 | 2026 | USD | 1.26 | Travelex | 1000_GBP |

## Setup

```bash
pip install -r requirements.txt
```

You also need ChromeDriver installed locally. On Mac:

```bash
brew install chromedriver
```

On Ubuntu/Debian:

```bash
sudo apt install chromium-chromedriver
```

## Project Structure

```
├── fx_tracker.py          # Travelex scraper example
├── utils/
│   └── scraper_base.py    # Reusable Selenium helpers
├── data/                  # Output goes here
│   └── rates.csv
├── requirements.txt
└── README.md
```

## Using for Other Sites

The `scraper_base.py` has reusable bits:

```python
from utils.scraper_base import Scraper, save_to_csv

scraper = Scraper(headless=True)
driver = scraper.start()

# do your scraping here
# ...

scraper.close()

# save results
save_to_csv(data, "data/output.csv", columns=["col1", "col2"])
```

## What I Learned

- Selenium button clicking is fragile (IDs change, sites update)
- Always add good wait times for dynamic content
- CSV appends are simple but effective for time-series data
- Headless mode breaks some sites (Cloudflare sometimes blocks it)

## Legal Note

Only scrape sites that allow it. Check `robots.txt` and terms of service. This project is for learning and personal use on my own accounts.

## Requirements

- Python 3.8+
- Chrome browser
- ChromeDriver
- pandas
- selenium
