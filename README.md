# Lits HR ERP - Enterprise HR Management System with AI Assistant

Lits HR ERP is a premium enterprise-grade Human Resource Management web application. It features a complete role-based dashboard for Administrators and Employees, real-time attendance management, automated leave tracking, database audit logs, and an AI-powered floating chat assistant to help employees check policies and company updates.

## 🚀 Key Features

*   **Role-Based Access Control (RBAC)**: Secure separation between the Administrator and Employee portals.
*   **AI Chatbot Assistant (🤖)**: A persistent, intelligent floating chatbot across all pages to guide users.
*   **Leave Management System**: Allows employees to request leaves and admins to approve or reject them with real-time status updates.
*   **Attendance Tracking**: Direct logs for clocking in/out, stored securely in a relational database with local CSV fallbacks.
*   **Interactive Admin Dashboard**: Quick counters for total employees, pending leaves, active notices, and comprehensive database audit logs.
*   **Premium Glassmorphic UI**: Beautiful, modern dark-mode aesthetic with custom animations and transitions.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask, Flask-SQLAlchemy (ORM)
*   **Database**: MySQL / MariaDB
*   **Frontend**: HTML5, JavaScript (Vanilla ES6), CSS3 (Glassmorphic Stylesheet)
*   **Authentication**: Secure SHA-256 salted password hashing and session management

## 📂 Project Structure

```text
├── HR_Erp.py                 # Core Flask Application & Server Routes
├── db_setup.sql              # Relational Database Schema & Setup Scripts
├── check_db.py               # Database Health Check & Diagnostic Tool
├── migrate_passwords.py      # SHA-256 Password Migration & Overhaul Script
├── static/
│   ├── style.css             # Main Glassmorphic Dark-Mode Stylesheet
│   └── images/               # App Icons, Mascots, and Graphics
└── templates/
    ├── admin/                # Admin Panel HTML Templates
    ├── employee/             # Employee Portal HTML Templates
    ├── index_erp.html        # Public Landing Page
    ├── chatbot.html          # Chatbot Interface
    └── contactus.html        # Interactive Contact Us Page
```

## 💿 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Sarvadnya28/HR-ERP-System.git
cd HR-ERP-System
```

### 2. Configure Virtual Environment & Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Initialize the Database
Configure your MySQL credentials in `HR_Erp.py` and run:
```bash
mysql -u root -p < db_setup.sql
```

### 4. Run the Application
```bash
python HR_Erp.py
```
Open `http://127.0.0.1:5000` in your web browser!
