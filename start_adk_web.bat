@echo off
REM Start ADK Web UI for MediScribe
echo ============================================================
echo MediScribe ADK Web UI
echo ============================================================
echo.

cd adk-web

echo Installing dependencies (if needed)...
call npm install

echo.
echo Starting web UI...
echo Web UI will be available at: http://localhost:4200
echo Make sure ADK API server is running on http://localhost:8000
echo.
echo Press Ctrl+C to stop the web UI
echo ============================================================
echo.

REM Start web UI with backend configuration
call npm run serve --backend=http://localhost:8000

pause
