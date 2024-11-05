from flask import Flask, request, jsonify
from selenium_handler import place_order  # Import from selenium_handler

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()  # Receive JSON data from TradingView
    action = data.get("action")  # Get the action (buy/sell)
    ticker = data.get("ticker")  # Get the ticker symbol
    price = data.get("price")  # Get the price (optional)

    if action in ["buy", "sell"]:
        place_order(action, ticker, price)
        return jsonify({"status": "success", "message": f"Order {action} executed for {ticker}"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid action"}), 400

if __name__ == '__main__':
    app.run(port=5001)