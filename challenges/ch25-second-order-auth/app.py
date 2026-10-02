"""
STARK INDUSTRIES SQL — Challenge 25: Second-Order Authentication SQLi
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{s3c0nd_0rd3r_4uth_pwn}")
DB = "/tmp/ch25.db"

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
    c.execute("INSERT OR REPLACE INTO secrets VALUES (25, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch25 - Second-Order Authentication SQLi</title>
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
<h2>⚡ STARK INDUSTRIES — Challenge 25: Second-Order Authentication SQLi</h2>
<p><b style="color:#00d4ff">MISSION:</b> Stored input is later evaluated unsafely during an authentication workflow.<br>
<b>OBJECTIVE:</b> Inject payload that triggers during internal auth queries.</p>
<form method="POST">
<input type="text" name="input_val" value="{ input_val }" placeholder="Enter payload / parameter">
<button type="submit">[ SUBMIT ]</button>
</form>
{% if result %}
<pre>{ result }</pre>
{% endif %}
<div class="hint">
💡 Try payload: <code style='color:#ffd700;'>admin' OR '1'='1' UNION SELECT 1, flag, 'Auth', 'SecondOrder' FROM secrets WHERE id=25--</code>
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
            # Stage 1: Store input safely
            c.execute("INSERT OR REPLACE INTO data_items (id, name, category, secret_data) VALUES (99, ?, 'StoredAuth', 'Payload')", (input_val,))
            conn.commit()
            # Stage 2: Execute stored payload unsafely in auth logic
            c.execute("SELECT name FROM data_items WHERE id=99")
            stored = c.fetchone()[0]
            sql = f"SELECT * FROM data_items WHERE name='{stored}'"
            c.execute(sql)
            rows = c.fetchall()
            result = f"Second-Order Authentication check triggered for [{stored}]:\n" + "\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 25})

@app.route("/reset")
def reset():
    init_db()
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
