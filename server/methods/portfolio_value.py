import sqlite3
from pathlib import Path
import time
import threading
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import json

cache = {}

def clear_cache_periodically():
    while True:
        time.sleep(300)  
        cache.clear()    
        print("Portfolio Plot Cache cleared automatically.")

t = threading.Thread(target=clear_cache_periodically, daemon=True)
t.start()

TIMEFRAME_MAP = {
    '1D': ('5d', '1h'),      
    '5D': ('5d', '1d'),
    '1M': ('1mo', '1d'),
    '3M': ('3mo', '1d'),
    '6M': ('6mo', '1d'),
    'YTD': ('ytd', '1d'),
    '1Y': ('1y', '1d'),
    '5Y': ('5y', '1wk'),
    'ALL': ('max', '1wk'),
}

def get_user_equity(user_id, time_frame='3M'):
    cache_key = f"{user_id}_{time_frame}"
    
    if cache_key in cache:
        print(f"Using Portfolio Plot Cache for {cache_key}")
        return cache[cache_key]
    
    current_dir = Path(__file__).resolve().parent
    db_path = current_dir / "data" / "portfolio.db"

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
        
    query = "SELECT ticker, number_of_shares, date_purchased FROM portfolio WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.close()
        
    portfolio = []
    for row in rows:
        portfolio.append({'ticker': row["ticker"], 'shares': float(row["number_of_shares"]), 'buy_date': row["date_purchased"]})

    if not portfolio:
        return {"error": "No holdings found"}

    tickers = [item['ticker'] for item in portfolio]
    
    yf_period, yf_interval = TIMEFRAME_MAP.get(time_frame.upper(), ('3mo', '1d'))

    df = yf.download(tickers, period=yf_period, interval=yf_interval)['Close']
    
    if df.empty:
        return {"error": "No price data available for this time frame"}
    
    if time_frame.upper() == '1D':
        df.index = pd.to_datetime(df.index)
        last_date = df.index[-1].date()
        df = df[df.index.date == last_date]
        if df.empty:
            return {"error": "No intraday data available"}
    
    df.index = pd.to_datetime(df.index) 

    position_values = pd.DataFrame(index=df.index)

    for item in portfolio:
        ticker = item['ticker']
        shares = item['shares']
        buy_date = pd.to_datetime(item['buy_date'])
        
        if df.index.tz is not None:
            buy_date = buy_date.tz_localize(df.index.tz)
        
        if isinstance(df, pd.Series):
            ticker_prices = df
        else:
            ticker_prices = df[ticker] if ticker in df.columns else df
        
        raw_value = ticker_prices * shares
        
        raw_value.loc[raw_value.index < buy_date] = 0
        
        position_values[ticker] = raw_value

    position_values['Total Portfolio'] = position_values.sum(axis=1)
    
    total_values = position_values['Total Portfolio']
    y_min = total_values.min()
    y_max = total_values.max()
    y_range = y_max - y_min
    padding = y_range * 0.15 if y_range > 0 else y_max * 0.15
    y_axis_min = max(0, y_min - padding)
    y_axis_max = y_max + padding
    
    current_value = total_values.iloc[-1]
    start_value = total_values[total_values > 0].iloc[0] if (total_values > 0).any() else current_value
    pct_change = ((current_value - start_value) / start_value * 100) if start_value > 0 else 0
    pct_sign = '+' if pct_change >= 0 else ''

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=position_values.index, 
        y=position_values['Total Portfolio'], 
        mode='lines', 
        name='Total Value',
        fill='tozeroy', 
        line=dict(color='#00C805', width=3)
    ))

    fig.update_layout(
        title=f'Portfolio Value: ${current_value:,.2f} ({pct_sign}{pct_change:.2f}%)',
        yaxis_title='Value ($)',
        template='plotly_dark',
        yaxis=dict(range=[y_axis_min, y_axis_max])
    )
    fig_json = json.loads(fig.to_json())

    cache[cache_key] = fig_json 
    return fig_json
