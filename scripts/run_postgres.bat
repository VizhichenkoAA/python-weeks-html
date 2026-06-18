@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."
docker compose up -d
if %ERRORLEVEL% neq 0 (
    echo [ERROR] docker compose failed
    exit /b 1
)
echo [OK] Postgres starting. Wait for healthcheck, then run scripts\run_load.bat
exit /b 0
