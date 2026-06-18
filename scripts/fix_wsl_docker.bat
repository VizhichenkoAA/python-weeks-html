@echo off
setlocal EnableExtensions
echo ============================================================
echo  Launch fix_wsl_docker.ps1 AS ADMINISTRATOR
echo ============================================================
echo.
powershell -NoProfile -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"%~dp0fix_wsl_docker.ps1\"'"
exit /b 0
