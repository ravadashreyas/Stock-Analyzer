import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date

def rsiCalc(ticker):
    stock = yf.Ticker(ticker)
    stockData = stock.history(period ="1y", interval="1w")
    change = stockData['Close'].diff()
    gain = (change.where(change > 0, 0)).fillna(0)
    loss = (-change.where(change < 0, 0)).fillna(0)

    avgGain = gain.rolling(window=14).mean()
    avgLoss = loss.rolling(window=14).mean()

    rs = avgGain / avgLoss
    rsi = 100 - (100 / (1 + rs))
    stockData['RSI'] = rsi
    return rsi

def movingAvg(ticker):
    stock = yf.Ticker(ticker)
    stockData = stock.history(period ="12mo", interval="1d")
    stockDataW = stock.history(period ="12mo", interval="1wk")
    stockData["SMA_20"] = stockData["Close"].rolling(window=20).mean()
    stockData["SMA_50"] = stockData["Close"].rolling(window=50).mean()
    stockData["SMA_200"] = stockData["Close"].rolling(window=200).mean()
    stockData["WSMA_20"] = stockDataW["Close"].rolling(window=20).mean()
    stockData = stockData.dropna()
    movAvg = stockData[["SMA_20", "SMA_50", "SMA_200", "WSMA_20"]]
    return movAvg



def plotGraph(ticker):
    #How to Plot the data
    todayD = str(date.today())
    stock = yf.download(ticker, start="2020-01-01", end=todayD, interval="1d", auto_adjust=True)
    answer = False
    while answer == False:
        yGraph = input("Do you want a technical graph of " + ticker.upper() +  " (Yes or No ONLY)")
        yGraph = yGraph.strip().upper()
        if yGraph == "YES" or yGraph == "Y":
            stock["Close"].plot(title= ticker.upper() + " Price")
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