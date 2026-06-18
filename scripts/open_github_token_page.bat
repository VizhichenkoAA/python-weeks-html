@echo off
setlocal EnableExtensions

echo ============================================================
echo  Create GitHub Personal Access Token (for git push)
echo ============================================================
echo.
echo 1. Sign OUT of other GitHub accounts in browser.
echo 2. Sign IN as: https://github.com/VizhichenkoAA
echo 3. Open: https://github.com/settings/tokens
echo 4. Generate new token (classic), scope: repo
echo 5. Copy token (shown once).
echo.
echo When git push asks for password, paste the TOKEN (not account password).
echo.
start https://github.com/settings/tokens
pause
