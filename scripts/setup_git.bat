@echo off
setlocal EnableExtensions

echo ============================================================
echo  TP Project - Git setup for VizhichenkoAA
echo ============================================================
echo.

cd /d "%~dp0\.."
echo Working directory: %CD%
echo.

echo [1/4] Current GLOBAL git identity:
git config --global user.name
git config --global user.email
echo.

echo [2/4] Setting LOCAL identity for this repo only:
git config user.name "Alex Vizhichenko"
git config user.email "l.iluinceva@mail.ru"
echo   user.name  = %CD% ... OK
git config user.name
git config user.email
echo.

echo [3/4] Stored GitHub credentials in Windows:
cmdkey /list | findstr /i "github"
echo.
echo If push asks for wrong account, run:
echo   scripts\clear_github_credentials.bat
echo Then run git push again and sign in as VizhichenkoAA.
echo.

echo [4/4] Git status:
git status -sb
echo.
echo Done. Next: create repo on GitHub and run scripts\connect_github.bat
pause
