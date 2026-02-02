from .earnings import fundDataQuart
import yfinance as yf
import pandas as pd
import numpy as np



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