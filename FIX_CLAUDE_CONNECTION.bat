@echo off
echo ========================================
echo Fix Claude Desktop MCP Connection
echo ========================================
echo.

echo Step 1: Finding Python path...
for /f "tokens=*" %%i in ('where python') do set PYTHON_PATH=%%i
echo Python found at: %PYTHON_PATH%
echo.

echo Step 2: Killing all Claude processes...
taskkill /F /IM claude.exe 2>nul
if %errorlevel% equ 0 (
    echo ✓ Claude processes stopped
) else (
    echo ℹ️  No Claude processes running
)
echo.

echo Step 3: Waiting 5 seconds...
timeout /t 5 /nobreak >nul
echo.

echo Step 4: Testing MCP server...
python test_mcp_connection.py
echo.

echo Step 5: Updating Claude config with full Python path...
echo {> "%APPDATA%\Claude\claude_desktop_config.json"
echo   "mcpServers": {>> "%APPDATA%\Claude\claude_desktop_config.json"
echo     "mediscribe": {>> "%APPDATA%\Claude\claude_desktop_config.json"
echo       "command": "%PYTHON_PATH:\=/%",>> "%APPDATA%\Claude\claude_desktop_config.json"
echo       "args": [>> "%APPDATA%\Claude\claude_desktop_config.json"
echo         "C:/Clone_wars/MediScribe/mcp_server.py">> "%APPDATA%\Claude\claude_desktop_config.json"
echo       ]>> "%APPDATA%\Claude\claude_desktop_config.json"
echo     }>> "%APPDATA%\Claude\claude_desktop_config.json"
echo   }>> "%APPDATA%\Claude\claude_desktop_config.json"
echo }>> "%APPDATA%\Claude\claude_desktop_config.json"
echo ✓ Config updated
echo.

echo ========================================
echo Configuration Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start MCP server: python mcp_server.py
echo 2. Start Claude Desktop
echo 3. Wait 30 seconds
echo 4. Look for tools icon in Claude
echo.

pause
