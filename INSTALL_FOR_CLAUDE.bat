@echo off
echo ========================================
echo MediScribe Setup for Claude Desktop
echo ========================================
echo.

echo Step 1: Installing Python packages...
pip install -r requirements.txt

echo.
echo Step 2: Downloading spaCy model...
python -m spacy download en_core_web_sm

echo.
echo Step 3: Testing installation...
python -c "import spacy; import mcp; print('✓ All packages installed!')"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy claude_desktop_config.json content
echo 2. Paste into: %%APPDATA%%\Claude\claude_desktop_config.json
echo 3. Restart Claude Desktop
echo 4. Run: python mcp_server.py
echo.
echo See CLAUDE_SETUP.md for detailed instructions
echo.

pause
