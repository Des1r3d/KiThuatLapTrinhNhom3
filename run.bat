@echo off
REM Pharmacy Management System - Windows Launcher
REM This script launches the application

echo Starting Pharmacy Management System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.13 or higher
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
pip show PyQt6 >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Launch application
echo Launching application...
python app.py

if errorlevel 1 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)
