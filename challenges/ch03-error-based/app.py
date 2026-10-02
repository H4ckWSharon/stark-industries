"""
STARK INDUSTRIES SQL — Challenge 03: Error-Based SQL Injection (MySQL)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import time
import pymysql
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{err0r_based_exfil}")

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

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Stark Industries — Product Catalog API</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0a0a0f; color: #e0e0e0; font-family: 'Courier New', monospace; min-height: 100vh; }
.header { background: #0d1117; border-bottom: 1px solid #00d4ff33; padding: 16px 40px; display: flex; align-items: center; gap: 20px; }
.logo { color: #00d4ff; font-weight: bold; letter-spacing: 2px; }
.badge { background: #ff2244; color: white; padding: 3px 10px; border-radius: 4px; font-size: 0.7rem; }
.container { max-width: 900px; margin: 40px auto; padding: 0 20px; }
.mission { background: #0d1117; border: 1px solid #00d4ff33; border-radius: 8px; padding: 20px; margin-bottom: 24px; }
.mission-title { color: #00d4ff; font-size: 0.9rem; letter-spacing: 2px; margin-bottom: 10px; }
.mission-text { color: #8b949e; line-height: 1.6; font-size: 0.9rem; }
.search-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 24px; }
input { background: #010409; border: 1px solid #30363d; color: #00d4ff; padding: 10px 14px; border-radius: 6px; width: 300px; font-family: monospace; font-size: 0.95rem; outline: none; }
input:focus { border-color: #00d4ff; }
button { background: linear-gradient(135deg, #00d4ff, #0066cc); color: #0a0a0f; border: none; padding: 10px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-left: 10px; }
.result-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 20px; }
.result-title { color: #8b949e; font-size: 0.8rem; letter-spacing: 1px; margin-bottom: 12px; }
pre { background: #010409; border: 1px solid #21262d; border-radius: 6px; padding: 16px; color: #8b949e; font-size: 0.85rem; white-space: pre-wrap; overflow-x: auto; }
.error-output { background: #2d1b1b; border: 1px solid #ff2244; border-radius: 6px; padding: 16px; color: #ff8080; font-size: 0.85rem; white-space: pre-wrap; }
.flag-found { background: #0d2b0d; border: 1px solid #00ff88; border-radius: 6px; padding: 16px; color: #00ff88; font-size: 0.85rem; margin-top: 12px; }
.hint-box { background: #0d1b0d; border: 1px solid #00ff8833; border-radius: 6px; padding: 14px; margin-top: 20px; color: #8b949e; font-size: 0.82rem; line-height: 1.5; }
</style>
</head>
<body>
<div class="header">
  <div class="logo">⚡ STARK INDUSTRIES</div>
  <div>PRODUCT CATALOG API</div>
  <div class="badge">CHALLENGE 03 — ERROR BASED</div>
  <div style="margin-left:auto;color:#ff2244;font-size:0.8rem;">⚠ VERBOSE ERRORS ENABLED</div>
</div>
<div class="container">
  <div class="mission">
    <div class="mission-title">// MISSION 03 — ERROR-BASED SQL INJECTION</div>
    <div class="mission-text">
      This product catalog API has verbose error reporting enabled — a dangerous misconfiguration.<br>
      MySQL's <code style="color:#00d4ff;">EXTRACTVALUE()</code> function throws errors that can contain query results.<br><br>
      <strong style="color:#00d4ff;">OBJECTIVE:</strong> Use error-based extraction to retrieve the challenge flag from the database.
    </div>
  </div>
  <div class="search-box">
    <form method="GET">
      <label style="color:#8b949e;font-size:0.8rem;">PRODUCT ID:</label><br><br>
      <input type="text" name="id" value="{{ pid }}" placeholder="e.g. 1 or inject here">
      <button type="submit">[ QUERY ]</button>
    </form>
  </div>
  {% if output %}
  <div class="result-box">
    <div class="result-title">// DATABASE RESPONSE</div>
    {% if is_error %}
    <div class="error-output">{{ output }}</div>
    {% elif flag_found %}
    <div class="flag-found">{{ output }}</div>
    {% else %}
    <pre>{{ output }}</pre>
    {% endif %}
  </div>
  {% endif %}
  <div class="hint-box">
    💡 Executing: <code style="color:#00d4ff;">SELECT * FROM products WHERE id = {{ pid or '&lt;input&gt;' }}</code><br>
    Try: <code style="color:#ffd700;">1 AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version())))</code>
  </div>
</div>
</body>
</html>"""


@app.route("/", methods=["GET"])
def index():
    pid = request.args.get("id", "")
    output = None
    is_error = False
    flag_found = False

    if pid:
        try:
            conn = get_db()
            if not conn:
                return "Database not ready", 503
            with conn.cursor() as c:
                # INTENTIONALLY VULNERABLE
                sql = f"SELECT id, name, category, price FROM products WHERE id = {pid}"
                c.execute(sql)
                rows = c.fetchall()
                if rows:
                    output = "\n".join([str(dict(r)) for r in rows])
                else:
                    output = "No products found."
            conn.close()
        except Exception as e:
            output = f"MySQL Error: {str(e)}"
            is_error = True
            if FLAG in output:
                flag_found = True

    return render_template_string(PAGE, pid=pid, output=output, is_error=is_error, flag_found=flag_found)


@app.route("/health")
def health():
    conn = get_db()
    if conn:
        conn.close()
        return jsonify({"status": "ok", "challenge": 3})
    return jsonify({"status": "db_not_ready"}), 503


@app.route("/reset")
def reset():
    return jsonify({"status": "reset", "message": "MySQL data persists in shared container"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
