@echo off
REM Complete startup script for MediScribe with ADK
echo ============================================================
echo MediScribe + Google ADK Integration
echo ============================================================
echo.
echo This will start:
echo   1. ADK API Server (backend) on http://localhost:8000
echo   2. ADK Web UI (frontend) on http://localhost:4200
echo.
echo Two terminal windows will open.
echo Keep both running to use the voice interface.
echo ============================================================
echo.

REM Start API server in new window
start "MediScribe ADK API Server" cmd /k start_adk_server.bat

REM Wait a bit for server to start
echo Waiting for API server to start...
timeout /t 5 /nobreak >nul

REM Start Web UI in new window
start "MediScribe ADK Web UI" cmd /k start_adk_web.bat

echo.
echo ============================================================
echo Both services are starting...
echo.
echo Once ready, open your browser to: http://localhost:4200
echo.
echo You can now use voice interaction with Gemini 2.5 Flash
echo to transcribe, translate, and extract medical data!
echo ============================================================
echo.

pause
