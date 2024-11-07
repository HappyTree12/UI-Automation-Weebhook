from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import time

def place_order(action, ticker, value, takeProfit, stopLoss):
    options = webdriver.ChromeOptions()
    # Uncomment for headless mode if desired
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(options=options)
        
        # Maximize the window for full screen
        driver.maximize_window()

        # Navigate to the trading page
        trading_url = "https://www.propw.com/en_US/futures"
        driver.get(trading_url)
        print(f"Navigated to {trading_url}")

        # Wait for the "Size" input field within the buyamount-input container and input the value
        size_input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".buyamount-input .el-input__inner"))
        )
        size_input_field.send_keys(str(value))  # Input the value directly

        # Wait for and set the takeProfit field
        take_profit_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".take-profit-input-selector"))  # Replace with actual selector
        )
        take_profit_field.send_keys(str(takeProfit))  # Input the takeProfit value directly

        # Wait for and set the stopLoss field
        stop_loss_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".stop-loss-input-selector"))  # Replace with actual selector
        )
        stop_loss_field.send_keys(str(stopLoss))  # Input the stopLoss value directly

        # Locate and click the action button (e.g., "long" or "short")
        action_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, f"{action.lower()}_button"))
        )
        action_button.click()
        
        print(f"Order placed: {action} {value} of {ticker} with takeProfit: {takeProfit}, stopLoss: {stopLoss}")

    except Exception as e:
        print(f"Error placing order: {e}")

# Example usage
# place_order("long", "AAPL", 10, 150.00, 145.00)