from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class FocusSession(BaseModel):
    category: str
    notes: Optional[str] = None

class FocusSessionResponse(FocusSession):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None

@router.post("/start", response_model=FocusSessionResponse)
async def start_session(session: FocusSession):
    from agents.study_timer import StudyTimer
    timer = StudyTimer()
    session_id = timer.start_session(session.category)
    return {
        **session.dict(),
        "id": session_id,
        "start_time": datetime.now(),
    }

@router.post("/{session_id}/end")
async def end_session(session_id: int, session: FocusSession):
    from agents.study_timer import StudyTimer
    timer = StudyTimer()
    try:
        duration = timer.end_session(notes=session.notes)
        return {
            "message": "Session ended successfully",
            "duration_minutes": duration / 60 if duration else 0
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/stats")
async def get_stats(timeframe: str = "today"):
    from agents.study_timer import StudyTimer
    timer = StudyTimer()
    stats = timer.get_session_stats(timeframe)
    return {
        "timeframe": timeframe,
        "stats": [
            {
                "category": cat,
                "sessions": count,
                "hours": hours
            }
            for cat, count, hours in stats
        ] if stats else []
    }
