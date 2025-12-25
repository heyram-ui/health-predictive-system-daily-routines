# gamification/challenges.py
class HealthChallenges:
    CHALLENGES = {
        '10k_steps': {
            'name': '10K Steps Daily',
            'description': 'Walk 10,000 steps every day for a week',
            'reward': 1000,
            'icon': '🏃‍♂️',
            'target': 10000,
            'duration': 7
        },
        'sleep_master': {
            'name': 'Sleep Master',
            'description': 'Maintain 8 hours sleep for 5 consecutive nights',
            'reward': 1500,
            'icon': '😴',
            'target': 8,
            'duration': 5
        },
        'hydration_champ': {
            'name': 'Hydration Champion',
            'description': 'Drink 2L water daily for 7 days',
            'reward': 800,
            'icon': '💧',
            'target': 2.0,
            'duration': 7
        }
    }
    
    def check_challenge_completion(self, user_id, challenge_id):
        """Check if user completed challenge"""
        challenge = self.CHALLENGES[challenge_id]
        user_data = self.get_user_data(user_id, challenge['duration'])
        
        completed = all(
            self.evaluate_day(day_data, challenge)
            for day_data in user_data
        )
        
        if completed:
            self.award_rewards(user_id, challenge['reward'])
            self.unlock_achievement(user_id, challenge_id)
        
        return completed