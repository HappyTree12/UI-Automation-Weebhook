import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import config  # Import your configuration variables

def place_order(action, ticker, quantity):
    # Initialize the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        # Open the trading page for the specific symbol
        driver.get(f"https://propw.com/trade/{ticker}")  # Directly access the trading page

        # Example: Assuming there are elements for entering the quantity and submitting the order
        driver.find_element(By.ID, "trade_quantity_field").send_keys(quantity)  # Update with actual field ID
        driver.find_element(By.ID, f"{action}_button").click()  # Click buy/sell based on action
        time.sleep(2)  # Wait for order to process

    finally:
        driver.quit()  # Always quit the driver, even if there's an error

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python selenium_handler.py <action> <ticker> <quantity>")
    else:
        action = sys.argv[1]
        ticker = sys.argv[2]
        quantity = sys.argv[3]
        place_order(action, ticker, quantity)