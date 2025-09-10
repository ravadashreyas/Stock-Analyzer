from pandas._libs.tslibs import Tick
import yfinance as yf
import pandasql as ps
import pandas as pd
import matplotlib.pyplot as plt

x = "AAPL"
def stockInfo(x):
#downloading YF data

    stock = yf.download(x, start="2022-01-01", end="2025-9-8", interval="1d")
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)
   

    #getting moving avg
    stock["SMA_20"] = stock["Close"].rolling(window=20).mean()
    stock["SMA_50"] = stock["Close"].rolling(window=50).mean()
    stock["SMA_200"] = stock["Close"].rolling(window=200).mean()

    #get closing prices only
    close_prices_df = stock[["Close"]].reset_index()
    #sort by date (others dont work)
    sorted_df = stock.sort_values(by="Date", ascending=False)
    #sorted_df = close_prices_df.drop(columns=["Date"])
    return stock

stock = stockInfo(x)

def sortData(stock):
    sorted_df = stock.sort_values(by="Close", ascending=False)
    print(sorted_df.head()) 

def checkCond(stock):
    #check condition for column
    close = stock[["Close"]].reset_index()
    close["Above 230"] = close["Close"] > 230
    true = close[close["Above 230"] == True]
    #print(true.head(50))

    #finding all time high
    max_close = close["Close"].max()
    print(max_close)

def plotData(stock):
    #How to Plot the data
    stock["Close"].plot(title="Apple Closing Prices")
    stock["SMA_20"].plot()
    stock["SMA_50"].plot()
    stock["SMA_200"].plot()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

stockInfo(x)
checkCond(stock)
plotData(stock)

