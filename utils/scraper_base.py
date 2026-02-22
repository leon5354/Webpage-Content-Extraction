"""
Base scraper utilities. Nothing fancy, just stuff I use repeatedly.
"""

import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import pandas as pd


class Scraper:
    """
    Wrapper around Selenium so I don't repeat the same setup code.
    """
    
    def __init__(self, headless=True, window_size="1920,1080"):
        self.headless = headless
        self.window_size = window_size
        self.driver = None
    
    def start(self):
        """Fire up Chrome."""
        opts = Options()
        
        if self.headless:
            opts.add_argument("--headless")
        
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument(f"--window-size={self.window_size}")
        
        # helps with some sites that block headless
        opts.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        self.driver = webdriver.Chrome(options=opts)
        return self.driver
    
    def close(self):
        """Shut it down."""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def get(self, url, wait=3):
        """Load a page and wait for it."""
        if not self.driver:
            self.start()
        self.driver.get(url)
        time.sleep(wait)
    
    def click(self, by, value):
        """Click something if it exists."""
        try:
            el = self.driver.find_element(by, value)
            el.click()
            return True
        except NoSuchElementException:
            return False
    
    def get_attr(self, by, value, attr):
        """Get an attribute from an element."""
        try:
            el = self.driver.find_element(by, value)
            return el.get_attribute(attr)
        except NoSuchElementException:
            return None
    
    def get_text(self, by, value):
        """Get text from an element."""
        try:
            el = self.driver.find_element(by, value)
            return el.text
        except NoSuchElementException:
            return None


def save_to_csv(data, filepath, columns=None):
    """
    Append data to CSV. Creates file if it doesn't exist.
    
    data: list of dicts
    filepath: where to save
    columns: optional, specify column order
    """
    if not data:
        print("No data to save.")
        return False
    
    # make sure directory exists
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    
    df = pd.DataFrame(data)
    
    if columns:
        df = df[columns]
    
    file_exists = os.path.exists(filepath)
    
    df.to_csv(
        filepath,
        mode="a",
        header=not file_exists,
        index=False
    )
    
    print(f"Saved {len(data)} rows to {filepath}")
    return True


def get_date_parts():
    """Return current date split into parts. Useful for time series."""
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "day": now.day,
        "month": now.month,
        "year": now.year,
    }
