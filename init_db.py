# init_db.py - Simple version
from app import app, db
from models.user import User
from datetime import datetime, timedelta
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        print("🗃️ Creating database tables...")
        
        # Create all tables
        db.create_all()
        print("✅ Tables created successfully!")
        
        # Check if demo user exists
        if User.query.filter_by(username='demo').first():
            print("✅ Demo user already exists")
        else:
            print("👤 Creating demo user...")
            demo_user = User(
                username='demo',
                email='demo@healthpredict.com',
                age=28,
                gender='Male',
                height=175,
                weight=70,
                occupation='Student'
            )
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            db.session.commit()
            print("✅ Demo user created (username: demo, password: demo123)")
        
        print("\n🎉 Database initialized successfully!")
        print("📋 You can now run the application:")
        print("   python app.py")
        print("\n🌐 Access at: http://localhost:5000")
        print("   👉 Username: demo")
        print("   👉 Password: demo123")

if __name__ == '__main__':
    init_database()