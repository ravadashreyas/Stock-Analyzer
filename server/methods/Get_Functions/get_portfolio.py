import sqlite3
from pathlib import Path
from methods.trade import pData
import time
import threading

cache = {}

def clear_cache_periodically():
    while True:
        time.sleep(300)  
        cache.clear()    
        print("Portfolio Cache cleared automatically.")

t = threading.Thread(target=clear_cache_periodically, daemon=True)
t.start()

def get_user_holdings(user_id):
    if user_id in cache:
        print("Using Portfolio Cache")
        return cache[user_id]
    else:
        current_dir = Path(__file__).resolve().parent

        db_path = current_dir.parent / "data" / "portfolio.db"

        conn = sqlite3.connect(str(db_path))
            
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
            
        query = "SELECT ticker, number_of_shares, price_at_purchase, date_purchased FROM portfolio WHERE user_id = ?"
        cursor.execute(query, (user_id,))
            
        rows = cursor.fetchall()

        conn.close()
            
        results = []
        for row in rows:
            stock_data = pData(row["ticker"])
            current_price = float(stock_data["Current Price"]) 
            purchase_price = float(row["price_at_purchase"])
            shares = float(row["number_of_shares"])

            total_cost = shares * purchase_price
            current_cost = shares * current_price
            gain_loss = (current_price - purchase_price) * shares
            stock_name = stock_data["Company Name"]

            
            results.append({
                "date_of_purchase": row["date_purchased"],
                "stock_name": stock_name,
                "stock_ticker": row["ticker"],
                "price_at_purchase": purchase_price,
                "number_of_shares": shares,
                "current_price": current_price,
                "total_cost": total_cost,
                "current_value": current_cost,
                "gain_loss": gain_loss,
                "percent_gain_loss": (gain_loss / total_cost) * 100 if total_cost != 0 else 0
            })
        cache[user_id] = results  
        return results



