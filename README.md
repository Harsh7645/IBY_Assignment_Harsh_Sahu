# I'm Beside You - Mindfulness and Productivity App

A full-stack application that helps users manage their productivity, mindfulness, and personal growth through various features including habit tracking, focus sessions, meditation, and creative journaling.

## Project Structure

```
I'm Beside You Assignment/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── habits.py
│   │   │   ├── focus.py
│   │   │   ├── creativity.py
│   │   │   └── meditation.py
│   │   └── __init__.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── agents/
│   ├── habit_tracker.py
│   ├── study_timer.py
│   ├── meditation.py
│   └── creativity.py
├── data/
│   └── mindful_app.db
├── start_backend.bat
└── start_frontend.bat
```

## Features

- Habit Tracking
- Focus Timer
- Meditation Sessions
- Creative Journaling
- Daily Quotes and Prompts

## Setup

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv_frontend
.\venv_frontend\Scripts\activate
```

2. Install dependencies:
```bash
cd frontend
pip install -r requirements.txt
```

3. Start the Streamlit app:
```bash
streamlit run app.py
```

## Quick Start

For Windows users, you can use the provided batch files:

1. Start the backend:
```bash
start_backend.bat
```

2. Start the frontend:
```bash
start_frontend.bat
```

## API Documentation

Once the backend is running, you can access:
- API documentation at http://localhost:8000/docs
- Alternative API documentation at http://localhost:8000/redoc

## Frontend Access

The Streamlit frontend will be available at http://localhost:8501
