from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class CanvasEntry(BaseModel):
    entry_type: str
    title: str
    content: str
    mood: Optional[str] = None
    tags: Optional[List[str]] = None

class CanvasEntryResponse(CanvasEntry):
    id: int
    created_at: datetime

@router.post("/entries", response_model=CanvasEntryResponse)
async def create_entry(entry: CanvasEntry):
    from agents.creativity import CreativityAgent
    agent = CreativityAgent()
    entry_id = agent.add_entry(
        entry.entry_type,
        entry.title,
        entry.content,
        mood=entry.mood,
        tags=entry.tags
    )
    return {
        **entry.dict(),
        "id": entry_id,
        "created_at": datetime.now()
    }

@router.get("/entries")
async def get_entries(entry_type: Optional[str] = None, tag: Optional[str] = None):
    from agents.creativity import CreativityAgent
    agent = CreativityAgent()
    entries = agent.get_entries(entry_type=entry_type, tag=tag)
    return {
        "entries": entries
    }

@router.get("/entries/{entry_id}")
async def get_entry(entry_id: int):
    from agents.creativity import CreativityAgent
    agent = CreativityAgent()
    entry = agent.get_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry
