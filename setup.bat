@echo off
title Jewelry E-commerce Platform - Setup
color 0A
echo.
echo ================================================
echo    JEWELRY E-COMMERCE PLATFORM - SETUP WIZARD
echo ================================================
echo.

:: Check if Python is installed
echo [Step 1/5] Checking Python installation...
"C:\Users\T F\AppData\Local\Programs\Python\Python311\python.exe" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found!
echo.

:: Check if XAMPP MySQL is running
echo [Step 2/5] Checking MySQL (XAMPP)...
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] MySQL is running!
) else (
    echo [WARNING] MySQL is not running!
    echo Please start MySQL from XAMPP Control Panel.
    echo.
    echo Opening XAMPP Control Panel...
    start "" "C:\xampp\xampp-control.exe" 2>nul
    echo.
    echo After starting MySQL, press any key to continue...
    pause >nul
)
echo.

:: Create database if not exists
echo [Step 3/5] Creating database...
"C:\xampp\mysql\bin\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS jewelry_db;" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create database!
    echo Make sure MySQL is running in XAMPP.
    pause
    exit /b 1
)
echo [OK] Database 'jewelry_db' created/verified!
echo.

:: Install Python dependencies
echo [Step 4/5] Installing Python dependencies...
cd /d "%~dp0backend"
"C:\Users\T F\AppData\Local\Programs\Python\Python311\python.exe" -m pip install --upgrade pip --quiet
"C:\Users\T F\AppData\Local\Programs\Python\Python311\python.exe" -m pip install fastapi uvicorn sqlalchemy pymysql pydantic pydantic-settings python-jose passlib python-multipart python-dotenv email-validator bcrypt==4.0.1 google-generativeai --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo [OK] Dependencies installed!
echo.

:: Create .env file if not exists
echo [Step 5/5] Configuring environment...
if not exist .env (
    copy .env.example .env >nul
    echo [OK] Created .env file!
    echo.
    echo [IMPORTANT] Please edit backend\.env and add your Gemini API key!
    echo Get your API key from: https://makersuite.google.com/app/apikey
) else (
    echo [OK] .env file already exists!
)
echo.

:: Run seeder
echo ================================================
echo    RUNNING DATABASE SEEDER...
echo ================================================
"C:\Users\T F\AppData\Local\Programs\Python\Python311\python.exe" seeder.py
if %errorlevel% neq 0 (
    echo [ERROR] Seeder failed!
    pause
    exit /b 1
)
echo.

echo ================================================
echo    SETUP COMPLETED SUCCESSFULLY!
echo ================================================
echo.
echo Test Credentials:
echo   Username: john_doe
echo   Password: password123
echo.
echo Next steps:
echo   1. Make sure MySQL is running in XAMPP
echo   2. Edit backend\.env with your Gemini API key (optional)
echo   3. Run start.bat to start the application
echo.
pause
