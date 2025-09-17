@echo off
echo ================================================================
echo 🧘‍♀️ I'm Beside You - Mindfulness & Productivity Companion
echo ================================================================
echo Starting application services...
echo 📍 Backend will be available at: http://localhost:8000
echo 📍 Frontend will be available at: http://localhost:8501
echo 📖 API Documentation: http://localhost:8000/docs
echo ================================================================

REM Check if virtual environment exists
if not exist "venv_frontend\" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first to install dependencies.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv_frontend\Scripts\activate.bat

REM Start backend in new window
echo 🚀 Starting Backend API server...
start "Backend API" cmd /k "cd backend && python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend
echo 🎨 Starting Frontend application...
cd frontend
streamlit run app.py

pause