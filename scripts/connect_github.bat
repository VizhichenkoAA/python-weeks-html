@echo off
setlocal EnableExtensions

set REPO_URL=https://github.com/VizhichenkoAA/python-weeks-html.git

cd /d "%~dp0\.."
echo ============================================================
echo  Connect local repo to GitHub
echo ============================================================
echo.
echo Target remote: %REPO_URL%
echo.
echo BEFORE running: create empty repo on GitHub:
echo   https://github.com/new
echo   Name: python-weeks-html
echo   Public, WITHOUT README / .gitignore / license
echo.

set /p CONFIRM=Repo created on GitHub? Press Enter to continue or Ctrl+C to cancel...

git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main

echo.
echo Pushing initial commit...
git push -u origin main
if %ERRORLEVEL%==0 (
    echo [OK] Remote connected and pushed.
) else (
    echo [ERROR] Push failed. Try:
    echo   1. scripts\clear_github_credentials.bat
    echo   2. git push -u origin main
    echo   3. Use PAT token as password if prompted
)
pause
