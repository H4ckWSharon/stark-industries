"""
STARK INDUSTRIES SQL — Challenge 29: PostgreSQL Dedicated SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import time
import psycopg2
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{p0stgr3sql_m4st3r}")

def get_db():
    for _ in range(30):
        try:
            return psycopg2.connect(
                host=os.environ.get("PGSQL_HOST", "postgres-challenge"),
                user=os.environ.get("PGSQL_USER", "challenge_user"),
                password=os.environ.get("PGSQL_PASSWORD", "challenge_pg_password"),
                dbname=os.environ.get("PGSQL_DB", "stark_challenge_db")
            )
        except Exception:
            time.sleep(3)
    return None

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch29 - PostgreSQL Dedicated</title>
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
<h2>⚡ STARK INDUSTRIES — Challenge 29: PostgreSQL SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Explore PostgreSQL pg_catalog metadata and functions.<br>
<b>OBJECTIVE:</b> Enumerate tables via pg_tables and extract the flag from ch29_secrets.</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Item name">
<button type="submit">[ SEARCH PGSQL ]</button>
</form>
{% if result %}
<pre>{{ result }}</pre>
{% endif %}
<div class="hint">
💡 Try: <code style="color:#ffd700;">' UNION SELECT 1, flag, 'PgExfil' FROM ch29_secrets WHERE challenge_id=29--</code>
</div>
</body></html>"""

@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        try:
            conn = get_db()
            if conn:
                cur = conn.cursor()
                sql = f"SELECT id, name, location FROM inventory WHERE name='{input_val}'"
                cur.execute(sql)
                rows = cur.fetchall()
                result = "\n".join([str(r) for r in rows])
                conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health(): return jsonify({"status": "ok", "challenge": 29})
@app.route("/reset")
def reset(): return jsonify({"status": "reset"})
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000, debug=False)
