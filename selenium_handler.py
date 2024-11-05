from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import time

def place_order(action, ticker, quantity):
    options = webdriver.ChromeOptions()
    # Uncomment for headless mode if desired
    # options.add_argument('--headless')  
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(options=options)

        # Navigate to the trading page
        trading_url = f"https://www.coinw.com/futures/usdt/{ticker}"
        driver.get(trading_url)
        print(f"Navigated to {trading_url}")

        # Wait for the quantity field and ensure it's interactable
        quantity_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".el-input__inner"))
        )
        
        # Attempt to clear the field and set the value directly using JavaScript
        driver.execute_script("arguments[0].value = '';", quantity_field)  # Clear any existing value
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", quantity_field, str(quantity))

        # Locate and click the action button (e.g., "long" or "short")
        action_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"{action.lower()}_button"))
        )
        action_button.click()
        
        print(f"Order placed: {action} {quantity} of {ticker}")

    except Exception as e:
        print(f"Error placing order: {e}")
    finally:
        driver.quit()