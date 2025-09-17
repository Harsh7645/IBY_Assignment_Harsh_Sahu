from fastapi import APIRouter, HTTPException
from typing import List, Optional
import sqlite3
from datetime import datetime, timedelta
import random
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from config import get_db

router = APIRouter()

# Pool of motivational meditation quotes
MEDITATION_QUOTES = [
    "The mind is everything. What you think you become. - Buddha",
    "Meditation is not about stopping thoughts, but recognizing that you are not your thoughts.",
    "Peace comes from within. Do not seek it without. - Buddha", 
    "In the midst of movement and chaos, keep stillness inside of you.",
    "The present moment is the only time over which we have dominion. - Thich Nhat Hanh",
    "Meditation is a way for nourishing and blossoming the divinity within you.",
    "Quiet the mind and the soul will speak.",
    "Your calm mind is the ultimate weapon against your challenges.",
    "Meditation brings wisdom; lack of meditation leaves ignorance.",
    "The goal of meditation isn't to control your thoughts, it's to stop letting them control you."
]

def get_db_connection():
    """Get database connection"""
    # Get the project root directory (go up from backend/app/routes/)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    db_path = os.path.join(project_root, 'data', 'mindful_app.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_meditation_tables():
    """Initialize meditation-related database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create meditation sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meditation_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration_minutes INTEGER NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'completed',
            notes TEXT
        )
    """)
    
    # Create meditation reflections table for post-session thoughts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meditation_reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            mood_rating INTEGER,
            thoughts TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES meditation_sessions (id)
        )
    """)
    
    conn.commit()
    conn.close()

@router.get("/quote")
async def get_daily_quote():
    """Get a random motivational quote for meditation"""
    quote = random.choice(MEDITATION_QUOTES)
    return {"quote": quote}

@router.get("/daily-progress")
async def get_daily_meditation_progress():
    """Get today's meditation progress and weekly streak"""
    initialize_meditation_tables()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Today's meditation time
    cursor.execute("""
        SELECT SUM(duration_minutes) as today_minutes
        FROM meditation_sessions 
        WHERE DATE(completed_at) = DATE('now')
        AND status = 'completed'
    """)
    
    today_result = cursor.fetchone()
    today_minutes = today_result['today_minutes'] or 0
    
    # Weekly meditation days
    cursor.execute("""
        SELECT COUNT(DISTINCT DATE(completed_at)) as weekly_days
        FROM meditation_sessions 
        WHERE DATE(completed_at) >= DATE('now', '-7 days')
        AND status = 'completed'
    """)
    
    weekly_result = cursor.fetchone()
    weekly_days = weekly_result['weekly_days'] or 0
    
    # Calculate meditation streak (consecutive days)
    cursor.execute("""
        SELECT DISTINCT DATE(completed_at) as meditation_date
        FROM meditation_sessions 
        WHERE status = 'completed'
        ORDER BY meditation_date DESC
    """)
    
    meditation_dates = [row['meditation_date'] for row in cursor.fetchall()]
    
    # Calculate streak
    streak = 0
    current_date = datetime.now().date()
    
    for i, meditation_date in enumerate(meditation_dates):
        meditation_date_obj = datetime.strptime(meditation_date, '%Y-%m-%d').date()
        expected_date = current_date - timedelta(days=i)
        
        if meditation_date_obj == expected_date:
            streak += 1
        else:
            break
    
    conn.close()
    
    return {
        "today_minutes": today_minutes,
        "weekly_days": weekly_days,
        "streak_days": streak
    }

@router.post("/start-session")
async def start_meditation_session(session_data: dict):
    """Start a new meditation session"""
    initialize_meditation_tables()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO meditation_sessions (duration_minutes, status)
        VALUES (?, ?)
    """, (session_data["duration_minutes"], "in_progress"))
    
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"session_id": session_id, "message": "Meditation session started"}

@router.put("/complete-session/{session_id}")
async def complete_meditation_session(session_id: int, completion_data: dict = None):
    """Complete a meditation session"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE meditation_sessions 
        SET status = 'completed', completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (session_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": "Meditation session completed successfully"}

@router.post("/reflection")
async def add_meditation_reflection(reflection_data: dict):
    """Add post-meditation reflection/thoughts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO meditation_reflections (session_id, mood_rating, thoughts)
        VALUES (?, ?, ?)
    """, (reflection_data.get("session_id"), reflection_data.get("mood_rating"), reflection_data.get("thoughts")))
    
    conn.commit()
    conn.close()
    
    return {"message": "Reflection saved successfully"}

@router.get("/active-session")
async def get_active_meditation_session():
    """Check if there's an active meditation session"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM meditation_sessions 
        WHERE status = 'in_progress'
        ORDER BY id DESC LIMIT 1
    """)
    
    session = cursor.fetchone()
    conn.close()
    
    if session:
        return dict(session)
    return None
