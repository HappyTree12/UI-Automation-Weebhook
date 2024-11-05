from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import config  # Import configuration variables

def place_order(action, ticker, price):
    
    # Initialize the Selenium WebDriver
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')  # Optional: run in headless mode
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(options=options)
        print("Chrome Initialized Successful")

    except Exception as e:
        print(f"Error initializing Chrome:{e}")
        return

    try:
        # Open the Propw website
        driver.get(config.PROPW_URL)
        print("Chrome Open Successful")
        
        # Log in
        driver.find_element(By.ID, "username").send_keys(config.USERNAME)  # Update with actual field ID
        driver.find_element(By.ID, "password").send_keys(config.PASSWORD)  # Update with actual field ID
        driver.find_element(By.ID, "login_button").click()  # Update with actual button ID
        time.sleep(5) # Wait for login to complete

        # Place the order
        driver.find_element(By.ID, "trade_ticker_field").send_keys(ticker)  # Enter ticker
        driver.find_element(By.ID, "trade_price_field").send_keys(price)  # Enter price if required
        driver.find_element(By.ID, f"{action}_button").click()  # Click buy/sell based on action
        time.sleep(2)

    finally:
        driver.quit()  # Always quit the driver, even if there's an error
        print("Browser Closed")