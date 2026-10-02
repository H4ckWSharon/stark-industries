-- ============================================================
-- STARK INDUSTRIES SQL — MySQL Challenge Seed Data
-- Fake Stark Industries laboratory data only.
-- No real credentials. Educational use only.
-- ============================================================

USE stark_lab;

-- ─── Challenge Secrets Table ───────────────────────────────
CREATE TABLE IF NOT EXISTS challenge_secrets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    challenge_id INT NOT NULL,
    secret_value VARCHAR(200) NOT NULL,
    label VARCHAR(100)
);

INSERT INTO challenge_secrets (challenge_id, secret_value, label) VALUES
(3,  'STARKSQL{err0r_based_exfil}',      'Error-Based Flag'),
(4,  'STARKSQL{un10n_m4st3r_s3l3ct}',    'UNION Flag'),
(6,  'STARKSQL{t1m3_blind_d3t3ctiv3}',   'Time-Blind Flag'),
(7,  'STARKSQL{00b_callb4ck_m4st3r}',    'OOB Flag'),
(10, 'STARKSQL{st0r3d_pr0c_byp4ss}',     'Stored Proc Flag'),
(28, 'STARKSQL{mysql_d33p_d1v3}',        'MySQL Flag');

-- ─── Employees (Fake Stark Industries Data) ────────────────
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    role VARCHAR(100),
    email VARCHAR(100),
    active TINYINT DEFAULT 1,
    clearance_level VARCHAR(20) DEFAULT 'STANDARD'
);

INSERT INTO employees (name, department, role, email, active, clearance_level) VALUES
('Tony Stark',      'R&D',          'Chief Technology Officer',  'tstark@stark-lab.test',    1, 'ALPHA'),
('Pepper Potts',    'Executive',    'Chief Executive Officer',   'ppotts@stark-lab.test',    1, 'ALPHA'),
('Happy Hogan',     'Security',     'Head of Security',          'hhogan@stark-lab.test',    1, 'BETA'),
('James Rhodes',    'Military',     'Defense Liaison',           'jrhodes@stark-lab.test',   1, 'ALPHA'),
('Jarvis AI',       'AI Division',  'Virtual Assistant System',  'jarvis@stark-lab.test',    1, 'SYSTEM'),
('Dummy Employee',  'Testing',      'Lab Test Account',          'dummy@stark-lab.test',     0, 'NONE');

-- ─── Products Catalog ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    description TEXT,
    price DECIMAL(10,2),
    stock INT DEFAULT 0
);

INSERT INTO products (name, category, description, price, stock) VALUES
('Arc Reactor Mark I',  'Power',      'Laboratory prototype power cell',  15000.00, 2),
('Repulsor Gauntlet',   'Defense',    'Palm-mounted directed energy emitter', 8500.00, 5),
('Iron Man Suit v3',    'Armor',      'Modular combat exoskeleton frame', 250000.00, 1),
('Holographic Display', 'Technology', 'Multi-touch floating interface',   12000.00, 10),
('Vibranium Sample',    'Materials',  'Synthetic alloy research specimen', 1000000.00, 0);

-- ─── Systems ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS systems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    status VARCHAR(50) DEFAULT 'OPERATIONAL',
    host VARCHAR(100),
    last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO systems (name, status, host) VALUES
('JARVIS Core',     'OPERATIONAL', 'jarvis.stark-lab.test'),
('Arc Reactor Net', 'OPERATIONAL', 'arc.stark-lab.test'),
('Security Grid',   'MAINTENANCE', 'grid.stark-lab.test'),
('Lab Network',     'OPERATIONAL', 'lab.stark-lab.test');

-- ─── Diagnostics (for OOB challenge) ──────────────────────
CREATE TABLE IF NOT EXISTS diagnostics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host VARCHAR(200),
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO diagnostics (host) VALUES
('jarvis.stark-lab.test'),
('arc.stark-lab.test');

-- ─── Stored Procedure for Challenge 10 ────────────────────
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS GetEmployeesByDept(IN dept VARCHAR(100))
BEGIN
    -- INTENTIONALLY VULNERABLE for educational demonstration
    SET @sql = CONCAT('SELECT name, role, email FROM employees WHERE department = ''', dept, '''');
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END//

CREATE PROCEDURE IF NOT EXISTS GetEmployeesByDeptSECURE(IN dept VARCHAR(100))
BEGIN
    -- SECURE version using native parameter
    SELECT name, role, email FROM employees WHERE department = dept;
END//
DELIMITER ;

-- ─── ch28 specific secrets ─────────────────────────────────
CREATE TABLE IF NOT EXISTS ch28_secrets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    challenge_id INT,
    flag VARCHAR(200)
);

INSERT INTO ch28_secrets (challenge_id, flag) VALUES
(28, 'STARKSQL{mysql_d33p_d1v3}');
