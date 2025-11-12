

# Import necessary libraries
import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# ===============================
# 1. Load and plot your CSV file
# ===============================

# Load your CSV file
df = pd.read_csv("stock_data.csv")

# Fix the Date column - handle both possible column names
if "qUnnamed: 0" in df.columns:
    df.rename(columns={"qUnnamed: 0": "Date"}, inplace=True)
elif "Unnamed: 0" in df.columns:
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Define a color palette (one color per company)
colors = ['blue', 'green', 'red', 'orange', 'purple']

# Plot all company stock prices from CSV
plt.figure(figsize=(12,6))
for i, col in enumerate(df.columns):
    plt.plot(df.index, df[col], label=col, color=colors[i % len(colors)])

# Add labels, title, and legend
plt.title("Company Stock Prices (from CSV)", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Stock Price (USD)", fontsize=12)
plt.legend(title="Companies", loc="best")
plt.grid(True)
plt.show()


# =====================================
# 2. Fetch and plot live stock & crypto
# =====================================

# Define tickers
stock_ticker = 'GOOGL'
crypto_ticker = 'BTC-USD'

# Set date range (last 30 days)
start_date = dt.date.today() - dt.timedelta(days=30)
end_date = dt.date.today()

# Download stock & crypto data
stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
crypto_data = yf.download(crypto_ticker, start=start_date, end=end_date)

print("\nStock Data (GOOGL):")
print(stock_data.head())

print("\nCryptocurrency Data (BTC-USD):")
print(crypto_data.head())

# Plot both GOOGL and BTC closing prices
plt.figure(figsize=(12,6))
plt.plot(stock_data.index, stock_data['Close'], label="GOOGL", color="blue")
plt.plot(crypto_data.index, crypto_data['Close'], label="BTC-USD", color="orange")

plt.title("GOOGL vs BTC-USD Closing Prices (Last 30 Days)", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Closing Price (USD)", fontsize=12)
plt.legend(title="Assets", loc="best")
plt.grid(True)
plt.show()