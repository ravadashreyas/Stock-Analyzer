import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from datetime import date
import datetime

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