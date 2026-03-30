@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title YT to MP3 - Install

call setup.bat
if errorlevel 1 (
    echo.
    echo [ERROR] Setup ni uspel. Build se ne bo zagnal.
    pause
    exit /b 1
)

call build.bat
if errorlevel 1 (
    echo.
    echo [ERROR] Build ni uspel.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo     ALL DONE - YT to MP3 IS READY
echo ==========================================
echo Aplikacija je v:
echo dist\YTtoMP3\
pause
exit /b 0