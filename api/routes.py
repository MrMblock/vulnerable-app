"""API routes with various injection vulnerabilities."""
import sqlite3
import yaml
import xml.etree.ElementTree as ET
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
    db = get_db()
    # Unsanitized column name and order direction
    query = f"SELECT * FROM users ORDER BY {sort_by} {order}"
    users = db.execute(query).fetchall()
    return jsonify(users)


@api.route("/api/users/<username>")
def get_user(username):
    db = get_db()
    # SQL injection via string concatenation
    user = db.execute(
        "SELECT * FROM users WHERE username = '" + username + "'"
    ).fetchone()
    if user:
        return jsonify({"id": user[0], "username": user[1], "email": user[3]})
    return jsonify({"error": "Not found"}), 404


@api.route("/api/posts", methods=["POST"])
def create_post():
    data = request.json
    db = get_db()
    # SQL injection via format string
    db.execute(
        "INSERT INTO posts (title, content, author_id) VALUES ('%s', '%s', %s)"
        % (data["title"], data["content"], data["author_id"])
    )
    db.commit()
    return jsonify({"status": "created"}), 201


# XXE - XML External Entity
@api.route("/api/import-xml", methods=["POST"])
def import_xml():
    xml_data = request.data
    # Vulnerable XML parser - allows external entities
    tree = ET.fromstring(xml_data)
    return jsonify({"root_tag": tree.tag, "text": tree.text})


# YAML deserialization
@api.route("/api/import-config", methods=["POST"])
def import_config():
    yaml_data = request.data.decode()
    # Unsafe YAML loading - allows arbitrary code execution
    config = yaml.load(yaml_data, Loader=yaml.Loader)
    return jsonify({"config": str(config)})


# Mass assignment
@api.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    db = get_db()
    # Allows updating ANY field including role - mass assignment
    for key, value in data.items():
        db.execute(
            f"UPDATE users SET {key} = ? WHERE id = ?", (value, user_id)
        )
    db.commit()
    return jsonify({"status": "updated"})


# Broken authentication
@api.route("/api/admin/users", methods=["DELETE"])
def delete_all_users():
    # No authentication check, no CSRF protection
    db = get_db()
    db.execute("DELETE FROM users")
    db.commit()
    return jsonify({"status": "all users deleted"})
