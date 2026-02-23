@echo off
REM Production run script for Windows

setlocal enabledelayedexpansion

set PORT=5000
set WORKERS=1
set TIMEOUT=120

if not "%1"=="" set PORT=%1
if not "%2"=="" set WORKERS=%2
if not "%3"=="" set TIMEOUT=%3

echo Starting Voice Assistant Server...
echo Port: %PORT%
echo Workers: %WORKERS%
echo Timeout: %TIMEOUT%
echo.

gunicorn ^
  --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker ^
  -w %WORKERS% ^
  -b 0.0.0.0:%PORT% ^
  --timeout %TIMEOUT% ^
  --access-logfile - ^
  --error-logfile - ^
  wsgi:app

pause
