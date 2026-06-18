@echo off
setlocal EnableExtensions

cd /d "%~dp0\.."
set "ENV_NAME=tp-v03"
set "PYTHON_VERSION=3.11"

echo ============================================================
echo  TP variant 03 - setup_env.bat
echo ============================================================

set "CONDA_EXE="
if exist "%USERPROFILE%\miniconda3\Scripts\conda.exe" (
    set "CONDA_EXE=%USERPROFILE%\miniconda3\Scripts\conda.exe"
    goto :found_conda
)
if exist "%USERPROFILE%\anaconda3\Scripts\conda.exe" (
    set "CONDA_EXE=%USERPROFILE%\anaconda3\Scripts\conda.exe"
    goto :found_conda
)
if exist "%ProgramData%\miniconda3\Scripts\conda.exe" (
    set "CONDA_EXE=%ProgramData%\miniconda3\Scripts\conda.exe"
    goto :found_conda
)
where conda.exe >nul 2>&1
if %ERRORLEVEL%==0 (
    set "CONDA_EXE=conda.exe"
    goto :found_conda
)

echo [ERROR] conda not found. Install Miniconda first.
exit /b 1

:found_conda
echo [OK] conda: %CONDA_EXE%

"%CONDA_EXE%" env list | findstr /C:"%ENV_NAME% " >nul
if %ERRORLEVEL%==0 (
    echo [OK] env %ENV_NAME% already exists
) else (
    echo [INFO] creating env %ENV_NAME% (python %PYTHON_VERSION%)
    call "%CONDA_EXE%" create -y -n %ENV_NAME% python=%PYTHON_VERSION%
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] conda create failed
        exit /b 1
    )
)

echo [INFO] installing requirements.txt
call "%CONDA_EXE%" run -n %ENV_NAME% python -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] pip install failed
    exit /b 1
)

echo [INFO] smoke test: broken_env.py
call "%CONDA_EXE%" run -n %ENV_NAME% python broken_env.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] smoke test failed
    exit /b 1
)

echo [OK]
exit /b 0
