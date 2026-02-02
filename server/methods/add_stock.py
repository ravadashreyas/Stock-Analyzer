import sqlite3
from pathlib import Path

def add_equity(user_id, ticker, number_of_shares, date_purchased):
      current_dir = Path(__file__).parent
      db_path = "data" / "portfolio.db"
      conn = sqlite3.connect(str(db_path))

      cursor = conn.cursor()

      cursor.execute("""INSERT INTO portfolio.db VALUES(
            
            )
      """)

      print(f"{user_id} added {number_of_shares} of {ticker} to the database")

      conn.commit()

      conn.close()