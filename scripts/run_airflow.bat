@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."
docker compose -f docker-compose.airflow.yml up -d
echo [OK] Airflow UI: http://localhost:8080  login: airflow / airflow
exit /b %ERRORLEVEL%
