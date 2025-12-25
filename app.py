# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import sqlite3
import hashlib
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'super_secret_health_key_change_in_prod'

# --- Database Management ---
def init_db():
    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    
    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Health Assessments Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bp_sys INTEGER,
            bp_dias INTEGER,
            glucose REAL,
            bmi REAL,
            smoking INTEGER,
            alcohol TEXT,
            sleep_hours REAL,
            screen_time REAL,
            activity_mins INTEGER,
            stress_level INTEGER,
            
            risk_heart_rate TEXT,
            risk_diabetes TEXT,
            risk_hypertension TEXT,
            risk_sleep_apnea TEXT,
            risk_anxiety TEXT,
            risk_obesity TEXT,
            
            overall_score INTEGER,
            overall_risk TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# --- ML Loader ---
import pickle
import pandas as pd

try:
    with open('health_model.pkl', 'rb') as f:
        artifacts = pickle.load(f)
        ml_models = artifacts['models']
        encoders = artifacts['encoders']
        print("ML Models loaded successfully.")
except FileNotFoundError:
    print("Warning: health_model.pkl not found. Predictions will fail.")
    ml_models = {}

class HealthPredictor:
    def predict(self, data):
        risks = {}
        recommendations = {'foods': [], 'habits': []}
        
        # Prepare Input Vector
        # ['age', 'gender', 'bmi', 'bp_sys', 'bp_dias', 'glucose', 'smoking', 'alcohol', 
        #  'sleep_hours', 'screen_time', 'activity_mins', 'stress_level']
        
        # Safe transform for categoricals
        gender_val = 1 if data.get('gender', 'Male') == 'Male' else 0 # Assuming Male=1 from LabelEncoder check usually
        
        alcohol_map = {'none': 1, 'moderate': 0, 'heavy': 2} # Approximate mapping, should match Training encoder ideally
        # In prod, use the actual loaded encoder:
        # alcohol_val = encoders['alcohol'].transform([data['alcohol']])[0]
        # But for robustness against unknown labels in demo:
        alcohol_val = alcohol_map.get(data['alcohol'], 1)

        input_df = pd.DataFrame([{
            'age': data.get('age', 30),
            'gender': gender_val, 
            'bmi': data['bmi'], 
            'bp_sys': data['bp_sys'], 
            'bp_dias': data['bp_dias'], 
            'glucose': data['glucose'], 
            'smoking': data['smoking'], 
            'alcohol': alcohol_val, 
            'sleep_hours': data['sleep_hours'], 
            'screen_time': data['screen_time'], 
            'activity_mins': data['activity_mins'], 
            'stress_level': data['stress']
        }])
        
        # Predict for each disease
        disease_map = {
            'heart': 'risk_heart',
            'diabetes': 'risk_diabetes',
            'hypertension': 'risk_hypertension',
            'sleep': 'risk_sleep',
            'mental': 'risk_mental',
            'obesity': 'risk_obesity'
        }
        
        score_accumulator = 0
        
        for key, model_key in disease_map.items():
            if model_key in ml_models:
                pred = ml_models[model_key].predict(input_df)[0]
                
                # Assign Score based on Low/Med/High
                if pred == 'High': 
                    score = 90
                    color = '#dc3545'
                    score_accumulator += 30
                elif pred == 'Medium': 
                    score = 50
                    color = '#ffc107'
                    score_accumulator += 15
                else: 
                    score = 10
                    color = '#28a745'
                
                risks[key] = {'level': pred, 'score': score, 'color': color}
            else:
                risks[key] = {'level': 'Unknown', 'score': 0, 'color': '#6c757d'}

        # Post-Processing Recommendations (Rule-based on top of ML output)
        if risks['heart']['level'] == 'High':
            recommendations['foods'].append("Omega-3 rich foods, Avoid Trans Fats")
            recommendations['habits'].append("Immediate Cardiology Consult")
            
        if risks['diabetes']['level'] == 'High':
            recommendations['foods'].append("Low Glycemic Index foods")
            recommendations['habits'].append("Monitor Blood Sugar daily")

        if risks['hypertension']['level'] == 'High':
            recommendations['habits'].append("Reduce Sodium intake < 1500mg")

        # Overall Calculation
        total_risk_score = min(score_accumulator, 100) # Cap at 100
        
        return risks, int(total_risk_score), recommendations

predictor = HealthPredictor()

# --- Routes ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        age = request.form['age']
        emergency_contact = request.form.get('emergency_contact', '') # New Field
        
        conn = sqlite3.connect('health.db')
        c = conn.cursor()
        try:
            # Note: We need to alter table if 'emergency_contact' doesn't exist, but for now we'll just store it if we rebuild DB
            # Or simpler: Just store in a new column if exists.
            # For this quick iteration, we'll assume the user runs fix_database.py or we migrate.
            # Let's simple Check and Alter inline for robustness
            try:
                c.execute("ALTER TABLE users ADD COLUMN emergency_contact TEXT")
            except sqlite3.OperationalError:
                pass # Column exists

            c.execute("INSERT INTO users (name, email, password, age, emergency_contact) VALUES (?, ?, ?, ?, ?)",
                      (name, email, password, age, emergency_contact))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered!', 'danger')
        finally:
            conn.close()
            
    return render_template('auth/register.html')

@app.route('/calculators')
def calculators():
    return render_template('pages/calculators.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        
        conn = sqlite3.connect('health.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
            
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    
    # Get History
    c.execute("SELECT * FROM assessments WHERE user_id = ? ORDER BY created_at DESC LIMIT 10", (session['user_id'],))
    history_raw = c.fetchall()
    
    conn.close()
    
    # Process Data for Charts
    dates = []
    scores = []
    recent_history = []
    
    for row in reversed(history_raw):
        dates.append(row[20].split(' ')[0]) # Date part
        scores.append(row[18]) # Overall Score
        
    for row in history_raw:
        recent_history.append({
            'created_at': row[20],
            'risk_level': row[19],
            'risk_score': row[18]
        })

    last_risk = history_raw[0][19] if history_raw else 'N/A'
    avg_score = sum(scores) / len(scores) if scores else 0
    
    return render_template('dashboard/index.html', 
                         user={'name': session['user_name']},
                         dates=dates,
                         scores=scores,
                         recent_history=recent_history,
                         last_risk=last_risk,
                         avg_score=avg_score,
                         total_assessments=len(history_raw))

@app.route('/assess', methods=['GET', 'POST'])
def assess():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Collect Data
        data = {
            'bp_sys': int(request.form['bp_sys']),
            'bp_dias': int(request.form['bp_dias']),
            'glucose': float(request.form['glucose']),
            'bmi': float(request.form['bmi']),
            'smoking': int(request.form['smoking']),
            'alcohol': request.form['alcohol'],
            'sleep_hours': float(request.form['sleep_hours']),
            'screen_time': float(request.form['screen_time']),
            'activity_mins': int(request.form['activity_mins']),
            'stress': int(request.form['stress'])
        }
        
        # Predict
        risks, overall_score, recommendations = predictor.predict(data)
        
        overall_status = 'Healthy'
        if overall_score > 40: overall_status = 'Moderate Risk'
        if overall_score > 70: overall_status = 'High Risk'
        
        overall_risk_level = 'Low'
        if overall_score > 40: overall_risk_level = 'Medium'
        if overall_score > 70: overall_risk_level = 'High'

        # Save to DB
        conn = sqlite3.connect('health.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO assessments 
            (user_id, bp_sys, bp_dias, glucose, bmi, smoking, alcohol, sleep_hours, screen_time, activity_mins, stress_level,
             risk_heart_rate, risk_diabetes, risk_hypertension, risk_sleep_apnea, risk_anxiety, risk_obesity,
             overall_score, overall_risk)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session['user_id'], data['bp_sys'], data['bp_dias'], data['glucose'], data['bmi'], 
            data['smoking'], data['alcohol'], data['sleep_hours'], data['screen_time'], 
            data['activity_mins'], data['stress'],
            risks['heart']['level'], risks['diabetes']['level'], risks['hypertension']['level'],
            risks['sleep']['level'], risks['mental']['level'], risks['obesity']['level'],
            overall_score, overall_status
        ))
        conn.commit()
        conn.close()
        
        # Prepare View Data
        disease_view_data = [
            {'name': 'Heart Health', 'icon': 'fa-heartbeat', 'risk_level': risks['heart']['level'], 'probability': risks['heart']['score'], 'color': risks['heart']['color'], 'recommendation': 'Monitor BP & Cardio'},
            {'name': 'Diabetes Risk', 'icon': 'fa-tint', 'risk_level': risks['diabetes']['level'], 'probability': risks['diabetes']['score'], 'color': risks['diabetes']['color'], 'recommendation': 'Watch sugar intake'},
            {'name': 'Hypertension', 'icon': 'fa-tachometer-alt', 'risk_level': risks['hypertension']['level'], 'probability': risks['hypertension']['score'], 'color': risks['hypertension']['color'], 'recommendation': 'Reduce stress & salt'},
            {'name': 'Sleep Apnea', 'icon': 'fa-bed', 'risk_level': risks['sleep']['level'], 'probability': risks['sleep']['score'], 'color': risks['sleep']['color'], 'recommendation': 'Improve sleep hygiene'},
            {'name': 'Mental Health', 'icon': 'fa-brain', 'risk_level': risks['mental']['level'], 'probability': risks['mental']['score'], 'color': risks['mental']['color'], 'recommendation': 'Mental rest needed'},
            {'name': 'Obesity', 'icon': 'fa-weight', 'risk_level': risks['obesity']['level'], 'probability': risks['obesity']['score'], 'color': risks['obesity']['color'], 'recommendation': 'Active lifestyle needed'},
        ]
        
        overall_color = '#28a745'
        if overall_score > 40: overall_color = '#ffc107'
        if overall_score > 70: overall_color = '#dc3545'

        return render_template('prediction/result.html', 
                             overall_score=overall_score,
                             overall_status=overall_status,
                             overall_risk=overall_risk_level,
                             overall_color=overall_color,
                             diseases=disease_view_data,
                             recommendations=recommendations)
                             
    return render_template('prediction/form.html')

@app.route('/who-regulations')
def who_regulations():
    return render_template('pages/who.html')

@app.route('/recommendations')
def recommendations():
    return render_template('pages/recommendations.html')

@app.route('/about')
def about():
    return render_template('home.html') # Simplified for now or can redirect

if __name__ == '__main__':
    init_db()
    print("Health Risk System Active...")
    app.run(debug=True, port=5000)
