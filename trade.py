from pandas._libs.tslibs import Tick
from pandas.core.indexes.base import F
import yfinance as yf
import pandasql as ps
import pandas as pd
import matplotlib.pyplot as plt
import backtrader as bt

stockName = ""
stockData = ""
def getTicker():
    global stockName 
    stockName = input("Enter the ticker you would like to analyze: ")
    global stockData
    stockData = stockData = yf.Ticker(stockName)
    stockCheck(stockName)


def stockCheck(stockName):
    stockHis = stockData.history(period ="5d")
    return stockHis.empty

#downloading YF data
def stockInfo(stockName):
    stock = yf.download(stockName, start="2022-01-01", end="2025-09-08", interval="1d", auto_adjust=True)
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


def sortData(stock):
    sorted_df = stock.sort_values(by="Close", ascending=False)
     #finding all time high
    max_close = sorted_df["Close"].max()
    

def checkCond(stock):
    #check condition for column
    close = stock[["Close"]].reset_index()
    close["Above 230"] = close["Close"] > 230
    true = close[close["Above 230"] == True]
    #print(true.head(50))

def optionsData(stock):
    avaExp = stockData.options

    if not avaExp:
        print(f"No options data available for {stockName}.")
    first_expiry = avaExp[0]
    opt_chain = stockData.option_chain(first_expiry)
    calls = opt_chain.calls
    puts = opt_chain.puts
   
def fundData():
    anEarnings = stockData.earnings
    print(anEarnings)

def pData():
    info = stockData.info

   
    answer = False
    while answer == False:
        yData = input("Do you want more basic information on the ticker provided? (Yes or No ONLY)")
        yData = yData.strip().upper()
        print(yData)
        if yData == "YES":
            print("Company Name: " + str(info.get("longName")))
            print("Sector: " + str(info.get("sector")))
            print("Industry: " + str(info.get("industry")))
            print("Market Cap: " + str(info.get("marketCap")))
            answer = True
        elif yData == "NO":
            print("Great!")
            answer = True
        else:
            print("Please Provide a Yes or No answer")
    
    
def plotGraph(stock, stockName):
    #How to Plot the data
    stock["Close"].plot(title= stockName + " Price")
    stock["SMA_20"].plot()
    stock["SMA_50"].plot()
    stock["SMA_200"].plot()
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()


def main():
    getTicker()
    funcRun = False
    while funcRun == False:
        if stockCheck(stockData) ==  True:
            print("Not valid ticker please try again")
            getTicker()
        else:
            #wish = input("Would you : ")
            funcRun = True
            stock = stockInfo(stockName)
            stockInfo(stockName)
            sortData(stock)
            checkCond(stock)
            optionsData(stock)
            pData()
            fundData()
            plotGraph(stock, stockName)

main()

