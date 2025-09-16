from datetime import datetime, timedelta

class StudyTimer:
    def __init__(self):
        self.current_session = None
        self.start_time = None
        self.is_paused = False
        self.pause_duration = 0

    def start_session(self, category='study'):
        from config import get_db
        
        self.start_time = datetime.now()
        self.is_paused = False
        self.pause_duration = 0
        
        with get_db() as (conn, cur):
            cur.execute('''
                INSERT INTO focus_sessions (start_time, category)
                VALUES (?, ?)
            ''', (self.start_time, category))
            self.current_session = cur.lastrowid
        
        return self.current_session

    def pause_session(self):
        if self.start_time and not self.is_paused:
            self.pause_start = datetime.now()
            self.is_paused = True

    def resume_session(self):
        if self.is_paused:
            self.pause_duration += (datetime.now() - self.pause_start).total_seconds()
            self.is_paused = False

    def end_session(self, notes=None):
        from config import get_db
        
        if not self.start_time:
            return None
            
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds() - self.pause_duration
        
        with get_db() as (conn, cur):
            cur.execute('''
                UPDATE focus_sessions
                SET end_time = ?, duration = ?, notes = ?
                WHERE id = ?
            ''', (end_time, duration, notes, self.current_session))
        
        self.start_time = None
        self.current_session = None
        return duration

    def get_session_stats(self, timeframe='today'):
        from config import get_db
        
        if timeframe == 'today':
            start_date = datetime.now().replace(hour=0, minute=0, second=0)
        elif timeframe == 'week':
            start_date = datetime.now() - timedelta(days=7)
        else:
            start_date = datetime.now() - timedelta(days=30)
            
        with get_db() as (conn, cur):
            cur.execute('''
                SELECT 
                    category, 
                    COUNT(*) as sessions, 
                    COALESCE(SUM(duration)/3600.0, 0) as hours
                FROM focus_sessions
                WHERE start_time >= ?
                GROUP BY category
            ''', (start_date,))
            
            results = cur.fetchall()
            return results if results else []

    def is_in_focus(self):
        return self.start_time is not None and not self.is_paused
