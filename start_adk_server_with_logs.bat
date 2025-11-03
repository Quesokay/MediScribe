@echo off
REM Start ADK API Server with logging
echo Starting ADK API server with logging...

set GOOGLE_API_KEY=AIzaSyCZXSOHSVMKt92YQxLvSZl0z8Esk1jypjI

REM Start server and capture output to log file
adk api_server --allow_origins=http://localhost:4200 --host=0.0.0.0 --port=8000 agents > adk_server.log 2>&1

pause
