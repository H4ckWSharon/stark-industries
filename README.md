<div align="center">

<img src="assets/banner.png" alt="Stark Industries SQL" width="780" style="max-width: 100%; border-radius: 10px;" />

<br/><br/>

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=700&size=26&duration=2500&pause=1000&color=FF2244&center=true&vCenter=true&width=750&lines=STARK+INDUSTRIES+SQL;30+Vulnerable+Challenge+Labs;SQL+Injection+Training+Platform;Built+by+Sharon+Anil" alt="Stark Industries SQL" />

<br/>

[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![Python](https://img.shields.io/badge/Python-3.12-FFD700?style=for-the-badge&logo=python&logoColor=black)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-Vite-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![License](https://img.shields.io/badge/License-Educational-FF2244?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](#)

</div>

---

## ⚡ What Is This?

**STARK INDUSTRIES SQL** is a fully self-hosted **SQL Injection training platform** built for cybersecurity students, red teamers, and instructors. It features **30 deliberately vulnerable challenge labs** across **4 database engines**, wrapped in a stunning JARVIS HUD interface.

> Think of it as **Hack The Box**, but purpose-built for SQL injection — running entirely on your local machine in Docker containers.

---

## 🎯 Platform Highlights

| Feature | Details |
|---|---|
| 🏆 **30 Challenge Labs** | Beginner → Expert difficulty |
| 🗄️ **4 Database Engines** | MySQL · PostgreSQL · MSSQL · SQLite |
| 🎖️ **XP & Leveling System** | Earn XP, level up, climb the leaderboard |
| 🎊 **Animated Celebrations** | Confetti + trophy overlay on every solve |
| 🔓 **Post-Solve Learning** | Vulnerable code → Secure fix revealed after solve |
| 📡 **OOB Injection Lab** | Live out-of-band HTTP callback listener |
| 🐳 **Fully Dockerized** | One command to run everything |
| 🔐 **JWT Auth** | Register with your own username & password |
| 📊 **Live Attack Monitor** | Real-time event stream per challenge |
| 🧠 **Progressive Hints** | 3-tier hint system (-10 XP each) |

---

## 🗺️ Challenge Map — All 30 Rooms

<div align="center">

| # | Challenge | Category | DB Engine | Difficulty |
|---|-----------|----------|-----------|------------|
| 01 | Basic String Injection | In-Band | SQLite | 🟢 Easy |
| 02 | Authentication Bypass | Auth Bypass | SQLite | 🟢 Easy |
| 03 | Error-Based Extraction | Error-Based | MySQL | 🟡 Medium |
| 04 | UNION SELECT Attack | UNION | SQLite | 🟢 Easy |
| 05 | Boolean Blind Injection | Blind | SQLite | 🟡 Medium |
| 06 | Time-Based Blind | Blind | SQLite | 🟡 Medium |
| 07 | Out-of-Band (OOB) | OOB | MySQL | 🔴 Hard |
| 08 | Second-Order Injection | Second-Order | SQLite | 🔴 Hard |
| 09 | Stacked Queries | Stacked | PostgreSQL | 🟡 Medium |
| 10 | Stored Procedure Bypass | Stored Proc | MySQL | 🔴 Hard |
| 11 | INSERT Injection | DML | SQLite | 🟡 Medium |
| 12 | UPDATE Injection | DML | SQLite | 🟡 Medium |
| 13 | DELETE Injection | DML | SQLite | 🟡 Medium |
| 14 | ORDER BY Manipulation | Clause | SQLite | 🟡 Medium |
| 15 | WHERE Clause Bypass | Clause | SQLite | 🟢 Easy |
| 16 | LIKE Clause Injection | Clause | SQLite | 🟢 Easy |
| 17 | Numeric Injection | Type | SQLite | 🟢 Easy |
| 18 | String Context Injection | Type | SQLite | 🟢 Easy |
| 19 | JSON API Injection | API | SQLite | 🟡 Medium |
| 20 | HTTP Header Injection | Header | SQLite | 🟡 Medium |
| 21 | Cookie-Based Injection | Cookie | SQLite | 🟡 Medium |
| 22 | HTTP Parameter Pollution | HPP | SQLite | 🔴 Hard |
| 23 | WAF Bypass Injection | Evasion | SQLite | 🔴 Hard |
| 24 | Filter Bypass | Evasion | SQLite | 🔴 Hard |
| 25 | Second-Order Auth Bypass | Second-Order | SQLite | 🔴 Hard |
| 26 | Multi-Database Enumeration | Recon | MySQL | 🔴 Hard |
| 27 | SQLite Master Enumeration | SQLite-Specific | SQLite | 🟡 Medium |
| 28 | MySQL Deep Dive | MySQL-Specific | MySQL | 🔴 Hard |
| 29 | PostgreSQL Advanced | PgSQL-Specific | PostgreSQL | 🔴 Hard |
| 30 | MSSQL Exploitation | MSSQL-Specific | MSSQL | 🔴 Expert |

</div>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STARK INDUSTRIES SQL                      │
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │   Frontend   │────▶│   Backend    │────▶│  Platform   │ │
│  │  React/Vite  │     │   FastAPI    │     │  PostgreSQL │ │
│  │  Port: 3000  │     │  Port: 8000  │     │   + Redis   │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           30 CHALLENGE CONTAINERS                    │   │
│  │  stark-ch01 (8001) ──── stark-ch30 (8030)           │   │
│  │  Each runs its own Flask app + intentional SQLi bug  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │    MySQL     │  │  PostgreSQL  │  │  MSSQL Server    │  │
│  │  Challenge   │  │  Challenge   │  │  2022 Developer  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                              │
│  ┌──────────────────────┐                                   │
│  │   OOB HTTP Listener  │  (Port 8888 — internal)          │
│  └──────────────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start — Run in 3 Steps

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed & running
- 8 GB RAM recommended (30 containers!)
- Git

### Step 1 — Clone
```bash
git clone https://github.com/H4ckWSharon/stark-industries.git
cd stark-industries
```

### Step 2 — Configure Environment
```bash
# Copy the example env file
cp .env.example .env
# Edit .env if you want to change any flags or passwords
```

### Step 3 — Launch Everything
```bash
docker compose up -d
```

> ⏳ First run downloads images and builds all containers — takes ~5 minutes.
> Subsequent starts take ~30 seconds.

### Step 4 — Open the Platform
```
http://localhost:3000
```
Register with any username and password you choose, then start hacking!

---

## 🔐 Authentication

| Account | How to Create |
|---|---|
| 🎓 **Student / User** | Register on the login page with any username or email + password |

---

## 🧪 Connecting with Kali Linux / Pentest Tools

### From Kali WSL2 or same machine
```bash
# Challenges are exposed on ports 8001–8030
curl http://localhost:8001/
sqlmap -u "http://localhost:8001/?name=test" --dbs --batch
```

### From Kali VM (VirtualBox/VMware — Host-Only or Bridged)
```bash
# Replace HOST_IP with your Windows machine's LAN IP
sqlmap -u "http://HOST_IP:8001/?name=test" --batch
```

### Useful Tools
| Tool | Usage |
|---|---|
| `sqlmap` | `sqlmap -u "http://localhost:8001/?id=1" --dbs --batch` |
| `curl` | `curl -X POST http://localhost:8002/ -d "username=admin'--"` |
| `Burp Suite` | Set browser proxy → intercept & modify requests |
| `ffuf` | `ffuf -u http://localhost:8001/?name=FUZZ -w sqli.txt` |

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Frontend** | React 18 + TypeScript + Vite + Tailwind CSS + Framer Motion |
| **Backend** | FastAPI (Python 3.12) + SQLAlchemy + JWT Auth |
| **Platform DB** | PostgreSQL 15 + Redis 7 |
| **Challenge DBs** | MySQL 8 · PostgreSQL 15 · MSSQL 2022 · SQLite 3 |
| **Challenge Apps** | Flask (Python) — 30 individual containers |
| **Orchestration** | Docker Compose |
| **Web Server** | Nginx (serving built React SPA) |

</div>

---

## 📁 Project Structure

```
stark-industries/
├── 📂 frontend/               # React SPA (Iron Man HUD theme)
│   ├── src/
│   │   ├── pages/             # Dashboard, Challenges, ChallengePage, etc.
│   │   ├── components/        # Navbar, Sidebar, ArcReactorLogo, etc.
│   │   ├── store/             # Zustand auth store
│   │   └── api/               # Axios client
│   └── Dockerfile
│
├── 📂 backend/                # FastAPI REST API
│   ├── app/
│   │   ├── auth/              # JWT auth, user model, router
│   │   ├── challenges/        # Challenge registry, submission, hints
│   │   ├── monitor/           # Attack event streaming
│   │   └── main.py
│   └── Dockerfile
│
├── 📂 challenges/             # 30 vulnerable Flask applications
│   ├── ch01-basic/            # Challenge 01: Basic SQLi
│   ├── ch02-auth-bypass/      # Challenge 02: Auth Bypass
│   │   ...
│   └── ch30-mssql/            # Challenge 30: MSSQL Exploitation
│
├── 📂 oob-listener/           # Out-of-Band HTTP callback listener
├── 🐳 docker-compose.yml      # Full platform orchestration
├── ⚙️ .env.example            # Environment variable template
└── 📖 README.md
```

---

## 🎮 How to Use

1. **Register** — Create your pilot account on the login page
2. **Browse Challenges** — Click `TARGET LABS (30)` in the sidebar
3. **Launch a Lab** — Click `LAUNCH LAB` to open the vulnerable app in a new tab
4. **Attack** — Exploit the SQL injection vulnerability in the lab
5. **Capture the Flag** — Find the `STARKSQL{...}` flag in the response
6. **Submit** — Paste the flag back into the platform and hit `SUBMIT`
7. **Celebrate** — Watch the animated confetti congratulations overlay 🎊
8. **Learn** — Defensive Learning Mode unlocks showing vulnerable vs secure code

---

## 🏆 XP & Ranking System

| Rank | XP Required |
|---|---|
| 🔰 Recruit | 0 XP |
| 🛡️ Initiate | 500 XP |
| ⚔️ Operative | 1,500 XP |
| 🎯 Specialist | 3,000 XP |
| 🔥 Expert | 5,000 XP |
| 💀 Elite Hacker | 8,000 XP |
| ⚡ Iron Man | 10,000+ XP |

---

## ⚠️ Legal Disclaimer

> [!CAUTION]
> **FOR EDUCATIONAL AND AUTHORIZED LAB TESTING ONLY**
> 
> All 30 challenge applications are **intentionally vulnerable**. Run only on your local machine or in an isolated lab environment. Do **NOT** expose these containers to the public internet. The author is not responsible for misuse.

---

## 👨‍💻 Built by Sharon Anil

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=600&size=22&duration=2500&pause=1000&color=FFB800&center=true&vCenter=true&width=700&lines=Built+by+Sharon+Anil;Ethical+Hacker+%26+Pentester;CTF+Player+%7C+Web+Developer;Hardware+Hacking" alt="Sharon Anil Skills" />

<br/><br/>

### **Sharon Anil**
#### 🛡️ Ethical Hacker & Pentester · 🚩 CTF Player · 💻 Developer & Web Developer · 🔌 Hardware Hacking

<br/>

[![YouTube Channel](https://img.shields.io/badge/YouTube-@HackWSharon-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@HackWSharon)
[![GitHub Profile](https://img.shields.io/badge/GitHub-H4ckWSharon-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/H4ckWSharon)

<br/><br/>

[![Ethical Hacker](https://img.shields.io/badge/🛡️_Ethical_Hacker-E62429?style=for-the-badge&logo=kalilinux&logoColor=white)](https://www.youtube.com/@HackWSharon)
[![Pentester](https://img.shields.io/badge/🎯_Skill-Pentester-FFB800?style=for-the-badge&logo=target&logoColor=black)](https://www.youtube.com/@HackWSharon)
[![CTF Player](https://img.shields.io/badge/🚩_CTF-Player-00A8FF?style=for-the-badge&logo=flag&logoColor=white)](https://github.com/H4ckWSharon)
[![Web Developer](https://img.shields.io/badge/💻_Web-Developer-00D47E?style=for-the-badge&logo=react&logoColor=white)](https://github.com/H4ckWSharon)
[![Hardware Hacking](https://img.shields.io/badge/🔌_Hardware-Hacking-FF6B00?style=for-the-badge&logo=raspberrypi&logoColor=white)](https://www.youtube.com/@HackWSharon)

<br/><br/>

> 📺 **Subscribe on YouTube:** [youtube.com/@HackWSharon](https://www.youtube.com/@HackWSharon) — Ethical Hacking, CTF Walkthroughs & Cyber Defense tutorials!

</div>

---

<div align="center">

**⚡ STARK INDUSTRIES RESEARCH DIVISION · MARK VIII CYBER RANGE ⚡**

*"Sometimes you gotta run before you can walk." — Tony Stark*

</div>
