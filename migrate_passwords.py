import MySQLdb
from werkzeug.security import generate_password_hash

# Configuration (Matches HR_Erp.py)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "passwd": "root",
    "db": "hr_erp_db_25"
}

def migrate():
    try:
        db = MySQLdb.connect(**DB_CONFIG)
        cur = db.cursor()
        
        # Fetch all users
        cur.execute("SELECT empid, password FROM registration")
        users = cur.fetchall()
        
        print(f"Found {len(users)} users to migrate.")
        
        for empid, pwd in users:
            # Check if already hashed (crude check: werkzeug hashes start with pbkdf2:sha256: or similar)
            if pwd and (pwd.startswith('pbkdf2:sha256:') or pwd.startswith('scrypt:')):
                print(f"Skipping {empid} (already hashed).")
                continue
            
            if not pwd:
                print(f"Skipping {empid} (missing password).")
                continue
            
            hashed_pwd = generate_password_hash(pwd)
            cur.execute("UPDATE registration SET password=%s WHERE empid=%s", (hashed_pwd, empid))
            print(f"Migrated {empid}.")
        
        db.commit()
        db.close()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate()
