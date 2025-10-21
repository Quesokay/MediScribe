@echo off
echo ============================================
echo MediScribe MCP Server Installation
echo ============================================
echo.

echo Installing MCP dependencies...
pip install mcp>=0.9.0

echo.
echo Verifying MediScribe dependencies...
pip install -r requirements.txt

echo.
echo Downloading spaCy model (if not already installed)...
python -m spacy download en_core_web_sm

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Test the server: python mcp_server.py
echo 2. Run test client: python test_mcp_client.py
echo 3. Configure your MCP client (see MCP_SETUP.md)
echo.
pause
