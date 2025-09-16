from datetime import datetime
import json

class CreativityAgent:
    def __init__(self):
        pass

    def add_entry(self, entry_type, title, content, mood=None, tags=None):
        from config import get_db
        with get_db() as (conn, cur):
            cur.execute('''
                INSERT INTO journal_entries (entry_type, title, content, mood, tags)
                VALUES (?, ?, ?, ?, ?)
            ''', (entry_type, title, content, mood, json.dumps(tags or [])))
            return cur.lastrowid

    def get_entries(self, entry_type=None, tag=None, start_date=None, end_date=None):
        from config import get_db
        
        query = 'SELECT * FROM journal_entries WHERE 1=1'
        params = []
        
        if entry_type:
            query += ' AND entry_type = ?'
            params.append(entry_type)
        if tag:
            query += ' AND tags LIKE ?'
            params.append(f'%{tag}%')
        if start_date:
            query += ' AND created_at >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND created_at <= ?'
            params.append(end_date)
            
        query += ' ORDER BY created_at DESC'
        
        with get_db() as (conn, cur):
            cur.execute(query, params)
            return cur.fetchall()

    def get_entry(self, entry_id):
        from config import get_db
        with get_db() as (conn, cur):
            cur.execute('SELECT * FROM journal_entries WHERE id = ?', (entry_id,))
            return cur.fetchone()

    def update_entry(self, entry_id, title=None, content=None, mood=None, tags=None):
        from config import get_db
        
        updates = []
        params = []
        
        if title:
            updates.append('title = ?')
            params.append(title)
        if content:
            updates.append('content = ?')
            params.append(content)
        if mood:
            updates.append('mood = ?')
            params.append(mood)
        if tags:
            updates.append('tags = ?')
            params.append(json.dumps(tags))
            
        if updates:
            query = f'''
                UPDATE journal_entries 
                SET {', '.join(updates)}
                WHERE id = ?
            '''
            params.append(entry_id)
            with get_db() as (conn, cur):
                cur.execute(query, params)
            
    def delete_entry(self, entry_id):
        from config import get_db
        with get_db() as (conn, cur):
            cur.execute('DELETE FROM journal_entries WHERE id = ?', (entry_id,))
