from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

router = APIRouter()

class MeditationSession(BaseModel):
    session_type: str
    duration: int
    notes: Optional[str] = None

@router.post("/sessions")
async def log_session(session: MeditationSession):
    from agents.meditation import MeditationModule
    meditation = MeditationModule()
    try:
        meditation.log_session(session.session_type, session.duration, session.notes)
        return {"message": "Meditation session logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/quote")
async def get_daily_quote():
    from agents.meditation import MeditationModule
    meditation = MeditationModule()
    quote = meditation.get_daily_quote()
    return {"quote": quote}

@router.get("/sessions/{session_type}")
async def get_session(session_type: str) -> Dict[str, Any]:
    from agents.meditation import MeditationModule
    meditation = MeditationModule()
    session = meditation.get_session(session_type)
    if not session:
        raise HTTPException(status_code=404, detail="Session type not found")
    return session
