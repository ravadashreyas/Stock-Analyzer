from flask import Blueprint, request, jsonify, session
from flask_session import Session
from app import bcrypt
import sqlite3
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '..', 'methods', 'data', 'portfolio.db')
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id'] 
            session['username'] = user['username'] 
            return jsonify({"message": "Logged in successfully"})
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"error": "Server error during login"}), 500
    
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None) 
    return jsonify({"message": "Logged out"})

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    username = session.get('username')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401 
    return jsonify({"user_id": user_id, "username": username})

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '..', 'methods', 'data', 'portfolio.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "Username already taken"}), 400
            
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pw_hash))
        
        new_user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        session['user_id'] = new_user_id
        session['username'] = username
        
        return jsonify({"message": "Registered successfully"})
        
    except Exception as e:
        print(f"Register error: {e}")
        return jsonify({"error": "Server error"}), 500