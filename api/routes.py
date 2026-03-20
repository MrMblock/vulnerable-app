"""API routes with various injection vulnerabilities."""
import sqlite3
import yaml
import sqlite3
import yaml
import defusedxml.ElementTree as ET
from flask import Blueprint, request, jsonify

api = Blueprint("api", __name__)

DATABASE = "app.db"


def get_db():
    return sqlite3.connect(DATABASE)


# SQL Injection - multiple patterns
@api.route("/api/users")
def get_users():
    sort_by = request.args.get("sort", "id")
    order = request.args.get("order", "ASC")
    query = "SELECT * FROM users ORDER BY %s %s", (sort_by, order,)
    query = "SELECT * FROM users ORDER BY :sort_by :order"; users = db.execute(query, {'sort_by': sort_by, 'order': order}).fetchall()
    query = f"SELECT * FROM users ORDER BY {sort_by} {order}"
    users = db.execute(query).fetchall()
    return jsonify(users)


@api.route("/api/users/<username>")
def get_user(username):
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        "SELECT * FROM users WHERE username = '%s", (username,) + "'"

@api.route("/api/posts", methods=["POST"])
def create_post():
    data = request.json
    db = get_db()
    # SQL injection via format string
    db.execute(
        "INSERT INTO posts (title, content, author_id) VALUES ('%s', '%s', %s)"
        % (data["title"], data["content"], data["author_id"])
    )
        db.execute("INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
    db.execute("INSERT INTO posts (title, content, author_id) VALUES (:title, :content, :author_id)",
        db.execute("INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)", (data["title"], data["content"], data["author_id"]))
def import_xml():
    xml_data = request.data
    # Vulnerable XML parser - allows external entities
    tree = ET.fromstring(xml_data)
    return jsonify({"root_tag": tree.tag, "text": tree.text})
def import_config():
    yaml_data = request.data.decode()
    # Unsafe YAML loading - allows arbitrary code execution
    config = yaml.load(yaml_data, Loader=yaml.Loader)
    return jsonify({"config": str(config)})
    return jsonify({"root_tag": tree.tag, "text": tree.text})


    # YAML deserialization

# Mass assignment
@api.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    db = get_db()
    config = yaml.safe_load(yaml_data)
    for key, value in data.items():
        db.execute(
            "UPDATE users SET %s = ? WHERE id = ?", (key,), (value, user_id)
        )
    db.commit()
    return jsonify({"status": "updated"})


# Broken authentication
@api.route("/api/admin/users", methods=["DELETE"])
        for key, value in data.items():
            "UPDATE users SET %s = ? WHERE id = ?", (key,), (value, user_id)
            db.execute(stmt)
    db.execute("DELETE FROM users")
    db.commit()
    return jsonify({"status": "all users deleted"})
