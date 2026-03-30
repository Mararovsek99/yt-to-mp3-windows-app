@echo off
setlocal EnableExtensions
title YT to MP3 - Install

call setup.bat
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Setup ni uspel. Build se ne bo zagnal.
    pause
    exit /b 1
)

call build.bat
if %errorlevel% neq 0 (
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
echo.
pause
exit /b 0