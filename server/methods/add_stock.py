import sqlite3
from .trade import stockCheck, pData
from pathlib import Path
from datetime import datetime

def add_equity(user_id, ticker, number_of_shares, date_purchased):
      if is_valid_number(number_of_shares) and not(stockCheck(ticker)) and valid_date(date_purchased) and not (user_id == None) :
            current_dir = Path(__file__).resolve().parent

            db_path = current_dir / "data" / "portfolio.db"
            stock_db_path = current_dir / "data" / "portfolio.db"

            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            price_at_purchase = pData(ticker)["Current Price"]

            # Insert into portfolio
            query = """
                        INSERT INTO portfolio (user_id, ticker, price_at_purchase, number_of_shares, date_purchased)
                        VALUES (?, ?, ?, ?, ?)
                  """
            cursor.execute(query, (user_id, ticker, price_at_purchase, number_of_shares, date_purchased))

            # Insert into history
            query2 = """
                        INSERT INTO history (user_id, transaction_type, ticker, price_at_purchase, number_of_shares, date_purchased)
                        VALUES (?, ?, ?, ?, ?, ?)
                  """
            cursor.execute(query2, (user_id, 'buy', ticker, price_at_purchase, number_of_shares, date_purchased))

            print(f"{user_id} added {number_of_shares} of {ticker} to the database at a price of {price_at_purchase}")

            conn.commit()
            conn.close()

            return True, {"Result": "Successful Trade"}
      else:
            print("Unable to add Purchase")
            if not (valid_date(date_purchased)):
                 return False, {"Result": "Invalid Date"}
            if not (is_valid_number(number_of_shares)):
                 return False, {"Result": "Invalid Number of Shares"}
            return False, {"Result": "User not signed in"}
            

def valid_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False