"""
STARK INDUSTRIES SQL — Challenge 22: HTTP Parameter Pollution + SQLi
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{hpp_p4r4m_p0llut10n}")
DB = "/tmp/ch22.db"

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
    c.execute("INSERT OR REPLACE INTO secrets VALUES (22, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch22 - HTTP Parameter Pollution + SQLi</title>
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
<h2>⚡ STARK INDUSTRIES — Challenge 22: HTTP Parameter Pollution + SQLi</h2>
<p><b style="color:#00d4ff">MISSION:</b> Application improperly handles duplicate HTTP query parameters (e.g. ?id=1&id=UNION...).<br>
<b>OBJECTIVE:</b> Combine HPP with SQLi to construct a complete injection payload.</p>
<form method="POST">
<input type="text" name="input_val" value="{ input_val }" placeholder="Enter payload / parameter">
<button type="submit">[ SUBMIT ]</button>
</form>
{% if result %}
<pre>{ result }</pre>
{% endif %}
<div class="hint">
💡 Try URL parameters: <code style='color:#ffd700;'>?id=1&id=UNION&id=SELECT&id=1,flag,'HPP','Exfil'&id=FROM&id=secrets&id=WHERE&id=id=22</code>
</div>
</body></html>"""

@app.route("/", methods=["GET", "POST"])
def index():
    # Demonstrating parameter pollution where backend receives array of params
    args = request.args.getlist("id")
    result = None
    if args:
        # Backend concatenates multiple params improperly
        combined = " ".join(args)
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"SELECT * FROM data_items WHERE id={combined}"
            c.execute(sql)
            rows = c.fetchall()
            result = "\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val="&id=".join(args) if args else "1", result=result)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 22})

@app.route("/reset")
def reset():
    init_db()
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
