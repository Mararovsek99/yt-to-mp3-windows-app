@echo off
setlocal EnableExtensions EnableDelayedExpansion
title YT to MP3 - Setup

echo ==========================================
echo          YT to MP3 SETUP
echo ==========================================
echo.

where py >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python launcher (py) ni namescen ali ni v PATH.
    echo Namesti Python za Windows in obkljukaj "Add Python to PATH".
    pause
    exit /b 1
)

echo [1/5] Preverjam Python...
py --version
if %errorlevel% neq 0 (
    echo [ERROR] Python ni pravilno namescen.
    pause
    exit /b 1
)

echo.
echo [2/5] Nadgrajujem pip...
py -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [ERROR] pip upgrade ni uspel.
    pause
    exit /b 1
)

echo.
echo [3/5] Namescam Python pakete...
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Namestitev requirements.txt ni uspela.
    pause
    exit /b 1
)

echo.
echo [4/5] Pripravljam bin mapo...
if not exist bin mkdir bin

echo.
echo [5/5] Prenalagam yt-dlp in FFmpeg...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference='Stop';" ^
  "Invoke-WebRequest 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe' -OutFile 'bin\\yt-dlp.exe';" ^
  "Invoke-WebRequest 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'bin\\ffmpeg.zip';" ^
  "if (Test-Path 'bin\\ffmpeg_temp') { Remove-Item 'bin\\ffmpeg_temp' -Recurse -Force };" ^
  "Expand-Archive 'bin\\ffmpeg.zip' -DestinationPath 'bin\\ffmpeg_temp' -Force;" ^
  "$ffmpeg = Get-ChildItem 'bin\\ffmpeg_temp' -Recurse -Filter 'ffmpeg.exe' | Select-Object -First 1;" ^
  "$ffprobe = Get-ChildItem 'bin\\ffmpeg_temp' -Recurse -Filter 'ffprobe.exe' | Select-Object -First 1;" ^
  "if (-not $ffmpeg) { throw 'ffmpeg.exe not found after extraction.' };" ^
  "if (-not $ffprobe) { throw 'ffprobe.exe not found after extraction.' };" ^
  "Copy-Item $ffmpeg.FullName 'bin\\ffmpeg.exe' -Force;" ^
  "Copy-Item $ffprobe.FullName 'bin\\ffprobe.exe' -Force;" ^
  "Remove-Item 'bin\\ffmpeg.zip' -Force;" ^
  "Remove-Item 'bin\\ffmpeg_temp' -Recurse -Force;"
if %errorlevel% neq 0 (
    echo [ERROR] Download ali extract za yt-dlp / FFmpeg ni uspel.
    pause
    exit /b 1
)

if not exist bin\yt-dlp.exe (
    echo [ERROR] bin\yt-dlp.exe manjka.
    pause
    exit /b 1
)

if not exist bin\ffmpeg.exe (
    echo [ERROR] bin\ffmpeg.exe manjka.
    pause
    exit /b 1
)

if not exist bin\ffprobe.exe (
    echo [ERROR] bin\ffprobe.exe manjka.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Setup completed successfully.
echo ==========================================
echo Zdaj lahko zazenes build.bat ali install.bat
echo.
pause
exit /b 0