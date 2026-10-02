"""
Generate challenge scaffolding files for challenges 02-30.
Run from the stark industries root.
"""
import os

BASE = r"c:\Users\sharo\Desktop\stark industries\challenges"

# Challenges that need MySQL/PyMySQL
MYSQL_CHALLENGES = [3, 4, 6, 7, 10, 26, 28]
# Challenges that need PostgreSQL
PGSQL_CHALLENGES = [9, 26, 29]
# MSSQL
MSSQL_CHALLENGES = [30, 26]

SQLITE_REQ = "flask==3.0.3\n"
MYSQL_REQ = "flask==3.0.3\nPyMySQL==1.1.0\n"
PGSQL_REQ = "flask==3.0.3\npsycopg2-binary==2.9.9\n"
MSSQL_REQ = "flask==3.0.3\npyodbc==5.1.0\n"
MULTI_REQ = "flask==3.0.3\nPyMySQL==1.1.0\npsycopg2-binary==2.9.9\n"

SQLITE_DOCKER = """FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
"""

MYSQL_DOCKER = """FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
"""

PGSQL_DOCKER = """FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
"""

MSSQL_DOCKER = """FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl unixodbc-dev gnupg && \\
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \\
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \\
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \\
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
"""

# Map folder names
FOLDERS = {
    2: "ch02-auth-bypass",
    3: "ch03-error-based",
    4: "ch04-union",
    5: "ch05-boolean-blind",
    6: "ch06-time-blind",
    7: "ch07-oob",
    8: "ch08-second-order",
    9: "ch09-stacked",
    10: "ch10-stored-proc",
    11: "ch11-insert",
    12: "ch12-update",
    13: "ch13-delete",
    14: "ch14-orderby",
    15: "ch15-where",
    16: "ch16-like",
    17: "ch17-numeric",
    18: "ch18-string",
    19: "ch19-json-api",
    20: "ch20-header",
    21: "ch21-cookie",
    22: "ch22-hpp",
    23: "ch23-waf-bypass",
    24: "ch24-filter-bypass",
    25: "ch25-second-order-auth",
    26: "ch26-multi-db",
    27: "ch27-sqlite",
    28: "ch28-mysql",
    29: "ch29-postgresql",
    30: "ch30-mssql",
}

for ch_id, folder in FOLDERS.items():
    path = os.path.join(BASE, folder)
    os.makedirs(path, exist_ok=True)
    
    # Write requirements.txt if app.py doesn't exist yet
    req_path = os.path.join(path, "requirements.txt")
    if not os.path.exists(req_path):
        if ch_id == 26:
            req = MULTI_REQ
        elif ch_id in MSSQL_CHALLENGES:
            req = MSSQL_REQ
        elif ch_id in PGSQL_CHALLENGES:
            req = PGSQL_REQ
        elif ch_id in MYSQL_CHALLENGES:
            req = MYSQL_REQ
        else:
            req = SQLITE_REQ
        with open(req_path, "w") as f:
            f.write(req)
    
    # Write Dockerfile if doesn't exist
    df_path = os.path.join(path, "Dockerfile")
    if not os.path.exists(df_path):
        if ch_id == 30:
            df = MSSQL_DOCKER
        elif ch_id in PGSQL_CHALLENGES:
            df = PGSQL_DOCKER
        elif ch_id in MYSQL_CHALLENGES or ch_id == 26:
            df = MYSQL_DOCKER
        else:
            df = SQLITE_DOCKER
        with open(df_path, "w") as f:
            f.write(df)

print("Done creating scaffolding.")
