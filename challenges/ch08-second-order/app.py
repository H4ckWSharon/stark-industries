"""
STARK INDUSTRIES SQL — Challenge 08: Second-Order SQL Injection (SQLite)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = "ch08_lab_key_not_secure"
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{s3c0nd_0rd3r_str1k3}")
DB = "/tmp/ch08.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS registrations (id INTEGER PRIMARY KEY, username TEXT, role TEXT);
        CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, clearance TEXT);
        CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM registrations;
        DELETE FROM employees;
        DELETE FROM secrets;
        INSERT INTO employees VALUES
            (1,'Tony Stark','R&D','ALPHA'),
            (2,'Pepper Potts','Executive','ALPHA'),
            (3,'Happy Hogan','Security','BETA');
    """)
    c.execute("INSERT OR REPLACE INTO secrets VALUES (8, ?)", (FLAG,))
    conn.commit()
    conn.close()


STYLE = """body{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;}
input{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:350px;font-family:monospace;outline:none;}
button{background:#00d4ff;color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;}
h2{color:#00d4ff;letter-spacing:2px;margin-bottom:16px;}
p{color:#8b949e;margin-bottom:16px;line-height:1.5;}
.card{background:#0d1117;border:1px solid #00d4ff33;border-radius:8px;padding:24px;max-width:700px;}
pre{background:#010409;border:1px solid #21262d;border-radius:6px;padding:16px;color:#8b949e;white-space:pre-wrap;}
.hint{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;max-width:700px;}
.msg{background:#0d2b0d;border:1px solid #00ff88;border-radius:6px;padding:14px;color:#00ff88;margin-bottom:16px;}
.tabs{display:flex;gap:8px;margin-bottom:24px;}
a.tab{padding:8px 20px;border-radius:6px;border:1px solid #30363d;color:#8b949e;text-decoration:none;font-size:.85rem;}
a.tab.active{border-color:#00d4ff;color:#00d4ff;background:#00d4ff11;}"""


@app.route("/")
def index():
    reg_user = session.get("reg_user", "")
    msg = f"<div class='msg'>Registered as: {reg_user}. Now view your profile!</div>" if reg_user else ""
    return f"""<!DOCTYPE html><html><head><title>Stark Ch08 - Second Order</title>
<style>{STYLE}</style></head><body>
<h2>&#9889; STARK INDUSTRIES - Challenge 08: Second-Order SQLi</h2>
<div class="tabs">
  <a href="/" class="tab active">[ REGISTER ]</a>
  <a href="/profile" class="tab">[ VIEW PROFILE ]</a>
</div>
<div class="card">
<p><b style="color:#00d4ff">MISSION:</b> Register with a crafted username. The INSERT is parameterized (safe).<br>
But your profile page uses your stored username in a new <em>vulnerable</em> query.<br>
<b>OBJECTIVE:</b> Trigger second-order injection via profile view.</p>
{msg}
<form method="POST" action="/register">
<label style="display:block;color:#8b949e;font-size:.8rem;margin-bottom:6px;">USERNAME:</label>
<input type="text" name="username" placeholder="Enter username"><br><br>
<button type="submit">[ REGISTER ]</button>
</form>
</div>
<div class="hint">&#128161; Try username: <code style="color:#ffd700;">' UNION SELECT flag,NULL,NULL FROM secrets WHERE id=8--</code><br>
Then go to View Profile to trigger the second-order execution.</div>
</body></html>"""


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # SAFE INSERT — parameterized
    c.execute("INSERT INTO registrations (username, role) VALUES (?, 'pending')", (username,))
    conn.commit()
    conn.close()
    session["reg_user"] = username
    return index()


@app.route("/profile")
def profile():
    stored_user = session.get("reg_user", "")
    records = []
    flag_found = False
    error = None

    if stored_user:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            # INTENTIONALLY VULNERABLE — uses stored data unsafely
            sql = f"SELECT name, department, clearance FROM employees WHERE name='{stored_user}'"
            c.execute(sql)
            rows = c.fetchall()
            records = [str(r) for r in rows]
            flag_found = any(FLAG in str(r) for r in rows)
            conn.close()
        except Exception as e:
            error = str(e)
            flag_found = FLAG in error

    records_html = ""
    for r in records:
        color = "#ffd700" if FLAG in r else "#8b949e"
        records_html += f'<pre style="color:{color};">{r}</pre>'
    if not records_html and not error:
        records_html = "<pre>No employee record found for this username.</pre>"
    if error:
        records_html = f'<pre style="color:#ff8080;">Error: {error}</pre>'

    success = f'<div class="msg">&#127942; SECOND-ORDER INJECTION TRIGGERED &mdash; FLAG CAPTURED!</div>' if flag_found else ""

    return f"""<!DOCTYPE html><html><head><title>Stark Ch08 - Profile</title>
<style>{STYLE}</style></head><body>
<h2>&#9889; STARK INDUSTRIES - Challenge 08: Profile Viewer</h2>
<div class="tabs">
  <a href="/" class="tab">[ REGISTER ]</a>
  <a href="/profile" class="tab active">[ VIEW PROFILE ]</a>
</div>
<div class="card">
<p style="color:#8b949e;font-size:.8rem;margin-bottom:8px;">Stored username: <span style="color:#ffd700;">{stored_user or "(not registered)"}</span></p>
<p style="color:#8b949e;font-size:.8rem;">Executing: <code style="color:#00d4ff;">SELECT name, department, clearance FROM employees WHERE name='{stored_user}'</code></p>
{success}
{records_html}
</div>
</body></html>"""


@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 8})


@app.route("/reset")
def reset():
    init_db()
    session.clear()
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
