from pandas._libs.tslibs import Tick
from pandas.core.indexes.base import F
import plotly.graph_objects as go
import yfinance as yf
import pandasql as ps
import pandas as pd
import matplotlib.pyplot as plt
import backtrader as bt
from datetime import date
import datetime

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
    print(avaExp)

    if not avaExp:
        print(f"No options data available for {stockName}.")
    first_expiry = avaExp[0]
    opt_chain = stockData.option_chain(first_expiry)
    calls = opt_chain.calls
    puts = opt_chain.puts
    return calls, puts
    print(calls.head(100))
    print(puts.head(50))

stockData = stockData = yf.Ticker('aapl')
optionsData()
   
def fundData():
    anEarnings = stockData.income_stmt
    ebGrowth = False
    gpGrowth = False
    epsGrowth = False
    value = 0
    ebD = []
    gpD = []
    eps = []

    if "EBITDA" in anEarnings.index:
        ebData = anEarnings.loc["EBITDA"]
        for i in ebData:
            ebD[i] = ebData.iloc[i]
            if i > 5:
                break

    if "Gross Profit" in anEarnings.index:
        gpData = anEarnings.loc["Gross Profit"]
        for i in gpData:
            gpD[i] = gpData.iloc[i]
            if i > 5:
                break

    if "Basic EPS" in anEarnings.index:
        epsData = anEarnings.loc["Basic EPS"]
        for i in gpData:
            eps[i] = epsData.iloc[i]
            if i > 5:
                break

    

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
        
def plotGraphW(ticker, timeFrame):
    #How to Plot the data with plotly
    stock_data = yf.download(ticker, period='max')
    print(timeFrame)
    if timeFrame == "ALL":
        first_date = stock_data.index[0]
        todayD = str(date.today())
        stock = yf.download(ticker, start=first_date, end=todayD, interval="1d", auto_adjust=True)
    elif timeFrame == "5Y":
        five_years = pd.Timestamp.today() - pd.DateOffset(years=5)
        Y5 = five_years.date()
        todayD = str(date.today())
        stock = yf.download(ticker, start=Y5, end=todayD, interval="1d", auto_adjust=True)
    elif timeFrame == "1Y":
        one_year = pd.Timestamp.today() - pd.DateOffset(years=1)
        Y1 = one_year.date()
        todayD = str(date.today())
        stock = yf.download(ticker, start=Y1, end=todayD, interval="4h", auto_adjust=True)
    elif timeFrame == "YTD":
        yearTD = pd.Timestamp.today() - pd.DateOffset(months=pd.Timestamp.today().month - 1, days=pd.Timestamp.today().day - 1)
        YTD = yearTD.date()
        todayD = str(date.today())
        stock = yf.download(ticker, start=YTD, end=todayD, interval="1h", auto_adjust=True)
    elif timeFrame == "6M":
        six_months = pd.Timestamp.today() - pd.DateOffset(months=6)
        M6 = six_months.date()
        todayD = str(date.today())
        stock = yf.download(ticker, start=M6, end=todayD, interval="30m", auto_adjust=True)
    elif timeFrame == "3M":
        three_months = pd.Timestamp.today() - pd.DateOffset(months=3)
        M3 = three_months.date()
        todayD = str(date.today())
        stock = yf.download(ticker, start=M3, end=todayD, interval="30m", auto_adjust=True)
    elif timeFrame == "1M":
        one_month = pd.Timestamp.today() - pd.DateOffset(months=1)
        M1 = one_month.date()
        todayD = str(date.today())
        stock = yf.download(ticker, start=M1, end=todayD, interval="15m", auto_adjust=True)
    elif timeFrame == "5D":
        one_week = pd.Timestamp.today() - pd.DateOffset(weeks=1)
        W1 = one_week.date()
        todayD = str(date.today())
        stock = yf.download(ticker, start=W1, end=todayD, interval="5m", auto_adjust=True)
    elif timeFrame == "1D":
        x = datetime.datetime.now()
        day = x.strftime("%a")
        if day == "Sat":
            satDay = pd.Timestamp.today() - pd.DateOffset(days=2)
            D1 = satDay.date()
            todayD = one_day = (pd.Timestamp.today()) - pd.DateOffset(days=1)
            stock = yf.download(ticker, start=D1, end=todayD, interval="1m", auto_adjust=True)
        elif day == "Sun":
            sunDay =( pd.Timestamp.today()) - pd.DateOffset(days=3)
            D1 = sunDay.date()
            todayD = one_day = (pd.Timestamp.today()) - pd.DateOffset(days=2)
            stock = yf.download(ticker, start=D1, end=todayD, interval="1m", auto_adjust=True)
        elif day == "Mon" and x.hour < 15:
            one_day = (pd.Timestamp.today()) - pd.DateOffset(days=4)
            D1 = one_day.date()
            todayD = (pd.Timestamp.today()) - pd.DateOffset(days=3)
            stock = yf.download(ticker, start=one_day, end=todayD, interval="1m", auto_adjust=True)
        elif day == "Mon" and x.hour > 15:
            one_day = (pd.Timestamp.today()) - pd.DateOffset(days=4)
            D1 = one_day.date()
            todayD = (pd.Timestamp.today()) - pd.DateOffset(days=3)
            todayDa = str(date.today())
            stock = yf.download(ticker,period='1d',interval='1m')
        else:
            one_day = pd.Timestamp.today() - pd.DateOffset(days=1)
            D1 = one_day.date()
            todayD = str(date.today())
            stock = yf.download(ticker,period='1d',interval='1m')

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

        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Legend',
        width=1000,
        height=600
    )

    return fig

def plotGraph(ticker):
    #How to Plot the data
    todayD = str(date.today())
    stock = yf.download(ticker, start="2020-01-01", end=todayD, interval="1d", auto_adjust=True)
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

