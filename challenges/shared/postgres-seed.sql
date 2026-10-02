-- ============================================================
-- STARK INDUSTRIES SQL — PostgreSQL Challenge Seed Data
-- Fake Stark Industries laboratory data only.
-- Educational use only.
-- ============================================================

-- Challenge secrets
CREATE TABLE IF NOT EXISTS challenge_secrets (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER NOT NULL,
    secret_value VARCHAR(200) NOT NULL,
    label VARCHAR(100)
);

INSERT INTO challenge_secrets (challenge_id, secret_value, label) VALUES
(9,  'STARKSQL{st4ck3d_qu3ry_ch4in}', 'Stacked Queries Flag'),
(29, 'STARKSQL{p0stgr3sql_m4st3r}',   'PostgreSQL Flag');

-- Inventory (for stacked queries challenge)
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    quantity INTEGER DEFAULT 0,
    location VARCHAR(100)
);

INSERT INTO inventory (name, quantity, location) VALUES
('Stark Alloy Sheets',      500, 'Warehouse A'),
('Quantum Capacitors',       50, 'Lab B-4'),
('Miniaturized Arc Cell',    10, 'Secure Storage'),
('Holographic Emitter Unit',  5, 'R&D Lab 3');

-- Employees (PostgreSQL version)
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    role VARCHAR(100),
    active BOOLEAN DEFAULT TRUE
);

INSERT INTO employees (name, department, role, active) VALUES
('Tony Stark',   'R&D',       'CTO',               TRUE),
('Pepper Potts', 'Executive', 'CEO',               TRUE),
('Happy Hogan',  'Security',  'Head of Security',  TRUE),
('Lab Dummy',    'Testing',   'Test Account',      FALSE);

-- ch29 specific
CREATE TABLE IF NOT EXISTS ch29_secrets (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER,
    flag VARCHAR(200)
);

INSERT INTO ch29_secrets (challenge_id, flag) VALUES
(29, 'STARKSQL{p0stgr3sql_m4st3r}');
