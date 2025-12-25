import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

def train_models():
    print("Loading dataset...")
    df = pd.read_csv('comprehensive_health_data.csv')
    
    # Preprocessing
    le_gender = LabelEncoder()
    df['gender'] = le_gender.fit_transform(df['gender'])
    
    le_alcohol = LabelEncoder()
    df['alcohol'] = le_alcohol.fit_transform(df['alcohol'])
    
    # Features
    X = df[['age', 'gender', 'bmi', 'bp_sys', 'bp_dias', 'glucose', 'smoking', 'alcohol', 
            'sleep_hours', 'screen_time', 'activity_mins', 'stress_level']]
            
    # Targets
    targets = ['risk_heart', 'risk_diabetes', 'risk_hypertension', 'risk_sleep', 'risk_mental', 'risk_obesity']
    
    models = {}
    
    print("Training models...")
    for target in targets:
        y = df[target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        
        score = clf.score(X_test, y_test)
        print(f"  {target}: Accuracy = {score:.2f}")
        
        models[target] = clf
        
    # Save encoders and models
    artifacts = {
        'models': models,
        'encoders': {
            'gender': le_gender,
            'alcohol': le_alcohol
        }
    }
    
    with open('health_model.pkl', 'wb') as f:
        pickle.dump(artifacts, f)
        
    print("All models trained and saved to 'health_model.pkl'")

if __name__ == "__main__":
    train_models()
