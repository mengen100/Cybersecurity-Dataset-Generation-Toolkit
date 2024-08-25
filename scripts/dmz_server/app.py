from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Web app!"

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/vulnerable_endpoint', methods=['POST'])
def vulnerable_endpoint():
    data = request.json
    if 'command' in data:
        try:
            output = subprocess.check_output(data['command'], shell=True, stderr=subprocess.STDOUT)
            return jsonify({"output": output.decode()})
        except subprocess.CalledProcessError as e:
            return jsonify({"error": e.output.decode()}), 500
    return jsonify({"error": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)