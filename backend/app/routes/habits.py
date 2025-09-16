from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class HabitBase(BaseModel):
    name: str
    category: str
    target_frequency: str

class HabitCreate(HabitBase):
    pass

class Habit(HabitBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class HabitLog(BaseModel):
    habit_id: int
    notes: Optional[str] = None

@router.post("/", response_model=Habit)
async def create_habit(habit: HabitCreate):
    from agents.habit_tracker import HabitTracker
    tracker = HabitTracker()
    habit_id = tracker.add_habit(habit.name, habit.category, habit.target_frequency)
    return {**habit.dict(), "id": habit_id, "created_at": datetime.now()}

@router.get("/", response_model=List[Habit])
async def get_habits():
    from agents.habit_tracker import HabitTracker
    tracker = HabitTracker()
    habits = tracker.get_all_habits()
    return habits

@router.post("/{habit_id}/log")
async def log_habit(habit_id: int, log: HabitLog):
    from agents.habit_tracker import HabitTracker
    tracker = HabitTracker()
    try:
        tracker.log_habit(habit_id, notes=log.notes)
        return {"message": "Habit logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{habit_id}/streak")
async def get_streak(habit_id: int):
    from agents.habit_tracker import HabitTracker
    tracker = HabitTracker()
    streak = tracker.get_streak(habit_id)
    return {"streak": streak}
