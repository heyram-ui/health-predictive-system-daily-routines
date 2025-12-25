# chronic_disease.py - Complete implementation
import json
from datetime import datetime, timedelta

class ChronicDiseaseManager:
    """Comprehensive chronic disease management system"""
    
    def __init__(self):
        self.disease_profiles = self.load_disease_profiles()
    
    def load_disease_profiles(self):
        """Load disease management guidelines"""
        return {
            'diabetes': {
                'name': 'Diabetes',
                'critical_params': ['blood_sugar', 'blood_pressure', 'weight'],
                'targets': {
                    'fasting_blood_sugar': {'min': 80, 'max': 130},
                    'post_meal_sugar': {'min': 80, 'max': 180},
                    'blood_pressure': {'systolic': {'min': 90, 'max': 140},
                                      'diastolic': {'min': 60, 'max': 90}},
                    'bmi': {'min': 18.5, 'max': 25}
                },
                'daily_checklist': [
                    'Check blood sugar',
                    'Take medication',
                    'Monitor feet',
                    'Stay hydrated'
                ],
                'emergency_symptoms': [
                    'extreme thirst',
                    'frequent urination',
                    'blurred vision',
                    'fatigue'
                ]
            },
            'hypertension': {
                'name': 'Hypertension (High Blood Pressure)',
                'critical_params': ['blood_pressure', 'heart_rate', 'stress_level'],
                'targets': {
                    'blood_pressure': {'systolic': {'min': 90, 'max': 120},
                                      'diastolic': {'min': 60, 'max': 80}},
                    'salt_intake': {'max': 2300},  # mg per day
                    'stress_level': {'max': 5}
                },
                'diet_recommendations': [
                    'Low sodium diet',
                    'Increase potassium',
                    'Reduce caffeine',
                    'Limit alcohol'
                ]
            },
            'sleep_apnea': {
                'name': 'Sleep Apnea',
                'critical_params': ['sleep_hours', 'snoring', 'daytime_sleepiness'],
                'monitoring': [
                    'Use CPAP if prescribed',
                    'Sleep on side',
                    'Avoid alcohol before bed',
                    'Maintain healthy weight'
                ]
            },
            'asthma': {
                'name': 'Asthma',
                'critical_params': ['breathing_difficulty', 'peak_flow', 'cough'],
                'action_plan': {
                    'green_zone': 'No symptoms, use maintenance inhaler',
                    'yellow_zone': 'Mild symptoms, use rescue inhaler',
                    'red_zone': 'Severe symptoms, seek emergency care'
                }
            }
        }
    
    def create_personalized_plan(self, user, disease_type):
        """Create personalized disease management plan"""
        profile = self.disease_profiles.get(disease_type)
        if not profile:
            return None
        
        plan = {
            'disease': profile['name'],
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'user_info': {
                'name': user.username,
                'age': user.age,
                'bmi': user.calculate_bmi()
            },
            'daily_targets': profile.get('targets', {}),
            'daily_checklist': profile.get('daily_checklist', []),
            'medication_schedule': self.generate_medication_schedule(disease_type),
            'appointment_reminders': self.generate_appointments(disease_type),
            'emergency_contacts': self.get_emergency_contacts(user.id),
            'progress_tracking': {
                'parameters_to_track': profile['critical_params'],
                'frequency': 'daily',
                'goal': 'Maintain parameters within target ranges'
            }
        }
        
        return plan
    
    def track_progress(self, user_id, disease_type, readings):
        """Track disease progress and provide feedback"""
        profile = self.disease_profiles.get(disease_type)
        if not profile:
            return None
        
        feedback = []
        warnings = []
        
        # Check each parameter
        for param, value in readings.items():
            if param in profile.get('targets', {}):
                targets = profile['targets'][param]
                
                if isinstance(targets, dict) and 'min' in targets and 'max' in targets:
                    if value < targets['min']:
                        warnings.append(f"{param} is too low: {value} (target: {targets['min']}-{targets['max']})")
                    elif value > targets['max']:
                        warnings.append(f"{param} is too high: {value} (target: {targets['min']}-{targets['max']})")
                    else:
                        feedback.append(f"✅ {param} is within target range")
        
        # Calculate compliance score
        total_params = len(profile.get('targets', {}))
        compliant_params = len(feedback)
        compliance_score = (compliant_params / total_params * 100) if total_params > 0 else 0
        
        return {
            'compliance_score': round(compliance_score, 1),
            'feedback': feedback,
            'warnings': warnings,
            'next_steps': self.get_next_steps(disease_type, readings),
            'trend': self.analyze_trend(user_id, disease_type, readings)
        }
    
    def generate_medication_schedule(self, disease_type):
        """Generate medication schedule based on disease"""
        schedules = {
            'diabetes': [
                {'medication': 'Metformin', 'time': 'Morning with breakfast', 'dose': 'As prescribed'},
                {'medication': 'Insulin (if prescribed)', 'time': 'Before meals', 'dose': 'As prescribed'}
            ],
            'hypertension': [
                {'medication': 'Blood pressure medication', 'time': 'Morning', 'dose': 'As prescribed'}
            ],
            'asthma': [
                {'medication': 'Controller inhaler', 'time': 'Morning and evening', 'dose': 'As prescribed'},
                {'medication': 'Rescue inhaler', 'time': 'As needed', 'dose': 'For symptoms'}
            ]
        }
        
        return schedules.get(disease_type, [])
    
    def get_emergency_contacts(self, user_id):
        """Get user's emergency contacts"""
        # In real implementation, fetch from database
        return [
            {'name': 'Primary Care Physician', 'phone': 'Clinic number'},
            {'name': 'Emergency Contact', 'phone': 'Family member'},
            {'name': 'Pharmacy', 'phone': 'Local pharmacy'}
        ]