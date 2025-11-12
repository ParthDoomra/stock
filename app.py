from flask import Flask, jsonify
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/scrape/<symbol>', methods=['GET'])
def scrape(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d")

        # Check if data is valid
        if data.empty:
            return jsonify({
                "success": False,
                "error": f"No data found for '{symbol}'. Check the ticker symbol."
            }), 404

        recent = data.tail(1).iloc[0]
        result = {
            "symbol": symbol.upper(),
            "price": round(float(recent["Close"]), 2),
            "open": round(float(recent["Open"]), 2),
            "high": round(float(recent["High"]), 2),
            "low": round(float(recent["Low"]), 2),
            "volume": int(recent["Volume"]),
        }

        return jsonify({"success": True, "data": result}), 200

    except Exception as e:
        print(f"Error scraping {symbol}: {e}")
        return jsonify({
            "success": False,
            "error": f"Failed to fetch data for '{symbol}': {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)
