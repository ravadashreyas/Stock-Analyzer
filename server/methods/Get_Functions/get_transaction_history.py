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
        print("Transaction Cache cleared automatically.")

t = threading.Thread(target=clear_cache_periodically, daemon=True)
t.start()

def get_trade_db(user_id):
    if user_id in cache:
        print("Using Transaction Cache")
        return cache[user_id]
    else:
        current_dir = Path(__file__).resolve().parent

        db_path = current_dir.parent / "data" / "portfolio.db"

        conn = sqlite3.connect(str(db_path))
            
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
            
        query = "SELECT ticker, number_of_shares, transaction_type, price_at_purchase, date_purchased FROM history WHERE user_id = ?"
        cursor.execute(query, (user_id,))
            
        rows = cursor.fetchall()

        conn.close()
            
        results = []
        for row in rows:
            stock_data = pData(row["ticker"])
            purchase_price = float(row["price_at_purchase"])
            shares = float(row["number_of_shares"])
            stock_name = stock_data["Company Name"]
            total_cost = (shares * purchase_price) if row["transaction_type"] == "sell" else (-1 * shares * purchase_price)

            
            results.append({
                "date_of_purchase": row["date_purchased"],
                "stock_name": stock_name,
                "stock_ticker": row["ticker"],
                "action": row["transaction_type"],
                "price_at_purchase": purchase_price,
                "number_of_shares": shares,
                "total_cost" : total_cost
            })
        cache[user_id] = results  
        return results



