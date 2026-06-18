@echo off
setlocal EnableExtensions

echo ============================================================
echo  Clear saved GitHub credentials (Windows Credential Manager)
echo ============================================================
echo.
echo This removes cached login for git:https://github.com
echo Next "git push" will ask you to sign in again.
echo.

cmdkey /delete:LegacyGeneric:target=git:https://github.com 2>nul
if %ERRORLEVEL%==0 (
    echo [OK] GitHub credential removed.
) else (
    echo [INFO] No GitHub credential found or already removed.
)

echo.
echo Now open browser and sign in as: https://github.com/VizhichenkoAA
echo Recommended: use Personal Access Token as password when git asks.
pause
