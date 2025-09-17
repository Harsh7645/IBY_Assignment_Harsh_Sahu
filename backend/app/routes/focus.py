from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime, date, timedelta
import sqlite3
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from config import get_db

router = APIRouter()

class FocusSessionStart(BaseModel):
    duration_minutes: int
    task_selected: Optional[str] = None
    break_enabled: bool = True
    break_duration: int = 5

class FocusSessionUpdate(BaseModel):
    status: str  # 'paused', 'resumed', 'completed', 'cancelled'
    completed_duration: Optional[int] = None
    tree_stage: Optional[int] = None

class DailyTarget(BaseModel):
    target_description: str
    category: str = "General"
    priority: str = "medium"

@router.post("/start-session")
async def start_focus_session(session_data: FocusSessionStart):
    try:
        conn = get_db()
        cur = conn.cursor()
        current_date = date.today().isoformat()
        cur.execute('''
            INSERT INTO focus_sessions 
            (date, task_selected, duration_minutes, break_enabled, break_duration, status, start_time)
            VALUES (?, ?, ?, ?, ?, 'running', ?)
        ''', (current_date, session_data.task_selected, session_data.duration_minutes, 
              session_data.break_enabled, session_data.break_duration, datetime.now()))
        
        session_id = cur.lastrowid
        conn.commit()
        conn.close()
        return {
            "session_id": session_id,
            "status": "started",
            "duration_minutes": session_data.duration_minutes,
            "message": "Focus session started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting session: {str(e)}")

@router.put("/session/{session_id}")
async def update_focus_session(session_id: int, update_data: FocusSessionUpdate):
    try:
        conn = get_db()
        cur = conn.cursor()
        update_fields = []
        values = []
        
        if update_data.status:
            update_fields.append("status = ?")
            values.append(update_data.status)
            
            # If completing session, set end_time
            if update_data.status == 'completed':
                update_fields.append("end_time = ?")
                values.append(datetime.now())
        
        if update_data.completed_duration is not None:
            update_fields.append("completed_duration = ?")
            values.append(update_data.completed_duration)
        
        if update_data.tree_stage is not None:
            update_fields.append("tree_stage = ?")
            values.append(update_data.tree_stage)
        
        values.append(session_id)
        
        cur.execute(f'''
            UPDATE focus_sessions 
        SET {", ".join(update_fields)}
        WHERE id = ?
        ''', values)
        
        conn.commit()
        conn.close()
        return {"message": "Session updated successfully", "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating session: {str(e)}")

@router.get("/daily-progress")
async def get_daily_progress():
    try:
        conn = get_db()
        cur = conn.cursor()
        current_date = date.today().isoformat()
        
        # Get today's completed focus time
        cur.execute('''
            SELECT COALESCE(SUM(completed_duration), 0) as total_minutes,
                   COUNT(*) as sessions_count
            FROM focus_sessions 
            WHERE date = ? AND status = 'completed'
        ''', (current_date,))
        
        result = cur.fetchone()
        total_minutes = result[0] if result else 0
        sessions_count = result[1] if result else 0
        
        # Get yesterday's focus time for comparison
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
        cur.execute('''
            SELECT COALESCE(SUM(completed_duration), 0) as yesterday_minutes
            FROM focus_sessions 
            WHERE date = ? AND status = 'completed'
        ''', (yesterday,))
        
        yesterday_result = cur.fetchone()
        yesterday_minutes = yesterday_result[0] if yesterday_result else 0
        
        # Count total trees planted (completed sessions)
        cur.execute('''
            SELECT COUNT(*) as trees_planted
            FROM focus_sessions 
            WHERE status = 'completed'
        ''')
        
        trees_result = cur.fetchone()
        trees_planted = trees_result[0] if trees_result else 0
        
        conn.close()
        return {
            "today_minutes": total_minutes,
            "today_hours": round(total_minutes / 60, 1),
            "yesterday_minutes": yesterday_minutes,
            "sessions_today": sessions_count,
            "trees_planted": trees_planted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting daily progress: {str(e)}")

@router.get("/targets")
async def get_daily_targets():
    try:
        conn = get_db()
        cur = conn.cursor()
        current_date = date.today().isoformat()
        cur.execute('''
            SELECT id, target_description, category, is_completed, priority
            FROM daily_targets 
            WHERE date = ?
            ORDER BY 
                CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
                is_completed ASC
        ''', (current_date,))
        
        targets = []
        for row in cur.fetchall():
            targets.append({
                "id": row[0],
                "target_description": row[1],
                "category": row[2],
                "is_completed": bool(row[3]),
                "priority": row[4]
            })
        
        conn.close()
        return {"targets": targets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting targets: {str(e)}")

@router.post("/targets")
async def add_daily_target(target: DailyTarget):
    try:
        conn = get_db()
        cur = conn.cursor()
        current_date = date.today().isoformat()
        cur.execute('''
            INSERT INTO daily_targets (date, target_description, category, priority)
            VALUES (?, ?, ?, ?)
        ''', (current_date, target.target_description, target.category, target.priority))
        
        target_id = cur.lastrowid
        conn.commit()
        conn.close()
        return {
            "id": target_id,
            "message": "Target added successfully",
            **target.dict()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding target: {str(e)}")

@router.put("/targets/{target_id}/complete")
async def complete_target(target_id: int):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            UPDATE daily_targets 
            SET is_completed = 1
            WHERE id = ?
        ''', (target_id,))
        
        conn.commit()
        conn.close()
        return {"message": "Target marked as completed", "target_id": target_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error completing target: {str(e)}")

@router.get("/active-session")
async def get_active_session():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            SELECT id, task_selected, duration_minutes, completed_duration, 
                   tree_stage, start_time, break_enabled, break_duration
            FROM focus_sessions 
            WHERE status = 'running'
            ORDER BY start_time DESC
            LIMIT 1
        ''')
        
        result = cur.fetchone()
        if result:
            conn.close()
            return {
                "session_id": result[0],
                "task_selected": result[1],
                "duration_minutes": result[2],
                "completed_duration": result[3] or 0,
                "tree_stage": result[4] or 0,
                "start_time": result[5],
                "break_enabled": bool(result[6]),
                "break_duration": result[7]
            }
        else:
            conn.close()
            return {"session_id": None, "message": "No active session"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting active session: {str(e)}")
