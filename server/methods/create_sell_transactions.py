import sqlite3
from pathlib import Path


current_dir = Path(__file__).resolve().parent

db_path = current_dir / "data" / "StockHistory.db"

conn = sqlite3.connect(str(db_path))

cursor = conn.cursor()

cursor.execute("""CREATE TABLE history (
        user_id text,
        ticker text,
        price_sold int,
        number_of_shares int,
        date_sold text
      )
""")

conn.commit()

conn.close()