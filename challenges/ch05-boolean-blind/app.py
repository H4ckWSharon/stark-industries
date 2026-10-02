"""
STARK INDUSTRIES SQL — Challenge 05: Boolean-Based Blind SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{bl1nd_b00l_hunt3r}")
DB = "/tmp/ch05.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT);
        CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM users;
        DELETE FROM secrets;
        INSERT INTO users VALUES (1, 'tony.stark'), (2, 'pepper.potts'), (3, 'happy.hogan');
    """)
    c.execute("INSERT OR REPLACE INTO secrets VALUES (5, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch05 - Boolean Blind</title>
<style>
body { background:#0a0a0f; color:#e0e0e0; font-family:monospace; padding:40px; }
input { background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px; border-radius:6px; width:350px; font-family:monospace; outline:none; }
button { background:#00d4ff; color:#000; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:8px; }
h2 { color:#00d4ff; letter-spacing:2px; margin-bottom:16px; }
p { color:#8b949e; margin-bottom:16px; line-height:1.5; }
.hint { background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; }
.true-resp { background:#0d2b0d; border:1px solid #00ff88; padding:16px; border-radius:6px; color:#00ff88; margin-top:16px; }
.false-resp { background:#2d1b1b; border:1px solid #ff2244; padding:16px; border-radius:6px; color:#ff8080; margin-top:16px; }
</style></head>
<body>
<h2>⚡ STARK INDUSTRIES — Challenge 05: Boolean-Based Blind SQLi</h2>
<p><b style="color:#00d4ff">MISSION:</b> The app shows only USER FOUND or USER NOT FOUND.<br>
Use boolean conditions with SUBSTR() to extract the flag character by character.<br>
<b>OBJECTIVE:</b> Infer the flag from the secrets table (id=5).</p>
<form method="GET">
<input type="text" name="name" value="{{ name }}" placeholder="Enter username">
<button type="submit">[ LOOKUP ]</button>
</form>
{% if name %}
  {% if found %}
  <div class="true-resp">✓ USER FOUND — Condition evaluated TRUE</div>
  {% else %}
  <div class="false-resp">✗ USER NOT FOUND — Condition evaluated FALSE</div>
  {% endif %}
{% endif %}
<div class="hint">
💡 Try: <code style="color:#ffd700;">tony.stark' AND SUBSTR((SELECT flag FROM secrets WHERE id=5),1,1)='S'--</code>
</div>
</body></html>"""

@app.route("/", methods=["GET"])
def index():
    name = request.args.get("name", "")
    found = False
    if name:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute(f"SELECT id FROM users WHERE username='{name}'")
            found = c.fetchone() is not None
            conn.close()
        except:
            found = False
    return render_template_string(PAGE, name=name, found=found)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 5})

@app.route("/reset")
def reset():
    init_db()
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
