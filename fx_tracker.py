"""
FX Rate Tracker - Travelex UK
Pulls live exchange rates and saves to CSV.
"""

from utils.scraper_base import Scraper, save_to_csv, get_date_parts


# currencies available on Travelex UK site
CURRENCY_BUTTONS = [
    "currency-europeanunion-EUR",
    "currency-usa-USD",
    "currency-canada-CAD",
    "currency-japan-JPY",
    "currency-unitedarabemirates-AED",
    "currency-thailand-THB",
    "currency-australia-AUD",
    "currency-bulgaria-BGN",
    "currency-switzerland-CHF",
    "currency-china-CNY",
    "currency-czechrepublic-CZK",
    "currency-denmark-DKK",
    "currency-hongkong-HKD",
    "currency-hungary-HUF",
    "currency-israel-ILS",
    "currency-mexico-MXN",
    "currency-newzealand-NZD",
    "currency-poland-PLN",
    "currency-qatar-QAR",
    "currency-romania-RON",
    "currency-saudiarabia-SAR",
    "currency-sweden-SEK",
    "currency-singapore-SGD",
    "currency-türkiye-TRY",
    "currency-southafrica-ZAR",
]

OUTPUT_FILE = "data/rates.csv"
SOURCE_NAME = "Travelex"
QUERY_AMOUNT = "1000_GBP"  # what I'm checking rates for


def scrape_travelex(url="https://www.travelex.co.uk/"):
    """
    Scrape FX rates from Travelex UK.
    
    The site uses buttons with data-rate attributes for each currency.
    We click through them and grab the values.
    """
    scraper = Scraper(headless=True)
    results = []
    
    try:
        scraper.get(url, wait=5)
        print(f"Loaded {url}")
        
        for btn_id in CURRENCY_BUTTONS:
            # each button has value=currency code and data-rate=the rate
            currency = scraper.get_attr(By.ID, btn_id, "value")
            rate = scraper.get_attr(By.ID, btn_id, "data-rate")
            
            if currency and rate:
                try:
                    results.append({
                        "Currency": currency,
                        "Rate": float(rate),
                    })
                except ValueError:
                    # rate wasn't a number, skip it
                    continue
        
        print(f"Found {len(results)} currencies")
        
    except Exception as e:
        print(f"Scraping failed: {e}")
        
    finally:
        scraper.close()
    
    return results


def run():
    """Main entry point."""
    print("Starting FX scrape...")
    
    raw_data = scrape_travelex()
    
    if not raw_data:
        print("No data scraped. Site might be blocking or structure changed.")
        return
    
    # add date and metadata
    date_parts = get_date_parts()
    
    records = []
    for item in raw_data:
        records.append({
            "Date": date_parts["date"],
            "Day": date_parts["day"],
            "Month": date_parts["month"],
            "Year": date_parts["year"],
            "Currency": item["Currency"],
            "Rate": item["Rate"],
            "Source": SOURCE_NAME,
            "Query_Amount": QUERY_AMOUNT,
        })
    
    save_to_csv(
        records,
        OUTPUT_FILE,
        columns=["Date", "Day", "Month", "Year", "Currency", "Rate", "Source", "Query_Amount"]
    )


if __name__ == "__main__":
    from selenium.webdriver.common.by import By
    run()
