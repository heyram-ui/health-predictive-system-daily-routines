# gamification/achievements.py
class AchievementSystem:
    ACHIEVEMENTS = {
        'first_prediction': {'name': 'First Prediction', 'icon': '🔮', 'points': 100},
        'week_streak': {'name': '7-Day Streak', 'icon': '🔥', 'points': 500},
        'health_guru': {'name': 'Health Guru', 'icon': '👨‍⚕️', 'points': 1000},
        'sleep_expert': {'name': 'Sleep Expert', 'icon': '🌙', 'points': 750},
        'activity_champ': {'name': 'Activity Champion', 'icon': '🏆', 'points': 800}
    }
    
    def check_and_award(self, user):
        """Check user progress and award achievements"""
        new_achievements = []
        
        # Check streak
        if user.streak_days >= 7:
            if not self.has_achievement(user, 'week_streak'):
                new_achievements.append('week_streak')
        
        # Check health score
        if user.health_score >= 90:
            if not self.has_achievement(user, 'health_guru'):
                new_achievements.append('health_guru')
        
        # Award new achievements
        for achievement_id in new_achievements:
            self.award_achievement(user, achievement_id)
        
        return new_achievements