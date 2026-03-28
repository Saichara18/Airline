@echo off
REM ProjectAir - Quick Start Setup Script for Windows

echo.
echo ========================================
echo   ProjectAir - SQLite Production Ready
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt

echo [4/4] Initializing database...
python setup_database.py

echo.
echo ========================================
echo   ✅ Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Run this command:
echo      venv\Scripts\activate.bat
echo   2. Then run:
echo      cd frontend
echo      python app.py
echo.
echo   Access the app at: http://localhost:5000
echo.
echo To deploy on Render:
echo   1. Read: README.md
echo   2. Check: DEPLOYMENT_CHECKLIST.md
echo   3. Follow: PRODUCTION_GUIDE.md
echo.
pause
