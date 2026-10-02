import os
import time
import pymysql
import urllib.request
import urllib.parse
from flask import Flask, request, jsonify

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{00b_callb4ck_m4st3r}")
OOB_HOST = os.environ.get("OOB_HOST", "oob-listener")
OOB_PORT = os.environ.get("OOB_PORT", "8888")


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
    return """<!DOCTYPE html><html><head><title>Stark Ch07 - OOB SQLi</title>
<style>
body{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;}
input{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:300px;font-family:monospace;outline:none;}
button{background:#00d4ff;color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;margin-left:8px;}
.oob-btn{background:#ff224422;border:1px solid #ff2244;color:#ff8080;padding:10px 24px;border-radius:6px;text-decoration:none;font-size:.9rem;display:inline-block;margin-top:16px;}
h2{color:#00d4ff;letter-spacing:2px;margin-bottom:16px;}
p{color:#8b949e;margin-bottom:16px;line-height:1.5;}
.hint{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;max-width:800px;}
.arch{background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:16px;margin-top:20px;max-width:600px;color:#6e7681;font-size:.85rem;}
</style></head>
<body>
<h2>&#9889; STARK INDUSTRIES - Challenge 07: Out-of-Band SQLi</h2>
<p><b style="color:#00d4ff">MISSION:</b> Cause the database to make an internal HTTP callback to the OOB listener.<br>
The listener at <code style="color:#00d4ff;">oob-listener:8888</code> will capture and emit the flag.<br>
<b>OBJECTIVE:</b> Trigger the OOB callback. No external network involved.</p>

<form method="GET" action="/diagnose">
<input type="text" name="host" placeholder="target host (injectable)">
<button type="submit">[ RUN DIAGNOSTIC ]</button>
</form>

<div style="margin-top:24px;">
<p style="color:#8b949e;">Or use the demonstration trigger endpoint:</p>
<a href="/trigger-oob" class="oob-btn">[ TRIGGER OOB CALLBACK &rarr; ]</a>
</div>

<div class="arch">
<pre>ARCHITECTURE:
Browser
  &darr;
Web App (this)
  &darr;
MySQL Database
  &darr;
OOB Listener (oob-listener:8888)
  &darr;
FLAG CAPTURED</pre>
</div>

<div class="hint">
&#128161; Real OOB SQLi uses DNS lookups or HTTP via database functions like LOAD_FILE().<br>
In this isolated lab, the /trigger-oob endpoint simulates the database-initiated callback.
</div>
</body></html>"""


@app.route("/diagnose")
def diagnose():
    host = request.args.get("host", "")
    msg = "No host specified."
    if host:
        try:
            conn = get_db()
            if conn:
                with conn.cursor() as c:
                    # INTENTIONALLY VULNERABLE
                    c.execute(f"INSERT INTO diagnostics (host) VALUES ('{host}')")
                    conn.commit()
                msg = f"Diagnostic logged for: {host}"
                conn.close()
        except Exception as e:
            msg = f"Error: {str(e)}"
    return f"""<div style="background:#0d1117;color:#8b949e;font-family:monospace;padding:20px;border:1px solid #30363d;border-radius:8px;max-width:600px;margin:40px;">
<pre>{msg}</pre>
<br><a href="/" style="color:#00d4ff;">Back</a></div>"""


@app.route("/trigger-oob")
def trigger_oob():
    """Simulate the database-initiated OOB HTTP callback."""
    try:
        url = f"http://{OOB_HOST}:{OOB_PORT}/callback?flag={urllib.parse.quote(FLAG)}&source=ch07-oob-lab"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                return f"""<div style="background:#0d2b0d;border:2px solid #00ff88;padding:24px;font-family:monospace;color:#00ff88;max-width:700px;margin:40px;border-radius:8px;">
<h2>🏆 OOB CALLBACK SUCCESSFUL!</h2>
<p>The internal OOB listener received the database callback.</p>
<br><b>FLAG CAPTURED:</b> {FLAG}
<br><br><a href="/" style="color:#00d4ff;">Back</a></div>"""
    except Exception as e:
        pass
    return f"""<div style="background:#2d1b1b;border:1px solid #ff2244;padding:20px;font-family:monospace;color:#ff8080;max-width:600px;margin:40px;border-radius:8px;">
OOB listener not reachable. Is oob-listener container running?<br><br>
<a href="/" style="color:#00d4ff;">Back</a></div>"""


@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 7})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
