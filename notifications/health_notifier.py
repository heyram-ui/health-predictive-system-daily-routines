# notifications/health_notifier.py
class HealthNotifier:
    def __init__(self):
        self.notification_types = {
            'reminder': {
                'sleep': 'Time to wind down for better sleep',
                'water': 'Stay hydrated! Drink water',
                'activity': 'Time for a quick walk',
                'meditation': 'Take 5 minutes to relax'
            },
            'alert': {
                'high_stress': 'High stress detected - try deep breathing',
                'poor_sleep': 'Insufficient sleep patterns detected',
                'low_activity': 'Low activity levels today'
            },
            'achievement': {
                'goal_reached': 'Congratulations! Goal achieved 🎉',
                'streak_milestone': 'New streak record! 🔥',
                'level_up': 'Level up! New features unlocked'
            }
        }
    
    def schedule_smart_notifications(self, user):
        """Schedule personalized notifications"""
        schedule = []
        
        # Based on user patterns
        if user.avg_sleep < 7:
            schedule.append({
                'time': '21:00',
                'type': 'reminder',
                'message': self.notification_types['reminder']['sleep']
            })
        
        if user.avg_steps < 5000:
            schedule.append({
                'time': '15:00',
                'type': 'reminder', 
                'message': self.notification_types['reminder']['activity']
            })
        
        return schedule