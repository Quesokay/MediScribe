@echo off
echo ========================================
echo MediScribe - ChatGPT Voice Mode Setup
echo ========================================
echo.

echo Step 1: Installing Python packages...
pip install spacy transformers torch mcp

echo.
echo Step 2: Downloading spaCy model...
python -m spacy download en_core_web_sm

echo.
echo Step 3: Testing installation...
python -c "import spacy; import transformers; import mcp; print('✓ All packages installed successfully!')"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: python realtime_chatgpt_processor.py
echo 2. Or start MCP server: python mcp_server.py
echo.
echo See README_CHATGPT_INTEGRATION.md for full guide
echo.

pause
