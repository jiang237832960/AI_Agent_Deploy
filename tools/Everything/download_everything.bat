@echo off
chcp 65001 >nul
title 下载 Everything 便携版

echo ========================================
echo      正在下载 Everything 便携版...
echo ========================================

set "DOWNLOAD_URL=https://www.voidtools.com/Everything-1.4a.zip"
set "ZIP_FILE=%~dp0Everything.zip"
set "EXTRACT_DIR=%~dp0"

if exist "%~dp0Everything.exe" (
    echo.
    echo Everything 已存在，跳过下载。
    echo.
    pause
    exit /b
)

echo.
echo 正在下载，请稍候...
echo.

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%ZIP_FILE%'}" 2>nul

if not exist "%ZIP_FILE%" (
    echo.
    echo 自动下载失败，请手动下载：
    echo 1. 访问 https://www.voidtools.com/zh-cn/downloads/
    echo 2. 下载 "Everything" 的 "Portable" 版本
    echo 3. 解压后将 Everything.exe 和 es.exe 放到本目录
    echo.
    pause
    exit /b
)

echo.
echo 下载完成，正在解压...
echo.

powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%EXTRACT_DIR%' -Force"

del /f /q "%ZIP_FILE%" 2>nul

if exist "%~dp0Everything.exe" (
    echo.
    echo ========================================
    echo      下载并解压成功！
    echo ========================================
    echo.
    echo 首次运行前，请先运行 Everything索引
    echo.exe 建立.
) else (
    echo.
    echo 解压失败，请手动解压
    echo.
)

echo.
pause
