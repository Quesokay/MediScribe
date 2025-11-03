@echo off
REM Start ADK API Server for MediScribe
echo ============================================================
echo MediScribe ADK API Server
echo ============================================================
echo.

REM Set Google API Key
set GOOGLE_API_KEY=AIzaSyCZXSOHSVMKt92YQxLvSZl0z8Esk1jypjI

echo Starting ADK API server...
echo Server will be available at: http://localhost:8000
echo Web UI should connect from: http://localhost:4200
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Start ADK API server with MCP integration
adk api_server --allow_origins=http://localhost:4200 --host=0.0.0.0 --port=8000 agents

pause
