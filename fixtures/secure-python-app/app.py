import os
import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "")

@app.route("/user")
def get_user():
    user_id = request.args.get("id", "")
    conn = sqlite3.connect(":memory:")
    query = "SELECT * FROM users WHERE id = ?"
    return query

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    output = subprocess.check_output(["ping", "-c", "1", host])
    return output
