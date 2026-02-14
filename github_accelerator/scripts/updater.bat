@echo off
chcp 65001 >nul
setlocal

title GitHub 镜像源更新

where python >nul 2>nul
if %errorlevel%==0 (
    python "%~dp0updater.py" %*
) else (
    echo Python not found. Please install Python first.
    pause
)