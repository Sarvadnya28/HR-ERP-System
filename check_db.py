import MySQLdb
import sys

config = {
    "host": "localhost",
    "user": "root",
    "passwd": "root",
    "db": "hr_erp_db_25"
}

try:
    db = MySQLdb.connect(**config)
    print("SUCCESS: Connected to hr_erp_db_25")
    db.close()
except MySQLdb.Error as e:
    print(f"❌ FAILURE: Database connection error: {e}")
    # Try connecting without DB to see if server is up
    try:
        db = MySQLdb.connect(host=config["host"], user=config["user"], passwd=config["passwd"])
        print("⚠️ INFO: MySQL server is reachable, but the database 'hr_erp_db_25' might be missing.")
        db.close()
    except MySQLdb.Error as e2:
        print(f"❌ FAILURE: Could not connect to MySQL server at all. Check if MySQL is running and credentials are correct: {e2}")
    sys.exit(1)
except Exception as e:
    print(f"❌ UNEXPECTED ERROR: {e}")
    sys.exit(1)
