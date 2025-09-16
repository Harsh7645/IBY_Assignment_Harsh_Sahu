from datetime import datetime, timedelta

class HabitTracker:
    def __init__(self):
        pass

    def add_habit(self, name, category, target_frequency):
        from config import get_db
        with get_db() as (conn, cur):
            cur.execute('''
                INSERT INTO habits (name, category, target_frequency)
                VALUES (?, ?, ?)
            ''', (name, category, target_frequency))
            return cur.lastrowid

    def log_habit(self, habit_id, completed=True, notes=None):
        from config import get_db
        with get_db() as (conn, cur):
            cur.execute('''
                INSERT INTO habit_logs (habit_id, completed_at, notes)
                VALUES (?, datetime('now', 'localtime'), ?)
            ''', (habit_id, notes))

    def get_streak(self, habit_id):
        from config import get_db
        with get_db() as (conn, cur):
            cur.execute('''
                SELECT date(completed_at) as completed_date 
                FROM habit_logs
                WHERE habit_id = ?
                ORDER BY completed_at DESC
            ''', (habit_id,))
            logs = cur.fetchall()
        
        if not logs:
            return 0
            
        streak = 0
        last_date = datetime.now().date()
        
        for (completed_at,) in logs:
            # SQLite date() function returns YYYY-MM-DD format
            completed_date = datetime.strptime(completed_at, '%Y-%m-%d').date()
            if (last_date - completed_date).days == 1:
                streak += 1
                last_date = completed_date
            else:
                break
        return streak

    def get_habit_stats(self, habit_id, timeframe='week'):
        from config import get_db
        # Calculate date range
        end_date = datetime.now()
        if timeframe == 'week':
            start_date = end_date - timedelta(days=7)
        elif timeframe == 'month':
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=365)
            
        with get_db() as (conn, cur):
            cur.execute('''
                SELECT COUNT(*) as count, 
                       date(completed_at) as day,
                       strftime('%Y-%m-%d', completed_at) as formatted_day
                FROM habit_logs
                WHERE habit_id = ? 
                AND date(completed_at) BETWEEN date(?) AND date(?)
                GROUP BY day
                ORDER BY day DESC
            ''', (habit_id, start_date, end_date))
            
            results = cur.fetchall()
            return results if results else []

    def get_all_habits(self):
        from config import get_db
        with get_db() as (conn, cur):
            cur.execute('SELECT * FROM habits')
            return cur.fetchall()

    def get_habit_by_id(self, habit_id):
        from config import get_db
        with get_db() as (conn, cur):
            cur.execute('SELECT * FROM habits WHERE id = ?', (habit_id,))
            return cur.fetchone()
