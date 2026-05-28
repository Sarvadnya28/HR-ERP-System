-- ============================================================
--  HR ERP System - Database Setup Script
--  Database: hr_erp_db_25
-- ============================================================

CREATE DATABASE IF NOT EXISTS hr_erp_db_25;
USE hr_erp_db_25;

-- ── Employee Registration ────────────────────────────────────
CREATE TABLE IF NOT EXISTS registration (
    empid       VARCHAR(20)  PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    salary      DECIMAL(10,2) NOT NULL DEFAULT 0,
    designation VARCHAR(100) NOT NULL,
    mobile      VARCHAR(15)  NOT NULL,
    password    VARCHAR(255) NOT NULL DEFAULT '',
    photo       VARCHAR(255) NOT NULL DEFAULT 'default.png'
);

-- ── Attendance ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attendance (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    empid         VARCHAR(20)  NOT NULL,
    emp_name      VARCHAR(100) NOT NULL,
    att_date      DATE         NOT NULL DEFAULT (CURDATE()),
    att_day       VARCHAR(15)  NOT NULL,
    status        ENUM('Present', 'Absent') NOT NULL DEFAULT 'Present',
    captured_photo VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (empid) REFERENCES registration(empid) ON DELETE CASCADE,
    UNIQUE KEY uq_att (empid, att_date)
);

-- ── Leave Applications ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS leave_applications (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    empid         VARCHAR(20)  NOT NULL,
    emp_name      VARCHAR(100) NOT NULL,
    leave_date    DATE         NOT NULL,
    reason        TEXT         NOT NULL,
    status        ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Pending',
    applied_on    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empid) REFERENCES registration(empid) ON DELETE CASCADE
);

-- ── Notice Board ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notices (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    title         VARCHAR(200) NOT NULL,
    message       TEXT         NOT NULL,
    published_on  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ── Sample Notices ───────────────────────────────────────────
INSERT IGNORE INTO notices (title, message) VALUES
  ('Welcome to Lits HR ERP', 'The new HR ERP system is now live. Please update your profile.'),
  ('Holiday Notice', 'The office will be closed on Friday for a public holiday.');
