import sys
import os
import MySQLdb
import py_compile
from werkzeug.security import generate_password_hash, check_password_hash

def check_syntax(filename):
    try:
        py_compile.compile(filename, doraise=True)
        print(f"✅ {filename}: Syntax OK")
        return True
    except Exception as e:
        print(f"❌ {filename}: Syntax Error: {e}")
        return False

def check_db_connection():
    config = {
        "host": "localhost",
        "user": "root",
        "passwd": "root",
        "db": "hr_erp_db_25"
    }
    try:
        db = MySQLdb.connect(**config)
        print("✅ Database: Connection Successful")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database: Connection Failed: {e}")
        return False

def check_file_exists(path):
    if os.path.exists(path):
        print(f"✅ File: {path} exists")
        return True
    else:
        print(f"❌ File: {path} MISSING")
        return False

print("--- Project Diagnostic ---")
files_to_check = [
    "HR_Erp.py",
    "check_db.py",
    "migrate_passwords.py",
    "verify_routes.py"
]

all_ok = True
for f in files_to_check:
    if check_file_exists(f):
        if not check_syntax(f):
            all_ok = False
    else:
        all_ok = False

check_db_connection()

# Check templates
templates = [
    "templates/admin/dashboard.html",
    "templates/employee/emp_home.html"
]
for t in templates:
    check_file_exists(t)

print("--- Diagnostic Complete ---")
