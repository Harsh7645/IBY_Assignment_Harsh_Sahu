import sqlite3
import os
from contextlib import contextmanager

DB_PATH = 'data/mindful_app.db'

SCHEMA = '''
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        target_frequency TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS habit_logs (
        id INTEGER PRIMARY KEY,
        habit_id INTEGER,
        completed_at TIMESTAMP,
        notes TEXT,
        FOREIGN KEY (habit_id) REFERENCES habits (id)
    );
    
    CREATE TABLE IF NOT EXISTS journal_entries (
        id INTEGER PRIMARY KEY,
        entry_type TEXT,
        title TEXT,
        content TEXT,
        mood TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        tags TEXT
    );
    
    CREATE TABLE IF NOT EXISTS focus_sessions (
        id INTEGER PRIMARY KEY,
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        duration INTEGER,
        category TEXT,
        notes TEXT
    );
    
    CREATE TABLE IF NOT EXISTS meditation_logs (
        id INTEGER PRIMARY KEY,
        session_type TEXT,
        duration INTEGER,
        notes TEXT,
        completed_at TIMESTAMP
    );
'''

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        yield conn, cursor
        conn.commit()
    finally:
        conn.close()

def init_db():
    """Initialize the database and create tables"""
    os.makedirs('data', exist_ok=True)
    
    with get_db() as (conn, cur):
        # Create tables
        cur.executescript(SCHEMA)
