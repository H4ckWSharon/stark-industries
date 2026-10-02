"""
STARK INDUSTRIES SQL — Challenge 27: SQLite Dedicated SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{sql1t3_sp3c14l1st}")
DB = "/tmp/ch27.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS lab_data_sqlite (id INTEGER PRIMARY KEY, name TEXT, meta TEXT);
        CREATE TABLE IF NOT EXISTS lab_secrets_sqlite (id INTEGER PRIMARY KEY, secret_flag TEXT);
        DELETE FROM lab_data_sqlite; DELETE FROM lab_secrets_sqlite;
        INSERT INTO lab_data_sqlite VALUES (1, 'SQLite Engine Core', 'v3.x');
    """)
    c.execute("INSERT OR REPLACE INTO lab_secrets_sqlite VALUES (27, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch27 - SQLite Dedicated</title>
<style>
body { background:#0a0a0f; color:#e0e0e0; font-family:monospace; padding:40px; }
input { background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px; border-radius:6px; width:350px; font-family:monospace; outline:none; }
button { background:#00d4ff; color:#000; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:8px; }
h2 { color:#00d4ff; letter-spacing:2px; margin-bottom:16px; }
p { color:#8b949e; margin-bottom:16px; line-height:1.5; }
pre { background:#010409; border:1px solid #21262d; border-radius:6px; padding:16px; color:#8b949e; white-space:pre-wrap; margin-top:16px; }
.hint { background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; }
code { color:#ffd700; }
</style></head>
<body>
<h2>⚡ STARK INDUSTRIES — Challenge 27: SQLite SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Explore SQLite metadata (sqlite_master) and syntax.<br>
<b>OBJECTIVE:</b> Enumerate tables via sqlite_master and retrieve the flag from lab_secrets_sqlite.</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Item name">
<button type="submit">[ SEARCH SQLITE ]</button>
</form>
{% if result %}
<pre>{{ result }}</pre>
{% endif %}
<div class="hint">
💡 Step 1: <code style="color:#ffd700;">' UNION SELECT 1, tbl_name, sql FROM sqlite_master--</code><br>
Step 2: <code style="color:#ffd700;">' UNION SELECT 1, secret_flag, 'Flag' FROM lab_secrets_sqlite--</code>
</div>
</body></html>"""

@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"SELECT * FROM lab_data_sqlite WHERE name='{input_val}'"
            c.execute(sql)
            rows = c.fetchall()
            result = "\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health(): return jsonify({"status": "ok", "challenge": 27})
@app.route("/reset")
def reset(): init_db(); return jsonify({"status": "reset"})
if __name__ == "__main__": init_db(); app.run(host="0.0.0.0", port=5000, debug=False)
