@echo off
REM NUAA WebUI Quick Start - Windows
REM Double-click this file to start the WebUI

title NUAA WebUI Quick Start

echo.
echo ===================================================================
echo.
echo           NUAA WebUI - One-Click Start (Windows)
echo.
echo           Starting up... Please wait...
echo.
echo ===================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Run the quick start script
python quick-start.py

REM If the script exits, pause so user can see any errors
pause
