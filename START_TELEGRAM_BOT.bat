@echo off
title Rani Makeover - 24/7 Telegram Asset Ingestion Hub
echo ======================================================================
echo 👑 RANI MAKEOVER — 24/7 TELEGRAM BOT DAEMON (@RaniMakeover_reel_bot)
echo ======================================================================
cd /d "%~dp0"

python core\telegram_bot_daemon.py

echo.
pause
