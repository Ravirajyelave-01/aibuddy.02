@echo off
echo Installing Voice Assistant dependencies...
echo.

python --version
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To run the voice assistant, execute: python main.py
echo.
pause
