# Add community.py
class HealthCommunity:
    """Community support for health challenges"""
    
    @staticmethod
    def create_support_group(group_type):
        """Create support groups for specific health conditions"""
        groups = {
            'diabetes': {
                'name': 'Diabetes Support Circle',
                'description': 'Share experiences and tips for managing diabetes',
                'resources': ['meal_plans', 'exercise_routines', 'glucose_logs']
            },
            'insomnia': {
                'name': 'Sleep Better Together',
                'description': 'Support group for improving sleep quality',
                'resources': ['sleep_schedules', 'relaxation_techniques', 'success_stories']
            },
            'anxiety': {
                'name': 'Calm Minds Community',
                'description': 'Safe space for discussing mental health',
                'resources': ['coping_strategies', 'therapist_directory', 'meditation_guides']
            }
        }
        
        return groups.get(group_type)
    
    @staticmethod
    def match_buddies(user1, user2):
        """Match users with similar health goals for mutual support"""
        compatibility_score = 0
        
        # Match based on health goals
        if user1.target_steps == user2.target_steps:
            compatibility_score += 20
        
        # Match based on health conditions
        if user1.health_conditions == user2.health_conditions:
            compatibility_score += 30
        
        # Match based on activity level
        user1_avg = DailyHealthData.query.filter_by(user_id=user1.id).avg('steps') or 0
        user2_avg = DailyHealthData.query.filter_by(user_id=user2.id).avg('steps') or 0
        
        if abs(user1_avg - user2_avg) < 1000:
            compatibility_score += 20
        
        return compatibility_score >= 50