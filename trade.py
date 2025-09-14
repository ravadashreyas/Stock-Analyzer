from pandas._libs.tslibs import Tick
from pandas.core.indexes.base import F
import plotly.graph_objects as go
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
    global stockData
    stockData = stockData = yf.Ticker(stockName)


def stockCheck():
    stockHis = stockData.history(period ="5d")
    return stockHis.empty

#downloading YF data
def stockInfo():
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
    ebD = []

    if "EBITDA" in anEarnings.index:
        ebData = anEarnings.loc["EBITDA"]
        for i in ebData:
            ebD[i] = ebData.iloc[i]
            if i > 5:
                break

    if "Gross Profit" in anEarnings.index:
        gpData = anEarnings.loc["Gross Profit"]
        gp = gpData.iloc[:, 1]

    if "Basic EPS" in anEarnings.index:
        epsData = anEarnings.loc["Basic EPS"]
        eps = epsData.iloc[:, 1]
    


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
    
    
    
    


def pData(stockTicker):
    stockIn = yf.Ticker(stockTicker)
    info = stockIn.info
    tickerData = {
        "Company Name": str(info.get("longName")),
        "Sector": str(info.get("sector")),
        "Industry": str(info.get("industry")),
        "Market Cap": str(info.get("marketCap"))
    }
    
    return tickerData
        
def plotGraphW(ticker):
    #How to Plot the data with plotly
    todayD = str(date.today())
    stock = yf.download(ticker, start="2020-01-01", end=todayD, interval="1d", auto_adjust=True)
    
    if stock.empty:
        print(f"No data found for {ticker}")
        return None
        
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)

    # Calculate indicators
    stock["SMA_20"] = stock["Close"].rolling(window=20).mean()
    stock["SMA_50"] = stock["Close"].rolling(window=50).mean()
    stock["SMA_200"] = stock["Close"].rolling(window=200).mean()
    
    # Fix VWAP calculation - use proper VWAP formula
    stock["VWAP"] = ((stock["High"] + stock["Low"] + stock["Close"]) / 3 * stock["Volume"]).cumsum() / stock["Volume"].cumsum()
    fig = go.Figure()
    
    # Always plot Close price
    fig.add_trace(go.Scatter(
        x=stock.index.tolist(), 
        y=stock['Close'].tolist(), 
        mode='lines', 
        name='Close Price', 
        line=dict(color='blue', width=2)
    ))
    
    # Plot SMAs with different colors - filter out NaN values
    if stock['SMA_20'].notna().any():
        sma20_data = stock['SMA_20'].dropna()
        fig.add_trace(go.Scatter(
            x=sma20_data.index.tolist(), 
            y=sma20_data.tolist(), 
            mode='lines', 
            name='SMA 20', 
            line=dict(color='orange', width=1)
        ))
    
    if stock['SMA_50'].notna().any():
        sma50_data = stock['SMA_50'].dropna()
        fig.add_trace(go.Scatter(
            x=sma50_data.index.tolist(), 
            y=sma50_data.tolist(), 
            mode='lines', 
            name='SMA 50', 
            line=dict(color='red', width=1)
        ))
    
    if stock['SMA_200'].notna().any():
        sma200_data = stock['SMA_200'].dropna()
        fig.add_trace(go.Scatter(
            x=sma200_data.index.tolist(), 
            y=sma200_data.tolist(), 
            mode='lines', 
            name='SMA 200', 
            line=dict(color='purple', width=1)
        ))
    
    # Plot VWAP
    if stock['VWAP'].notna().any():
        vwap_data = stock['VWAP'].dropna()
        fig.add_trace(go.Scatter(
            x=vwap_data.index.tolist(), 
            y=vwap_data.tolist(), 
            mode='lines', 
            name='VWAP', 
            line=dict(color='green', width=1, dash='dash')
        ))

    fig.update_layout(
        title=f'{ticker.upper()} Price Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Legend',
        width=1000,
        height=600
    )

    return fig

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
            anEarnings = stockData.balance_sheet
            print(anEarnings)
            plotGraph()

#main()

