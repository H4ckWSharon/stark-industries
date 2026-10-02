"""
STARK INDUSTRIES SQL — Challenge 04: UNION-Based SQL Injection (MySQL)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import time
import pymysql
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{un10n_m4st3r_s3l3ct}")


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
<html lang="en"><head><meta charset="UTF-8">
<title>Stark Industries — Catalog Search</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#0a0a0f; color:#e0e0e0; font-family:'Courier New',monospace; min-height:100vh; }
.header { background:#0d1117; border-bottom:1px solid #00d4ff33; padding:16px 40px; display:flex; align-items:center; gap:20px; }
.logo { color:#00d4ff; font-weight:bold; letter-spacing:2px; }
.badge { background:#ff2244; color:white; padding:3px 10px; border-radius:4px; font-size:.7rem; }
.container { max-width:900px; margin:40px auto; padding:0 20px; }
.mission { background:#0d1117; border:1px solid #00d4ff33; border-radius:8px; padding:20px; margin-bottom:24px; }
.mission-title { color:#00d4ff; font-size:.9rem; letter-spacing:2px; margin-bottom:10px; }
.mission-text { color:#8b949e; line-height:1.6; font-size:.9rem; }
.search-box { background:#0d1117; border:1px solid #30363d; border-radius:8px; padding:20px; margin-bottom:24px; }
input { background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px 14px; border-radius:6px; width:300px; font-family:monospace; font-size:.95rem; outline:none; }
input:focus { border-color:#00d4ff; }
button { background:linear-gradient(135deg,#00d4ff,#0066cc); color:#0a0a0f; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:10px; }
.result-box { background:#0d1117; border:1px solid #30363d; border-radius:8px; padding:20px; }
pre { background:#010409; border:1px solid #21262d; border-radius:6px; padding:16px; color:#8b949e; font-size:.85rem; white-space:pre-wrap; overflow-x:auto; }
.hint-box { background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; line-height:1.5; }
</style></head><body>
<div class="header">
  <div class="logo">&#9889; STARK INDUSTRIES</div>
  <div>PRODUCT CATALOG</div>
  <div class="badge">CHALLENGE 04 &mdash; UNION</div>
  <div style="margin-left:auto;color:#ff2244;font-size:.8rem;">&#9888; INTENTIONALLY VULNERABLE</div>
</div>
<div class="container">
  <div class="mission">
    <div class="mission-title">// MISSION 04 &mdash; UNION-BASED SQL INJECTION</div>
    <div class="mission-text">
      The catalog search is injectable via UNION SELECT.<br>
      Step 1: Determine column count using ORDER BY.<br>
      Step 2: Find which columns are displayed.<br>
      Step 3: UNION SELECT the flag from challenge_secrets.<br><br>
      <strong style="color:#00d4ff;">OBJECTIVE:</strong> Extract the flag using UNION SELECT.
    </div>
  </div>
  <div class="search-box">
    <form method="GET">
      <label style="color:#8b949e;font-size:.8rem;">SEARCH BY CATEGORY:</label><br><br>
      <input type="text" name="cat" value="{{ cat }}" placeholder="e.g. Power">
      <button type="submit">[ SEARCH ]</button>
    </form>
  </div>
  {% if results is not none %}
  <div class="result-box">
    <pre>{% for r in results %}{{ r }}
{% endfor %}{% if not results %}No results found.{% endif %}</pre>
  </div>
  {% endif %}
  <div class="hint-box">
    &#128161; Query: <code style="color:#00d4ff;">SELECT id, name, description FROM products WHERE category = '{{ cat or "input" }}'</code><br>
    Try ORDER BY 1, ORDER BY 2, ORDER BY 3 to count columns first.
  </div>
</div>
</body></html>"""


@app.route("/", methods=["GET"])
def index():
    cat = request.args.get("cat", "")
    results = None
    if cat:
        try:
            conn = get_db()
            if not conn:
                return "Database not ready", 503
            with conn.cursor() as c:
                # INTENTIONALLY VULNERABLE
                sql = f"SELECT id, name, description FROM products WHERE category = '{cat}'"
                c.execute(sql)
                rows = c.fetchall()
                results = [str(dict(r)) for r in rows]
            conn.close()
        except Exception as e:
            results = [f"Error: {str(e)}"]
    return render_template_string(PAGE, cat=cat, results=results)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 4})


@app.route("/reset")
def reset():
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
