@echo off
title Jewelry E-commerce Platform - Running
color 0B
echo.
echo ================================================
echo    JEWELRY E-COMMERCE PLATFORM - STARTING
echo ================================================
echo.

:: Check if MySQL is running
echo [Checking MySQL...]
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] MySQL is running!
) else (
    echo [WARNING] MySQL is not running!
    echo Starting XAMPP Control Panel...
    start "" "C:\xampp\xampp-control.exe" 2>nul
    echo.
    echo Please start MySQL in XAMPP, then press any key to continue...
    pause >nul
)
echo.

:: Start Backend Server
echo ================================================
echo    STARTING BACKEND SERVER (FastAPI)
echo ================================================
echo.
echo Starting FastAPI server on http://localhost:8000
echo.
echo API Documentation:
echo   - Swagger UI: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C in this window to stop the server
echo ================================================
echo.

cd /d "%~dp0backend"
start "Jewelry Backend API" cmd /k ""C:\Users\T F\AppData\Local\Programs\Python\Python311\python.exe" -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul
echo.

:: Open Frontend
echo ================================================
echo    STARTING FRONTEND
echo ================================================
echo.
echo Opening frontend in browser...
echo.

:: Check if Live Server is available, otherwise use simple HTTP server
where live-server >nul 2>&1
if %errorlevel%==0 (
    start "Jewelry Frontend" cmd /k "cd /d "%~dp0" && live-server --port=5500"
    timeout /t 2 /nobreak >nul
    start http://localhost:5500
) else (
    :: Use Python's built-in HTTP server as fallback
    start "Jewelry Frontend" cmd /k "cd /d "%~dp0" && "C:\Users\T F\AppData\Local\Programs\Python\Python311\python.exe" -m http.server 8080"
    timeout /t 2 /nobreak >nul
    start http://localhost:8080
)

echo.
echo ================================================
echo    APPLICATION STARTED SUCCESSFULLY!
echo ================================================
echo.
echo Services running:
echo   - Backend API:  http://localhost:8000
echo   - Frontend:     http://localhost:8080 (or 5500)
echo.
echo Test Credentials:
echo   Username: john_doe
echo   Password: password123
echo.
echo Pages available:
echo   - Home:           http://localhost:8080/index.html
echo   - Login:          http://localhost:8080/login.html
echo   - AI Design:      http://localhost:8080/ai-design.html
echo   - API Docs:       http://localhost:8000/docs
echo.
echo Close this window to exit (servers will keep running)
echo ================================================
echo.
pause
