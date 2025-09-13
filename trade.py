from pandas._libs.tslibs import Tick
from pandas.core.indexes.base import F
import yfinance as yf
import pandasql as ps
import pandas as pd
import matplotlib.pyplot as plt
import backtrader as bt
from datetime import date

stockName = ""
stockData = ""
def getTicker():
    global stockName 
    stockName = input("Enter the ticker you would like to analyze: ")
    global stockData
    stockData = stockData = yf.Ticker(stockName)
    stockCheck()


def stockCheck():
    stockHis = stockData.history(period ="5d")
    return stockHis.empty

#downloading YF data
def stockInfo():
    global stock
    inF = False
    while (inF == False):
        startD = input("From what date would you like to see the data from? : ")
        if len(startD) == 10 and startD[4] == '-' and startD[7] == '-':
            inF = True
        else:
            print("Please enter date in YYYY-MM-DD format.")
        
    todayD = str(date.today())
    stock = yf.download(stockName, start=startD, end=todayD, interval="1d", auto_adjust=True)
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


def sortData():
    sorted_df = stock.sort_values(by="Close", ascending=False)
     #finding all time high
    max_close = sorted_df["Close"].max()
    

def checkCond():
    #check condition for column
    close = stock[["Close"]].reset_index()
    close["Above 230"] = close["Close"] > 230
    true = close[close["Above 230"] == True]
    #print(true.head(50))

def optionsData():
    avaExp = stockData.options

    if not avaExp:
        print(f"No options data available for {stockName}.")
    first_expiry = avaExp[0]
    opt_chain = stockData.option_chain(first_expiry)
    calls = opt_chain.calls
    puts = opt_chain.puts
   
def fundData():
    anEarnings = stockData.income_stmt
    ebGrowth = False
    gpGrowth = False
    epsGrowth = False
    value = 0



    if "EBITDA" in anEarnings.index:
        ebData = anEarnings.loc["EBITDA"]
        eb = ebData.iloc[:, 1]
    print(ebData)
    if "Gross Profit" in anEarnings.index:
        gpData = anEarnings.loc["Gross Profit"]
        gp = gpData.iloc[:, 1]
    if "Basic EPS" in anEarnings.index:
        epsData = anEarnings.loc["Basic EPS"]
        eps = epsData.iloc[:, 1]
    
    for u in eb:
        if (eb[u]) > (eb[u + 1]):
            value = value + 1
        elif (eb[u]) < (eb[u + 1]):
            value = 1

    answer = False
    while answer == False:
        yData = input("Do you want the financial information on the ticker provided? (Yes or No ONLY)")
        yData = yData.strip().upper()
        if yData == "YES" or yData == "Y":
            answer = True
        elif yData == "NO" or yData == "N":
            print("Great!")
            answer = True
        else:
            print("Please Provide a Yes or No answer")
    
    
    
    


def pData():
    info = stockData.info
    print("----------- Company Information ----------- ")
    print("Company Name: " + str(info.get("longName")))
    print("Sector: " + str(info.get("sector")))
    print("Industry: " + str(info.get("industry")))
    print("Market Cap: " + str(info.get("marketCap")))
    print("------------------------------------------- ")
        
    
def plotGraph():
    #How to Plot the data
    answer = False
    while answer == False:
        yGraph = input("Do you want a technical graph of " + stockName.upper() +  " (Yes or No ONLY)")
        yGraph = yGraph.strip().upper()
        if yGraph == "YES" or yGraph == "Y":
            stock["Close"].plot(title= stockName.upper() + " Price")
            stock["SMA_20"].plot()
            stock["SMA_50"].plot()
            stock["SMA_200"].plot()
            stock["VWAP"].plot()
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.legend()
            plt.show()
            answer = True
        elif yGraph == "NO" or yGraph == "N":
            answer = True
        else:
            print("Please Provide a Yes or No answer")
    


def main():
    getTicker()
    funcRun = False
    while funcRun == False:
        if stockCheck() ==  True:
            print("Not valid ticker please try again")
            getTicker()
        else:
            #wish = input("Would you : ")
            funcRun = True
            stock = stockInfo()
            sortData()
            checkCond()
            optionsData()
            pData()
            anEarnings = stockData.income_stmt
            ebData = anEarnings.loc["EBITDA"]
            eb = ebData.iloc[:, 1]
            print(ebData)
            plotGraph()

main()

