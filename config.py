# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        'instance', 
        'health_predict_pro.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SESSION_PROTECTION = 'strong'
    REMEMBER_COOKIE_DURATION = 86400  # 1 day in seconds
    
    # Application
    HEALTH_SCORE_UPDATE_INTERVAL = 3600  # 1 hour
    MAX_RECOMMENDATIONS = 5
    CHALLENGE_AUTO_REFRESH = True
    
    # File upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    
    # ML Models path
    ML_MODELS_PATH = os.path.join(os.path.dirname(__file__), 'ml_models')
    
    # Email configuration (optional)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@healthpredict.com')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENVIRONMENT = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENVIRONMENT = 'production'
    
    # Use environment variable for database in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}