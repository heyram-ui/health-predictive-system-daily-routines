# setup.py
import os
import shutil
import sys
from pathlib import Path

def setup_project():
    """Setup the HealthPredict Pro project"""
    
    print("🚀 Setting up HealthPredict Pro...")
    
    # Create necessary directories
    directories = [
        'instance',
        'ml_models',
        'models',
        'services',
        'static/css',
        'static/js',
        'static/icons',
        'templates/layouts',
        'templates/dashboard',
        'templates/auth',
        'templates/health',
        'templates/errors',
        'data',
        'uploads'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Create __init__.py files
    for init_dir in ['models', 'services', 'ml_models']:
        init_file = Path(init_dir) / '__init__.py'
        init_file.touch(exist_ok=True)
        print(f"✅ Created {init_dir}/__init__.py")
    
    # Copy ML model files if they exist in root
    model_files = [
        'label_encoder.pkl',
        'decision_tree_model.pkl',
        'logistic_model.pkl',
        'feature_columns.pkl',
        'scaler.pkl',
        'dt_model.pkl',
        'log_model.pkl',
        'random_forest_model.pkl',
        'xgb_model.pkl'
    ]
    
    for model_file in model_files:
        if os.path.exists(model_file):
            try:
                shutil.copy(model_file, f'ml_models/{model_file}')
                print(f"✅ Copied {model_file} to ml_models/")
            except Exception as e:
                print(f"⚠️ Could not copy {model_file}: {e}")
    
    # Create .env file if it doesn't exist
    env_file = Path('.env')
    if not env_file.exists():
        env_file.write_text("""# HealthPredict Pro Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
DEBUG=True

# Database
DATABASE_URL=sqlite:///instance/health_predict_pro.db

# Email (optional)
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password
""")
        print("✅ Created .env file")
    
    # Create requirements.txt if it doesn't exist
    req_file = Path('requirements.txt')
    if not req_file.exists():
        req_file.write_text("""Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-Migrate==4.0.5
Flask-SocketIO==5.3.4
python-dotenv==1.0.0
Werkzeug==2.3.7
scikit-learn==1.3.0
pandas==2.0.3
numpy==1.24.3
joblib==1.3.2
plotly==5.17.0
python-socketio==5.9.0
eventlet==0.33.3
""")
        print("✅ Created requirements.txt")
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the app: python app.py")
    print("3. Open browser: http://localhost:5000")
    print("\n💡 For production:")
    print("- Change SECRET_KEY in .env")
    print("- Set FLASK_ENV=production")
    print("- Set DEBUG=False")

if __name__ == '__main__':
    setup_project()