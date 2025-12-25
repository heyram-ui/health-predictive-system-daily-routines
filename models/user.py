# models/user.py
from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Personal info
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    occupation = db.Column(db.String(100))
    
    # Tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    health_score = db.Column(db.Float, default=0.0)
    points = db.Column(db.Integer, default=0)
    streak_days = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def calculate_bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 1)
        return None
    
    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if not bmi:
            return "Unknown"
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def __repr__(self):
        return f'<User {self.username}>'