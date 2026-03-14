@echo off
REM Run all tests for Pharmacy Management System

echo Running Unit Tests...
echo.

REM Check if pytest is installed
pip show pytest >nul 2>&1
if errorlevel 1 (
    echo Installing pytest...
    pip install pytest pytest-cov
)

REM Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

echo.
echo Tests completed!
pause
