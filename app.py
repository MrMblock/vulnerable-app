"""Main Flask application with intentional security vulnerabilities."""
import os
import sqlite3
import pickle
import subprocess
import hashlib
import requests
from flask import Flask, request, render_template_string, redirect, session, send_file

app = Flask(__name__)
app.secret_key = "super_secret_key_12345"  # Hardcoded secret key

# Hardcoded credentials
DB_PASSWORD = "admin123"
API_KEY = "openai_api_abc123def456ghi789jkl012mno345pqr678stu901vwx234"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_SECRET = "stripe_live_key_4eC39HqLyjWDarjtT1zdp7dc"


def get_db():
    db = sqlite3.connect("app.db")
    db.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        email TEXT,
        role TEXT DEFAULT 'user'
    )""")
    db.execute("""CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT,
        author_id INTEGER
    )""")
    return db


# A01:2021 - Broken Access Control
@app.route("/admin")
def admin_panel():
    # No authentication check - anyone can access admin
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template_string("""
        <h1>Admin Panel</h1>
        <table>
        {% for user in users %}
            <tr><td>{{ user[1] }}</td><td>{{ user[2] }}</td><td>{{ user[4] }}</td></tr>
        {% endfor %}
        </table>
    """, users=users)


@app.route("/user/<int:user_id>/profile")
def user_profile(user_id):
    # IDOR - No check that logged-in user matches requested user_id
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return {"id": user[0], "username": user[1], "password": user[2], "email": user[3]}


# A02:2021 - Cryptographic Failures
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]

    # MD5 for password hashing - weak and broken
# A02:2021 - Cryptographic Failures
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]

    # sha256 for password hashing - weak and broken
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    db = get_db()
    db.execute(
        "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
        (username, password_hash, email),
    )
    db.commit()
    return redirect("/login")

    db = get_db()
    db.execute(
        "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
        (username, password_hash, email),
    )
    db.commit()
    return redirect("/login")


# A03:2021 - Injection (SQL Injection)
@app.route("/search")
def search():
    query = request.args.get("q", "")
    db = get_db()
    # Direct string concatenation - SQL injection
    results = db.execute(
        "SELECT * FROM posts WHERE title LIKE '%" + query + "%' OR content LIKE '%" + query + "%'"
    ).fetchall()
    return {"results": results}


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    db = get_db()
    # SQL injection via string formatting
    user = db.execute(
        f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashlib.md5(password.encode()).hexdigest()}'"
    ).fetchone()
    if user:
        session["user_id"] = user[0]
        session["role"] = user[4]
        return redirect("/dashboard")
    return "Login failed", 401


# A03:2021 - Injection (XSS)
@app.route("/comment", methods=["POST"])
def add_comment():
    comment = request.form["comment"]
    # Reflected XSS - user input directly in HTML without escaping
    return render_template_string("<h2>Your comment:</h2><p>" + comment + "</p>")


@app.route("/greet")
def greet():
    name = request.args.get("name", "World")
    # Stored XSS potential
    return f"<html><body><h1>Hello {name}!</h1></body></html>"


# A03:2021 - Injection (Command Injection)
@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    # Command injection - user input directly in shell command
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return result.decode()


@app.route("/lookup")
def dns_lookup():
    domain = request.args.get("domain", "")
    # Another command injection vector
    output = os.popen(f"nslookup {domain}").read()
    return f"<pre>{output}</pre>"


# A04:2021 - Insecure Design
@app.route("/reset-password", methods=["POST"])
def reset_password():
    email = request.form["email"]
    # Predictable reset token - just MD5 of email
    token = hashlib.md5(email.encode()).hexdigest()
    # In real app would send email, here just return it
    return {"reset_token": token, "reset_url": f"/reset?token={token}"}


# A05:2021 - Security Misconfiguration
@app.route("/debug")
def debug_info():
    # Exposes sensitive system information
    return {
        "env": dict(os.environ),
        "python_path": os.sys.path,
        "cwd": os.getcwd(),
        "db_password": DB_PASSWORD,
        "api_key": API_KEY,
    }


# A07:2021 - Identification and Authentication Failures
@app.route("/api/data")
def api_data():
    # No authentication required for sensitive data
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    return {"users": [{"id": u[0], "username": u[1], "email": u[3]} for u in users]}


# A08:2021 - Software and Data Integrity Failures
@app.route("/load-session")
def load_session():
    data = request.args.get("data", "")
    # Insecure deserialization - pickle from user input
    obj = pickle.loads(bytes.fromhex(data))
    return {"loaded": str(obj)}


@app.route("/webhook", methods=["POST"])
def webhook():
    # No signature verification on webhook
    payload = request.json
    # Process webhook without verifying origin
    return {"status": "processed", "data": payload}


# A10:2021 - Server-Side Request Forgery (SSRF)
@app.route("/fetch")
def fetch_url():
    url = request.args.get("url", "")
    # SSRF - fetches any URL including internal services
    response = requests.get(url)
    return response.text


@app.route("/proxy")
def proxy():
    target = request.args.get("target", "")
    # Another SSRF vector - no URL validation
    resp = requests.get(target, timeout=5)
    return {"status": resp.status_code, "body": resp.text[:1000]}


# Path Traversal
@app.route("/download")
def download_file():
    filename = request.args.get("file", "")
    # Path traversal - no sanitization of filename
    filepath = os.path.join("/var/uploads", filename)
    return send_file(filepath)


@app.route("/read-log")
def read_log():
    logfile = request.args.get("path", "app.log")
    # Direct file read without validation
    with open(logfile, "r") as f:
        return f"<pre>{f.read()}</pre>"


# Insecure file upload
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    # No file type validation - allows uploading .py, .sh, .exe, etc.
    file.save(os.path.join("uploads", file.filename))
    return {"message": f"Uploaded {file.filename}"}


# Eval injection
@app.route("/calc")
def calculator():
    expr = request.args.get("expr", "0")
    # eval on user input - arbitrary code execution
    result = eval(expr)
    return {"result": str(result)}


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    # Debug mode enabled in production
    app.run(host="0.0.0.0", port=5000, debug=True)
