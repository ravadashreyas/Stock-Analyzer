import yfinance as yf
import pandasql as ps
import pandas as pd
import matplotlib.pyplot as pl

x = "AAPL"
data = yf.download(x, start="2025-09-01", end="2025-9-8", interval="1d")
print(data.head())

close_prices_df = data[["Close"]].reset_index()
print(close_prices_df.head())


#data["Close"].plot(title="Apple Closing Prices")
#plt.show()

