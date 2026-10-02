"""
STARK INDUSTRIES SQL — Challenge 09: Stacked Queries (PostgreSQL)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import time
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{st4ck3d_qu3ry_ch4in}")


def get_db():
    for _ in range(30):
        try:
            return psycopg2.connect(
                host=os.environ.get("PGSQL_HOST", "postgres-challenge"),
                user=os.environ.get("PGSQL_USER", "challenge_user"),
                password=os.environ.get("PGSQL_PASSWORD", "challenge_pg_password"),
                dbname=os.environ.get("PGSQL_DB", "stark_challenge_db"),
            )
        except Exception:
            time.sleep(3)
    return None


@app.route("/")
def index():
    iid = request.args.get("id", "")
    output = ""
    results_html = ""

    if iid:
        try:
            conn = get_db()
            if conn:
                cur = conn.cursor()
                # INTENTIONALLY VULNERABLE — stacked queries possible in PostgreSQL
                sql = f"SELECT id, name, quantity FROM inventory WHERE id={iid}"
                cur.execute(sql)
                rows = cur.fetchall()
                output = "\n".join([str(r) for r in rows]) if rows else "No items found."
                conn.close()
        except Exception as e:
            output = f"Error: {str(e)}"
        results_html = f'<pre style="background:#010409;border:1px solid #21262d;border-radius:6px;padding:16px;color:#8b949e;white-space:pre-wrap;margin-top:16px;">{output}</pre>'

    return f"""<!DOCTYPE html><html><head><title>Stark Ch09 - Stacked Queries</title>
<style>
body{{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;}}
input{{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:200px;font-family:monospace;outline:none;}}
button{{background:#00d4ff;color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;margin-left:8px;}}
h2{{color:#00d4ff;letter-spacing:2px;margin-bottom:16px;}}
p{{color:#8b949e;margin-bottom:16px;line-height:1.5;}}
.hint{{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;max-width:800px;}}
code{{color:#ffd700;}}
</style></head>
<body>
<h2>&#9889; STARK INDUSTRIES - Challenge 09: Stacked Queries (PostgreSQL)</h2>
<p><b style="color:#00d4ff">MISSION:</b> PostgreSQL supports multiple semicolon-separated statements.<br>
Inject a second SELECT statement to read from challenge_secrets.<br>
<b>OBJECTIVE:</b> Use stacked queries to extract the flag.</p>
<form method="GET">
<input type="text" name="id" value="{iid}" placeholder="Item ID">
<button type="submit">[ LOOKUP ]</button>
</form>
{results_html}
<div class="hint">
&#128161; Try: <code>1; SELECT secret_value FROM challenge_secrets WHERE challenge_id=9--</code><br>
PostgreSQL (unlike MySQL) fully supports multiple statements via semicolons.
</div>
</body></html>"""


@app.route("/health")
def health():
    conn = get_db()
    if conn:
        conn.close()
        return jsonify({"status": "ok", "challenge": 9})
    return jsonify({"status": "db_not_ready"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
