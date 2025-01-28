import plotly.graph_objects as go
import yfinance as yf
import pandas as pd

stock = yf.Ticker("AAPL")
from_date = "2022-01-01"
to_date = "2025-01-01"
stock_data = stock.history(start=from_date, end=to_date)

stock_data.reset_index(inplace=True) # this just makes the date and accessible column

data = [go.Candlestick(x = stock_data["Date"], open = stock_data["Open"], high = stock_data["High"], low = stock_data["Low"], close = stock_data["Close"])]
fig = go.Figure(data)

fig.show()



