"""
STARK INDUSTRIES SQL — Challenge 06: Time-Based Blind SQL Injection (MySQL)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import time
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{t1m3_blind_d3t3ctiv3}")


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
    sid = request.args.get("id", "")
    status = ""
    resp_time = 0
    if sid:
        t0 = time.time()
        try:
            conn = get_db()
            if conn:
                with conn.cursor() as c:
                    # INTENTIONALLY VULNERABLE
                    c.execute(f"SELECT status FROM systems WHERE id={sid}")
                    row = c.fetchone()
                    status = row["status"] if row else "NOT FOUND"
                conn.close()
        except Exception:
            status = "ERROR"
        resp_time = int((time.time() - t0) * 1000)

    result_html = ""
    if sid:
        result_html = f"""<div style="background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:20px;margin-top:16px;max-width:600px;">
<pre style="color:#00ff88;">STATUS: {status}
Response time: {resp_time}ms</pre></div>"""

    return f"""<!DOCTYPE html><html><head><title>Stark Ch06 - Time Blind</title>
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
<h2>&#9889; STARK INDUSTRIES - Challenge 06: Time-Based Blind SQLi</h2>
<p><b style="color:#00d4ff">MISSION:</b> The response always looks the same. Use MySQL SLEEP() to infer data through response timing.<br>
<b>OBJECTIVE:</b> Extract the flag by measuring conditional delays (id=6 in challenge_secrets).</p>
<form method="GET">
<input type="text" name="id" value="{sid}" placeholder="System ID">
<button type="submit">[ CHECK STATUS ]</button>
</form>
{result_html}
<div class="hint">
&#128161; Try: <code>1 AND SLEEP(2)--</code> - if slow, injection works!<br>
Then: <code>1 AND IF(SUBSTR((SELECT secret_value FROM challenge_secrets WHERE challenge_id=6),1,1)='S',SLEEP(2),0)--</code>
</div>
</body></html>"""


@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 6})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
