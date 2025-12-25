# simple_app.py - One file, no templates needed!
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>HealthPredict Pro</title>
        <style>
            body { font-family: Arial; padding: 40px; background: #f0f8ff; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
            h1 { color: #4361ee; }
            .btn { display: inline-block; padding: 10px 20px; margin: 10px; background: #4361ee; color: white; text-decoration: none; border-radius: 5px; }
            .feature { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #4361ee; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 HealthPredict Pro</h1>
            <p class="lead">Final Year Project - Predictive Health Risk using ML</p>
            
            <div class="feature">
                <h3>✅ System is Running!</h3>
                <p>Your health prediction website is now live at http://localhost:5000</p>
            </div>
            
            <h3>Features:</h3>
            <div class="feature">
                <strong>ML Predictions:</strong> Sleep disorder risk prediction using your trained models
            </div>
            <div class="feature">
                <strong>Health Analytics:</strong> Track sleep, steps, stress, heart rate
            </div>
            <div class="feature">
                <strong>Dashboard:</strong> Beautiful charts and insights
            </div>
            <div class="feature">
                <strong>User Profiles:</strong> Personalized recommendations
            </div>
            
            <h3>Quick Actions:</h3>
            <a href="/predict" class="btn">Test Prediction</a>
            <a href="/dashboard" class="btn">View Dashboard</a>
            <a href="/login" class="btn">Login</a>
            <a href="/register" class="btn">Register</a>
            
            <h3 class="mt-4">For Demonstration:</h3>
            <p>Use these demo credentials:</p>
            <ul>
                <li><strong>Username:</strong> demo</li>
                <li><strong>Password:</strong> demo123</li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/predict')
def predict():
    return '''
    <div class="container">
        <h2>Health Risk Prediction</h2>
        <p>This is where your ML model predicts health risks based on:</p>
        <ul>
            <li>Sleep patterns</li>
            <li>Physical activity</li>
            <li>Stress levels</li>
            <li>Vital signs</li>
        </ul>
        <a href="/">← Back to Home</a>
    </div>
    '''

@app.route('/dashboard')
def dashboard():
    return '''
    <div class="container">
        <h2>Health Dashboard</h2>
        <p>Interactive charts showing:</p>
        <ul>
            <li>Sleep trends</li>
            <li>Step counts</li>
            <li>Heart rate</li>
            <li>Health score</li>
        </ul>
        <a href="/">← Back to Home</a>
    </div>
    '''

@app.route('/login')
def login():
    return '''
    <div class="container">
        <h2>Login Page</h2>
        <p>User authentication system</p>
        <a href="/">← Back to Home</a>
    </div>
    '''

@app.route('/register')
def register():
    return '''
    <div class="container">
        <h2>Registration Page</h2>
        <p>Create new user accounts</p>
        <a href="/">← Back to Home</a>
    </div>
    '''

if __name__ == '__main__':
    print("🚀 HealthPredict Pro Starting...")
    print("🌐 Open: http://localhost:5000")
    print("📱 Mobile-friendly website ready!")
    app.run(debug=True, port=5000)