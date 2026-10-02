"""
STARK INDUSTRIES SQL — Challenge 28: MySQL Dedicated SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import time
import pymysql
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{mysql_d33p_d1v3}")

def get_db():
    for _ in range(20):
        try:
            return pymysql.connect(
                host=os.environ.get("MYSQL_HOST", "mysql-challenge"),
                user=os.environ.get("MYSQL_USER", "lab_user"),
                password=os.environ.get("MYSQL_PASSWORD", "lab_mysql_password"),
                database=os.environ.get("MYSQL_DB", "stark_lab"),
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception:
            time.sleep(3)
    return None

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch28 - MySQL Dedicated</title>
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
<h2>⚡ STARK INDUSTRIES — Challenge 28: MySQL SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Explore MySQL information_schema and functions (GROUP_CONCAT).<br>
<b>OBJECTIVE:</b> Use information_schema to discover table names and extract the flag from ch28_secrets.</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Product category">
<button type="submit">[ SEARCH MYSQL ]</button>
</form>
{% if result %}
<pre>{{ result }}</pre>
{% endif %}
<div class="hint">
💡 Try: <code style="color:#ffd700;">' UNION SELECT 1, flag, 'Exfil' FROM ch28_secrets WHERE challenge_id=28--</code>
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
                with conn.cursor() as c:
                    sql = f"SELECT id, name, category FROM products WHERE category='{input_val}'"
                    c.execute(sql)
                    rows = c.fetchall()
                    result = "\n".join([str(dict(r)) for r in rows])
                conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health(): return jsonify({"status": "ok", "challenge": 28})
@app.route("/reset")
def reset(): return jsonify({"status": "reset"})
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000, debug=False)
