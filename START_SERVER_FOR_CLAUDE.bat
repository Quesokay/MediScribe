@echo off
cls
echo ========================================
echo MediScribe MCP Server for Claude
echo ========================================
echo.
echo Starting MCP server...
echo.
echo IMPORTANT:
echo - Keep this window open
echo - Don't type anything here
echo - Use Claude Desktop to interact
echo.
echo ========================================
echo.

python mcp_server.py

echo.
echo Server stopped.
pause
