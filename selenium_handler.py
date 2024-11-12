from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def place_order(symbol, action, value, stopLoss, takeProfit):
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    try:
        # Connect to the existing Chrome session
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        # Navigate to the trading page
        trading_url = "https://www.propw.com/en_US/futures"
        driver.get(trading_url)
        print(f"Navigated to {trading_url}")
        time.sleep(5)

        # Locate and input value for Size
        size_input_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'buyamount-input')]//input[@type='number']"))
        )
        size_input_field.click()
        size_input_field.send_keys(str(value))
        print(f"Input value set in Size field: {value}")

        # Click the TP/SL checkbox to activate TakeProfit and StopLoss
        tp_sl_checkbox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'el-checkbox__inner')]"))
        )
        tp_sl_checkbox.click()
        print("TP/SL checkbox clicked.")

        # Retrieve the current price
        price_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'price')]"))
        )
        price_value = float(price_element.text)  # Convert price to float for calculations
        print(f"The price is: {price_value}")

        # Calculate takeProfit and stopLoss based on action
        if action.lower() == "long":
            takeProfit = price_value + (price_value * takeProfit / 100)
            stopLoss = price_value - (price_value * stopLoss / 100)
        elif action.lower() == "short":
            takeProfit = price_value - (price_value * takeProfit / 100)
            stopLoss = price_value + (price_value * stopLoss / 100)
        else:
            raise ValueError("Invalid action. Expected 'long' or 'short'.")
        print(f"Calculated TakeProfit: {takeProfit}, StopLoss: {stopLoss}")

        # Set TakeProfit
        take_profit_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'profits-input')]//input[@class='el-input__inner']"))
        )
        take_profit_field.click()
        take_profit_field.clear()
        take_profit_field.send_keys(str(takeProfit))
        print(f"TakeProfit set to: {takeProfit}")

        # Set StopLoss
        stop_loss_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'loss-input')]//input[@class='el-input__inner']"))
        )
        stop_loss_field.click()
        stop_loss_field.clear()
        stop_loss_field.send_keys(str(stopLoss))
        print(f"StopLoss set to: {stopLoss}")

        # Click the Long or Short button based on action
        if action.lower() == "long":
            buy_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'el-button') and contains(@class, 'buy-btn') and .//span[text()='Buy/Long']]"))
            )
            buy_button.click()
        elif action.lower() == "short":
            sell_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'el-button') and contains(@class, 'sale-btn') and .//span[text()='Sell/Short']]"))
            )
            sell_button.click()
        print(f"{action.capitalize()} button clicked.")

        # Confirm the order in the popup dialog
        time.sleep(3)  # Allow time for the popup dialog to appear

        confirm_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'sure-btn') and //span[text()='Confirm']]")
        for button in confirm_buttons:
            try:
                button.click()
                break
            except Exception as err:
                continue
        else:
            raise Exception("Unable to click the 'Confirm' button.")

        print(f"Order placed: {action} {value} value of {symbol} with TakeProfit: {takeProfit}, StopLoss: {stopLoss}")

    except Exception as e:
        print(f"Error placing order: {e}")

# Example usage for testing purpose
place_order("JiaLinSeiFakBoi", "long", 100, 5, 5)