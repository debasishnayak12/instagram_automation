#automation using playwright
<!-- pip install playwright
playwright install -->

<!-- 
from playwright.sync_api import sync_playwright
import time
import random

def human_like_delay():
    time.sleep(random.uniform(3, 7))

def download_booking_data(property_name, start_date, end_date):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()

        # 1. Navigate to login page
        page.goto("https://example.com/login")

        # 2. Fill login form
        page.fill("#username", "your_username")
        page.fill("#password", "your_password")
        page.click("button[type='submit']")
        
        human_like_delay()

        # 3. Search for property
        page.fill("#search-bar", property_name)
        page.click("#search-button")

        human_like_delay()

        # 4. Select date range
        page.fill("#start-date", start_date)
        page.fill("#end-date", end_date)
        page.click("#apply-dates")

        human_like_delay()

        # 5. Download Excel file
        with page.expect_download() as download_info:
            page.click("#download-excel")
        download = download_info.value
        download.save_as(f"{property_name}_{start_date}_to_{end_date}.xlsx")

        print(f"Downloaded: {download.path}")

        browser.close()

# List of properties and date ranges
property_list = [
    {"name": "Property A", "start_date": "2024-01-01", "end_date": "2024-01-07"},
    {"name": "Property B", "start_date": "2024-02-01", "end_date": "2024-02-07"},
]

for property in property_list:
    download_booking_data(property["name"], property["start_date"], property["end_date"])
    print(f"Completed download for: {property['name']}")

 -->