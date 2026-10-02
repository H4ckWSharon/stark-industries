"""
STARK INDUSTRIES SQL — Challenge 26: Multi-Database SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{mult1_db_3xpl0r3r}")
DB = "/tmp/ch26.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS data_items (id INTEGER PRIMARY KEY, engine TEXT, status TEXT);
        CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM data_items; DELETE FROM secrets;
        INSERT INTO data_items VALUES (1, 'SQLite Engine', 'ACTIVE'), (2, 'MySQL Engine', 'ACTIVE'), (3, 'PostgreSQL Engine', 'ACTIVE'), (4, 'MSSQL Engine', 'ACTIVE');
    """)
    c.execute("INSERT OR REPLACE INTO secrets VALUES (26, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch26 - Multi-DB SQLi</title>
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
<h2>⚡ STARK INDUSTRIES — Challenge 26: Multi-Database SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Target multi-database environment features.<br>
<b>OBJECTIVE:</b> Understand differences between database dialects and extract the flag.</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Engine query filter">
<button type="submit">[ SEARCH ENGINE ]</button>
</form>
{% if result %}
<pre>{{ result }}</pre>
{% endif %}
<div class="hint">
💡 Try: <code style="color:#ffd700;">SQLite Engine' UNION SELECT 1, flag, 'Exfil' FROM secrets WHERE id=26--</code>
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
            sql = f"SELECT * FROM data_items WHERE engine='{input_val}'"
            c.execute(sql)
            rows = c.fetchall()
            result = "\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health(): return jsonify({"status": "ok", "challenge": 26})
@app.route("/reset")
def reset(): init_db(); return jsonify({"status": "reset"})
if __name__ == "__main__": init_db(); app.run(host="0.0.0.0", port=5000, debug=False)
