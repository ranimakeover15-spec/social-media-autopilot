@echo off
title Rani Makeover - Master Agency Reel Generator
echo ======================================================================
echo 👑 RANI MAKEOVER — 10/10 MASTER AGENCY REEL GENERATOR
echo ======================================================================
cd /d "%~dp0"

python scripts\generate_and_vault_rani_reels.py

echo.
pause
