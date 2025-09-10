import yfinance as yf
import pandasql as ps
import pandas as pd
import matplotlib.pyplot as plt

x = "AAPL"
data = yf.download(x, start="2022-01-01", end="2025-9-8", interval="1d")
print(data.head())

data["SMA_20"] = data["Close"].rolling(window=20).mean()
data["SMA_50"] = data["Close"].rolling(window=50).mean()
data["SMA_200"] = data["Close"].rolling(window=200).mean()
close_prices_df = data[["Close"]].reset_index()
sorted_df = data.sort_values(by="Date", ascending=False)
#sorted_df = close_prices_df.drop(columns=["Date"])


data["Close"].plot(title="Apple Closing Prices")
data["SMA_20"].plot(title="Apple Closing Prices")
data["SMA_50"].plot(title="Apple Closing Prices")
data["SMA_200"].plot(title="Apple Closing Prices")
plt.legend()
plt.show()



