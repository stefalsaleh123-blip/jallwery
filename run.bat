@echo off
title Jewelry E-commerce Platform
color 0E
echo.
echo ========================================================
echo        JEWELRY E-COMMERCE PLATFORM
echo        Running Frontend + Backend Together
echo ========================================================
echo.

:: Set Python path
set PYTHON_PATH=C:\Users\T F\AppData\Local\Programs\Python\Python311\python.exe

:: Check MySQL
echo [1/3] Checking MySQL...
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo       MySQL is running [OK]
) else (
    echo       MySQL not running - Starting XAMPP...
    start "" "C:\xampp\xampp-control.exe" 2>nul
    echo       Please start MySQL in XAMPP Control Panel
    echo       Press any key after MySQL starts...
    pause >nul
)
echo.

:: Start Backend
echo [2/3] Starting Backend Server (FastAPI)...
cd /d "%~dp0backend"
start "Backend API - Port 8000" /min cmd /c ""%PYTHON_PATH%" -m uvicorn main:app --host 0.0.0.0 --port 8000"
echo       Backend starting at http://localhost:8000
echo.
timeout /t 3 /nobreak >nul

:: Start Frontend
echo [3/3] Starting Frontend Server...
cd /d "%~dp0"
start "Frontend Server - Port 8080" /min cmd /c ""%PYTHON_PATH%" -m http.server 8080"
echo       Frontend starting at http://localhost:8080
echo.
timeout /t 2 /nobreak >nul

:: Open Browser
echo ========================================================
echo        OPENING BROWSER...
echo ========================================================
echo.
start http://localhost:8080/index.html

echo ========================================================
echo        ALL SERVICES RUNNING!
echo ========================================================
echo.
echo    Backend API:  http://localhost:8000
echo    Frontend:     http://localhost:8080
echo    API Docs:     http://localhost:8000/docs
echo.
echo    Test Login:
echo    Username: john_doe
echo    Password: password123
echo.
echo ========================================================
echo    Press any key to STOP all servers
echo ========================================================
pause >nul

:: Stop all services
echo.
echo Stopping services...
taskkill /F /FI "WINDOWTITLE eq Backend API*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Frontend Server*" >nul 2>&1
echo All services stopped.
timeout /t 2 /nobreak >nul
