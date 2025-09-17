import sqlite3
import os

db_path = "../data/mindful_app.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Get all tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    print("Tables:", tables)
    
    # Check focus_sessions table structure
    if 'focus_sessions' in tables:
        cur.execute("PRAGMA table_info(focus_sessions)")
        columns = [row[1] for row in cur.fetchall()]
        print("focus_sessions columns:", columns)
    
    # Check daily_targets table structure
    if 'daily_targets' in tables:
        cur.execute("PRAGMA table_info(daily_targets)")
        columns = [row[1] for row in cur.fetchall()]
        print("daily_targets columns:", columns)
    
    conn.close()
else:
    print("Database file not found")