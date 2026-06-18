@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."
set "ENV_NAME=tp-v03"
set "PYTHONPATH=src"
set "CONDA_EXE=%USERPROFILE%\miniconda3\Scripts\conda.exe"
if not exist "%CONDA_EXE%" set "CONDA_EXE=conda.exe"
if not exist ".env" (
    echo [INFO] copying .env.example to .env
    copy /Y .env.example .env >nul
)
"%CONDA_EXE%" run -n %ENV_NAME% python -m sem2_de.cli load
exit /b %ERRORLEVEL%
