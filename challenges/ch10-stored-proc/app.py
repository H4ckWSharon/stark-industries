"""
STARK INDUSTRIES SQL — Challenge 10: Stored Procedure Injection (MySQL)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import time
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{st0r3d_pr0c_byp4ss}")


def get_db():
    for _ in range(20):
        try:
            return pymysql.connect(
                host=os.environ.get("MYSQL_HOST", "mysql-challenge"),
                user=os.environ.get("MYSQL_USER", "lab_user"),
                password=os.environ.get("MYSQL_PASSWORD", "lab_mysql_password"),
                database=os.environ.get("MYSQL_DB", "stark_lab"),
                cursorclass=pymysql.cursors.DictCursor,
            )
        except Exception:
            time.sleep(3)
    return None


@app.route("/")
def index():
    dept = request.args.get("dept", "")
    output = ""
    results_html = ""

    if dept:
        try:
            conn = get_db()
            if conn:
                with conn.cursor() as c:
                    # Calls the intentionally vulnerable stored procedure
                    c.callproc("GetEmployeesByDept", (dept,))
                    rows = c.fetchall()
                    output = "\n".join([str(dict(r)) for r in rows]) if rows else "No employees in that department."
                conn.close()
        except Exception as e:
            output = f"Error: {str(e)}"
        results_html = f'<pre style="background:#010409;border:1px solid #21262d;border-radius:6px;padding:16px;color:#8b949e;white-space:pre-wrap;margin-top:16px;">{output}</pre>'

    return f"""<!DOCTYPE html><html><head><title>Stark Ch10 - Stored Proc</title>
<style>
body{{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;}}
input{{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:300px;font-family:monospace;outline:none;}}
button{{background:#00d4ff;color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;margin-left:8px;}}
h2{{color:#00d4ff;letter-spacing:2px;margin-bottom:16px;}}
p{{color:#8b949e;margin-bottom:16px;line-height:1.5;}}
.proc-code{{background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:16px;margin-top:16px;max-width:800px;}}
.proc-title{{color:#ffd700;font-size:.8rem;margin-bottom:8px;letter-spacing:1px;}}
.hint{{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;max-width:800px;}}
code{{color:#ffd700;}}
</style></head>
<body>
<h2>&#9889; STARK INDUSTRIES - Challenge 10: Stored Procedure Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> The report system calls a MySQL stored procedure with your department input.<br>
The procedure uses dynamic SQL with CONCAT() internally &mdash; making it vulnerable.<br>
<b>OBJECTIVE:</b> Inject through the procedure call to extract the flag.</p>
<form method="GET">
<input type="text" name="dept" value="{dept}" placeholder="Department (e.g. R&amp;D)">
<button type="submit">[ GET REPORT ]</button>
</form>
{results_html}
<div class="proc-code">
<div class="proc-title">// STORED PROCEDURE (intentionally vulnerable)</div>
<pre style="color:#8b949e;margin:0;">CREATE PROCEDURE GetEmployeesByDept(IN dept VARCHAR(100))
BEGIN
  SET @sql = CONCAT('SELECT * FROM employees WHERE department = ''', dept, '''');
  PREPARE stmt FROM @sql;
  EXECUTE stmt;  -- VULNERABLE: user input in dynamic SQL
  DEALLOCATE PREPARE stmt;
END</pre>
</div>
<div class="hint">
&#128161; Try department: <code>R&D' UNION SELECT secret_value,NULL,NULL FROM challenge_secrets WHERE challenge_id=10--</code>
</div>
</body></html>"""


@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 10})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
