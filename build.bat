@echo off
setlocal EnableExtensions
title YT to MP3 - Build

echo ==========================================
echo           YT to MP3 BUILD
echo ==========================================
echo.

if not exist app.py (
    echo [ERROR] app.py manjka.
    pause
    exit /b 1
)

if not exist bin\yt-dlp.exe (
    echo [ERROR] bin\yt-dlp.exe manjka. Najprej zazeni setup.bat
    pause
    exit /b 1
)

if not exist bin\ffmpeg.exe (
    echo [ERROR] bin\ffmpeg.exe manjka. Najprej zazeni setup.bat
    pause
    exit /b 1
)

if not exist bin\ffprobe.exe (
    echo [ERROR] bin\ffprobe.exe manjka. Najprej zazeni setup.bat
    pause
    exit /b 1
)

echo [1/3] Cistim stare build datoteke...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist YTtoMP3.spec del /q YTtoMP3.spec

echo.
echo [2/3] Gradim aplikacijo...
py -m PyInstaller ^
  --noconfirm ^
  --windowed ^
  --name YTtoMP3 ^
  --add-data "bin;bin" ^
  app.py

if %errorlevel% neq 0 (
    echo [ERROR] Build ni uspel.
    pause
    exit /b 1
)

echo.
echo [3/3] Build completed.
echo Output:
echo dist\YTtoMP3\
echo.
pause
exit /b 0