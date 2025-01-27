import yfinance as yf
import pandas as pd

stock = yf.Ticker("AAPL")
from_date = "2022-01-01"
to_date = "2025-01-01"
stock_data = stock.history(start=from_date, end=to_date)

open_values = stock_data["Open"].tolist()
close_values = stock_data["Close"].tolist()
low_values = stock_data["Low"].tolist()

dates = stock_data.index.tolist()
unix_timestamps = [int(timestamp.timestamp()) for timestamp in dates]
print("Unix Timestamps:", unix_timestamps)
