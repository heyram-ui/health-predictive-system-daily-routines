# create_demo.py
import sqlite3
from datetime import datetime

conn = sqlite3.connect('health.db')
c = conn.cursor()

# Create demo user if not exists
c.execute("SELECT * FROM users WHERE username = 'demo'")
if not c.fetchone():
    c.execute("INSERT INTO users (username, password, email, created_at) VALUES (?, ?, ?, ?)",
             ('demo', 'demo123', 'demo@healthpredict.com', datetime.now()))
    print("✅ Created demo user: username='demo', password='demo123'")
else:
    print("✅ Demo user already exists")

conn.commit()
conn.close()