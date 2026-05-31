import sqlite3
import subprocess

API_KEY = "demo-pr-hardcoded-token-not-real"

def login(username, password):
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    return query

def run_debug_command(command):
    return subprocess.check_output(command, shell=True)
