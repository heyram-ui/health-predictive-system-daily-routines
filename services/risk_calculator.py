# services/risk_calculator.py
class RiskCalculator:
    @staticmethod
    def calculate_health_score(daily_data):
        """Simple health score calculation"""
        if not daily_data:
            return 50.0
        
        score = 0
        
        # Sleep (0-25)
        sleep_hours = daily_data.sleep_hours or 0
        if 7 <= sleep_hours <= 9:
            score += 25
        elif 6 <= sleep_hours <= 10:
            score += 20
        elif 5 <= sleep_hours <= 11:
            score += 15
        else:
            score += 10
        
        # Steps (0-20)
        steps = daily_data.steps or 0
        if steps >= 10000:
            score += 20
        elif steps >= 7500:
            score += 15
        elif steps >= 5000:
            score += 10
        else:
            score += 5
        
        # Stress (0-15)
        stress = daily_data.stress_level or 5
        score += max(0, 15 - stress)
        
        # Water (0-10)
        water = daily_data.water_intake or 0
        if water >= 2.0:
            score += 10
        elif water >= 1.5:
            score += 7
        elif water >= 1.0:
            score += 5
        else:
            score += 3
        
        # Heart rate (0-10)
        hr = daily_data.heart_rate or 72
        if 60 <= hr <= 100:
            score += 10
        else:
            score += 5
        
        # BMI (0-10)
        bmi = daily_data.bmi or 22
        if 18.5 <= bmi <= 24.9:
            score += 10
        elif 17 <= bmi <= 30:
            score += 7
        else:
            score += 4
        
        return min(100, round(score, 1))