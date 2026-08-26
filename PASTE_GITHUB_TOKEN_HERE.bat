@echo off
title GitHub 1-Click Uploader (Token Mode)
echo ======================================================================
echo 🚀 GitHub Token-Based Instant Uploader
echo ======================================================================
cd /d "%~dp0"
set "PATH=%CD%\mingit\cmd;%PATH%"

echo.
set /p GITHUB_TOKEN="👉 Chrome se copy kiya hua GitHub Token yahan Paste karein: "

if "%GITHUB_TOKEN%"=="" (
    echo ❌ Token khali hai! Kripya token paste karein.
    pause
    exit /b 1
)

echo.
echo 1. Adding files...
git init
git config user.name "ranimakeover15-spec"
git config user.email "ranimakeover15@gmail.com"
git add .
git commit -m "🤖 [Autopilot] Complete 24/7 autonomous social media pipeline"
git branch -M main

echo 2. Pushing to GitHub (ranimakeover15-spec/social-media-autopilot)...
git remote remove origin 2>nul
git remote add origin https://ranimakeover15-spec:%GITHUB_TOKEN%@github.com/ranimakeover15-spec/social-media-autopilot.git

git push -u origin main --force

echo.
if %ERRORLEVEL% equ 0 (
    echo ======================================================================
    echo 🎉 BADHAI HO! Aapka sara code GitHub par 100%% upload ho gaya!
    echo ======================================================================
) else (
    echo ❌ Upload failed. Kripya check karein ki token sahi hai ya nahi.
)
echo.
pause
