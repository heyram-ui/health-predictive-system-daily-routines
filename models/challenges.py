# models/challenges.py
from datetime import datetime
from app import db

class HealthChallenge(db.Model):
    __tablename__ = 'health_challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    challenge_type = db.Column(db.String(50))
    target_value = db.Column(db.Float)
    duration_days = db.Column(db.Integer)
    start_date = db.Column(db.Date, default=datetime.utcnow().date)
    end_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    reward_points = db.Column(db.Integer, default=100)
    difficulty = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<Challenge {self.name}>'

class ChallengeParticipation(db.Model):
    __tablename__ = 'challenge_participation'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('health_challenges.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    current_progress = db.Column(db.JSON, default=dict)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)