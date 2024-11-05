from flask import Flask, request, jsonify
from selenium_handler import place_order  # Import place_order from selenium_handler

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.get_json()
        
        # Extract the necessary information from JSON payload
        symbol = data.get("symbol")
        action = data.get("action")
        quantity = data.get("quantity")

        # Check that all required fields are present
        if not all([symbol, action, quantity]):
            return jsonify({"status": "error", "message": "Missing data fields"}), 400

        try:
            # Call the place_order function with the extracted data
            place_order(action, symbol, quantity)
            return jsonify({"status": "success", "message": "Order placed successfully."}), 200
        except Exception as e:
            print(f"Error placing order: {e}")
            return jsonify({"status": "error", "message": "Failed to place order."}), 500
    else:
        return jsonify({"status": "error", "message": "Unsupported media type"}), 415

if __name__ == '__main__':
    app.run(port=5001)