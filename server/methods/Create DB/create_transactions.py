import sqlite3
from pathlib import Path


current_dir = Path(__file__).resolve().parent

db_path = current_dir.parent / "data" / "StockHistory.db"

conn = sqlite3.connect(str(db_path))

cursor = conn.cursor()

cursor.execute("""CREATE TABLE history (
        user_id text,
        action text,
        ticker text,
        price_at_action int,
        number_of_shares int,
        date_purchased text
      )
""")

conn.commit()

conn.close()