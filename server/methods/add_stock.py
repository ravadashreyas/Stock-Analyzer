import sqlite3
from pathlib import Path


current_dir = Path(__file__).parent
db_path = current_dir.parent / "data" / "portfolio.db"
conn = sqlite3.connect(str(db_path))

cursor = conn.cursor()

cursor.execute("""INSERT INTO portfolio.db VALUES(
        
      )
""")

conn.commit()

conn.close()