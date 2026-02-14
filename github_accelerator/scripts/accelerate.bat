@echo off
chcp 65001 >nul
setlocal

title GitHub 访问加速配置

where python >nul 2>nul
if %errorlevel%==0 (
    python "%~dp0accelerate.py"
) else (
    echo Python not found. Please install Python first.
    pause
)
