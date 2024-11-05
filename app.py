from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        symbol = data.get("symbol")
        action = data.get("action")
        quantity = data.get("quantity")

        # Print received data (for debugging)
        print(f"Received alert - Symbol: {symbol}, Action: {action}, Quantity: {quantity}")

        # Call the Selenium handler script with parameters
        try:
            # Construct the command to run the selenium_handler.py script
            command = ["python3", "selenium_handler.py", action, symbol, str(quantity)]
            subprocess.Popen(command)  # Run it in the background
            return jsonify({"status": "success", "message": "Order placed."}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "error", "message": "No data provided"}), 400

if __name__ == '__main__':
    app.run(port=5001)