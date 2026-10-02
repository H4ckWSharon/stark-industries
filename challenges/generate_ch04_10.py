"""
Generate all remaining challenge app.py files (04-30).
"""
import os

BASE = r"c:\Users\sharo\Desktop\stark industries\challenges"

# ─── Shared helper for Flask HTML pages ───────────────────────────────────────

COMMON_STYLE = """
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
input[type=text], input[type=password] { background: #010409; border: 1px solid #30363d; color: #00d4ff; padding: 10px 14px; border-radius: 6px; width: 300px; font-family: monospace; font-size: 0.95rem; outline: none; }
input:focus { border-color: #00d4ff; }
button { background: linear-gradient(135deg, #00d4ff, #0066cc); color: #0a0a0f; border: none; padding: 10px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-left: 10px; }
.result-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 20px; }
pre { background: #010409; border: 1px solid #21262d; border-radius: 6px; padding: 16px; color: #8b949e; font-size: 0.85rem; white-space: pre-wrap; overflow-x: auto; }
.error-output { background: #2d1b1b; border: 1px solid #ff2244; border-radius: 6px; padding: 16px; color: #ff8080; font-size: 0.85rem; white-space: pre-wrap; }
.flag-found { background: #0d2b0d; border: 1px solid #00ff88; border-radius: 6px; padding: 16px; color: #00ff88; font-size: 1rem; }
.hint-box { background: #0d1b0d; border: 1px solid #00ff8833; border-radius: 6px; padding: 14px; margin-top: 20px; color: #8b949e; font-size: 0.82rem; line-height: 1.5; }
.true-resp { background: #0d2b0d; border: 1px solid #00ff88; padding: 16px; border-radius: 6px; color: #00ff88; }
.false-resp { background: #2d1b1b; border: 1px solid #ff2244; padding: 16px; border-radius: 6px; color: #ff8080; }
"""

def write_if_missing(path, content):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created: {path}")
    else:
        print(f"Skipped (exists): {path}")


# ─── Challenge 04: UNION-Based ─────────────────────────────────────────────
CH04 = '''"""
STARK INDUSTRIES SQL — Challenge 04: UNION-Based SQL Injection (MySQL)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os, time, pymysql
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{un10n_m4st3r_s3l3ct}")

def get_db():
    for _ in range(20):
        try:
            return pymysql.connect(
                host=os.environ.get("MYSQL_HOST","mysql-challenge"),
                user=os.environ.get("MYSQL_USER","lab_user"),
                password=os.environ.get("MYSQL_PASSWORD","lab_mysql_password"),
                database=os.environ.get("MYSQL_DB","stark_lab"),
                cursorclass=pymysql.cursors.DictCursor)
        except: time.sleep(3)
    return None

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Stark Industries — Catalog Search</title>
<style>""" + COMMON_STYLE + """</style></head><body>
<div class="header"><div class="logo">⚡ STARK INDUSTRIES</div>
<div>PRODUCT CATALOG</div><div class="badge">CHALLENGE 04 — UNION</div>
<div style="margin-left:auto;color:#ff2244;font-size:0.8rem;">⚠ INTENTIONALLY VULNERABLE</div></div>
<div class="container">
<div class="mission"><div class="mission-title">// MISSION 04 — UNION-BASED SQL INJECTION</div>
<div class="mission-text">The catalog search is injectable via UNION. Determine column count, find displayed columns,
then use UNION SELECT to pull the flag from another table.<br><br>
<strong style="color:#00d4ff;">OBJECTIVE:</strong> Use UNION SELECT to retrieve the flag from challenge_secrets.</div></div>
<div class="search-box"><form method="GET">
<label style="color:#8b949e;font-size:0.8rem;">SEARCH BY CATEGORY:</label><br><br>
<input type="text" name="cat" value="{{ cat }}" placeholder="e.g. Power or inject">
<button type="submit">[ SEARCH ]</button></form></div>
{% if results is not none %}
<div class="result-box"><pre>{% for r in results %}{{ r }}
{% endfor %}{% if not results %}No results found.{% endif %}</pre></div>
{% endif %}
<div class="hint-box">💡 Query: <code style="color:#00d4ff;">SELECT id, name, description FROM products WHERE category = \'{{ cat or "input" }}\'</code></div>
</div></body></html>"""

@app.route("/", methods=["GET"])
def index():
    cat = request.args.get("cat", "")
    results = None
    if cat:
        try:
            conn = get_db()
            if not conn: return "DB not ready", 503
            with conn.cursor() as c:
                sql = f"SELECT id, name, description FROM products WHERE category = \'{cat}\'"
                c.execute(sql)
                results = [str(dict(r)) for r in c.fetchall()]
            conn.close()
        except Exception as e:
            results = [f"Error: {str(e)}"]
    return render_template_string(PAGE, cat=cat, results=results)

@app.route("/health")
def health():
    return jsonify({"status":"ok","challenge":4})

@app.route("/reset")
def reset():
    return jsonify({"status":"reset"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

# ─── Challenge 05: Boolean Blind ───────────────────────────────────────────
CH05 = '''"""
STARK INDUSTRIES SQL — Challenge 05: Boolean-Based Blind SQL Injection (SQLite)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os, sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{bl1nd_b00l_hunt3r}")
DB = "/tmp/ch05.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, active INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM users; DELETE FROM secrets;
        INSERT INTO users VALUES (1,'tony.stark',1),(2,'pepper.potts',1),(3,'happy.hogan',1);
    """)
    c.execute("INSERT OR REPLACE INTO secrets VALUES (5, ?)", (FLAG,))
    conn.commit(); conn.close()

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Stark Industries — User Lookup</title>
<style>""" + COMMON_STYLE + """</style></head><body>
<div class="header"><div class="logo">⚡ STARK INDUSTRIES</div>
<div>USER LOOKUP</div><div class="badge">CHALLENGE 05 — BOOLEAN BLIND</div>
<div style="margin-left:auto;color:#ff2244;font-size:0.8rem;">⚠ BLIND INJECTION LAB</div></div>
<div class="container">
<div class="mission"><div class="mission-title">// MISSION 05 — BOOLEAN-BASED BLIND SQL INJECTION</div>
<div class="mission-text">The response shows only "User found" or "User not found" — no data is displayed.
Use boolean inference to extract the flag character by character.<br><br>
<strong style="color:#00d4ff;">OBJECTIVE:</strong> Infer the flag using boolean conditions.</div></div>
<div class="search-box"><form method="GET">
<label style="color:#8b949e;font-size:0.8rem;">USERNAME LOOKUP:</label><br><br>
<input type="text" name="name" value="{{ name }}" placeholder="e.g. tony.stark">
<button type="submit">[ LOOKUP ]</button></form></div>
{% if name %}
<div class="result-box">
{% if found %}
<div class="true-resp">✓ USER FOUND — The condition evaluated as TRUE</div>
{% else %}
<div class="false-resp">✗ USER NOT FOUND — The condition evaluated as FALSE</div>
{% endif %}
</div>
{% endif %}
<div class="hint-box">💡 Try: <code style="color:#ffd700;">admin\' AND 1=1--</code> (true) vs <code style="color:#ffd700;">admin\' AND 1=2--</code> (false)</div>
</div></body></html>"""

@app.route("/", methods=["GET"])
def index():
    name = request.args.get("name", "")
    found = False
    if name:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"SELECT id FROM users WHERE username=\'{name}\'"
            c.execute(sql)
            found = c.fetchone() is not None
            conn.close()
        except: found = False
    return render_template_string(PAGE, name=name, found=found)

@app.route("/health")
def health():
    return jsonify({"status":"ok","challenge":5})

@app.route("/reset")
def reset():
    init_db()
    return jsonify({"status":"reset"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

# ─── Challenge 06: Time-Based Blind ────────────────────────────────────────
CH06 = '''"""
STARK INDUSTRIES SQL — Challenge 06: Time-Based Blind SQL Injection (MySQL)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os, time, pymysql
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{t1m3_blind_d3t3ctiv3}")

def get_db():
    for _ in range(20):
        try:
            return pymysql.connect(
                host=os.environ.get("MYSQL_HOST","mysql-challenge"),
                user=os.environ.get("MYSQL_USER","lab_user"),
                password=os.environ.get("MYSQL_PASSWORD","lab_mysql_password"),
                database=os.environ.get("MYSQL_DB","stark_lab"),
                cursorclass=pymysql.cursors.DictCursor)
        except: time.sleep(3)
    return None

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Stark Industries — System Status</title>
<style>""" + COMMON_STYLE + """</style></head><body>
<div class="header"><div class="logo">⚡ STARK INDUSTRIES</div>
<div>SYSTEM STATUS</div><div class="badge">CHALLENGE 06 — TIME BLIND</div></div>
<div class="container">
<div class="mission"><div class="mission-title">// MISSION 06 — TIME-BASED BLIND SQL INJECTION</div>
<div class="mission-text">The response is always the same — "OPERATIONAL" or "NOT FOUND".
Use MySQL\'s SLEEP() function to infer data through response timing.<br><br>
<strong style="color:#00d4ff;">OBJECTIVE:</strong> Extract the flag using conditional SLEEP() delays.</div></div>
<div class="search-box"><form method="GET">
<label style="color:#8b949e;font-size:0.8rem;">SYSTEM ID:</label><br><br>
<input type="text" name="id" value="{{ sid }}" placeholder="e.g. 1">
<button type="submit">[ CHECK STATUS ]</button></form></div>
{% if sid %}
<div class="result-box">
<pre style="color:#00ff88;">STATUS: {{ status }}
Response time: {{ resp_time }}ms</pre>
</div>
{% endif %}
<div class="hint-box">
💡 Try: <code style="color:#ffd700;">1 AND SLEEP(2)--</code> — if response takes 2+ seconds, injection works.<br>
Then: <code style="color:#ffd700;">1 AND IF(1=1,SLEEP(2),0)--</code> for conditional timing.
</div>
</div></body></html>"""

@app.route("/", methods=["GET"])
def index():
    sid = request.args.get("id","")
    status = None; resp_time = None
    if sid:
        t0 = time.time()
        try:
            conn = get_db()
            if not conn: return "DB not ready",503
            with conn.cursor() as c:
                sql = f"SELECT status FROM systems WHERE id={sid}"
                c.execute(sql)
                row = c.fetchone()
                status = row["status"] if row else "NOT FOUND"
            conn.close()
        except: status = "ERROR"
        resp_time = int((time.time()-t0)*1000)
    return render_template_string(PAGE, sid=sid, status=status, resp_time=resp_time)

@app.route("/health")
def health():
    return jsonify({"status":"ok","challenge":6})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

# ─── Challenge 07: OOB ─────────────────────────────────────────────────────
CH07 = '''"""
STARK INDUSTRIES SQL — Challenge 07: Out-of-Band SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
Uses internal OOB listener at oob-listener:8888.
"""
import os, time, pymysql, requests as req_lib
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{00b_callb4ck_m4st3r}")
OOB_HOST = os.environ.get("OOB_HOST","oob-listener")
OOB_PORT = os.environ.get("OOB_PORT","8888")

def get_db():
    for _ in range(20):
        try:
            return pymysql.connect(
                host=os.environ.get("MYSQL_HOST","mysql-challenge"),
                user=os.environ.get("MYSQL_USER","lab_user"),
                password=os.environ.get("MYSQL_PASSWORD","lab_mysql_password"),
                database=os.environ.get("MYSQL_DB","stark_lab"),
                cursorclass=pymysql.cursors.DictCursor)
        except: time.sleep(3)
    return None

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Stark Industries — Network Diagnostics</title>
<style>""" + COMMON_STYLE + """</style></head><body>
<div class="header"><div class="logo">⚡ STARK INDUSTRIES</div>
<div>NETWORK DIAGNOSTICS</div><div class="badge">CHALLENGE 07 — OOB</div></div>
<div class="container">
<div class="mission"><div class="mission-title">// MISSION 07 — OUT-OF-BAND SQL INJECTION</div>
<div class="mission-text">
The diagnostic system pings internal hosts. The database processes your input.<br>
An OOB listener at <code style="color:#00d4ff;">oob-listener:8888</code> is waiting for a callback.<br><br>
<strong style="color:#00d4ff;">OBJECTIVE:</strong> Trigger the internal OOB listener to capture the flag.<br>
Use the /trigger-oob endpoint or inject into the /diagnose endpoint.
</div></div>
<div class="search-box"><form method="GET" action="/diagnose">
<label style="color:#8b949e;font-size:0.8rem;">TARGET HOST:</label><br><br>
<input type="text" name="host" value="{{ host }}" placeholder="e.g. jarvis.stark-lab.test">
<button type="submit">[ RUN DIAGNOSTIC ]</button></form></div>
{% if result %}
<div class="result-box"><pre>{{ result }}</pre></div>
{% endif %}
<div style="margin-top:16px;background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:20px;">
<div style="color:#00d4ff;font-size:0.8rem;margin-bottom:12px;">// OOB TRIGGER</div>
<p style="color:#8b949e;font-size:0.85rem;margin-bottom:12px;">Manually trigger the OOB callback to the internal listener:</p>
<a href="/trigger-oob" style="background:#ff224422;border:1px solid #ff2244;color:#ff8080;padding:10px 20px;border-radius:6px;text-decoration:none;font-size:0.85rem;">[ TRIGGER OOB CALLBACK ]</a>
{% if oob_flag %}<div class="flag-found" style="margin-top:16px;">🏆 OOB FLAG CAPTURED: {{ oob_flag }}</div>{% endif %}
</div>
<div class="hint-box">💡 The /trigger-oob endpoint demonstrates the OOB technique. Real OOB uses DNS/HTTP callbacks from the database process itself.</div>
</div></body></html>"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(PAGE, host="", result=None, oob_flag=None)

@app.route("/diagnose", methods=["GET"])
def diagnose():
    host = request.args.get("host","")
    result = None
    if host:
        try:
            conn = get_db()
            if not conn: return "DB not ready",503
            with conn.cursor() as c:
                sql = f"INSERT INTO diagnostics (host) VALUES (\'{host}\')"
                c.execute(sql)
                conn.commit()
                result = f"Diagnostic logged for host: {host}"
            conn.close()
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template_string(PAGE, host=host, result=result, oob_flag=None)

@app.route("/trigger-oob")
def trigger_oob():
    """Simulate OOB callback — sends flag to internal listener."""
    try:
        r = req_lib.get(f"http://{OOB_HOST}:{OOB_PORT}/callback",
            params={"flag": FLAG, "source": "ch07-database-oob"}, timeout=5)
        if r.status_code == 200:
            return render_template_string(PAGE, host="", result=None, oob_flag=FLAG)
    except Exception as e:
        pass
    return render_template_string(PAGE, host="", result="OOB listener not reachable — check Docker network.", oob_flag=None)

@app.route("/health")
def health():
    return jsonify({"status":"ok","challenge":7})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

# ─── Challenge 08: Second-Order ────────────────────────────────────────────
CH08 = '''"""
STARK INDUSTRIES SQL — Challenge 08: Second-Order SQL Injection (SQLite)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os, sqlite3
from flask import Flask, request, jsonify, render_template_string, session

app = Flask(__name__)
app.secret_key = "ch08_lab_key"
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{s3c0nd_0rd3r_str1k3}")
DB = "/tmp/ch08.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS registrations (id INTEGER PRIMARY KEY, username TEXT, role TEXT, active INTEGER DEFAULT 1);
        CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, clearance TEXT);
        CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM registrations; DELETE FROM employees; DELETE FROM secrets;
        INSERT INTO employees VALUES (1,\'Tony Stark\',\'R&D\',\'ALPHA\'),(2,\'Pepper Potts\',\'Executive\',\'ALPHA\'),(3,\'Happy Hogan\',\'Security\',\'BETA\');
    """)
    c.execute("INSERT OR REPLACE INTO secrets VALUES (8, ?)", (FLAG,))
    conn.commit(); conn.close()

REG_PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Stark Industries — HR Registration</title>
<style>""" + COMMON_STYLE + """
.card { background: #0d1117; border: 1px solid #00d4ff33; border-radius: 12px; padding: 32px; max-width: 600px; margin: 0 auto; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.input-group label { display: block; color: #8b949e; font-size: 0.8rem; margin-bottom: 6px; }
.input-group input { width: 100%; }
.big-btn { width: 100%; padding: 14px; margin-top: 8px; }
.tabs { display: flex; gap: 8px; margin-bottom: 24px; }
.tab { padding: 8px 20px; border-radius: 6px; border: 1px solid #30363d; cursor: pointer; color: #8b949e; font-size: 0.85rem; text-decoration: none; }
.tab.active { border-color: #00d4ff; color: #00d4ff; background: #00d4ff11; }
</style></head><body>
<div class="header"><div class="logo">⚡ STARK INDUSTRIES</div>
<div>HR PORTAL</div><div class="badge">CHALLENGE 08 — SECOND ORDER</div></div>
<div class="container">
<div class="mission"><div class="mission-title">// MISSION 08 — SECOND-ORDER SQL INJECTION</div>
<div class="mission-text">Register with a crafted username. The registration INSERT is safe.<br>
But when you view your profile, your stored username is used in a new vulnerable query.<br><br>
<strong style="color:#00d4ff;">OBJECTIVE:</strong> Register → View Profile → Trigger second-order injection.</div></div>
<div class="tabs">
  <a href="/" class="tab {% if tab==\'reg\' %}active{% endif %}">[ REGISTER ]</a>
  <a href="/profile" class="tab {% if tab==\'profile\' %}active{% endif %}">[ VIEW PROFILE ]</a>
</div>
<div class="card">
{% if msg %}<div style="background:#0d2b0d;border:1px solid #00ff88;border-radius:6px;padding:14px;color:#00ff88;margin-bottom:16px;">{{ msg }}</div>{% endif %}
{% if error %}<div class="error-output" style="margin-bottom:16px;">{{ error }}</div>{% endif %}
<form method="POST" action="/register">
<div class="two-col">
  <div class="input-group"><label>// USERNAME</label><input type="text" name="username" value="{{ username }}" placeholder="Enter username"></div>
  <div class="input-group"><label>// DEPARTMENT</label><input type="text" name="dept" value="R&D" placeholder="Department"></div>
</div>
<button type="submit" class="big-btn">[ REGISTER EMPLOYEE ]</button>
</form>
</div>
<div class="hint-box">💡 Try registering with username: <code style="color:#ffd700;">\' UNION SELECT flag,NULL,NULL FROM secrets WHERE id=8--</code></div>
</div></body></html>"""

PROFILE_PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Stark Industries — Employee Profile</title>
<style>""" + COMMON_STYLE + """</style></head><body>
<div class="header"><div class="logo">⚡ STARK INDUSTRIES</div><div>HR PORTAL — PROFILE</div><div class="badge">CHALLENGE 08</div></div>
<div class="container">
<div class="tabs" style="margin-bottom:24px;">
  <a href="/" style="padding:8px 20px;border-radius:6px;border:1px solid #30363d;color:#8b949e;text-decoration:none;font-size:0.85rem;">[ REGISTER ]</a>
  <a href="/profile" style="padding:8px 20px;border-radius:6px;border:1px solid #00d4ff;color:#00d4ff;background:#00d4ff11;text-decoration:none;font-size:0.85rem;">[ VIEW PROFILE ]</a>
</div>
{% if not session_user %}<div style="color:#8b949e;padding:20px;">Register first to view profile.</div>
{% else %}
<div class="result-box">
<div style="color:#8b949e;font-size:0.8rem;margin-bottom:12px;">// EMPLOYEE RECORD LOOKUP — Using stored username: <span style="color:#ffd700;">{{ session_user }}</span></div>
{% if records %}
{% for r in records %}
<pre style="{% if flag_found %}color:#ffd700;{% endif %}">{{ r }}</pre>
{% endfor %}
{% else %}<pre>No employee record found.</pre>{% endif %}
</div>
{% if flag_found %}<div class="flag-found" style="margin-top:16px;">🏆 SECOND-ORDER INJECTION TRIGGERED — FLAG CAPTURED!</div>{% endif %}
{% endif %}
</div></body></html>"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(REG_PAGE, tab="reg", msg=None, error=None, username="")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username","")
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        # Safe INSERT — parameterized
        c.execute("INSERT INTO registrations (username, role) VALUES (?, \'pending\')", (username,))
        conn.commit(); conn.close()
        session["reg_user"] = username
        return render_template_string(REG_PAGE, tab="reg",
            msg=f"Registered as: {username}. Now view your profile!", error=None, username=username)
    except Exception as e:
        return render_template_string(REG_PAGE, tab="reg", msg=None, error=str(e), username=username)

@app.route("/profile")
def profile():
    stored_user = session.get("reg_user","")
    records = []; flag_found = False
    if stored_user:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            # INTENTIONALLY VULNERABLE — uses stored username directly
            sql = f"SELECT name, department, clearance FROM employees WHERE name=\'{stored_user}\'"
            c.execute(sql)
            rows = c.fetchall()
            records = [str(r) for r in rows]
            if any(FLAG in str(r) for r in rows): flag_found = True
            conn.close()
        except Exception as e:
            records = [f"Error: {str(e)}"]
            if FLAG in str(e): flag_found = True
    return render_template_string(PROFILE_PAGE, session_user=stored_user, records=records, flag_found=flag_found)

@app.route("/health")
def health():
    return jsonify({"status":"ok","challenge":8})

@app.route("/reset")
def reset():
    init_db(); session.clear()
    return jsonify({"status":"reset"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

# ─── Challenge 09: Stacked Queries (PostgreSQL) ────────────────────────────
CH09 = '''"""
STARK INDUSTRIES SQL — Challenge 09: Stacked Queries (PostgreSQL)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os, time, psycopg2
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{st4ck3d_qu3ry_ch4in}")

def get_db():
    for _ in range(30):
        try:
            return psycopg2.connect(
                host=os.environ.get("PGSQL_HOST","postgres-challenge"),
                user=os.environ.get("PGSQL_USER","challenge_user"),
                password=os.environ.get("PGSQL_PASSWORD","challenge_pg_password"),
                dbname=os.environ.get("PGSQL_DB","stark_challenge_db"))
        except: time.sleep(3)
    return None

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Stark Industries — Data Entry</title>
<style>""" + COMMON_STYLE + """</style></head><body>
<div class="header"><div class="logo">⚡ STARK INDUSTRIES</div>
<div>INVENTORY LOOKUP</div><div class="badge">CHALLENGE 09 — STACKED</div></div>
<div class="container">
<div class="mission"><div class="mission-title">// MISSION 09 — STACKED QUERIES</div>
<div class="mission-text">PostgreSQL supports multiple semicolon-separated statements.<br>
Inject a second statement to read from challenge_secrets.<br><br>
<strong style="color:#00d4ff;">OBJECTIVE:</strong> Use stacked queries to extract the flag.</div></div>
<div class="search-box"><form method="GET">
<label style="color:#8b949e;font-size:0.8rem;">INVENTORY ITEM ID:</label><br><br>
<input type="text" name="id" value="{{ iid }}" placeholder="e.g. 1">
<button type="submit">[ LOOKUP ]</button></form></div>
{% if results is not none %}
<div class="result-box"><pre>{% for r in results %}{{ r }}
{% endfor %}{% if not results %}No items found.{% endif %}</pre></div>
{% endif %}
<div class="hint-box">💡 Try: <code style="color:#ffd700;">1; SELECT secret_value FROM challenge_secrets WHERE challenge_id=9--</code></div>
</div></body></html>"""

@app.route("/", methods=["GET"])
def index():
    iid = request.args.get("id","")
    results = None
    if iid:
        try:
            conn = get_db()
            if not conn: return "DB not ready",503
            cur = conn.cursor()
            sql = f"SELECT id, name, quantity FROM inventory WHERE id={iid}"
            cur.execute(sql)
            rows = cur.fetchall()
            results = [str(r) for r in rows]
            conn.close()
        except Exception as e:
            results = [f"Error: {str(e)}"]
    return render_template_string(PAGE, iid=iid, results=results)

@app.route("/health")
def health():
    conn = get_db()
    if conn:
        conn.close()
        return jsonify({"status":"ok","challenge":9})
    return jsonify({"status":"db_not_ready"}),503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

# ─── Challenge 10: Stored Procedure (MySQL) ────────────────────────────────
CH10 = '''"""
STARK INDUSTRIES SQL — Challenge 10: Stored Procedure Injection (MySQL)
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os, time, pymysql
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{st0r3d_pr0c_byp4ss}")

def get_db():
    for _ in range(20):
        try:
            return pymysql.connect(
                host=os.environ.get("MYSQL_HOST","mysql-challenge"),
                user=os.environ.get("MYSQL_USER","lab_user"),
                password=os.environ.get("MYSQL_PASSWORD","lab_mysql_password"),
                database=os.environ.get("MYSQL_DB","stark_lab"),
                cursorclass=pymysql.cursors.DictCursor)
        except: time.sleep(3)
    return None

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Stark Industries — Employee Report</title>
<style>""" + COMMON_STYLE + """</style></head><body>
<div class="header"><div class="logo">⚡ STARK INDUSTRIES</div>
<div>EMPLOYEE REPORTS</div><div class="badge">CHALLENGE 10 — STORED PROC</div></div>
<div class="container">
<div class="mission"><div class="mission-title">// MISSION 10 — STORED PROCEDURE INJECTION</div>
<div class="mission-text">The report system calls a MySQL stored procedure with your department input.<br>
The procedure uses dynamic SQL internally — making it vulnerable.<br><br>
<strong style="color:#00d4ff;">OBJECTIVE:</strong> Inject into the department parameter to extract the flag.</div></div>
<div class="search-box"><form method="GET">
<label style="color:#8b949e;font-size:0.8rem;">DEPARTMENT:</label><br><br>
<input type="text" name="dept" value="{{ dept }}" placeholder="e.g. R&D">
<button type="submit">[ RUN REPORT ]</button></form></div>
{% if results is not none %}
<div class="result-box"><pre>{% for r in results %}{{ r }}
{% endfor %}{% if not results %}No employees found in that department.{% endif %}</pre></div>
{% endif %}
<div class="hint-box">💡 Try: <code style="color:#ffd700;">R&D\' UNION SELECT secret_value,NULL,NULL FROM challenge_secrets WHERE challenge_id=10--</code></div>
</div></body></html>"""

@app.route("/", methods=["GET"])
def index():
    dept = request.args.get("dept","")
    results = None
    if dept:
        try:
            conn = get_db()
            if not conn: return "DB not ready",503
            with conn.cursor() as c:
                c.callproc("GetEmployeesByDept", (dept,))
                rows = c.fetchall()
                results = [str(dict(r)) for r in rows]
            conn.close()
        except Exception as e:
            results = [f"Error: {str(e)}"]
    return render_template_string(PAGE, dept=dept, results=results)

@app.route("/health")
def health():
    return jsonify({"status":"ok","challenge":10})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

# Write challenge files
challenges_to_create = {
    "ch04-union": CH04,
    "ch05-boolean-blind": CH05,
    "ch06-time-blind": CH06,
    "ch07-oob": CH07,
    "ch08-second-order": CH08,
    "ch09-stacked": CH09,
    "ch10-stored-proc": CH10,
}

for folder, code in challenges_to_create.items():
    path = os.path.join(BASE, folder, "app.py")
    write_if_missing(path, code)

# Fix ch07 requirements (needs requests)
ch07_req = os.path.join(BASE, "ch07-oob", "requirements.txt")
if not os.path.exists(ch07_req) or "requests" not in open(ch07_req).read():
    with open(ch07_req, "w") as f:
        f.write("flask==3.0.3\nPyMySQL==1.1.0\nrequests==2.31.0\n")
    print("Updated ch07 requirements")

print("Challenges 04-10 app.py created!")
'''
