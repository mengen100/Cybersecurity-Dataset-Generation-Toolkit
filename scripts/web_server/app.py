from flask import Flask, request, jsonify
from urllib.parse import urlparse
import mysql.connector
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_db_connection():
    url = urlparse(os.environ['DATABASE_URL'])
    logger.debug(f"Parsed DATABASE_URL - hostname: {url.hostname}, username: {url.username}, database: {url.path[1:]}")
    
    try:
        conn = mysql.connector.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:],
            connect_timeout=10
        )
        logger.debug("Database connection successful")
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Database connection failed: {err}")
        logger.error(f"Error code: {err.errno}")
        logger.error(f"SQL State: {err.sqlstate}")
        raise

@app.route('/')
def home():
    return "Welcome to the Web app!"

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/profile')
def profile():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Also vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"user": user}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/search')
def search():
    q = request.args.get('q')
    return jsonify({"results": f"Search results for: {q}"}), 200

@app.route('/about')
def about():
    return "About our vulnerable web app"

@app.route('/contact')
def contact():
    return "Contact information for our vulnerable web app"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)