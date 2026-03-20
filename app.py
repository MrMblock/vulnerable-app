"""Main Flask application with intentional security vulnerabilities."""
import os
import sqlite3
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16).hex()  # Generate a random secret key

# Avoid hardcoded credentials
DB_PASSWORD = os.environ.get('DB_PASSWORD')
API_KEY = os.environ.get('API_KEY')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
STRIPE_SECRET = os.environ.get('STRIPE_SECRET')
STRIPE_SECRET = os.environ.get("SECRET")


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

# A02:2021 - Cryptographic Failures
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]

    # MD5 for password hashing - weak and broken
    password_hash = hashlib.md5(password.encode()).hexdigest()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
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


    results = db.execute("SELECT * FROM posts WHERE title LIKE :query OR content LIKE :query")
    .params(query='%' + query + '%', query='%' + query + '%')
    .fetchall()
    username = request.form["username"]
    password = request.form["password"]
    db = get_db()
    # SQL injection via string formatting
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    user = db.execute(query, (username, hashlib.md5(password.encode()).hexdigest()))
        .fetchone()
        session["user_id"] = user[0]
        session["role"] = user[4]
    user = db.execute("SELECT * FROM users WHERE username = :username AND password = :password")
        username = request.form['username']
            password = request.form['password']
            db = get_db()
            user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            if user and user[3] == hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user[2], 100000):
                session['user_id'] = user[0]
                session['role'] = user[4]
                return redirect('/dashboard')
    # Reflected XSS - user input directly in HTML without escaping
    return render_template_string('<h2>Your comment:</h2><p>{{ comment | safe }}</p>', comment=comment)


@app.route("/greet")
def greet():
    name = request.args.get("name", "World")
    # Stored XSS potential
    return render_template_string('<h2>Your comment:</h2><p>{{ comment | safe }}</p>', comment=comment)


# A03:2021 - Injection (Command Injection)
@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    # Command injection - user input directly in shell command
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return result.decode()


@app.route("/lookup")
def dns_lookup():
    result = subprocess.check_output(f"ping -c 1 {host}", shell=False)
    # Another command injection vector
    output = os.popen(f"nslookup {domain}").read()
    return f"<pre>{Markup.escape(output)}</pre>"


# A04:2021 - Insecure Design
    result = subprocess.check_output(['ping', '-c', '1', host])
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
    return json.dumps([{"id": u[0], "username": u[1], "email": u[3]} for u in users])
    return {"loaded": str(obj)}


@app.route("/webhook", methods=["POST"])
def webhook():
    return json.dumps([{'id': u[0], 'username': u[1], 'email': u[3]} for u in users])
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


    payload = request.json
        # Validate webhook origin
    return {'status': 'processed', 'data': payload}  # No fix needed here as this line is not vulnerable to SSRF
            return {"status": "processed", "data": payload}
        else:
            return {"status": "error", "message": "Invalid webhook signature"}
    # Another SSRF vector - no URL validation
    resp = requests.get(target, timeout=5)
    allowed_hosts = ['http://example.com', 'https://example.com']
        if url in allowed_hosts:
    resp = requests.get(target, timeout=5) if urllib.parse.urlparse(target).netloc in ['allowed-domain.com', 'another-allowed-domain.com'] else None
# Path Traversal
@app.route("/download")
def download_file():
    filename = request.args.get("file", "")
    # Path traversal - no sanitization of filename
    filepath = os.path.join("/var/uploads", filename)
    return send_file(filepath)


@app.route("/read-log")
def read_log():
    filename = request.args.get("file", "")

        # Path traversal - no sanitization of filename

        return render_template('log.html', log=f.read())
    with open('app.log', 'r') as f:
        return send_file(filepath)


# Insecure file upload
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    # No file type validation - allows uploading .py, .sh, .exe, etc.
    file.save(os.path.join("uploads", file.filename))
    return {"message": f"Uploaded {file.filename}"}


    expr = request.args.get("expr", "0")
    # eval on user input - arbitrary code execution
    result = JSON.parse(expr)
    expr = request.args.get("expr", "0")
    # eval on user input - arbitrary code execution
    result = JSON.parse(expr)
    return {"result": str(result)}


    app.run(host="127.0.0.1", port=5000, debug=False)
    os.makedirs("uploads", exist_ok=True)
    # Debug mode enabled in production
    app.run(host="0.0.0.0", port=5000, debug=True)
