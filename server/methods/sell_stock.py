import sqlite3
from .trade import stockCheck, pData
from pathlib import Path
from datetime import datetime

def sell_equity(user_id, ticker, number_of_shares):
      if is_valid_number(number_of_shares) and not(stockCheck(ticker)) and not (user_id == None) :
            current_dir = Path(__file__).resolve().parent

            db_path = current_dir / "data" / "portfolio.db"
            stock_db_path = current_dir / "data" / "portfolio.db"

            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            price_at_purchase = pData(ticker)["Current Price"]

            query_shares = """SELECT SUM(number_of_shares) FROM portfolio WHERE user_id = ? AND ticker = ?
            """
            cursor.execute(query_shares, (user_id, ticker))
            total_shares = cursor.fetchone()[0]

            if not (total_shares is None):
                total_shares = float(total_shares)
            else:
                return False, {"Result": f"User does not have this many shares of {ticker}"}
            number_of_shares = float(number_of_shares)

            if total_shares == number_of_shares:
                query_delete = """
                            DELETE FROM portfolio WHERE user_id = ? AND ticker = ?
                    """
                cursor.execute(query_delete, (user_id, ticker))
            elif total_shares > number_of_shares:
                query_change = """
                            UPDATE portfolio 
                            SET number_of_shares = ?
                            WHERE user_id = ? AND ticker = ?
                    """
                cursor.execute(query_change, ((total_shares - number_of_shares), user_id, ticker))
            else:
                 return False, {"Result": "User does not have this many shares of {ticker}"}
            
            query2 = """
                        INSERT INTO history (user_id, transaction_type, ticker, price_at_purchase, number_of_shares)
                        VALUES (?, ?, ?, ?, ?)
                  """
            cursor.execute(query2, (user_id, 'sell', ticker, price_at_purchase, number_of_shares))

            print(f"{user_id} sold {number_of_shares} of {ticker} to the database at a price of {price_at_purchase}")

            conn.commit()
            conn.close()

            return True, {"Result": "Successful Trade"}
      else:
            print("Unable to sell Purchase")
            if not(stockCheck(ticker)):
                 return False, {"Result": "Invalid Ticker"}
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