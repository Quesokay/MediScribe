@echo off
echo ======================================================================
echo   MULTILINGUAL VIBE-MEDISCRIBE INTEGRATION STARTER
echo ======================================================================
echo   Supports: Shona, Ndebele, Zulu, Xhosa, Afrikaans -^> English
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

python -c "import transformers" >nul 2>&1
if errorlevel 1 (
    echo Installing transformers...
    pip install transformers torch sentencepiece protobuf
)

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
echo Starting Multilingual Vibe-MediScribe Integration Service...
echo.
echo NOTE: First run will download ~2.5GB NLLB translation model
echo This is a one-time download and may take 5-10 minutes
echo.

python vibe_watcher_multilingual.py

pause
