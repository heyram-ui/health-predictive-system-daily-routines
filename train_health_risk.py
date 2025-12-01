# train_health_risk1.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///train_health_risk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- DATABASE MODELS --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# -------------------- ROUTES --------------------
@app.route('/')
def index():
    if "user" in session:
        username = session["user"]
        return render_template("index.html", username=username)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if "user" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login'))

    try:
        # Example features for prediction
        age = float(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])

        # Load your trained model (replace with your actual model path)
        model_path = os.path.join(os.getcwd(), "health_model.pkl")
        model = joblib.load(model_path)

        # Predict
        prediction = model.predict([[age, weight, height]])[0]
        return render_template("result.html", prediction=prediction)
    except Exception as e:
        flash(f"Error in prediction: {str(e)}", "danger")
        return redirect(url_for('index'))

# -------------------- RUN APP --------------------
if __name__ == "__main__":
    # Fixes "working outside application context" issue
    with app.app_context():
        db.create_all()
    app.run(debug=True)
