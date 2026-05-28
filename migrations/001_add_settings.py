import MySQLdb
import sys

try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="hr_erp_db_25")
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS settings (id INT PRIMARY KEY AUTO_INCREMENT, setting_key VARCHAR(50) UNIQUE, setting_value TEXT)")
    cur.execute("INSERT INTO settings (setting_key, setting_value) VALUES ('primary_color', '#17c3b2'), ('accent_color', '#22b391'), ('system_name', 'Lits HR ERP') ON DUPLICATE KEY UPDATE setting_value=setting_value")
    db.commit()
    print("Settings table created and initialized successfully.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
finally:
    if 'db' in locals(): db.close()
