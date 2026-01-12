import os
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
import time

CSV_FILENAME = 'travelex.csv'

def setup_csv_file():
    """
    Checks if the CSV file exists
    """
    if not os.path.exists(CSV_FILENAME):
        # Columns include a field to record the amount used to query the rate
        df = pd.DataFrame(columns=['Date', 'Day', 'Month', 'Year', 'Currency', 'Competitor', 'Amount_Input', 'Rate'])
        df.to_csv(CSV_FILENAME, index=False)
        print(f"A new CSV file '{CSV_FILENAME}' made.")
    else:
        print(f"CSV file '{CSV_FILENAME}' found.")

def get_current_date_info():
    """
    Gets the current date and returns the date string, day, month, and year.
    """
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    year = today.year
    month = today.month
    day = today.day
    return date_str, day, month, year

def get_data_from_webpage(url):
    """
    Selenium Part
    """
    scraped_data = []
    
    # Configure 
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080") #No use after trail
    
    driver = None
    try:
        print(f"Attempting to scrape webpage: {url}")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        print("Waiting for dynamic content to load...")
        time.sleep(5) 
        
        # List of button IDs
        button_ids = [
            'currency-europeanunion-EUR', 'currency-usa-USD', 'currency-canada-CAD',
            'currency-japan-JPY', 'currency-unitedarabemirates-AED', 'currency-thailand-THB',
            'currency-australia-AUD', 'currency-bulgaria-BGN', 'currency-switzerland-CHF',
            'currency-china-CNY', 'currency-czechrepublic-CZK', 'currency-denmark-DKK',
            'currency-hongkong-HKD', 'currency-hungary-HUF', 'currency-israel-ILS',
            'currency-mexico-MXN', 'currency-newzealand-NZD', 'currency-poland-PLN',
            'currency-qatar-QAR', 'currency-romania-RON', 'currency-saudiarabia-SAR',
            'currency-sweden-SEK', 'currency-singapore-SGD', 'currency-türkiye-TRY',
            'currency-southafrica-ZAR'
        ]

        # list of button IDs
        for button_id in button_ids:
            try:
                button = driver.find_element(By.ID, button_id)

                # Extract currency code and rate from attributes
                currency_code = button.get_attribute('value')
                rate = button.get_attribute('data-rate')
                
                if currency_code and rate:
                    scraped_data.append({
                        'Currency': currency_code,
                        'Rate': float(rate)
                    })
                else:
                    print(f"Missing data for button with ID '{button_id}'.")
            except NoSuchElementException:
                # Continue if an expected currency is not on the page
                continue 
            except (TypeError, ValueError) as e:
                print(f"An error occurred while processing data for '{button_id}': {e}")

    except WebDriverException as e:
        print(f"A WebDriver error occurred: {e}. Please ensure you have a compatible chromedriver installed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if driver:
            driver.quit() # Close the browser window
    
    return scraped_data

def run_scraper(url, competitor_name, amount_input):
    setup_csv_file()
    date_str, day, month, year = get_current_date_info()
    scraped_data = get_data_from_webpage(url)
    
    if not scraped_data:
        print("No data was scraped, error")
        return
        
    records_to_write = []
    
    for item in scraped_data:
        record = {
            'Date': date_str,
            'Day': day,
            'Month': month,
            'Year': year,
            'Currency': item['Currency'],
            'Competitor': competitor_name,
            # Use the input amount here
            'Amount_Input': amount_input, 
            'Rate': item['Rate']
        }
        records_to_write.append(record)
    
    new_df = pd.DataFrame(records_to_write)
    new_df.to_csv(CSV_FILENAME, mode='a', header=False, index=False)
    print(f"Successfully wrote {len(records_to_write)} records for amount input '{amount_input}' to '{CSV_FILENAME}'.")

if __name__ == "__main__":
    url_to_scrape = 'https://www.travelex.co.uk/'
    competitor_name = 'Travelex'
    input_amount = '1000_GBP_Test'
    run_scraper(url_to_scrape, competitor_name, input_amount)

