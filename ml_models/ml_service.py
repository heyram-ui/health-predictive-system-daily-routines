# ml_models/ml_service.py - Simple ML service
import joblib
import pandas as pd
import numpy as np
import os

class SimpleMLService:
    def __init__(self):
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load ML models"""
        try:
            models_dir = os.path.join(os.path.dirname(__file__))
            
            # Try to load models
            model_files = [
                ('logistic', 'logistic_model.pkl'),
                ('decision_tree', 'decision_tree_model.pkl'),
                ('label_encoder', 'label_encoder.pkl'),
                ('feature_columns', 'feature_columns.pkl')
            ]
            
            for name, filename in model_files:
                path = os.path.join(models_dir, filename)
                if os.path.exists(path):
                    self.models[name] = joblib.load(path)
                    print(f"✅ Loaded {name}")
                else:
                    print(f"⚠️ {filename} not found")
            
            print(f"✅ Loaded {len(self.models)} ML components")
            
        except Exception as e:
            print(f"⚠️ Error loading models: {e}")
            self.models = {}
    
    def predict_ensemble(self, input_data):
        """Make prediction"""
        if not self.models:
            return self.get_default_prediction()
        
        try:
            # Prepare data
            default_values = {
                'Gender': 'Male',
                'Age': 30,
                'Sleep Duration': 7.0,
                'Quality of Sleep': 7,
                'Physical Activity Level': 50,
                'Stress Level': 5,
                'BMI Category': 'Normal',
                'Heart Rate': 72,
                'Daily Steps': 5000
            }
            
            for key in default_values:
                if key not in input_data:
                    input_data[key] = default_values[key]
            
            # Create DataFrame
            df = pd.DataFrame([input_data])
            
            # Try to use ML model
            if 'logistic' in self.models and 'feature_columns' in self.models:
                # Select features
                features = self.models['feature_columns']
                X = df[features]
                
                # Predict
                prediction = self.models['logistic'].predict(X)[0]
                
                # Decode if label encoder exists
                if 'label_encoder' in self.models:
                    try:
                        le = self.models['label_encoder']
                        if 'Sleep Disorder' in le:
                            prediction = le['Sleep Disorder'].inverse_transform([prediction])[0]
                    except:
                        pass
                
                return {
                    'ensemble_prediction': str(prediction),
                    'risk_level': 'low' if str(prediction) == 'No Disorder' else 'medium',
                    'confidence': 'medium'
                }
            else:
                return self.get_default_prediction()
                
        except Exception as e:
            print(f"⚠️ Prediction error: {e}")
            return self.get_default_prediction()
    
    def get_default_prediction(self):
        """Default prediction"""
        return {
            'ensemble_prediction': 'No Disorder',
            'risk_level': 'low',
            'confidence': 'low',
            'is_simulation': True
        }

# Create instance
ml_service = SimpleMLService()