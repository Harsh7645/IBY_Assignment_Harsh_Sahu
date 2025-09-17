@echo off
echo ================================================================
echo 🧘‍♀️ I'm Beside You - Setup Script
echo ================================================================
echo This script will set up the application environment...
echo ================================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo ✅ Python detected
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv_frontend\" (
    echo 📦 Creating virtual environment...
    python -m venv venv_frontend
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment!
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv_frontend\Scripts\activate.bat

REM Upgrade pip
echo 📈 Upgrading pip...
python -m pip install --upgrade pip

REM Install backend dependencies
echo 📦 Installing backend dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install backend dependencies!
    pause
    exit /b 1
)
cd ..

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd frontend
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install frontend dependencies!
    pause
    exit /b 1
)
cd ..

echo ================================================================
echo ✅ Setup completed successfully!
echo ================================================================
echo You can now run the application using:
echo   start_app.bat          (Windows batch file)
echo   python start_app.py    (Cross-platform Python script)
echo ================================================================
pause