import pandas as pd
import joblib

# Load saved items
FEATURE_COLUMNS = joblib.load("feature_columns.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoder.pkl")
logistic_model = joblib.load("logistic_model.pkl")

# ----------- NEW INPUT (CHANGE THESE VALUES) ------------
new_data = pd.DataFrame([{
    "Gender": "Male",
    "Age": 25,
    "Sleep Duration": 6.5,
    "Quality of Sleep": 7,
    "Physical Activity Level": 30,
    "Stress Level": 6,
    "BMI Category": "Normal",
    "Heart Rate": 78,
    "Daily Steps": 6000
}])
# ---------------------------------------------------------

# Encode categorical columns
for col in ["Gender", "BMI Category"]:
    if col in label_encoders:
        new_data[col] = label_encoders[col].transform(new_data[col])

# Ensure correct column order
new_data = new_data[FEATURE_COLUMNS]

# Scale features
new_data_scaled = scaler.transform(new_data)

# Predict using logistic regression
prediction = logistic_model.predict(new_data_scaled)
decoded_prediction = label_encoders["Sleep Disorder"].inverse_transform(prediction)

print("Predicted Health Risk / Sleep Disorder:", decoded_prediction[0])
