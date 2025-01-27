import yfinance as yf

stock = yf.Ticker("AAPL")

from_date = "2021-01-01"
to_date = "2025-01-01"

stock_data = stock.history(start=from_date, end=to_date)

open_values = stock_data["Open"].tolist()
close_values = stock_data["Close"].tolist()
low_values = stock_data["Low"].tolist()

print(f"Number of 'Open' data points: {len(open_values)}")

print(len(open_values))
