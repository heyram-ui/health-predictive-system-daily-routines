# gamification/level_system.py
class LevelSystem:
    LEVELS = {
        1: {'name': 'Beginner', 'points_required': 0, 'reward': None},
        2: {'name': 'Active', 'points_required': 1000, 'reward': 'Basic Insights'},
        3: {'name': 'Pro', 'points_required': 5000, 'reward': 'Advanced Analytics'},
        4: {'name': 'Expert', 'points_required': 15000, 'reward': 'Personal Coach'},
        5: {'name': 'Master', 'points_required': 30000, 'reward': 'All Features'}
    }
    
    def calculate_level(self, total_points):
        """Calculate user level based on points"""
        for level, data in sorted(self.LEVELS.items(), reverse=True):
            if total_points >= data['points_required']:
                return level
        return 1