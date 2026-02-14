@echo off
setlocal

title AI Assistant Tools

echo.
echo ========================================
echo       AI Assistant Tools
echo ========================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.7+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

if "%~1"=="" (
    python "%~dp0main.py"
) else (
    python "%~dp0main.py" %*
)