@echo off
echo ============================================
echo   GAMIFY YOUR LIFE - INSTALLER
echo ============================================
echo.

:: Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

:: Run the Python installer
python "%~dp0install.py"

pause
