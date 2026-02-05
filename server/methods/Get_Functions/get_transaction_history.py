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
    if cache:
        print("Using Portfolio Cache")
        return cache[user_id]
    else:
        current_dir = Path(__file__).resolve().parent

        db_path = current_dir / "data" / "StockHistory.db"

        conn = sqlite3.connect(str(db_path))
            
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
            
        query = "SELECT ticker, number_of_shares, action, price_at_action, date_purchased FROM history WHERE user_id = ?"
        cursor.execute(query, (user_id,))
            
        rows = cursor.fetchall()

        conn.close()
            
        results = []
        for row in rows:
            stock_data = pData(row["ticker"])
            purchase_price = float(row["price_at_action"])
            shares = float(row["number_of_shares"])

            total_cost = shares * purchase_price
            stock_name = stock_data["Company Name"]

            
            results.append({
                "date_of_purchase": row["date_purchased"],
                "stock_name": stock_name,
                "stock_ticker": row["ticker"],
                "action": row["action"],
                "price_at_action": purchase_price,
                "number_of_shares": shares,
                "total_cost": total_cost,
            })
        cache[user_id] = results  
        return results



