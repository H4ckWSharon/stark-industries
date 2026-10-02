"""
STARK INDUSTRIES SQL — Challenge 13: DELETE-Based SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{d3l3t3_sqli_b00m}")
DB = "/tmp/ch13.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS data_items (id INTEGER PRIMARY KEY, name TEXT, category TEXT, secret_data TEXT);
        CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM data_items;
        DELETE FROM secrets;
        INSERT INTO data_items VALUES (1, 'Arc Reactor Mark II', 'Power Systems', 'Public Specs'), (2, 'Mark III Armor Framework', 'Defensive Armor', 'Public Specs');
    """)
    c.execute("INSERT OR REPLACE INTO secrets VALUES (13, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch13 - DELETE-Based SQL Injection</title>
<style>
body { background:#0a0a0f; color:#e0e0e0; font-family:monospace; padding:40px; }
input, select { background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px; border-radius:6px; width:350px; font-family:monospace; outline:none; }
button { background:#00d4ff; color:#000; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:8px; }
h2 { color:#00d4ff; letter-spacing:2px; margin-bottom:16px; }
p { color:#8b949e; margin-bottom:16px; line-height:1.5; }
pre { background:#010409; border:1px solid #21262d; border-radius:6px; padding:16px; color:#8b949e; white-space:pre-wrap; margin-top:16px; }
.hint { background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; }
code { color:#ffd700; }
</style></head>
<body>
<h2>⚡ STARK INDUSTRIES — Challenge 13: DELETE-Based SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Endpoint executes a DELETE statement directly incorporating numeric input.<br>
<b>OBJECTIVE:</b> Manipulate the DELETE WHERE clause or inject subqueries.</p>
<form method="POST">
<input type="text" name="input_val" value="{ input_val }" placeholder="Enter payload / parameter">
<button type="submit">[ SUBMIT ]</button>
</form>
{% if result %}
<pre>{ result }</pre>
{% endif %}
<div class="hint">
💡 Try payload: <code style='color:#ffd700;'>1 OR (SELECT load_extension(flag) FROM secrets WHERE id=13)</code> or subquery UNION tricks.
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
            # Vulnerable DELETE
            sql = f"DELETE FROM data_items WHERE id={input_val}"
            c.executescript(sql)
            conn.commit()
            c.execute("SELECT * FROM data_items")
            rows = c.fetchall()
            result = f"Remaining items:\n" + "\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 13})

@app.route("/reset")
def reset():
    init_db()
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
