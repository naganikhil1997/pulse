from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- New import
from shopping_utils import fetch_item_data
import os

app = Flask(__name__)
CORS(app)  # <-- Enable CORS for all routes

@app.route('/compare-prices', methods=['POST'])
def compare_prices():
    try:
        data = request.get_json()
        items = data.get('items', [])
        zipcode = data.get('zipcode')
        eco_mode = data.get('eco_mode', False)

        if not items or not zipcode:
            return jsonify({"error": "Missing items or zipcode"}), 400

        results = []
        for item in items:
            item_data = fetch_item_data(item, zipcode, eco_mode)
            results.append(item_data)

        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)