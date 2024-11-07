from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def place_order(symbol, action, value, stopLoss, takeProfit):
    options = Options()
    # Use remote debugging to connect to the already running Chrome session
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # The same port used to start Chrome with remote debugging
    
    # try:
        # Connect to the existing Chrome browser session
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()  # Ensure window is maximized

        # Navigate to the trading page
    trading_url = "https://www.propw.com/en_US/futures"
    driver.get(trading_url)
    print(f"Navigated to {trading_url}")

        # Extra wait to ensure page loads completely
    time.sleep(5)

        # Locate and input value for Size (using XPath)
    size_input_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'buyamount-input')]//input[@type='number']"))
    )
    size_input_field.click()  # Click to focus
    size_input_field.send_keys(str(value))  # Input the value
    print(f"Input value set in Size field: {value}")

    # Wait for and click the TP/SL checkbox to activate takeProfit and stopLoss
    tp_sl_checkbox = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'el-checkbox__inner')]"))  # TP/SL checkbox
    )
    tp_sl_checkbox.click()  # Click the checkbox to activate TP/SL fields
    print("TP/SL checkbox clicked.")

    # Locate and set TakeProfit using parent class 'profits-input'
    take_profit_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'profits-input')]//input[@class='el-input__inner']"))
    )
    take_profit_field.click()  # Focus on the field
    take_profit_field.send_keys(str(takeProfit))
    print(f"TakeProfit set to: {takeProfit}")

    # Locate and set StopLoss (using class name 'el-input__inner', assuming similar to takeProfit)
    stop_loss_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'loss-input')]//input[@class='el-input__inner']"))
    )
    stop_loss_field.click()  # Focus on the field
    stop_loss_field.send_keys(str(stopLoss))
    print(f"StopLoss set to: {stopLoss}")

    # Determine the correct button to click based on action (Long or Short)
    print(f"action --------> {action}")
    if action.lower() == "long":
        # Locate and click the Long button
        buy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'el-button') and contains(@class, 'buy-btn') and contains(@class, 'buy-sale-btn') and contains(@class, 'el-button--default') and .//span[text()='Buy/Long']]"))
        )
        buy_button.click()
    elif action.lower() == "short":
        # Locate and click the Short button
        action_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'el-button') and contains(@class, 'sale-btn') and contains(@class, 'buy-sale-btn') and contains(@class, 'el-button--default') and .//span[text()='Sell/Short']]"))
        )
    else:
        print(f"Invalid action: {action}. Expected 'long' or 'short'.")
        driver.quit()
        return

    # Locate and click the Confirm button
    # Wait for the "Confirm" button to be clickable inside the dialog
    driver.implicitly_wait(5)
#     confirm_button = WebDriverWait(driver, 10).until(
#     EC.element((By.CLASS_NAME, 
#                                 "el-dialog__wrapper padding40"
#                                 #"el-button sure-btn el-button--primary"
#                                 ))
# )
    confirm_button = driver.find_element(By.CSS_SELECTOR, ".el-button.sure-btn.el-button--primary")
    confirm_button.click()
    print("Clicked the Confirm button")

    print(f"Order placed: {action} {value} of {symbol} with takeProfit: {takeProfit}, stopLoss: {stopLoss}")

    # except Exception as e:
    #     print(f"Error placing order: {e}")

    # finally:
    #     input("Press Enter to close the browser...")
    #     driver.quit()

# Example usage
# place_order("long", "AAPL", 10, 150.00, 145.00)
# place_order("short", "AAPL", 10, 150.00, 145.00)
