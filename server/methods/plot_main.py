import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from datetime import date
import datetime

MAX_CACHE_SIZE = 10
cache = {}

def plotGraphW(ticker, timeFrame):

    if (ticker in cache) and (str(timeFrame) in cache[ticker]):
        data = cache.pop(ticker)
        cache[ticker] = data
        print("Used Plot Cache")
        return cache[ticker][timeFrame]
    else:
        if (len(cache) >= MAX_CACHE_SIZE) and (ticker not in cache):
            oldest_ticker = next(iter(cache))
            del cache[oldest_ticker]


        if cache.get(ticker) is None:
            cache[ticker] = {}



        timeFrame = (timeFrame or '').upper()

        if timeFrame == "ALL":
            stock = yf.download(ticker, period='max', interval='1d', auto_adjust=True)
        elif timeFrame == "5Y":
            stock = yf.download(ticker, period='5y', interval='1d', auto_adjust=True)
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

            if 'stock' not in locals() or stock is None:
                stock = yf.download(ticker, period='1d', interval='1m', auto_adjust=True)
        else:
            three_months = pd.Timestamp.today() - pd.DateOffset(months=3)
            M3 = three_months.date()
            todayD = str(date.today())
            stock = yf.download(ticker, start=M3, end=todayD, interval="1h", auto_adjust=True)

        if stock is None or stock.empty:
            print(f"No data found for {ticker}")
            return None
            
        if isinstance(stock.columns, pd.MultiIndex):
            stock.columns = stock.columns.get_level_values(0)

        try:
            import datetime as _dt
            is_intraday = any(idx.time() != _dt.time(0, 0) for idx in stock.index)
            if is_intraday:
                if stock.index.tz is None:
                    stock.index = stock.index.tz_localize('UTC')
                stock.index = stock.index.tz_convert('America/New_York')
                stock = stock.between_time('09:30', '16:00')
        except Exception as e:
            print(f"Time processing error: {e}")

        stock["SMA_20"] = stock["Close"].rolling(window=20).mean()
        stock["SMA_50"] = stock["Close"].rolling(window=50).mean()
        stock["SMA_200"] = stock["Close"].rolling(window=200).mean()
        
        stock["VWAP"] = ((stock["High"] + stock["Low"] + stock["Close"]) / 3 * stock["Volume"]).cumsum() / stock["Volume"].cumsum()
        fig = go.Figure()
        
        close_list = stock['Close'].tolist()
        date_strings = [str(d) for d in stock.index]
        close_list = stock['Close'].tolist()
        date_strings = [str(d) for d in stock.index]
        
        fig.add_trace(go.Scatter(
            x=date_strings, 
            y=close_list, 
            mode='lines', 
            name='Close Price', 
            line=dict(color='blue', width=2)
        ))
        
        if stock['SMA_20'].notna().any():
            sma20_data = stock['SMA_20'].dropna()
            sma20_dates = [str(d) for d in sma20_data.index]
            fig.add_trace(go.Scatter(
                x=sma20_dates, 
                y=sma20_data.tolist(), 
                mode='lines', 
                name='SMA 20', 
                line=dict(color='orange', width=1)
            ))
        
        if stock['SMA_50'].notna().any():
            sma50_data = stock['SMA_50'].dropna()
            sma50_dates = [str(d) for d in sma50_data.index]
            fig.add_trace(go.Scatter(
                x=sma50_dates, 
                y=sma50_data.tolist(), 
                mode='lines', 
                name='SMA 50', 
                line=dict(color='red', width=1)
            ))
        
        if stock['SMA_200'].notna().any():
            sma200_data = stock['SMA_200'].dropna()
            sma200_dates = [str(d) for d in sma200_data.index]
            fig.add_trace(go.Scatter(
                x=sma200_dates, 
                y=sma200_data.tolist(), 
                mode='lines', 
                name='SMA 200', 
                line=dict(color='purple', width=1)
            ))
        
        if stock['VWAP'].notna().any():
            vwap_data = stock['VWAP'].dropna()
            vwap_dates = [str(d) for d in vwap_data.index]
            fig.add_trace(go.Scatter(
                x=vwap_dates, 
                y=vwap_data.tolist(), 
                mode='lines', 
                name='VWAP', 
                line=dict(color='green', width=1, dash='dash')
            ))

        fig.update_layout(
            template='plotly_dark',
            xaxis_title='Date',
            yaxis_title='Price',
            legend_title='Legend',
            width=1000,
            height=600,
            xaxis=dict(type='date')
        )

        if timeFrame not in ['5Y', 'ALL']:
            try:
                fig.update_xaxes(
                    rangebreaks=[
                        dict(bounds=["sat", "mon"]),  
                        dict(bounds=[16, 9.5], pattern="hour")  
                    ]
                )
            except Exception:
                pass
        

        
        cache[ticker][timeFrame] = fig

        return fig