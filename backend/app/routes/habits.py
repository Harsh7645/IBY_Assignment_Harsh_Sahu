from fastapi import APIRouter, HTTPException
from typing import List, Optional
import sqlite3
from datetime import datetime, timedelta
import random
import os

router = APIRouter()

# Category icons mapping (using web icon URLs)
CATEGORY_ICONS = {
    "Health": "https://cdn-icons-png.flaticon.com/512/2382/2382533.png",
    "Learning": "https://cdn-icons-png.flaticon.com/512/3330/3330165.png", 
    "Productivity": "https://cdn-icons-png.flaticon.com/512/1055/1055666.png",
    "Wellness": "https://cdn-icons-png.flaticon.com/512/2382/2382461.png",
    "Exercise": "https://cdn-icons-png.flaticon.com/512/2382/2382460.png",
    "Mindfulness": "https://cdn-icons-png.flaticon.com/512/3588/3588435.png"
}

def get_db_connection():
    """Get database connection"""
    # Get the project root directory (go up from backend/app/routes/)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    db_path = os.path.join(project_root, 'data', 'mindful_app.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def create_synthetic_habits_data():
    """Create realistic synthetic habit data for 5 sample users"""
    
    synthetic_users_habits = [
        # User 1: Health-focused student
        [
            {"name": "Drink 8 glasses of water daily", "category": "Health", "streak": 23},
            {"name": "Study for 2 hours every morning", "category": "Learning", "streak": 15},
            {"name": "Do 30 push-ups before breakfast", "category": "Exercise", "streak": 8},
            {"name": "Meditate for 10 minutes", "category": "Mindfulness", "streak": 18},
            {"name": "Write in gratitude journal", "category": "Wellness", "streak": 12}
        ],
        
        # User 2: Productivity enthusiast
        [
            {"name": "Read for 30 minutes before bed", "category": "Learning", "streak": 27},
            {"name": "Complete daily to-do list", "category": "Productivity", "streak": 11},
            {"name": "Take vitamins after lunch", "category": "Health", "streak": 31},
            {"name": "Walk 10,000 steps daily", "category": "Exercise", "streak": 6},
            {"name": "Practice deep breathing exercises", "category": "Mindfulness", "streak": 4}
        ],
        
        # User 3: Fitness and wellness focused
        [
            {"name": "Morning workout for 45 minutes", "category": "Exercise", "streak": 19},
            {"name": "Eat 5 servings of fruits/vegetables", "category": "Health", "streak": 14},
            {"name": "Practice coding problems daily", "category": "Learning", "streak": 22},
            {"name": "Evening skincare routine", "category": "Wellness", "streak": 25},
            {"name": "Digital detox 1 hour before bed", "category": "Mindfulness", "streak": 7}
        ],
        
        # User 4: Learning and personal development
        [
            {"name": "Listen to educational podcast", "category": "Learning", "streak": 16},
            {"name": "Drink green tea every morning", "category": "Health", "streak": 29},
            {"name": "Organize workspace daily", "category": "Productivity", "streak": 9},
            {"name": "Yoga session for 20 minutes", "category": "Exercise", "streak": 13},
            {"name": "Practice mindful eating", "category": "Mindfulness", "streak": 5}
        ],
        
        # User 5: Balanced lifestyle focused
        [
            {"name": "Take stairs instead of elevator", "category": "Exercise", "streak": 21},
            {"name": "Write daily reflection notes", "category": "Wellness", "streak": 17},
            {"name": "Learn 10 new vocabulary words", "category": "Learning", "streak": 10},
            {"name": "Prepare healthy lunch", "category": "Health", "streak": 24},
            {"name": "Practice time-blocking schedule", "category": "Productivity", "streak": 3}
        ]
    ]
    
    # For this implementation, we'll use User 1's habits as default
    return synthetic_users_habits[0]

def initialize_synthetic_habits():
    """Initialize database with synthetic habit data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if habits already exist
    cursor.execute("SELECT COUNT(*) as count FROM habits")
    if cursor.fetchone()['count'] > 0:
        conn.close()
        return
    
    # Get synthetic habits for default user
    synthetic_habits = create_synthetic_habits_data()
    
    for habit in synthetic_habits:
        # Insert habit
        cursor.execute("""
            INSERT INTO habits (name, category, target_frequency, created_at)
            VALUES (?, ?, ?, ?)
        """, (habit["name"], habit["category"], "Daily", datetime.now()))
        
        habit_id = cursor.lastrowid
        
        # Create synthetic habit logs for streak
        for i in range(habit["streak"]):
            log_date = datetime.now() - timedelta(days=i)
            cursor.execute("""
                INSERT INTO habit_logs (habit_id, completed_at)
                VALUES (?, ?)
            """, (habit_id, log_date))
    
    conn.commit()
    conn.close()

def calculate_habit_streak(habit_id):
    """Calculate current streak for a habit"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all completion dates for this habit, ordered by date descending
    cursor.execute("""
        SELECT DATE(completed_at) as completion_date
        FROM habit_logs 
        WHERE habit_id = ?
        ORDER BY completion_date DESC
    """, (habit_id,))
    
    completion_dates = [row['completion_date'] for row in cursor.fetchall()]
    
    if not completion_dates:
        conn.close()
        return 0
    
    # Calculate streak from today backwards
    streak = 0
    current_date = datetime.now().date()
    
    # Check consecutive days
    for i, completion_date in enumerate(completion_dates):
        completion_date_obj = datetime.strptime(completion_date, '%Y-%m-%d').date()
        expected_date = current_date - timedelta(days=i)
        
        if completion_date_obj == expected_date:
            streak += 1
        else:
            break
    
    conn.close()
    return streak

@router.get("/")
async def get_habits():
    """Get all habits with current streaks"""
    # Initialize synthetic data if needed
    initialize_synthetic_habits()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT h.*, 
               MAX(DATE(hl.completed_at)) as last_completed
        FROM habits h
        LEFT JOIN habit_logs hl ON h.id = hl.habit_id
        GROUP BY h.id
        ORDER BY h.created_at DESC
    """)
    
    habits = []
    for row in cursor.fetchall():
        # Calculate current streak
        streak = calculate_habit_streak(row['id'])
        
        habits.append({
            "id": row['id'],
            "name": row['name'],
            "category": row['category'],
            "target_frequency": row['target_frequency'],
            "streak": streak,
            "icon": CATEGORY_ICONS.get(row['category'], CATEGORY_ICONS['Health']),
            "last_completed": row['last_completed']
        })
    
    conn.close()
    return {"habits": habits}

@router.get("/top-streaks")
async def get_top_streaks():
    """Get top 3 habit streaks for dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM habits")
    habits = cursor.fetchall()
    
    habit_streaks = []
    for habit in habits:
        streak = calculate_habit_streak(habit['id'])
        if streak > 0:
            habit_streaks.append({
                "id": habit['id'],
                "name": habit['name'],
                "category": habit['category'],
                "streak": streak,
                "icon": CATEGORY_ICONS.get(habit['category'], CATEGORY_ICONS['Health'])
            })
    
    # Sort by streak and get top 3
    top_streaks = sorted(habit_streaks, key=lambda x: x['streak'], reverse=True)[:3]
    
    conn.close()
    return {"top_streaks": top_streaks}

@router.post("/")
async def create_habit(habit_data: dict):
    """Create a new habit"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO habits (name, category, target_frequency, created_at)
        VALUES (?, ?, ?, ?)
    """, (habit_data["name"], habit_data["category"], habit_data["target_frequency"], datetime.now()))
    
    habit_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"id": habit_id, "message": "Habit created successfully"}

@router.post("/{habit_id}/log")
async def log_habit_completion(habit_id: int):
    """Log habit completion for today"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if already completed today
    cursor.execute("""
        SELECT COUNT(*) as count FROM habit_logs 
        WHERE habit_id = ? AND DATE(completed_at) = DATE('now')
    """, (habit_id,))
    
    if cursor.fetchone()['count'] > 0:
        conn.close()
        raise HTTPException(status_code=400, detail="Habit already completed today")
    
    cursor.execute("""
        INSERT INTO habit_logs (habit_id, completed_at)
        VALUES (?, ?)
    """, (habit_id, datetime.now()))
    
    conn.commit()
    conn.close()
    
    return {"message": "Habit completion logged successfully"}

@router.get("/{habit_id}/streak")
async def get_habit_streak(habit_id: int):
    """Get streak for specific habit"""
    streak = calculate_habit_streak(habit_id)
    return {"habit_id": habit_id, "streak": streak}
