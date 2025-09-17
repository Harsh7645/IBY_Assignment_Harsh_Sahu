#!/usr/bin/env python3
"""
Simple startup script for I'm Beside You Application
This script starts both the backend and frontend services
"""

import subprocess
import sys
import time
import os
from threading import Thread

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting Backend API server...")
    backend_path = os.path.join(os.getcwd(), "backend")
    subprocess.run([sys.executable, "main.py"], cwd=backend_path)

def start_frontend():
    """Start the Streamlit frontend server"""
    print("🎨 Starting Frontend application...")
    time.sleep(3)  # Give backend time to start
    frontend_path = os.path.join(os.getcwd(), "frontend")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], cwd=frontend_path)

def main():
    print("=" * 60)
    print("🧘‍♀️ I'm Beside You - Mindfulness & Productivity Companion")
    print("=" * 60)
    print("Starting application services...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📍 Frontend will be available at: http://localhost:8501")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if directories exist
    if not os.path.exists("backend"):
        print("❌ Backend directory not found!")
        sys.exit(1)
    if not os.path.exists("frontend"):
        print("❌ Frontend directory not found!")
        sys.exit(1)
    
    # Start backend in a separate thread
    backend_thread = Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Start frontend in main thread
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n👋 Shutting down application...")
        sys.exit(0)

if __name__ == "__main__":
    main()