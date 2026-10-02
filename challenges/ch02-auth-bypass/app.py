"""
STARK INDUSTRIES SQL — Challenge 02: Authentication Bypass
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string, session

app = Flask(__name__)
app.secret_key = "ch02_lab_session_key_not_secure"
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{auth_bypass_t0ny_st4rk}")
DB = "/tmp/ch02.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'employee',
            secret TEXT
        );
        DELETE FROM users;
    """)
    c.execute("""INSERT INTO users (username, password, role, secret) VALUES
        ('tony.stark',  'arc_reactor_pw_lab',   'admin',    ?),
        ('pepper.potts','ceo_password_lab',      'admin',    NULL),
        ('happy.hogan', 'security_pw_lab',       'employee', NULL),
        ('lab_dummy',   'test_password_lab',     'employee', NULL)
    """, (FLAG,))
    conn.commit()
    conn.close()


LOGIN_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Stark Industries — Employee Portal Login</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0a0a0f; color: #e0e0e0; font-family: 'Courier New', monospace; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.card { background: #0d1117; border: 1px solid #00d4ff44; border-radius: 12px; padding: 48px; width: 420px; box-shadow: 0 0 40px #00d4ff11; }
.logo { text-align: center; margin-bottom: 32px; }
.logo-text { color: #00d4ff; font-size: 1.3rem; letter-spacing: 3px; font-weight: bold; }
.logo-sub { color: #6e7681; font-size: 0.8rem; margin-top: 6px; letter-spacing: 2px; }
.mission { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 14px; margin-bottom: 24px; color: #8b949e; font-size: 0.82rem; line-height: 1.5; }
.mission strong { color: #00d4ff; }
label { color: #8b949e; font-size: 0.8rem; display: block; margin-bottom: 6px; letter-spacing: 1px; }
input { background: #010409; border: 1px solid #30363d; color: #00d4ff; padding: 12px; border-radius: 6px; width: 100%; font-family: 'Courier New', monospace; font-size: 0.95rem; outline: none; margin-bottom: 16px; }
input:focus { border-color: #00d4ff; }
button { width: 100%; background: linear-gradient(135deg, #00d4ff, #0066cc); color: #0a0a0f; border: none; padding: 14px; border-radius: 6px; font-weight: bold; font-size: 1rem; cursor: pointer; font-family: 'Courier New', monospace; letter-spacing: 1px; }
button:hover { opacity: 0.9; }
.error { background: #2d1b1b; border: 1px solid #ff2244; border-radius: 6px; padding: 12px; color: #ff8080; font-size: 0.85rem; margin-bottom: 16px; }
.warning { background: #1a1600; border: 1px solid #ffd70066; border-radius: 4px; padding: 8px 12px; color: #ffd700; font-size: 0.75rem; text-align: center; margin-top: 16px; }
</style>
</head>
<body>
<div class="card">
  <div class="logo">
    <div class="logo-text">⚡ STARK INDUSTRIES</div>
    <div class="logo-sub">EMPLOYEE PORTAL — CHALLENGE 02</div>
  </div>
  <div class="mission">
    <strong>MISSION:</strong> Bypass the login system and access the administrator account 
    (username: <code>tony.stark</code>) without knowing the password.<br><br>
    Retrieve the flag from the admin dashboard.
  </div>
  {% if error %}
  <div class="error">{{ error }}</div>
  {% endif %}
  <form method="POST" action="/login">
    <label>// USERNAME</label>
    <input type="text" name="username" placeholder="username" value="{{ username }}">
    <label>// PASSWORD</label>
    <input type="password" name="password" placeholder="••••••••">
    <button type="submit">[ AUTHENTICATE ]</button>
  </form>
  <div class="warning">⚠ INTENTIONALLY VULNERABLE LABORATORY — AUTHORIZED USE ONLY</div>
</div>
</body>
</html>"""

DASHBOARD_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Stark Industries — Admin Dashboard</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0a0a0f; color: #e0e0e0; font-family: 'Courier New', monospace; min-height: 100vh; }
.header { background: #0d1117; border-bottom: 1px solid #00d4ff33; padding: 16px 40px; display: flex; align-items: center; gap: 16px; }
.logo { color: #00d4ff; font-weight: bold; letter-spacing: 2px; }
.user-badge { background: #ffd70022; border: 1px solid #ffd70066; border-radius: 4px; padding: 4px 12px; color: #ffd700; font-size: 0.8rem; }
.container { max-width: 800px; margin: 60px auto; padding: 0 20px; }
.success-card { background: #0d2b0d; border: 2px solid #00ff88; border-radius: 12px; padding: 40px; text-align: center; }
.success-title { color: #00ff88; font-size: 1.4rem; margin-bottom: 16px; letter-spacing: 2px; }
.flag-container { background: #010409; border: 1px solid #ffd700; border-radius: 8px; padding: 20px; margin: 24px 0; }
.flag-label { color: #ffd700; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 8px; }
.flag { color: #ffd700; font-size: 1.2rem; font-weight: bold; letter-spacing: 1px; word-break: break-all; }
.user-info { color: #8b949e; font-size: 0.9rem; margin-top: 16px; }
.logout-btn { display: inline-block; margin-top: 24px; background: #ff224422; border: 1px solid #ff2244; color: #ff8080; padding: 10px 24px; border-radius: 6px; text-decoration: none; font-size: 0.85rem; }
</style>
</head>
<body>
<div class="header">
  <div class="logo">⚡ STARK INDUSTRIES ADMIN</div>
  <div class="user-badge">👤 {{ username }}</div>
  <div style="margin-left:auto;color:#00ff88;font-size:0.8rem;">● ACCESS GRANTED</div>
</div>
<div class="container">
  <div class="success-card">
    <div class="success-title">🏆 AUTHENTICATION BYPASS SUCCESSFUL</div>
    <p style="color:#8b949e;margin-bottom:20px;">You have gained unauthorized access to the Stark Industries administrator account.</p>
    <div class="flag-container">
      <div class="flag-label">// CAPTURED FLAG</div>
      <div class="flag">{{ flag }}</div>
    </div>
    <div class="user-info">
      Logged in as: <strong style="color:#00d4ff;">{{ username }}</strong> | Role: <strong style="color:#ffd700;">{{ role }}</strong>
    </div>
    <a href="/logout" class="logout-btn">[ LOGOUT ]</a>
  </div>
</div>
</body>
</html>"""


@app.route("/", methods=["GET"])
def index():
    if session.get("logged_in"):
        return render_template_string(DASHBOARD_PAGE,
            username=session.get("username", "unknown"),
            role=session.get("role", "unknown"),
            flag=FLAG)
    return render_template_string(LOGIN_PAGE, error=None, username="")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        # INTENTIONALLY VULNERABLE — direct string interpolation
        sql = f"SELECT id, username, role, secret FROM users WHERE username='{username}' AND password='{password}'"
        c.execute(sql)
        user = c.fetchone()
        conn.close()

        if user:
            session["logged_in"] = True
            session["username"] = user[1]
            session["role"] = user[2]
            return render_template_string(DASHBOARD_PAGE,
                username=user[1], role=user[2], flag=FLAG)
        else:
            return render_template_string(LOGIN_PAGE,
                error="Invalid credentials. Access denied.", username=username)
    except Exception as e:
        return render_template_string(LOGIN_PAGE,
            error=f"Database error: {str(e)}", username=username)


@app.route("/logout")
def logout():
    session.clear()
    return render_template_string(LOGIN_PAGE, error=None, username="")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 2})


@app.route("/reset")
def reset():
    init_db()
    session.clear()
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
