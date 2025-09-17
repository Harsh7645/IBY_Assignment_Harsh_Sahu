"""
Configuration module for the backend application
"""
import sqlite3
import os
from pathlib import Path

# Database configuration
DB_PATH = Path(__file__).parent.parent / "data" / "mindful_app.db"

def get_db():
    """Get database connection"""
    # Ensure data directory exists
    os.makedirs(DB_PATH.parent, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create habits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            frequency TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create habit_entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        )
    ''')
    
    # Create focus_sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration_minutes INTEGER NOT NULL,
            session_type TEXT DEFAULT 'pomodoro',
            completed BOOLEAN DEFAULT 0,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            notes TEXT
        )
    ''')
    
    # Create meditation_sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meditation_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration_minutes INTEGER NOT NULL,
            meditation_type TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            pre_mood INTEGER,
            post_mood INTEGER
        )
    ''')
    
    # Create meditation_reflections table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meditation_reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            reflection_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES meditation_sessions (id)
        )
    ''')
    
    # Create creativity table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS creativity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            entry_type TEXT DEFAULT 'journal',
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

# Initialize database when module is imported
if __name__ == "__main__":
    init_database()