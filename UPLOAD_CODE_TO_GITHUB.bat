@echo off
title GitHub Code Uploader
echo ======================================================================
echo 🚀 Uploading Code to GitHub (ranimakeover15-spec/social-media-autopilot)
echo ======================================================================
cd /d "%~dp0"

:: Use portable MinGit directly
set "PATH=%CD%\mingit\cmd;%PATH%"

echo 1. Initializing Git...
git init
git config user.name "ranimakeover15-spec"
git config user.email "ranimakeover15@gmail.com"

echo 2. Adding files...
git add .
git commit -m "🤖 [Autopilot] Complete 24/7 autonomous social media pipeline"
git branch -M main

echo 3. Connecting to GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/ranimakeover15-spec/social-media-autopilot.git

echo 4. Pushing to GitHub...
git push -u origin main --force

echo.
echo ======================================================================
echo 🎉 Code successfully uploaded to GitHub!
echo ======================================================================
echo.
pause
