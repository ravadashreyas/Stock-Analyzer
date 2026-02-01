import sqlite3
from pathlib import Path


current_dir = Path(__file__).parent
db_path = current_dir.parent / "data" / "portfolio.db"
conn = sqlite3.connect(str(db_path))

cursor = conn.cursor()

cursor.execute("""CREATE TABLE portfolio (
        user_id text,
        stock_name text,
        ticker text,
        number_of_shares int,
        date_purchased text
      )
""")

conn.commit()

conn.close()