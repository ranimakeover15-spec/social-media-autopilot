@echo off
title YouTube OAuth Token Generator
echo ======================================================================
echo 🔑 YouTube OAuth 2.0 Token Generator
echo ======================================================================
cd /d "%~dp0"

echo Current Directory: %CD%
echo.

if not exist "client_secrets.json" (
    echo ❌ ERROR: 'client_secrets.json' nahi mila!
    echo.
    pause
    exit /b 1
)

python scripts\generate_youtube_token.py

if exist "logs\YOUTUBE_SECRETS_FOR_GITHUB.txt" (
    echo.
    echo 📋 Notepad me secrets open kiye ja rahe hain...
    start notepad "logs\YOUTUBE_SECRETS_FOR_GITHUB.txt"
)

echo.
pause
