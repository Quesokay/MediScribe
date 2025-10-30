@echo off
echo ======================================================================
echo   VIBE-MEDISCRIBE INTEGRATION STARTER
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Checking dependencies...
python -c "import watchdog" >nul 2>&1
if errorlevel 1 (
    echo Installing watchdog...
    pip install watchdog
)

python -c "import spacy" >nul 2>&1
if errorlevel 1 (
    echo Installing spacy...
    pip install spacy
    python -m spacy download en_core_web_sm
)

echo.
echo Starting Vibe-MediScribe Integration Service...
echo.

python vibe_watcher.py

pause
