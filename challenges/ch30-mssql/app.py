"""
STARK INDUSTRIES SQL — Challenge 30: MSSQL Dedicated SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{mssql_pwn4g3}")
DB = "/tmp/ch30.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS sys_tables_sim (id INTEGER PRIMARY KEY, name TEXT, category TEXT);
        CREATE TABLE IF NOT EXISTS ch30_secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM sys_tables_sim; DELETE FROM ch30_secrets;
        INSERT INTO sys_tables_sim VALUES (1, 'MSSQL Executive Table', 'Master DB');
    """)
    c.execute("INSERT OR REPLACE INTO ch30_secrets VALUES (30, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch30 - MSSQL Dedicated</title>
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
<h2>⚡ STARK INDUSTRIES — Challenge 30: MSSQL SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Explore Microsoft SQL Server dialect (sys.tables, TOP, WAITFOR DELAY).<br>
<b>OBJECTIVE:</b> Extract the flag from ch30_secrets using MSSQL-compatible syntax.</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Table search">
<button type="submit">[ SEARCH MSSQL ]</button>
</form>
{% if result %}
<pre>{{ result }}</pre>
{% endif %}
<div class="hint">
💡 Try: <code style="color:#ffd700;">' UNION SELECT 1, flag, 'MSSQL_EXFIL' FROM ch30_secrets WHERE id=30--</code>
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
            sql = f"SELECT * FROM sys_tables_sim WHERE name='{input_val}'"
            c.execute(sql)
            rows = c.fetchall()
            result = "\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health(): return jsonify({"status": "ok", "challenge": 30})
@app.route("/reset")
def reset(): init_db(); return jsonify({"status": "reset"})
if __name__ == "__main__": init_db(); app.run(host="0.0.0.0", port=5000, debug=False)
