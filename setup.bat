@echo off
REM Voice Assistant Setup Script for Windows
REM Installs all dependencies and builds the React app

setlocal enabledelayedexpansion

echo ===================================
echo Voice Assistant Setup
echo ===================================

REM Step 1: Install Python dependencies
echo.
echo Step 1: Installing Python dependencies...
pip install -r requirements-deploy.txt
if errorlevel 1 (
    echo Failed to install Python dependencies
    pause
    exit /b 1
)

REM Step 2: Build React app
echo.
echo Step 2: Building React application...
cd react-app
if errorlevel 1 (
    echo Failed to change to react-app directory
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install
    if errorlevel 1 (
        echo Failed to install Node dependencies
        pause
        exit /b 1
    )
)

echo Building React app...
call npm run build
if errorlevel 1 (
    echo Failed to build React app
    pause
    exit /b 1
)

cd ..

echo.
echo ===================================
echo ✓ Setup Complete!
echo ===================================
echo.
echo To start the application:
echo.
echo Development mode:
echo   python app.py
echo.
echo Production mode:
echo   gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 -b 0.0.0.0:5000 wsgi:app
echo.
echo Visit http://localhost:5000
echo.
pause
