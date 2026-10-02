"""
STARK INDUSTRIES SQL — Challenge 01: Basic SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{basic_injection_r3d_t3am}")
DB = "/tmp/ch01.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            part_number TEXT,
            description TEXT,
            is_secret INTEGER DEFAULT 0
        );
        DELETE FROM parts;
        INSERT INTO parts (name, part_number, description, is_secret) VALUES
            ('Arc Reactor Core',     'ARC-001', 'Miniaturized fusion core unit',     0),
            ('Repulsor Module',      'REP-002', 'Palm-mounted propulsion system',    0),
            ('Vibranium Alloy',      'VIB-003', 'Synthetic lab alloy specimen',      0),
            ('Suit Frame v3',        'SFV-003', 'Modular exoskeleton chassis',       0),
            ('CLASSIFIED ITEM',      'SEC-999', 'FLAG: PLACEHOLDER',                 1);
    """)
    # Update flag in DB
    c.execute("UPDATE parts SET description = ? WHERE is_secret = 1", (f"FLAG: {FLAG}",))
    conn.commit()
    conn.close()


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Stark Industries — Parts Catalog</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0a0a0f; color: #e0e0e0; font-family: 'Courier New', monospace; min-height: 100vh; }
.header { background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); border-bottom: 1px solid #00d4ff33; padding: 20px 40px; display: flex; align-items: center; gap: 20px; }
.logo { color: #00d4ff; font-size: 1.4rem; font-weight: bold; letter-spacing: 2px; }
.badge { background: #ff2244; color: white; padding: 4px 12px; border-radius: 4px; font-size: 0.7rem; letter-spacing: 1px; }
.container { max-width: 900px; margin: 40px auto; padding: 0 20px; }
.mission-card { background: #0d1117; border: 1px solid #00d4ff33; border-radius: 8px; padding: 24px; margin-bottom: 30px; }
.mission-title { color: #00d4ff; font-size: 1.1rem; margin-bottom: 10px; letter-spacing: 2px; }
.mission-text { color: #8b949e; line-height: 1.6; }
.search-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 24px; margin-bottom: 30px; }
.search-label { color: #8b949e; font-size: 0.85rem; margin-bottom: 10px; display: block; }
input[type=text] { background: #010409; border: 1px solid #30363d; color: #00d4ff; padding: 12px 16px; border-radius: 6px; width: 100%; font-family: 'Courier New', monospace; font-size: 1rem; outline: none; transition: border-color 0.2s; }
input[type=text]:focus { border-color: #00d4ff; box-shadow: 0 0 0 3px #00d4ff22; }
button { background: linear-gradient(135deg, #00d4ff, #0066cc); color: #0a0a0f; border: none; padding: 12px 28px; border-radius: 6px; font-weight: bold; font-family: 'Courier New', monospace; font-size: 0.9rem; cursor: pointer; margin-top: 12px; transition: opacity 0.2s; }
button:hover { opacity: 0.85; }
.results { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; }
.result-header { background: #161b22; padding: 12px 20px; color: #8b949e; font-size: 0.8rem; display: grid; grid-template-columns: 80px 200px 120px 1fr; gap: 16px; }
.result-row { padding: 14px 20px; border-top: 1px solid #21262d; display: grid; grid-template-columns: 80px 200px 120px 1fr; gap: 16px; transition: background 0.15s; }
.result-row:hover { background: #161b22; }
.result-row.secret { border-left: 3px solid #ffd700; background: #1a1600; }
.col-id { color: #6e7681; }
.col-name { color: #e6edf3; font-weight: bold; }
.col-part { color: #58a6ff; font-size: 0.85rem; }
.col-desc { color: #8b949e; font-size: 0.9rem; }
.flag-value { color: #ffd700; font-weight: bold; }
.empty { padding: 40px; text-align: center; color: #6e7681; }
.error-box { background: #2d1b1b; border: 1px solid #ff2244; border-radius: 6px; padding: 16px; margin-top: 16px; color: #ff8080; font-size: 0.9rem; }
.hint-box { background: #0d1b0d; border: 1px solid #00ff8866; border-radius: 6px; padding: 16px; margin-top: 16px; color: #00ff88; font-size: 0.85rem; }
</style>
</head>
<body>
<div class="header">
  <div class="logo">⚡ STARK INDUSTRIES</div>
  <div>PARTS CATALOG SYSTEM</div>
  <div class="badge">CHALLENGE 01</div>
  <div style="margin-left:auto;color:#ff2244;font-size:0.8rem;">⚠ INTENTIONALLY VULNERABLE LAB</div>
</div>
<div class="container">
  <div class="mission-card">
    <div class="mission-title">// MISSION BRIEF</div>
    <div class="mission-text">
      Stark Industries' internal parts catalog uses a simple search feature.<br>
      Intelligence suggests the search query is vulnerable to SQL injection.<br><br>
      <strong style="color:#00d4ff;">OBJECTIVE:</strong> Retrieve the classified item and capture the flag.
    </div>
  </div>
  <div class="search-box">
    <form method="GET" action="/">
      <label class="search-label">// SEARCH PARTS CATALOG</label>
      <input type="text" name="q" placeholder="Enter part name..." value="{{ query }}">
      <br><button type="submit">[ SEARCH ]</button>
    </form>
    {% if error %}
    <div class="error-box">DATABASE ERROR: {{ error }}</div>
    {% endif %}
  </div>
  {% if results is not none %}
  <div class="results">
    <div class="result-header">
      <span>ID</span><span>PART NAME</span><span>PART #</span><span>DESCRIPTION</span>
    </div>
    {% if results %}
      {% for row in results %}
      <div class="result-row {% if row[4] %}secret{% endif %}">
        <span class="col-id">{{ row[0] }}</span>
        <span class="col-name">{{ row[1] }}</span>
        <span class="col-part">{{ row[2] }}</span>
        <span class="col-desc {% if 'STARKSQL{' in (row[3] or '') %}flag-value{% endif %}">{{ row[3] }}</span>
      </div>
      {% endfor %}
    {% else %}
      <div class="empty">No parts found matching your search.</div>
    {% endif %}
  </div>
  {% endif %}
  <div class="hint-box" style="margin-top:20px;">
    💡 TIP: The search runs a SQL query like: <code style="color:#00ff88;">SELECT * FROM parts WHERE name = '&lt;your_input&gt;'</code>
  </div>
</div>
</body>
</html>"""


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "")
    results = None
    error = None

    if query:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            # INTENTIONALLY VULNERABLE — direct string interpolation
            sql = f"SELECT id, name, part_number, description, is_secret FROM parts WHERE name = '{query}'"
            c.execute(sql)
            results = c.fetchall()
            conn.close()
        except Exception as e:
            error = str(e)

    return render_template_string(PAGE, query=query, results=results, error=error)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 1})


@app.route("/reset")
def reset():
    init_db()
    return jsonify({"status": "reset", "message": "Database reseeded"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
