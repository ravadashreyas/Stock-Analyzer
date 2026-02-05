import sqlite3
from flask import Flask
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)


current_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_dir, 'methods', 'data', 'portfolio.db')

def create_users_table():
    print(f"Connecting to database at: {DB_PATH}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Checking users table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    print("Checking history table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        transaction_type TEXT,
        ticker TEXT,
        price_at_purchase REAL,
        number_of_shares REAL,
        date_purchased TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
    print("Tables checked/created successfully.")

def add_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print(f"User '{username}' already exists.")
        conn.close()
        return

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                   (username, pw_hash))
    
    conn.commit()
    conn.close()
    print(f"User '{username}' created with encrypted password.")

if __name__ == "__main__":
    create_users_table()
    
    add_user("admin", "password")
    
