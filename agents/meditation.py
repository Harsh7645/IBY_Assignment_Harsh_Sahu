from datetime import datetime, timedelta
import random

class MeditationModule:
    def __init__(self):
        self.guided_sessions = {
            'breathing': [
                {'name': 'Square Breathing', 'duration': 5, 'instructions': [
                    'Inhale for 4 counts',
                    'Hold for 4 counts',
                    'Exhale for 4 counts',
                    'Hold for 4 counts'
                ]},
                {'name': '4-7-8 Breathing', 'duration': 5, 'instructions': [
                    'Inhale for 4 counts',
                    'Hold for 7 counts',
                    'Exhale for 8 counts'
                ]}
            ],
            'body_scan': [
                {'name': 'Progressive Relaxation', 'duration': 10},
                {'name': 'Mindful Body Awareness', 'duration': 15}
            ],
            'visualization': [
                {'name': 'Safe Place', 'duration': 10},
                {'name': 'Nature Walk', 'duration': 15}
            ]
        }
        
        self.daily_quotes = [
            "Breathe in peace, breathe out stress.",
            "Every moment is a fresh beginning.",
            "Let go of what you can't control.",
            "You are present, you are mindful.",
            "Peace begins with this moment."
        ]

    def get_session(self, session_type='breathing'):
        return random.choice(self.guided_sessions[session_type])

    def log_session(self, session_type, duration, notes=None):
        from config import get_db
        with get_db() as (conn, cur):
            cur.execute('''
                INSERT INTO meditation_logs (session_type, duration, notes, completed_at)
                VALUES (?, ?, ?, ?)
            ''', (session_type, duration, notes, datetime.now()))

    def get_daily_quote(self):
        return random.choice(self.daily_quotes)

    def get_stats(self, timeframe='week'):
        from config import get_db
        start_date = datetime.now()
        if timeframe == 'week':
            start_date -= timedelta(days=7)
        elif timeframe == 'month':
            start_date -= timedelta(days=30)
        
        with get_db() as (conn, cur):
            cur.execute('''
                SELECT session_type, COUNT(*) as sessions, 
                       SUM(duration) as total_minutes
                FROM meditation_logs
                WHERE completed_at >= ?
                GROUP BY session_type
            ''', (start_date,))
            
            return cur.fetchall()
