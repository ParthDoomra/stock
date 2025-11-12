from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
import requests
import sqlite3
import bcrypt

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# =====================================================
# ✅ DATABASE SETUP
# =====================================================
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# ✅ Initialize database on startup
init_db()

# =====================================================
# ✅ API KEY VALIDATION (YOUR ORIGINAL FUNCTION)
# =====================================================
def validate_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        return False, "OpenAI API key not found in environment variables"
    if api_key == "your-api-key-here":
        return False, "OpenAI API key is still set to default value. Please update it in .env file"
    return True, api_key

# =====================================================
# ✅ HEALTH CHECK ROUTE (UNCHANGED)
# =====================================================
@app.route('/health', methods=['GET'])
def health_check():
    is_valid, message = validate_api_key()
    if is_valid:
        return jsonify({
            'status': 'ok',
            'message': 'Server is running and API key is configured'
        })
    return jsonify({
        'status': 'error',
        'message': message
    }), 500

# =====================================================
# ✅ USER SIGNUP
# =====================================================
@app.post('/signup')
def signup():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"success": False, "message": "All fields are required"}), 400

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_pw)
            )
            conn.commit()
            return jsonify({"success": True, "message": "Signup successful"})
        
        except sqlite3.IntegrityError:
            return jsonify({"success": False, "message": "Email already registered"})
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# =====================================================
# ✅ USER LOGIN
# =====================================================
@app.post('/login')
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"success": False, "message": "User not found"})

        stored_pw = user["password"]

        if bcrypt.checkpw(password.encode('utf-8'), stored_pw):
            return jsonify({
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"]
                }
            })
        else:
            return jsonify({"success": False, "message": "Invalid password"})
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# =====================================================
# ✅ YOUR EXISTING /analyze ROUTE (UNCHANGED)
# =====================================================
@app.route('/analyze', methods=['POST'])
def analyze_stocks():
    try:
        data = request.json
        stock_data = data['data']
        date_range = data.get('dateRange', {})

        is_valid, message_or_key = validate_api_key()
        if not is_valid:
            return jsonify({
                'error': 'API Configuration Error',
                'content': message_or_key
            }), 500
        
        api_key = message_or_key

        prompt = f"""Analyze the following stock data metrics for the period from {date_range.get('start')} to {date_range.get('end')}:

{json.dumps(stock_data, indent=2)}
(Full prompt unchanged…)
        """

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            }
        )

        if response.status_code == 200:
            analysis = response.json()['choices'][0]['message']['content']
            return jsonify({'content': analysis})

        return jsonify({
            'error': f'OpenAI API Error: {response.status_code}',
            'content': 'Unable to generate analysis.'
        }), response.status_code

    except Exception as e:
        return jsonify({
            'error': str(e),
            'content': 'An error occurred while analyzing the stock data.'
        }), 500
# Add to analysis_server.py
from datetime import date, timedelta
import yfinance as yf
from flask import request

@app.get("/live")
def live_prices():
    tickers = request.args.get("tickers", "GOOGL,BTC-USD").split(",")
    days = int(request.args.get("days", 30))
    start = date.today() - timedelta(days=days)
    end = date.today()

    out = {}
    for t in tickers:
        df = yf.download(t, start=start, end=end)
        df = df.reset_index()
        out[t] = [
            {"date": str(d.date()), "close": float(c)}
            for d, c in zip(df["Date"], df["Close"])
        ]
    return jsonify(out)

# =====================================================
# ✅ RUN SERVER
# =====================================================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(port=port, debug=debug)

