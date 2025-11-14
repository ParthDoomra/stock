📊 StockSense — Smart Stock Analysis Platform

A complete stock analytics system with login, CSV visualization, portfolio allocation, and real-time stock scraping.

🚀 Overview

StockSense is a fully functional stock-analysis web application designed to visualize, compare, and analyze stock market data using clean UI and interactive dashboards.

It provides:

✔ CSV-based analysis
✔ Multi-stock trends & comparison
✔ Portfolio allocation (Pie + Bar)
✔ Live web scraping for real-time stock data
✔ Login & Signup authentication (SQLite)
✔ Light/Dark theme
✔ Responsive modern UI

This project is suitable for:

✨ Students learning full-stack development

📈 Developers exploring data visualization

⚙️ Anyone building stock tools or dashboards

🔥 Features
⭐ 1. User Authentication (Login/Signup)

Users stored locally using SQLite

Secure login and redirect flow

Registration with name/email/password

⭐ 2. CSV Stock Data Visualization

Automatically reads stock_data.csv

Displays 5 stock time-series charts

Date range filters and quick presets

Custom CSV upload supported

⭐ 3. Compare Stocks

Select ANY two stocks

Side-by-side comparison

Smooth animated Chart.js graphs

⭐ 4. Portfolio Allocation

Donut (Pie) Chart + Bar Chart

Automatic percentage calculations

Export Pie or Bar as PNG

⭐ 5. Live Stock Scraping

Enter any symbol (AAPL, TSLA, GOOGL)

Displays real-time price + trend

Demo fallback if API fails

Clickable tiles for quick analysis

⭐ 6. Beautiful UI + Animations

Fully responsive

Light/Dark mode

AOS animations

Smooth chart transitions

🧠 Tech Stack
Frontend
Technology	Purpose
HTML5	Structure
CSS3	Styling & responsive layout
JavaScript (Vanilla JS)	Interactivity & logic
Chart.js	Chart visualizations
PapaParse.js	CSV file parsing
AOS.js	Page animations
Backend
Technology	Purpose
Python	Backend logic
Flask	Server & API routes
SQLite	User database
pandas	Data handling
yfinance	Live stock scraping
📂 Folder Structure
├── home.html           # Home/Landing page
├── login.html          # Login screen
├── signup.html         # Signup form
├── index.html          # Main dashboard (Overview / Compare / Allocation / Live)
├── scrape.html         # Web scraping page (Live prices)
│
├── styles.css          # Global styling
├── stockAnalysis.js    # Dashboard logic (charts)
├── config.js           # API endpoints
│
├── stock_data.csv      # Sample stock dataset
├── stock_data.py       # Dummy generator (optional)
│
├── app.py              # Flask backend
├── create_db.py        # SQLite DB creator
├── users.db            # Stores user accounts
│
└── README.md

🛠️ Installation & Setup

Follow these steps to run the complete project on your system.

1️⃣ Clone the Repository
git clone https://github.com/ParthDoomra/stock.git
cd stock

2️⃣ Install Python Dependencies
pip install flask pandas yfinance

3️⃣ Create the SQLite Database
python create_db.py


This will create users.db with a users table.

4️⃣ Run the Backend Server
python app.py


Backend will start on:

http://127.0.0.1:8000

5️⃣ Run the Frontend

You must open the files through a local server (NOT double-clicking).

Best way: VS Code → Live Server
OR

live-server --port=5500


Your main frontend file is:

home.html  → landing page
index.html → dashboard (after login)
scrape.html → web scraper


Open:

http://127.0.0.1:5500/home.html

🧪 API Endpoints
POST /signup

Registers user
Body:

{
  "name": "Parth Doomra",
  "email": "parth@example.com",
  "password": "12345"
}

POST /login

Authenticates user

GET /scrape/<symbol>

Returns real-time data for stock symbol
Example:

/scrape/AAPL

GET /live

Real-time multi-stock API
Example:

/live?tickers=AAPL,TSLA,GOOGL&days=30

🏠 Home Page
![Home page] (https://github.com/ParthDoomra/stock/blob/2f64bb896e8db88bf849bab65168e18157c1b95b/Screenshot%20(138).png)
