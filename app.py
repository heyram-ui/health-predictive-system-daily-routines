from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib
import pandas as pd
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a strong secret

# Paths
USER_FILE = "users.json"

# Load saved models and preprocessors
FEATURE_COLUMNS = joblib.load("feature_columns.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoder.pkl")
logistic_model = joblib.load("logistic_model.pkl")

# Utility functions
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Routes
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("index"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        if username in users:
            flash("Username already exists!", "danger")
        else:
            users[username] = password
            save_users(users)
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))

@app.route("/index", methods=["GET", "POST"])
def index():
    if "username" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    prediction_result = None

    if request.method == "POST":
        # Get Form Data
        gender = request.form["gender"]
        age = int(request.form["age"])
        sleep_duration = float(request.form["sleep_duration"])
        quality_sleep = float(request.form["quality_sleep"])
        activity = float(request.form["activity"])
        stress = float(request.form["stress"])
        bmi = request.form["bmi"]
        heart_rate = float(request.form["heart_rate"])
        steps = float(request.form["steps"])

        # Convert to DataFrame
        new_data = pd.DataFrame([{
            "Gender": gender,
            "Age": age,
            "Sleep Duration": sleep_duration,
            "Quality of Sleep": quality_sleep,
            "Physical Activity Level": activity,
            "Stress Level": stress,
            "BMI Category": bmi,
            "Heart Rate": heart_rate,
            "Daily Steps": steps
        }])

        # Handle unseen label for BMI Category
        if new_data["BMI Category"][0] not in label_encoders["BMI Category"].classes_:
            new_data["BMI Category"] = "Normal"

        # Label encode categorical columns
        for col in ["Gender", "BMI Category"]:
            new_data[col] = label_encoders[col].transform(new_data[col])

        # Reorder columns
        new_data = new_data[FEATURE_COLUMNS]

        # Scale
        new_data_scaled = scaler.transform(new_data)

        # Predict
        pred = logistic_model.predict(new_data_scaled)
        result = label_encoders["Sleep Disorder"].inverse_transform(pred)
        prediction_result = result[0]

    return render_template("index.html", prediction=prediction_result, username=session["username"])

if __name__ == "__main__":
    app.run(debug=True)
