from flask import Flask, jsonify, request
import uuid
from datetime import datetime, timedelta
from database import Connection
import sqlite3


app = Flask(__name__)
cinema_db = Connection("auth.db")


@app.route("/")
def home():
    return "Running"


@app.route("/register", methods=["POST"])
def register():
    user_login = request.form.get("login")
    password = request.form.get("password")
    if None in (login, password):
        return "login or password is missing", 400
    with Connection() as c:
        try:
            c.execute("INSERT INTO users(login, password) VALUES (?,?)", (user_login, password))
        except sqlite3.IntegrityError:
            return "Login is already used", 409
        inserted_id = c.lastrowid
        token = str(uuid.uuid4())
        last_auth = datetime.now().strftime("%H:%M %d-%m-%Y")
        c.execute("UPDATE users SET last_auth = ?, token = ? WHERE id = ?", (last_auth, token, inserted_id))
    return token, 201


@app.route("/login", methods=["POST"])
def login():
    formatted_now = datetime.now().strftime("%H:%M %d-%m-%Y")
    user_login = request.form.get("login")
    password = request.form.get("password")
    if None not in (user_login, password):
        with Connection() as c:
            rows = c.execute("SELECT id FROM users WHERE login = ? AND password = ?", (user_login, password)).fetchall()
            if rows:
                token = str(uuid.uuid4())
                c.execute("UPDATE users SET token = ?, last_auth = ? WHERE id = ?", (token, formatted_now, rows[0][0]))
                return token, 200


@app.route("/get_user", methods=["POST"])
def get_user():
    now = datetime.now()
    formatted_now = now.strftime("%H:%M %d-%m-%Y")
    token = request.form.get("token")
    if token is not None:
        with Connection() as c:
            rows = c.execute("SELECT id, last_auth FROM users WHERE token = ?", (token, )).fetchall()
            if rows and now - datetime.strptime(rows[0][1], "%H:%M %d-%m-%Y") < timedelta(hours=24):
                c.execute("UPDATE users SET last_auth = ? WHERE id = ?", (formatted_now, rows[0][0]))
                return jsonify({"id": rows[0][0]}), 200
    return "Failed to log in", 401


@app.route("/list_users", methods=["GET"])
def list_users():
    with Connection() as c:
        rows = c.execute("SELECT id, login, last_auth FROM users").fetchall()
        headers = [x[0] for x in c.description]
    return jsonify([dict(zip(headers, row)) for row in rows])


if __name__ == '__main__':
    app.run()
