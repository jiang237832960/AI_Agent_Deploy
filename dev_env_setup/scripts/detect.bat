@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Dev Environment Detection

echo.
echo ========================================
echo       Development Environment Report
echo ========================================
echo.
echo Checking development environment...
echo.

echo [Node.js]
where node >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('node --version 2^>nul') do set "NODE_VER=%%a"
    for /f "tokens=* delims=" %%a in ('npm --version 2^>nul') do set "NPM_VER=%%a"
    for /f "tokens=* delims=" %%a in ('where node 2^>nul') do set "NODE_PATH=%%a"
    echo   Status: Installed
    echo   Version: !NODE_VER!
    echo   npm: !NPM_VER!
    echo   Path: !NODE_PATH!
) else (
    echo   Status: Not installed
    echo   Download: https://nodejs.org/
)

echo.
echo [Python]
where python >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('python --version 2^>^&1') do set "PY_VER=%%a"
    for /f "tokens=* delims=" %%a in ('where python 2^>nul') do set "PY_PATH=%%a"
    echo   Status: Installed
    echo   Version: !PY_VER!
    echo   Path: !PY_PATH!
) else (
    echo   Status: Not installed
    echo   Download: https://www.python.org/
)

echo.
echo [Java]
where java >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('java -version 2^>^&1 ^| findstr /i "version"') do set "JAVA_VER=%%a"
    for /f "tokens=* delims=" %%a in ('where java 2^>nul') do set "JAVA_PATH=%%a"
    echo   Status: Installed
    echo   Version: !JAVA_VER!
    echo   Path: !JAVA_PATH!
) else (
    echo   Status: Not installed
    echo   Download: https://www.oracle.com/java/
)

echo.
echo [Go]
where go >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('go version 2^>nul') do set "GO_VER=%%a"
    for /f "tokens=* delims=" %%a in ('where go 2^>nul') do set "GO_PATH=%%a"
    echo   Status: Installed
    echo   Version: !GO_VER!
    echo   Path: !GO_PATH!
) else (
    echo   Status: Not installed
    echo   Download: https://golang.org/dl/
)

echo.
echo [Rust]
where rustc >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('rustc --version 2^>nul') do set "RUST_VER=%%a"
    for /f "tokens=* delims=" %%a in ('where rustc 2^>nul') do set "RUST_PATH=%%a"
    echo   Status: Installed
    echo   Version: !RUST_VER!
    echo   Path: !RUST_PATH!
) else (
    echo   Status: Not installed
    echo   Download: https://www.rust-lang.org/
)

echo.
echo [Docker]
where docker >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('docker --version 2^>nul') do set "DOCKER_VER=%%a"
    for /f "tokens=* delims=" %%a in ('where docker 2^>nul') do set "DOCKER_PATH=%%a"
    echo   Status: Installed
    echo   Version: !DOCKER_VER!
    echo   Path: !DOCKER_PATH!
) else (
    echo   Status: Not installed
    echo   Download: https://www.docker.com/
)

echo.
echo [Git]
where git >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('git --version 2^>nul') do set "GIT_VER=%%a"
    for /f "tokens=* delims=" %%a in ('where git 2^>nul') do set "GIT_PATH=%%a"
    echo   Status: Installed
    echo   Version: !GIT_VER!
    echo   Path: !GIT_PATH!
) else (
    echo   Status: Not installed
    echo   Download: https://git-scm.com/
)

echo.
echo ========================================
echo         Detection Complete!
echo ========================================
echo.

pause