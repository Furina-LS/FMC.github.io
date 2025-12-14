@echo off
REM ===================================================================
REM Mouse Clicker Launcher
REM A professional launcher for the Mouse Clicker application
REM ===================================================================

setlocal EnableDelayedExpansion

REM ==================================================
REM Check if Python is installed and accessible
REM ==================================================
echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in your PATH!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo During installation, make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM ==================================================
REM Run the Mouse Clicker application
REM ==================================================
echo Python found! Starting Mouse Clicker...

echo.
echo Mouse Clicker has been launched successfully!
echo ===================================================================
echo ^|                  How to Use Mouse Clicker                       ^|
echo ===================================================================
echo ^| 1. Move your mouse to the desired clicking location              ^|
echo ^| 2. Press F9 to START/STOP clicking                              ^|
echo ^| 3. Adjust clicking speed using slider or input box               ^|
echo ^| 4. View current status (Running/Stopped) in the window          ^|
echo ===================================================================
echo.
echo Tip: If the window doesn't appear, check your taskbar!
echo.

REM Run the application in background using pythonw to hide console
start "Mouse Clicker" /B pythonw "%~dp0\mouse_clicker.py"

REM Keep the launcher window open for a few seconds for user to read
timeout /t 5 /nobreak >nul

echo Closing launcher...
exit /b 0
