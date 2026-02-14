@echo off
chcp 65001 >nul
setlocal

title GitHub 镜像源监控

where python >nul 2>nul
if %errorlevel%==0 (
    python "%~dp0monitor.py"
) else (
    echo Python not found. Please install Python first.
    pause
)