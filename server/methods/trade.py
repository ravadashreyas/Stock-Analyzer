from pandas._libs.tslibs import Tick
from pandas.core.indexes.base import F
from .options import optionsData
from .earnings import fundDataAnnual, fundDataQuart
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import datetime


def stockCheck(ticker):
    dat = yf.Ticker(ticker)
    stockHis = dat.history(period="5d")
    return stockHis.empty

#downloading YF data
def stockInfo(ticker):
    inF = False
    anF = False
    while (anF == False):
        isStartD = input("Is there a specific date you would like to see the data from? (Yes or No ONLY): ")
        isStartD = isStartD.strip().upper()
        if isStartD == "YES" or isStartD == "Y":
            anF = True
            while(inF == False):
                startD = input("From what date would you like to see the data from? : ")
                if len(startD) == 10 and startD[4] == '-' and startD[7] == '-':
                    inF = True
                else:
                    print("Please enter date in YYYY-MM-DD format.")
        elif isStartD == "NO" or isStartD == "N":
            print("Great!")
            startD = "2020-01-01"
            anF = True

        
    todayD = str(date.today())
    stock = yf.download(ticker, start=startD, end=todayD, interval="1d", auto_adjust=True)
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)
   
    #getting moving avg
    stock["SMA_20"] = stock["Close"].rolling(window=20).mean()
    stock["SMA_50"] = stock["Close"].rolling(window=50).mean()
    stock["SMA_200"] = stock["Close"].rolling(window=200).mean()

    stock["VWAP"] = (stock["Volume"] * stock ["Close"]).cumsum() / stock["Volume"].cumsum()

    #get closing prices only
    close_prices_df = stock[["Close"]].reset_index()
    #sort by date (others dont work)
    sorted_df = stock.sort_values(by="Date", ascending=False)
    #sorted_df = close_prices_df.drop(columns=["Date"])
    return stock


def pData(stockTicker):
    stockIn = yf.Ticker(stockTicker)
    info = stockIn.info
    tickerData = {
        "Company Name": str(info.get("longName")),
        "Current Price": str(info.get("currentPrice")),
        "Sector": str(info.get("sector")),
        "Industry": str(info.get("industry")),
        "Market Cap": str(info.get("marketCap"))
    }
    
    return tickerData

    

def checkCond(ticker):
    #check condition for column
    stock = yf.Ticker(ticker)
    close = stock[["Close"]].reset_index()
    close["Above 230"] = close["Close"] > 230
    
    
    

#main()
