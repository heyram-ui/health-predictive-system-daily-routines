# Add accessibility.py
class AccessibilityFeatures:
    """Features for users with disabilities"""
    
    @staticmethod
    def voice_commands_enabled():
        """Enable voice navigation for visually impaired users"""
        return '''
        <script>
        // Voice command recognition
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            
            recognition.onresult = function(event) {
                const transcript = event.results[event.resultIndex][0].transcript;
                
                // Voice commands
                if (transcript.includes('predict health')) {
                    window.location.href = '/predict';
                }
                if (transcript.includes('my dashboard')) {
                    window.location.href = '/dashboard';
                }
                if (transcript.includes('emergency')) {
                    document.getElementById('emergency-btn').click();
                }
            };
            
            // Start listening when button pressed
            document.getElementById('voice-btn').addEventListener('click', function() {
                recognition.start();
                speak('Voice commands activated. Say predict health, my dashboard, or emergency.');
            });
        }
        
        function speak(text) {
            const utterance = new SpeechSynthesisUtterance(text);
            speechSynthesis.speak(utterance);
        }
        </script>
        '''
    
    @staticmethod
    def high_contrast_mode():
        """High contrast theme for visually impaired users"""
        return '''
        <style>
        .high-contrast {
            background: black !important;
            color: yellow !important;
        }
        .high-contrast a {
            color: cyan !important;
            text-decoration: underline !important;
        }
        .high-contrast button {
            background: yellow !important;
            color: black !important;
            border: 3px solid white !important;
        }
        </style>
        '''