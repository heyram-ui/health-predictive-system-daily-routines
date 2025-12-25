# services/recommendation_engine.py
class RecommendationEngine:
    @staticmethod
    def generate_recommendations(user, daily_data, risk_level):
        """Generate basic recommendations"""
        recommendations = []
        
        if not daily_data:
            return recommendations
        
        # Sleep recommendation
        sleep_hours = daily_data.sleep_hours or 0
        if sleep_hours < 7:
            recommendations.append({
                'category': 'sleep',
                'priority': 'high',
                'title': 'Increase Sleep',
                'description': f'You slept only {sleep_hours} hours. Aim for 7-9 hours.',
                'action': 'Go to bed 30 minutes earlier tonight.',
                'icon': 'moon'
            })
        
        # Steps recommendation
        steps = daily_data.steps or 0
        if steps < 5000:
            recommendations.append({
                'category': 'activity',
                'priority': 'medium',
                'title': 'Walk More',
                'description': f'You walked {steps} steps today.',
                'action': 'Take a 15-minute walk after meals.',
                'icon': 'walking'
            })
        
        # Stress recommendation
        stress = daily_data.stress_level or 5
        if stress > 7:
            recommendations.append({
                'category': 'mental',
                'priority': 'high',
                'title': 'Reduce Stress',
                'description': f'Your stress level is {stress}/10.',
                'action': 'Try deep breathing for 5 minutes.',
                'icon': 'brain'
            })
        
        return recommendations