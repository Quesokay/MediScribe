@echo off
echo ======================================================================
echo   INSTALLING MEDISCRIBE DEPENDENCIES
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

echo Installing dependencies one at a time (to handle network issues)...
echo.

echo [1/8] Installing watchdog...
pip install --default-timeout=100 watchdog
if errorlevel 1 (
    echo WARNING: watchdog installation failed, retrying...
    pip install --default-timeout=100 --retries 5 watchdog
)

echo.
echo [2/8] Installing spacy...
pip install --default-timeout=100 spacy
if errorlevel 1 (
    echo WARNING: spacy installation failed, retrying...
    pip install --default-timeout=100 --retries 5 spacy
)

echo.
echo [3/8] Downloading spacy model...
python -m spacy download en_core_web_sm

echo.
echo [4/8] Installing sentencepiece (for translation)...
pip install --default-timeout=100 sentencepiece
if errorlevel 1 (
    echo WARNING: sentencepiece installation failed, retrying...
    pip install --default-timeout=100 --retries 5 sentencepiece
)

echo.
echo [5/8] Installing protobuf...
pip install --default-timeout=100 protobuf
if errorlevel 1 (
    echo WARNING: protobuf installation failed, retrying...
    pip install --default-timeout=100 --retries 5 protobuf
)

echo.
echo [6/8] Installing transformers (for NLLB translation)...
pip install --default-timeout=100 transformers
if errorlevel 1 (
    echo WARNING: transformers installation failed, retrying...
    pip install --default-timeout=100 --retries 5 transformers
)

echo.
echo [7/8] Installing torch (for NLLB translation)...
pip install --default-timeout=100 torch
if errorlevel 1 (
    echo WARNING: torch installation failed, retrying...
    pip install --default-timeout=100 --retries 5 torch
)

echo.
echo [8/8] Installing accelerate...
pip install --default-timeout=100 accelerate
if errorlevel 1 (
    echo WARNING: accelerate installation failed, retrying...
    pip install --default-timeout=100 --retries 5 accelerate
)

echo.
echo ======================================================================
echo   INSTALLATION COMPLETE
echo ======================================================================
echo.
echo Next steps:
echo   1. Configure Vibe save directory
echo   2. Edit vibe_config_multilingual.json
echo   3. Run: python vibe_watcher_multilingual.py
echo.
pause
