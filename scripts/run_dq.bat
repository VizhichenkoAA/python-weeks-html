@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."
set "ENV_NAME=tp-v03"
set "PYTHONPATH=src"
set "CONDA_EXE=%USERPROFILE%\miniconda3\Scripts\conda.exe"
if not exist "%CONDA_EXE%" set "CONDA_EXE=conda.exe"
"%CONDA_EXE%" run -n %ENV_NAME% python -m sem2_de.dq
exit /b %ERRORLEVEL%
