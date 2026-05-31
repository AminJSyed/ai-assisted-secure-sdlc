#!/usr/bin/env bash
set -euo pipefail

BRANCH_NAME="demo/insecure-pr-review"

git checkout -b "${BRANCH_NAME}" 2>/dev/null || git checkout "${BRANCH_NAME}"

mkdir -p demo-pr

cat > demo-pr/unsafe_login.py <<'PY'
import sqlite3
import subprocess

API_KEY = "demo-pr-hardcoded-token-not-real"

def login(username, password):
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    return query

def run_debug_command(command):
    return subprocess.check_output(command, shell=True)
PY

git add demo-pr/unsafe_login.py
git commit -m "Add demo insecure PR change" || true

echo ""
echo "Demo branch ready: ${BRANCH_NAME}"
echo ""
echo "Push it with:"
echo "git push -u origin ${BRANCH_NAME}"
echo ""
echo "Then create a pull request into main on GitHub."
