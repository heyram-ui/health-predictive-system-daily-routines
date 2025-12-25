import pandas as pd
import numpy as np
import random

def generate_synthetic_data(num_samples=1500):
    print(f"Generating {num_samples} synthetic health records...")
    
    data = {
        'age': np.random.randint(20, 80, num_samples),
        'gender': np.random.choice(['Male', 'Female'], num_samples),
        'bmi': np.random.uniform(18.5, 40.0, num_samples),
        'bp_sys': np.random.randint(90, 180, num_samples),
        'bp_dias': np.random.randint(60, 110, num_samples),
        'glucose': np.random.randint(70, 200, num_samples),
        'smoking': np.random.choice([0, 1, 2], num_samples, p=[0.7, 0.2, 0.1]), # 0=No, 1=Occasional, 2=Regular
        'alcohol': np.random.choice(['none', 'moderate', 'heavy'], num_samples, p=[0.6, 0.3, 0.1]),
        'sleep_hours': np.random.uniform(4.0, 10.0, num_samples),
        'screen_time': np.random.uniform(1.0, 12.0, num_samples),
        'activity_mins': np.random.randint(0, 120, num_samples),
        'stress_level': np.random.randint(1, 10, num_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate Targets based on logic (to simulate "ground truth" for the ML to learn)
    
    # 1. Heart Disease Risk
    def get_heart_risk(row):
        score = 0
        if row['bp_sys'] > 140 or row['bp_dias'] > 90: score += 30
        if row['bmi'] > 30: score += 20
        if row['smoking'] > 0: score += 30
        if row['activity_mins'] < 30: score += 20
        if row['age'] > 60: score += 20
        if score > 60: return 'High'
        if score > 30: return 'Medium'
        return 'Low'
    
    # 2. Diabetes Risk
    def get_diabetes_risk(row):
        score = 0
        if row['glucose'] > 140: score += 50
        if row['glucose'] > 100: score += 30
        if row['bmi'] > 30: score += 20
        if row['age'] > 45: score += 10
        if score > 50: return 'High'
        if score > 30: return 'Medium'
        return 'Low'

    # 3. Hypertension Risk
    def get_bp_risk(row):
        score = 0
        if row['bp_sys'] > 140: score += 50
        if row['bp_dias'] > 90: score += 40
        if row['stress_level'] > 7: score += 30
        if row['alcohol'] != 'none': score += 20
        if score > 50: return 'High'
        if score > 30: return 'Medium'
        return 'Low'

    # 4. Sleep Apnea Risk
    def get_sleep_risk(row):
        score = 0
        if row['bmi'] > 30: score += 40
        if row['sleep_hours'] < 6: score += 40
        if row['smoking'] > 0: score += 20
        if score > 50: return 'High'
        if score > 30: return 'Medium'
        return 'Low'

    # 5. Mental Health Risk
    def get_mental_risk(row):
        score = 0
        if row['stress_level'] > 8: score += 50
        if row['stress_level'] > 5: score += 20
        if row['screen_time'] > 6: score += 30
        if row['sleep_hours'] < 6: score += 20
        if score > 50: return 'High'
        if score > 30: return 'Medium'
        return 'Low'

    # 6. Obesity Risk
    def get_obesity_risk(row):
        if row['bmi'] > 30: return 'High'
        if row['bmi'] > 25: return 'Medium'
        return 'Low'

    print("Calculating target labels...")
    df['risk_heart'] = df.apply(get_heart_risk, axis=1)
    df['risk_diabetes'] = df.apply(get_diabetes_risk, axis=1)
    df['risk_hypertension'] = df.apply(get_bp_risk, axis=1)
    df['risk_sleep'] = df.apply(get_sleep_risk, axis=1)
    df['risk_mental'] = df.apply(get_mental_risk, axis=1)
    df['risk_obesity'] = df.apply(get_obesity_risk, axis=1)
    
    # Save
    df.to_csv('comprehensive_health_data.csv', index=False)
    print("Dataset saved to 'comprehensive_health_data.csv'")

if __name__ == "__main__":
    generate_synthetic_data()
