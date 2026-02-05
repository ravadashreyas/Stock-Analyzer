import sqlite3
from .trade import stockCheck, pData
from pathlib import Path

def add_equity(user_id, ticker, number_of_shares, date_purchased):
      if is_valid_number(number_of_shares) and not(stockCheck(ticker)) and valid_date(date_purchased)  :
            current_dir = Path(__file__).resolve().parent

            db_path = current_dir / "data" / "portfolio.db"

            conn = sqlite3.connect(str(db_path))

            cursor = conn.cursor()

            price_at_purchase = pData(ticker)["Current Price"]

            query = """
                        INSERT INTO portfolio (user_id, ticker, price_at_purchase, number_of_shares, date_purchased)
                        VALUES (?, ?, ?, ?, ?)
                  """

            cursor.execute(query, (user_id, ticker, price_at_purchase, number_of_shares, date_purchased))



            print(f"{user_id} added {number_of_shares} of {ticker} to the database at a price of {price_at_purchase}")

            conn.commit()

            conn.close()

            return True
      else:
            print("Unable to add Purchase")
            return False
            

def valid_date(date):
      return True

def is_valid_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False