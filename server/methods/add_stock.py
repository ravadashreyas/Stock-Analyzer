import sqlite3
from .trade import stockCheck
from pathlib import Path

def add_equity(user_id, ticker, number_of_shares, date_purchased):
      if is_valid_number(number_of_shares) and not(stockCheck(ticker)) and valid_date(date_purchased)  :
            current_dir = Path(__file__).resolve().parent

            db_path = current_dir / "data" / "portfolio.db"

            conn = sqlite3.connect(str(db_path))

            cursor = conn.cursor()

            query = """
                        INSERT INTO portfolio (user_id, ticker, number_of_shares, date_purchased)
                        VALUES (?, ?, ?, ?)
                  """

            cursor.execute(query, (user_id, ticker, number_of_shares, date_purchased))



            print(f"{user_id} added {number_of_shares} of {ticker} to the database")

            conn.commit()

            conn.close()

            return True
      else:
            print("False")
            print(is_valid_number(number_of_shares))
            print(not(stockCheck(ticker)))
            print(valid_date(date_purchased))
            return False
            

def valid_date(date):
      return True

def is_valid_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False