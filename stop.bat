@echo off
title Jewelry E-commerce Platform - Stop All
color 0C
echo.
echo ================================================
echo    STOPPING ALL SERVICES
echo ================================================
echo.

echo Stopping Python servers...
taskkill /F /IM python.exe /T 2>nul
echo.

echo Stopping Node.js servers (live-server)...
taskkill /F /IM node.exe /T 2>nul
echo.

echo ================================================
echo    ALL SERVICES STOPPED
echo ================================================
echo.
pause
