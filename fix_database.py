import sqlite3
import os

def fix_database():
    print("Attempting to fix database schema...")
    
    db_path = 'health.db'
    
    if not os.path.exists(db_path):
        print("Database does not exist. It will be created when you run the app.")
        return

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Check if users table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if c.fetchone():
            print("Found existing 'users' table. Dropping it to ensure clean schema...")
            c.execute("DROP TABLE users")
            conn.commit()
            print("Table 'users' dropped successfully.")
        else:
            print("Table 'users' not found.")
            
        conn.close()
        print("Database fixed. Please restart your application manually.")
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        print("If the file is locked, please stop the running Flask server (Ctrl+C) and try again.")

if __name__ == '__main__':
    fix_database()
