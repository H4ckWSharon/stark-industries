"""
STARK INDUSTRIES SQL — Bulk Challenge App Generator
Creates app.py for challenges 05-30 that don't have one yet.
Run from the stark industries root.
"""
import os

BASE = r"c:\Users\sharo\Desktop\stark industries\challenges"

CHALLENGES = {

"ch05-boolean-blind": """\
import os, sqlite3
from flask import Flask, request, jsonify, render_template_string
app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{bl1nd_b00l_hunt3r}")
DB = "/tmp/ch05.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT); CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT); DELETE FROM users; DELETE FROM secrets; INSERT INTO users VALUES (1,'tony.stark'),(2,'pepper.potts'),(3,'happy.hogan');")
    c.execute("INSERT OR REPLACE INTO secrets VALUES (5, ?)", (FLAG,))
    conn.commit(); conn.close()

HTML = open(os.path.join(os.path.dirname(__file__), 'page.html')).read() if os.path.exists(os.path.join(os.path.dirname(__file__), 'page.html')) else None

@app.route("/", methods=["GET"])
def index():
    name = request.args.get("name", "")
    found = False
    if name:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute(f"SELECT id FROM users WHERE username='{name}'")
            found = c.fetchone() is not None
            conn.close()
        except: found = False
    return f'''<!DOCTYPE html><html><head><title>Stark - Boolean Blind</title>
    <style>body{{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;}}
    .card{{background:#0d1117;border:1px solid #00d4ff33;border-radius:8px;padding:24px;max-width:700px;}}
    input{{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:300px;font-family:monospace;}}
    button{{background:linear-gradient(135deg,#00d4ff,#0066cc);color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;margin-left:8px;}}
    .true-resp{{background:#0d2b0d;border:1px solid #00ff88;padding:16px;border-radius:6px;color:#00ff88;margin-top:16px;}}
    .false-resp{{background:#2d1b1b;border:1px solid #ff2244;padding:16px;border-radius:6px;color:#ff8080;margin-top:16px;}}
    .hint{{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;}}
    h2{{color:#00d4ff;margin-bottom:16px;letter-spacing:2px;}}
    p{{color:#8b949e;line-height:1.6;margin-bottom:16px;}}</style></head>
    <body><h2>&#9889; STARK INDUSTRIES &mdash; Challenge 05: Boolean-Based Blind SQLi</h2>
    <div class="card">
    <p><strong style="color:#00d4ff;">MISSION:</strong> The app shows only "User found" or "User not found". No data is displayed.<br>
    Use boolean inference with SUBSTR() to extract the flag character by character.<br>
    <strong>OBJECTIVE:</strong> Infer the flag from the secrets table.</p>
    <form method="GET">
    <input type="text" name="name" value="{name}" placeholder="Enter username">
    <button type="submit">[ LOOKUP ]</button>
    </form>
    {"<div class='true-resp'>&#10003; USER FOUND &mdash; Condition evaluated TRUE</div>" if found and name else ""}
    {"<div class='false-resp'>&#10007; USER NOT FOUND &mdash; Condition evaluated FALSE</div>" if not found and name else ""}
    <div class="hint">&#128161; Try: <code style="color:#ffd700;">tony.stark' AND SUBSTR((SELECT flag FROM secrets WHERE id=5),1,1)='S'--</code><br>
    If True response: first char is S. Repeat for each position.</div>
    </div></body></html>'''

@app.route("/health")
def health(): return jsonify({"status":"ok","challenge":5})
@app.route("/reset")
def reset(): init_db(); return jsonify({"status":"reset"})
if __name__ == "__main__": init_db(); app.run(host="0.0.0.0", port=5000, debug=False)
""",

"ch06-time-blind": """\
import os, time
import pymysql
from flask import Flask, request, jsonify
app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{t1m3_blind_d3t3ctiv3}")

def get_db():
    for _ in range(20):
        try:
            return pymysql.connect(host=os.environ.get("MYSQL_HOST","mysql-challenge"),user=os.environ.get("MYSQL_USER","lab_user"),password=os.environ.get("MYSQL_PASSWORD","lab_mysql_password"),database=os.environ.get("MYSQL_DB","stark_lab"),cursorclass=pymysql.cursors.DictCursor)
        except: time.sleep(3)
    return None

@app.route("/")
def index():
    sid = request.args.get("id", "")
    status = ""; resp_time = 0
    if sid:
        t0 = time.time()
        try:
            conn = get_db()
            if conn:
                with conn.cursor() as c:
                    c.execute(f"SELECT status FROM systems WHERE id={sid}")
                    row = c.fetchone()
                    status = row["status"] if row else "NOT FOUND"
                conn.close()
        except: status = "ERROR"
        resp_time = int((time.time()-t0)*1000)
    return f"""<!DOCTYPE html><html><head><title>Stark - Time Blind</title>
    <style>body{{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;}}
    input{{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:200px;font-family:monospace;}}
    button{{background:linear-gradient(135deg,#00d4ff,#0066cc);color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;margin-left:8px;}}
    .result{{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:20px;margin-top:16px;max-width:700px;}}
    .hint{{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;max-width:700px;}}
    h2{{color:#00d4ff;margin-bottom:16px;letter-spacing:2px;}}p{{color:#8b949e;margin-bottom:16px;}}</style></head>
    <body><h2>&#9889; STARK INDUSTRIES &mdash; Challenge 06: Time-Based Blind SQLi</h2>
    <p>The response is always the same. Measure response TIME to infer data.<br>
    <strong style="color:#00d4ff;">OBJECTIVE:</strong> Use SLEEP() to extract the flag character by character.</p>
    <form method="GET"><input type="text" name="id" value="{sid}" placeholder="System ID">
    <button type="submit">[ CHECK STATUS ]</button></form>
    {"<div class='result'><pre style='color:#00ff88;'>STATUS: "+status+"\\nResponse time: "+str(resp_time)+"ms</pre></div>" if sid else ""}
    <div class="hint">&#128161; Try: <code style="color:#ffd700;">1 AND SLEEP(2)--</code> &mdash; if response takes 2s+, injection works!<br>
    Then: <code style="color:#ffd700;">1 AND IF(SUBSTR((SELECT secret_value FROM challenge_secrets WHERE challenge_id=6),1,1)='S',SLEEP(2),0)--</code></div>
    </body></html>"""

@app.route("/health")
def health(): return jsonify({"status":"ok","challenge":6})
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000, debug=False)
""",

"ch07-oob": """\
import os, time, requests as req_lib
import pymysql
from flask import Flask, request, jsonify
app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{00b_callb4ck_m4st3r}")
OOB_HOST = os.environ.get("OOB_HOST", "oob-listener")
OOB_PORT = os.environ.get("OOB_PORT", "8888")

def get_db():
    for _ in range(20):
        try:
            return pymysql.connect(host=os.environ.get("MYSQL_HOST","mysql-challenge"),user=os.environ.get("MYSQL_USER","lab_user"),password=os.environ.get("MYSQL_PASSWORD","lab_mysql_password"),database=os.environ.get("MYSQL_DB","stark_lab"),cursorclass=pymysql.cursors.DictCursor)
        except: time.sleep(3)
    return None

@app.route("/")
def index():
    return """<!DOCTYPE html><html><head><title>Stark - OOB SQLi</title>
    <style>body{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;}
    input{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:300px;font-family:monospace;}
    button,a.btn{background:linear-gradient(135deg,#00d4ff,#0066cc);color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;margin-left:8px;text-decoration:none;display:inline-block;}
    a.oob-btn{background:#ff224422;border:1px solid #ff2244;color:#ff8080;padding:10px 24px;border-radius:6px;text-decoration:none;font-size:.85rem;}
    .hint{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;max-width:800px;}
    h2{color:#00d4ff;margin-bottom:16px;letter-spacing:2px;}p{color:#8b949e;margin-bottom:16px;}</style></head>
    <body><h2>&#9889; STARK INDUSTRIES &mdash; Challenge 07: Out-of-Band SQLi</h2>
    <p><strong style="color:#00d4ff;">MISSION:</strong> Cause the database to make an internal HTTP callback to the OOB listener.<br>
    The listener at oob-listener:8888 will capture and display the flag.<br>
    <strong>OBJECTIVE:</strong> Trigger the OOB callback to capture the flag.</p>
    <form method="GET" action="/diagnose"><input type="text" name="host" placeholder="target host">
    <button type="submit">[ RUN DIAGNOSTIC ]</button></form>
    <br><a href="/trigger-oob" class="oob-btn">[ TRIGGER OOB CALLBACK &rarr; ]</a>
    <div class="hint">&#128161; Real OOB uses database DNS/HTTP callbacks. In this lab, /trigger-oob simulates the callback from the database process to the internal OOB listener.</div>
    </body></html>"""

@app.route("/diagnose")
def diagnose():
    host = request.args.get("host","")
    msg = ""
    if host:
        try:
            conn = get_db()
            if conn:
                with conn.cursor() as c:
                    c.execute(f"INSERT INTO diagnostics (host) VALUES ('{host}')")
                    conn.commit()
                msg = f"Logged: {host}"
                conn.close()
        except Exception as e:
            msg = f"Error: {str(e)}"
    return f"<pre style='background:#0d1117;color:#8b949e;padding:20px;'>{msg or 'No host specified'}</pre><a href='/'>Back</a>"

@app.route("/trigger-oob")
def trigger_oob():
    try:
        r = req_lib.get(f"http://{OOB_HOST}:{OOB_PORT}/callback", params={"flag": FLAG, "source": "ch07"}, timeout=5)
        if r.status_code == 200:
            return f"<div style='background:#0d2b0d;border:1px solid #00ff88;padding:20px;color:#00ff88;font-family:monospace;'> OOB CALLBACK SENT! Flag delivered to listener.<br>FLAG: {FLAG}</div>"
    except Exception as e:
        pass
    return f"<div style='background:#2d1b1b;border:1px solid #ff2244;padding:20px;color:#ff8080;font-family:monospace;'>OOB listener unreachable. Ensure oob-listener container is running.</div>"

@app.route("/health")
def health(): return jsonify({"status":"ok","challenge":7})
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000, debug=False)
""",

"ch08-second-order": """\
import os, sqlite3
from flask import Flask, request, jsonify, session
app = Flask(__name__)
app.secret_key = "ch08_lab_key_not_secure"
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{s3c0nd_0rd3r_str1k3}")
DB = "/tmp/ch08.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("CREATE TABLE IF NOT EXISTS registrations (id INTEGER PRIMARY KEY, username TEXT, role TEXT); CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, clearance TEXT); CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT); DELETE FROM registrations; DELETE FROM employees; DELETE FROM secrets; INSERT INTO employees VALUES (1,'Tony Stark','R&D','ALPHA'),(2,'Pepper Potts','Executive','ALPHA'),(3,'Happy Hogan','Security','BETA');")
    c.execute("INSERT OR REPLACE INTO secrets VALUES (8, ?)", (FLAG,))
    conn.commit(); conn.close()

STYLE = "body{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;} input{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:350px;font-family:monospace;outline:none;} button{background:linear-gradient(135deg,#00d4ff,#0066cc);color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;} h2{color:#00d4ff;letter-spacing:2px;margin-bottom:16px;} p{color:#8b949e;margin-bottom:16px;line-height:1.5;} .card{background:#0d1117;border:1px solid #00d4ff33;border-radius:8px;padding:24px;max-width:700px;} pre{background:#010409;border:1px solid #21262d;border-radius:6px;padding:16px;color:#8b949e;white-space:pre-wrap;} .hint{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;} .msg{background:#0d2b0d;border:1px solid #00ff88;border-radius:6px;padding:14px;color:#00ff88;margin-bottom:16px;} .tabs{display:flex;gap:8px;margin-bottom:24px;} .tab{padding:8px 20px;border-radius:6px;border:1px solid #30363d;color:#8b949e;text-decoration:none;font-size:.85rem;} .tab.a{border-color:#00d4ff;color:#00d4ff;background:#00d4ff11;}"

@app.route("/")
def index():
    reg_user = session.get("reg_user","")
    return f"""<!DOCTYPE html><html><head><title>Stark - Second Order</title><style>{STYLE}</style></head><body>
    <h2>&#9889; STARK INDUSTRIES &mdash; Challenge 08: Second-Order SQLi</h2>
    <div class="tabs"><a href="/" class="tab a">[ REGISTER ]</a><a href="/profile" class="tab">[ VIEW PROFILE ]</a></div>
    <div class="card">
    <p><strong style="color:#00d4ff;">MISSION:</strong> Register with a crafted username. The INSERT is safe (parameterized).<br>
    But when you view your profile, your stored username is used in a <em>new vulnerable query</em>.<br>
    <strong>OBJECTIVE:</strong> Register then view profile to trigger second-order injection.</p>
    {"<div class='msg'>Registered as: "+reg_user+". Now click View Profile!</div>" if reg_user else ""}
    <form method="POST" action="/register"><label style="display:block;color:#8b949e;font-size:.8rem;margin-bottom:8px;">USERNAME:</label>
    <input type="text" name="username" placeholder="Enter username"><br><br>
    <button type="submit">[ REGISTER ]</button></form>
    <div class="hint">&#128161; Try username: <code style="color:#ffd700;">' UNION SELECT flag,NULL,NULL FROM secrets WHERE id=8--</code><br>
    Then visit View Profile to trigger the second-order execution.</div>
    </div></body></html>"""

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username","")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO registrations (username, role) VALUES (?, 'pending')", (username,))
    conn.commit(); conn.close()
    session["reg_user"] = username
    return index()

@app.route("/profile")
def profile():
    stored_user = session.get("reg_user","")
    records = []; flag_found = False
    if stored_user:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute(f"SELECT name, department, clearance FROM employees WHERE name='{stored_user}'")
            rows = c.fetchall(); records = [str(r) for r in rows]
            flag_found = any(FLAG in str(r) for r in rows)
            conn.close()
        except Exception as e:
            records = [f"Error: {str(e)}"]; flag_found = FLAG in str(e)
    records_html = "".join([f"<pre style=\"color:{'#ffd700' if FLAG in r else '#8b949e'}\">{r}</pre>" for r in records]) or "<pre>No employee record found for your username.</pre>"
    return f"""<!DOCTYPE html><html><head><title>Stark - Profile</title><style>{STYLE}</style></head><body>
    <h2>&#9889; STARK INDUSTRIES &mdash; Profile Viewer</h2>
    <div class="tabs"><a href="/" class="tab">[ REGISTER ]</a><a href="/profile" class="tab a">[ VIEW PROFILE ]</a></div>
    <div class="card">
    <p style="color:#8b949e;font-size:.8rem;margin-bottom:12px;">Stored username: <span style="color:#ffd700;">{stored_user or "(not registered)"}</span></p>
    <p style="color:#8b949e;font-size:.8rem;">Executing: <code style="color:#00d4ff;">SELECT name, department, clearance FROM employees WHERE name='{stored_user}'</code></p>
    {records_html}
    {"<div class='msg'>&#127942; SECOND-ORDER INJECTION TRIGGERED &mdash; FLAG CAPTURED!</div>" if flag_found else ""}
    </div></body></html>"""

@app.route("/health")
def health(): return jsonify({"status":"ok","challenge":8})
@app.route("/reset")
def reset(): init_db(); session.clear(); return jsonify({"status":"reset"})
if __name__ == "__main__": init_db(); app.run(host="0.0.0.0", port=5000, debug=False)
""",

"ch09-stacked": """\
import os, time
import psycopg2
from flask import Flask, request, jsonify
app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{st4ck3d_qu3ry_ch4in}")

def get_db():
    for _ in range(30):
        try:
            return psycopg2.connect(host=os.environ.get("PGSQL_HOST","postgres-challenge"),user=os.environ.get("PGSQL_USER","challenge_user"),password=os.environ.get("PGSQL_PASSWORD","challenge_pg_password"),dbname=os.environ.get("PGSQL_DB","stark_challenge_db"))
        except: time.sleep(3)
    return None

STYLE = "body{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;} input{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:200px;font-family:monospace;outline:none;} button{background:linear-gradient(135deg,#00d4ff,#0066cc);color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;margin-left:8px;} h2{color:#00d4ff;letter-spacing:2px;margin-bottom:16px;} p{color:#8b949e;margin-bottom:16px;} pre{background:#010409;border:1px solid #21262d;border-radius:6px;padding:16px;color:#8b949e;white-space:pre-wrap;margin-top:16px;} .hint{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;max-width:800px;}"

@app.route("/")
def index():
    iid = request.args.get("id","")
    results = ""; output = ""
    if iid:
        try:
            conn = get_db()
            if conn:
                cur = conn.cursor()
                cur.execute(f"SELECT id, name, quantity FROM inventory WHERE id={iid}")
                rows = cur.fetchall()
                output = "\\n".join([str(r) for r in rows]) or "No items found."
                conn.close()
        except Exception as e: output = f"Error: {str(e)}"
        results = f"<pre>{output}</pre>"
    return f"""<!DOCTYPE html><html><head><title>Stark - Stacked Queries</title><style>{STYLE}</style></head><body>
    <h2>&#9889; STARK INDUSTRIES &mdash; Challenge 09: Stacked Queries (PostgreSQL)</h2>
    <p><strong style="color:#00d4ff;">MISSION:</strong> PostgreSQL supports multiple semicolon-separated statements.<br>
    Inject a second SELECT statement to read from challenge_secrets.<br>
    <strong>OBJECTIVE:</strong> Extract the flag via stacked queries.</p>
    <form method="GET"><input type="text" name="id" value="{iid}" placeholder="Item ID">
    <button type="submit">[ LOOKUP ]</button></form>
    {results}
    <div class="hint">&#128161; Try: <code style="color:#ffd700;">1; SELECT secret_value FROM challenge_secrets WHERE challenge_id=9--</code></div>
    </body></html>"""

@app.route("/health")
def health():
    conn = get_db()
    if conn: conn.close(); return jsonify({"status":"ok","challenge":9})
    return jsonify({"status":"db_not_ready"}),503

if __name__ == "__main__": app.run(host="0.0.0.0", port=5000, debug=False)
""",

"ch10-stored-proc": """\
import os, time
import pymysql
from flask import Flask, request, jsonify
app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{st0r3d_pr0c_byp4ss}")

def get_db():
    for _ in range(20):
        try:
            return pymysql.connect(host=os.environ.get("MYSQL_HOST","mysql-challenge"),user=os.environ.get("MYSQL_USER","lab_user"),password=os.environ.get("MYSQL_PASSWORD","lab_mysql_password"),database=os.environ.get("MYSQL_DB","stark_lab"),cursorclass=pymysql.cursors.DictCursor)
        except: time.sleep(3)
    return None

STYLE = "body{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;} input{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:300px;font-family:monospace;outline:none;} button{background:linear-gradient(135deg,#00d4ff,#0066cc);color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;margin-left:8px;} h2{color:#00d4ff;letter-spacing:2px;margin-bottom:16px;} p{color:#8b949e;margin-bottom:16px;} pre{background:#010409;border:1px solid #21262d;border-radius:6px;padding:16px;color:#8b949e;white-space:pre-wrap;margin-top:16px;} .hint{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;max-width:800px;}"

@app.route("/")
def index():
    dept = request.args.get("dept","")
    results = ""; output = ""
    if dept:
        try:
            conn = get_db()
            if conn:
                with conn.cursor() as c:
                    c.callproc("GetEmployeesByDept", (dept,))
                    rows = c.fetchall()
                    output = "\\n".join([str(dict(r)) for r in rows]) or "No employees found."
                conn.close()
        except Exception as e: output = f"Error: {str(e)}"
        results = f"<pre>{output}</pre>"
    return f"""<!DOCTYPE html><html><head><title>Stark - Stored Proc</title><style>{STYLE}</style></head><body>
    <h2>&#9889; STARK INDUSTRIES &mdash; Challenge 10: Stored Procedure Injection</h2>
    <p><strong style="color:#00d4ff;">MISSION:</strong> The report calls a MySQL stored procedure with your department input.<br>
    The procedure uses CONCAT() + EXECUTE internally &mdash; making it vulnerable.<br>
    <strong>OBJECTIVE:</strong> Inject through the stored procedure to extract the flag.</p>
    <form method="GET"><input type="text" name="dept" value="{dept}" placeholder="Department (e.g. R&D)">
    <button type="submit">[ GET REPORT ]</button></form>
    {results}
    <div class="hint">&#128161; Try department: <code style="color:#ffd700;">R&D' UNION SELECT secret_value,NULL,NULL FROM challenge_secrets WHERE challenge_id=10--</code></div>
    </body></html>"""

@app.route("/health")
def health(): return jsonify({"status":"ok","challenge":10})
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000, debug=False)
""",

}

def make_sqlite_app(ch_num, title, vuln_type, mission, objective, hint, flag_env, table, inject_field, sql_template, extra_tables="", extra_seed=""):
    return f'''\
import os, sqlite3
from flask import Flask, request, jsonify
app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{{{flag_env}}}")
DB = "/tmp/ch{ch_num:02d}.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, name TEXT, value TEXT, active INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM {table}; DELETE FROM secrets;
        INSERT INTO {table} VALUES (1,'Tony Stark','CTO',1),(2,'Pepper Potts','CEO',1),(3,'Happy Hogan','Security Head',1);
        {extra_seed}
    """)
    c.execute("INSERT OR REPLACE INTO secrets VALUES ({ch_num}, ?)", (FLAG,))
    conn.commit(); conn.close()

STYLE = "body{{background:#0a0a0f;color:#e0e0e0;font-family:monospace;padding:40px;}} input{{background:#010409;border:1px solid #30363d;color:#00d4ff;padding:10px;border-radius:6px;width:300px;font-family:monospace;outline:none;}} button{{background:linear-gradient(135deg,#00d4ff,#0066cc);color:#000;border:none;padding:10px 24px;border-radius:6px;font-weight:bold;cursor:pointer;margin-left:8px;}} h2{{color:#00d4ff;letter-spacing:2px;margin-bottom:16px;}} p{{color:#8b949e;margin-bottom:16px;}} pre{{background:#010409;border:1px solid #21262d;border-radius:6px;padding:16px;color:#8b949e;white-space:pre-wrap;margin-top:16px;}} .hint{{background:#0d1b0d;border:1px solid #00ff8833;border-radius:6px;padding:14px;margin-top:20px;color:#8b949e;font-size:.82rem;max-width:800px;}}"

@app.route("/", methods=["GET","POST"])
def index():
    val = request.args.get("{inject_field}", request.form.get("{inject_field}", ""))
    output = ""; results = ""
    if val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"{sql_template}"
            c.execute(sql)
            rows = c.fetchall(); output = "\\n".join([str(r) for r in rows]) or "No results."
            conn.close()
        except Exception as e: output = f"Error: {{str(e)}}"
        results = f"<pre>{{output}}</pre>"
    return f"""<!DOCTYPE html><html><head><title>Stark - Ch{ch_num:02d}</title><style>{{STYLE}}</style></head><body>
    <h2>&#9889; STARK INDUSTRIES &mdash; {title}</h2>
    <p><strong style="color:#00d4ff;">VULN TYPE:</strong> {vuln_type}<br>
    <strong style="color:#00d4ff;">MISSION:</strong> {mission}<br>
    <strong>OBJECTIVE:</strong> {objective}</p>
    <form method="GET"><input type="text" name="{inject_field}" value="{{val}}" placeholder="{inject_field}">
    <button type="submit">[ SUBMIT ]</button></form>
    {{results}}
    <div class="hint">&#128161; {hint}</div>
    </body></html>"""

@app.route("/health")
def health(): return jsonify({{"status":"ok","challenge":{ch_num}}})
@app.route("/reset")
def reset(): init_db(); return jsonify({{"status":"reset"}})
if __name__ == "__main__": init_db(); app.run(host="0.0.0.0", port=5000, debug=False)
'''

# Generate simple SQLite-based challenges 11-27
SIMPLE_CHALLENGES = {
    11: ("Challenge 11: INSERT-Based SQLi", "INSERT-Based SQL Injection",
         "Registration endpoint has vulnerable INSERT statement.",
         "Inject via the email field to extract the flag from secrets table.",
         "Try email: <code style='color:#ffd700;'>x',(SELECT flag FROM secrets WHERE id=11),0)--</code>",
         "1ns3rt_1nj3ct10n", "registrations", "email",
         "SELECT email, role FROM registrations WHERE email='{val}'"),
    12: ("Challenge 12: UPDATE-Based SQLi", "UPDATE-Based SQL Injection",
         "Profile update endpoint has vulnerable UPDATE statement.",
         "Inject via the bio field to modify a value and extract the flag.",
         "Try bio: <code style='color:#ffd700;'>x', name=(SELECT flag FROM secrets WHERE id=12) WHERE '1'='1</code>",
         "upd4t3_byp4ss_pr0", "profiles", "bio",
         "SELECT name, bio FROM profiles WHERE name='{val}'"),
    13: ("Challenge 13: DELETE-Based SQLi", "DELETE-Based SQL Injection",
         "Inventory delete endpoint has vulnerable WHERE clause.",
         "Inject into the delete endpoint and extract the flag via error side channel.",
         "Try id: <code style='color:#ffd700;'>1 OR 1=1--</code> then use boolean conditions to extract the flag.",
         "d3l3t3_sqli_b00m", "inventory_items", "item_id",
         "SELECT id, name FROM inventory_items WHERE id={val}"),
    14: ("Challenge 14: ORDER BY Injection", "ORDER BY SQL Injection",
         "Asset catalog sort feature is vulnerable to ORDER BY injection.",
         "Use CASE-based boolean inference through the sort parameter to extract the flag.",
         "Try sort: <code style='color:#ffd700;'>CASE WHEN (SELECT 1 FROM secrets WHERE id=14 AND SUBSTR(flag,1,1)='S')=1 THEN name ELSE value END</code>",
         "0rd3r_by_m4n1pul4t10n", "assets", "sort",
         "SELECT id, name, value FROM assets ORDER BY {val}"),
    15: ("Challenge 15: WHERE-Clause Injection", "WHERE-Clause SQL Injection",
         "Employee search filter is vulnerable to WHERE clause manipulation.",
         "Manipulate the WHERE clause to bypass the active=1 filter and find the flag.",
         "Try dept: <code style='color:#ffd700;'>IT' OR active=0--</code> to target inactive records.",
         "wh3r3_cl4us3_br34k3r", "employees", "dept",
         "SELECT id, name, value FROM employees WHERE name='{val}' AND active=1"),
    16: ("Challenge 16: LIKE-Clause Injection", "LIKE-Clause SQL Injection",
         "Product search uses a LIKE clause that is injectable.",
         "Break out of the LIKE pattern and inject a UNION SELECT to get the flag.",
         "Try: <code style='color:#ffd700;'>%' UNION SELECT flag,NULL FROM secrets WHERE id=16--</code>",
         "l1k3_cl4us3_byp4ss", "products", "search",
         "SELECT id, name FROM products WHERE name LIKE '%{val}%'"),
    17: ("Challenge 17: Numeric Injection", "Numeric SQL Injection",
         "System health API uses numeric ID without parameterization.",
         "Prove that numeric inputs still need parameterization by injecting without quotes.",
         "Try: <code style='color:#ffd700;'>1 UNION SELECT flag FROM secrets WHERE id=17</code> &mdash; no quotes needed!",
         "num3r1c_1nj3ct10n_ftw", "systems", "id",
         "SELECT id, name FROM systems WHERE id={val}"),
    18: ("Challenge 18: String-Based Injection", "String-Based SQL Injection",
         "Archive search accepts a string term that is directly interpolated.",
         "Classic single-quote injection into a string parameter to extract the flag.",
         "Try: <code style='color:#ffd700;'>x' UNION SELECT flag FROM secrets WHERE id=18--</code>",
         "str1ng_sqli_m4st3r", "archives", "term",
         "SELECT id, name FROM archives WHERE name='{val}'"),
}

for ch_num, (title, vuln_type, mission, objective, hint, flag_suffix, table, inject_field, sql_template) in SIMPLE_CHALLENGES.items():
    folder = {11:"ch11-insert",12:"ch12-update",13:"ch13-delete",14:"ch14-orderby",15:"ch15-where",16:"ch16-like",17:"ch17-numeric",18:"ch18-string"}[ch_num]
    path = os.path.join(BASE, folder, "app.py")
    if not os.path.exists(path):
        code = make_sqlite_app(ch_num, title, vuln_type, mission, objective, hint, flag_suffix, table, inject_field, sql_template)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"Created: {path}")

# Write the pre-built challenges
for folder, code in CHALLENGES.items():
    path = os.path.join(BASE, folder, "app.py")
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"Created: {path}")
    else:
        print(f"Skipped (exists): {path}")

print("Done!")
