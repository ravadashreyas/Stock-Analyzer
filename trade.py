from pandas._libs.tslibs import Tick
from pandas.core.indexes.base import F
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import datetime


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




def optionsData(ticker):
    stockData = yf.Ticker(ticker)
    avaExp = stockData.options

    if not avaExp:
        print(f"No options data available for {stockName}.")
    first_expiry = avaExp[0]
    opt_chain = stockData.option_chain(first_expiry)
    calls = opt_chain.calls
    puts = opt_chain.puts

    if calls.empty and puts.empty:
            print(f"Option chain for {ticker} is empty.")
            return None, None
    if calls.empty:
            print(f"Calls data is empty for {ticker}.")
            return None, None
    if puts.empty:
            print(f"Puts data is empty for {ticker}.")
            return None, None
    
    calls = calls.replace({np.nan: None})
    puts = puts.replace({np.nan: None})
    callsDict = calls.to_dict(orient='records')
    putsDict = puts.to_dict(orient='records')
    callGraph = "callGraph"
    putGraph = "putGraph"
    callFig = plotBarGraph(callsDict, ticker, callGraph)
    putFig = plotBarGraph(putsDict, ticker, putGraph)
    return callsDict, putsDict, callFig, putFig
   


def fundDataQuart(ticker):
    stock = yf.Ticker(ticker)
    anEarnings = stock.quarterly_income_stmt

    if anEarnings is None or anEarnings.empty:
        print(f"No income statement data found for {ticker}.")
        return None

    anEarnings = anEarnings.transpose()
    anEarnings.dropna(how='all', inplace=True)
    anEarnings.reset_index(inplace=True)
    anEarnings = anEarnings.replace({np.nan: None})
    anEarnings = anEarnings.rename(columns={
        'index': 'date', 
        'Total Revenue': 'totalRevenue',
        'Gross Profit': 'grossProfit',
        'Normalized EBITDA': 'normalEBITDA',
        'Net Income': 'netIncome',
        'Diluted EPS': 'dilutedEPS',
        'Total Expenses': 'totalExpenses',
        'Operating Income': 'operatingIncome'
    })
   
    anEarnings['date'] = anEarnings['date'].dt.strftime('%Y-%m-%d')
    anEarningsJSON = anEarnings.to_dict(orient='records')
    
    return anEarningsJSON

def fundDataAnnual(ticker):
    stock = yf.Ticker(ticker)
    anEarnings = stock.income_stmt

    if anEarnings is None or anEarnings.empty:
        print(f"No income statement data found for {ticker}.")
        return None

    anEarnings = anEarnings.transpose()
    anEarnings.dropna(how='all', inplace=True)
    anEarnings.reset_index(inplace=True)
    anEarnings = anEarnings.replace({np.nan: None})
    anEarnings = anEarnings.rename(columns={
        'index': 'date', 
        'Total Revenue': 'totalRevenue',
        'Gross Profit': 'grossProfit',
        'Normalized EBITDA': 'normalEBITDA',
        'Net Income': 'netIncome',
        'Diluted EPS': 'dilutedEPS',
        'Total Expenses': 'totalExpenses',
        'Operating Income': 'operatingIncome'
    })
   
    anEarnings['date'] = anEarnings['date'].dt.strftime('%Y-%m-%d')
    anEarningsJSON = anEarnings.to_dict(orient='records')
    
    return anEarningsJSON

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

def plotBarGraph(options, ticker, graphType):
    ticker = ticker
    current_price = yf.Ticker(ticker).info.get("currentPrice")
    min_strike = current_price * 0.8
    max_strike = current_price * 1.2
    stockOptions = options
    filteredOptions = []
    for i in options: 
        if i['strike'] >= min_strike and i['strike'] <= max_strike:
            filteredOptions.append(i)
    
    if not filteredOptions:
        print(f"No options data found in the strike range {min_strike}-{max_strike}")
        return
    
    color = ''
    if graphType == "putGraph":
       color = 'red'
    elif graphType == "callGraph":
        color = 'green'
       
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[i['volume'] for i in filteredOptions],
        y=[i['strike'] for i in filteredOptions],
        name='Options Data',
        marker_color=color,
        orientation='h'
    ))
    fig.update_layout(

        xaxis_title='Volume',
        yaxis_title='Strike Price',
        width=700,
        height=400
    )
    return fig

def plotGraphW(ticker, timeFrame):
    #How to Plot the data with plotly
    stock_data = yf.download(ticker, period='max')
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
        stock = yf.download(ticker, start=M6, end=todayD, interval="1h", auto_adjust=True)
    elif timeFrame == "3M":
        three_months = pd.Timestamp.today() - pd.DateOffset(months=3)
        M3 = three_months.date()
        todayD = str(date.today())
        stock = yf.download(ticker, start=M3, end=todayD, interval="1h", auto_adjust=True)
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
            satDay = pd.Timestamp.today() - pd.DateOffset(days=1)
            D1 = satDay.date()
            todayD = (pd.Timestamp.today()) 
            stock = yf.download(ticker, start=D1, end=todayD, interval="1m", auto_adjust=True)
        elif day == "Sun":
            sunDay =( pd.Timestamp.today()) - pd.DateOffset(days=2)
            D1 = sunDay.date()
            todayD = one_day = (pd.Timestamp.today()) - pd.DateOffset(days=1)
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

def getHigh(stock):
    stock.columns = stock.columns.get_level_values(0)
    stock = stock.dropna()
    stock = stock.reset_index()
    stock = stock.replace({np.nan: None})
    sortedDf = stock.sort_values(by="High", ascending=False)
     #finding high
    maxClose = sortedDf["High"].max()
    return(maxClose)

def getLow(stock):
    stock.columns = stock.columns.get_level_values(0)
    stock = stock.dropna()
    stock = stock.reset_index()
    stock = stock.replace({np.nan: None})
    sortedDf = stock.sort_values(by="High", ascending=False)
     #finding high
    minClose = sortedDf["Low"].min()
    return(minClose)
    

def checkCond(ticker):
    #check condition for column
    stock = yf.Ticker(ticker)
    close = stock[["Close"]].reset_index()
    close["Above 230"] = close["Close"] > 230
    

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

def analyzeGammaProxy(currentPrice, calls, puts):
    if calls.empty or puts.empty:
        return "Insufficient options data for gamma proxy."
    priceRangeLower = currentPrice * 0.95
    priceRangeUpper = currentPrice * 1.05
    nearbyCalls = calls[(calls['strike'] >= priceRangeLower) & (calls['strike'] <= priceRangeUpper)]
    nearbyPuts = puts[(puts['strike'] >= priceRangeLower) & (puts['strike'] <= priceRangeUpper)]
    if nearbyCalls.empty or nearbyPuts.empty:
        return "No options found in the immediate price range."
    callOI = nearbyCalls['openInterest'].sum()
    putOI = nearbyPuts['openInterest'].sum()
    if callOI > putOI * 1.5:
        remark = f"Large call open interest ({callOI}) may act as resistance or accelerate a breakout."
    elif putOI > callOI * 1.5:
        remark = f"Large put open interest ({putOI}) may act as support or accelerate a breakdown."
    else:
        remark = "Options open interest is relatively balanced near the current price."
    return remark

def generateTradingSignal(currentPrice, rsi, movingAverages, supportLevels, resistanceLevels, fundamentals, putCallRatio, quarterlyFundamentals, gammaRemark):
    score = 0
    remarks = []
    nearestSupport = max([s for s in supportLevels if s is not None and s < currentPrice] or [0])
    nearestResistance = min([r for r in resistanceLevels if r is not None and r > currentPrice] or [float('inf')])
    if nearestSupport > 0 and (currentPrice - nearestSupport) / nearestSupport < 0.01:
        score += 3
        remarks.append("testing a key support level.")
    if (nearestResistance - currentPrice) / currentPrice < 0.01:
        score -= 3
        remarks.append("approaching strong resistance.")
    if rsi < 30:
        score += 5
        remarks.append("RSI is strongly oversold.")
    elif rsi > 70:
        score -= 5
        remarks.append("RSI is strongly overbought.")
    else:
        score += 1
        remarks.append("RSI is in a healthy range.")
    sma50 = movingAverages.get('SMA50')
    sma200 = movingAverages.get('SMA200')
    if sma50 and sma200:
        if currentPrice > sma50 and sma50 > sma200:
            score += 6
            remarks.append("In a strong bullish trend (Price > SMA50 > SMA200).")
        elif currentPrice < sma50 and sma50 < sma200:
            score -= 6
            remarks.append("In a strong bearish trend (Price < SMA50 < SMA200).")
        if (currentPrice - sma50) / sma50 > 0.10:
            score -= 2
            remarks.append("Price is overextended above its 50-day average.")
        if abs((currentPrice - sma50) / sma50) < 0.01:
            score += 3
            remarks.append("Price is finding support at the 50-day moving average.")
        if (currentPrice - sma200) / sma200 > 0.15:
            score -= 3
            remarks.append("Price is significantly overextended above its 200-day average.")
        if abs((currentPrice - sma200) / sma200) < 0.01:
            score += 5
            remarks.append("Price is finding long-term support at the 200-day moving average.")
    if fundamentals:
        peRatio = fundamentals.get('trailingPE')
        profitMargin = fundamentals.get('profitMargins')
        debtToEquity = fundamentals.get('debtToEquity')
        returnOnEquity = fundamentals.get('returnOnEquity')
        if peRatio and 0 < peRatio < 20:
            score += 3
            remarks.append("Valuation appears reasonable (P/E < 20).")
        elif peRatio and peRatio > 75:
            score -= 3
            remarks.append("Valuation appears high (P/E > 75).")
        if profitMargin and profitMargin > 0.10:
            score += 4
            remarks.append("Company is highly profitable (margin > 10%).")
        elif profitMargin and profitMargin < 0:
            score -= 4
            remarks.append("Company is unprofitable.")
        if debtToEquity and debtToEquity < 100:
            score += 3
            remarks.append("Low debt level (D/E < 1.0).")
        if returnOnEquity and returnOnEquity > 0.15:
            score += 2
            remarks.append("Efficient management (ROE > 15%).")
    if putCallRatio is not None:
        if putCallRatio < 0.7:
            score += 3
            remarks.append(f"Bullish options sentiment (PCR: {putCallRatio:.2f}).")
        elif putCallRatio > 1.0:
            score -= 3
            remarks.append(f"Bearish options sentiment (PCR: {putCallRatio:.2f}).")
    if quarterlyFundamentals and len(quarterlyFundamentals) >= 2:
        latestQuarter = quarterlyFundamentals[0]
        previousQuarter = quarterlyFundamentals[1]
        if latestQuarter.get('totalRevenue') and previousQuarter.get('totalRevenue'):
            if latestQuarter['totalRevenue'] > previousQuarter['totalRevenue']:
                score += 4
                remarks.append("Positive quarter-over-quarter revenue growth.")
            else:
                score -= 3
                remarks.append("Negative quarter-over-quarter revenue growth.")
        if latestQuarter.get('netIncome') and previousQuarter.get('netIncome'):
            if latestQuarter['netIncome'] > previousQuarter['netIncome']:
                score += 5
                remarks.append("Positive quarter-over-quarter earnings growth.")
            else:
                score -= 4
                remarks.append("Negative quarter-over-quarter earnings growth.")
    if gammaRemark:
        remarks.append(gammaRemark)
    if score >= 10:
        rating = "Buy"
    elif score <= -10:
        rating = "Sell"
    else:
        rating = "Neutral"
    finalRemark = " ".join(remarks).capitalize()
    return rating, finalRemark

def tecAnalysis(ticker):
    stock = yf.Ticker(ticker)
    masterDf = yf.download(ticker, period="5y", interval="1d", auto_adjust=True)
    if masterDf.empty:
        return None, None
    today = pd.Timestamp.now().normalize()
    weekDf = masterDf.loc[today - pd.DateOffset(weeks=1):]
    oneMonthDf = masterDf.loc[today - pd.DateOffset(months=1):]
    threeMonthDf = masterDf.loc[today - pd.DateOffset(months=3):]
    sixMonthDf = masterDf.loc[today - pd.DateOffset(months=6):]
    ytdDf = masterDf.loc[str(today.year):]
    oneYearDf = masterDf.loc[today - pd.DateOffset(years=1):]
    fiveYearDf = masterDf
    allTimeDf = yf.download(ticker, period="max", interval="1mo", auto_adjust=True)
    analysis = {
        "weekHigh": getHigh(weekDf), "weekLow": getLow(weekDf),
        "monthHigh": getHigh(oneMonthDf), "monthLow": getLow(oneMonthDf),
        "threeMonthHigh": getHigh(threeMonthDf), "threeMonthLow": getLow(threeMonthDf),
        "sixMonthHigh": getHigh(sixMonthDf), "sixMonthLow": getLow(sixMonthDf),
        "ytdHigh": getHigh(ytdDf), "ytdLow": getLow(ytdDf),
        "oneYearHigh": getHigh(oneYearDf), "oneYearLow": getLow(oneYearDf),
        "fiveYearHigh": getHigh(fiveYearDf), "fiveYearLow": getLow(fiveYearDf),
        "allTimeHigh": getHigh(allTimeDf), "allTimeLow": getLow(allTimeDf)
    }
    keySupport = []
    keyDemand = []
    currentPrice = stock.info.get('currentPrice')
    if currentPrice:
        for i in analysis:
            value = analysis[i]
            if value is not None:
                if currentPrice > value:
                    keySupport.append(value)
                elif currentPrice < value:
                    keyDemand.append(value)
    change = masterDf['Close'].diff()
    gain = change.where(change > 0, 0).fillna(0)
    loss = (-change.where(change < 0, 0)).fillna(0)
    avgGain = gain.rolling(window=14).mean()
    avgLoss = loss.rolling(window=14).mean()
    rs = avgGain / avgLoss
    rsiSeries = 100 - (100 / (1 + rs))
    masterDf['RSI'] = rsiSeries
    masterDf["SMA20"] = masterDf["Close"].rolling(window=20).mean()
    masterDf["SMA50"] = masterDf["Close"].rolling(window=50).mean()
    masterDf["SMA200"] = masterDf["Close"].rolling(window=200).mean()
    currentRSI = rsiSeries.iloc[-1] if not rsiSeries.empty else 50
    currentMAs = masterDf[["SMA20", "SMA50", "SMA200"]].iloc[-1].to_dict() if not masterDf.empty else {}
    fundamentals = stock.info
    quarterlyData = fundDataQuart(ticker)
    putCallRatio = None
    gammaRemark = "Gamma data not available."
    try:
        stockForOptions = yf.Ticker(ticker)
        firstExpiry = stockForOptions.options[0]
        optChain = stockForOptions.option_chain(firstExpiry)
        callsDf = optChain.calls
        putsDf = optChain.puts
        totalCallsOI = callsDf['openInterest'].sum()
        totalPutsOI = putsDf['openInterest'].sum()
        if totalCallsOI > 0:
            putCallRatio = totalPutsOI / totalCallsOI
        gammaRemark = analyzeGammaProxy(currentPrice, callsDf, putsDf)
    except Exception as e:
        print(f"Could not process options data: {e}")
    rating, remark = generateTradingSignal(
        currentPrice, currentRSI, currentMAs, 
        sorted(keySupport), sorted(keyDemand), 
        fundamentals, putCallRatio, quarterlyData, gammaRemark
    )
    analysis['rating'] = rating
    analysis['remark'] = remark
    stockDataFinal = masterDf.reset_index()
    stockDataFinal = stockDataFinal.replace({np.nan: None})
    stockDataFinal['Date'] = stockDataFinal['Date'].dt.strftime('%Y-%m-%d')
    stockDataDict = stockDataFinal.to_dict(orient='records')
    return analysis, stockDataDict


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

