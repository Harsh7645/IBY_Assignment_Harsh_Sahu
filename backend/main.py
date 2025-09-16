import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Create FastAPI app
app = FastAPI(title="Mindful App Backend")

app = FastAPI(title="Mindful App Backend")

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(habits.router, prefix="/api/habits", tags=["habits"])
app.include_router(focus.router, prefix="/api/focus", tags=["focus"])
app.include_router(creativity.router, prefix="/api/creativity", tags=["creativity"])
app.include_router(meditation.router, prefix="/api/meditation", tags=["meditation"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
