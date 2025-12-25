# Add mental_health.py
class MentalHealthSupport:
    """AI-powered mental health support"""
    
    @staticmethod
    def analyze_mood_patterns(user_data):
        """Analyze mood trends for depression/anxiety signs"""
        moods = []
        for entry in user_data:
            if entry.mood:
                moods.append({
                    'date': entry.date,
                    'mood': entry.mood,
                    'stress': entry.stress_level
                })
        
        if len(moods) < 3:
            return None
        
        # Detect declining mood patterns
        mood_scores = {'excellent': 5, 'good': 4, 'neutral': 3, 'poor': 2, 'bad': 1}
        scores = [mood_scores.get(m['mood'].lower(), 3) for m in moods[-7:]]
        
        if len(scores) >= 3 and np.mean(scores) < 2.5:
            return {
                'risk': 'high',
                'pattern': 'persistent_low_mood',
                'recommendation': 'Consider speaking with a mental health professional',
                'resources': [
                    'National Suicide Prevention Lifeline: 1-800-273-8255',
                    'Crisis Text Line: Text HOME to 741741',
                    'Find therapists: psychologytoday.com'
                ]
            }
        
        return None
    
    @staticmethod
    def get_coping_strategies(stress_level, mood):
        """Provide personalized coping strategies"""
        strategies = []
        
        if stress_level > 7:
            strategies.append({
                'title': 'Deep Breathing Exercise',
                'duration': '5 minutes',
                'steps': [
                    'Find a quiet place',
                    'Sit comfortably',
                    'Inhale for 4 seconds',
                    'Hold for 4 seconds',
                    'Exhale for 6 seconds',
                    'Repeat 10 times'
                ]
            })
        
        if mood in ['sad', 'depressed', 'anxious']:
            strategies.append({
                'title': 'Mindfulness Meditation',
                'duration': '10 minutes',
                'steps': [
                    'Focus on your breathing',
                    'Acknowledge thoughts without judgment',
                    'Return focus to breath',
                    'Practice self-compassion'
                ],
                'audio_guide': '/static/meditation/breathing.mp3'
            })
        
        return strategies