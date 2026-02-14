@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title 项目一键部署

echo.
echo ========================================
echo         项目一键部署
echo ========================================
echo.

echo ========================================
echo     第一步：检测已安装的开发环境
echo ========================================
echo.

set "DETECTED_ENV="

echo 检测 Node.js...
where node >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('node --version') do (
        echo   [√] Node.js: %%a
        set "DETECTED_ENV=!DETECTED_ENV! node"
    )
) else (
    echo   [ ] Node.js: 未安装
)

echo 检测 Python...
where python >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('python --version 2^>^&1') do (
        echo   [√] Python: %%a
        set "DETECTED_ENV=!DETECTED_ENV! python"
    )
) else (
    echo   [ ] Python: 未安装
)

echo 检测 Java...
where java >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('java -version 2^>^&1 ^| findstr "version"') do (
        echo   [√] Java: %%a
        set "DETECTED_ENV=!DETECTED_ENV! java"
    )
) else (
    echo   [ ] Java: 未安装
)

echo 检测 Go...
where go >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('go version') do (
        echo   [√] Go: %%a
        set "DETECTED_ENV=!DETECTED_ENV! go"
    )
) else (
    echo   [ ] Go: 未安装
)

echo 检测 Git...
where git >nul 2>nul
if !errorlevel!==0 (
    for /f "tokens=* delims=" %%a in ('git --version') do (
        echo   [√] Git: %%a
        set "DETECTED_ENV=!DETECTED_ENV! git"
    )
) else (
    echo   [ ] Git: 未安装
)

echo.
echo ========================================
echo     第二步：选择要部署的项目
echo ========================================
echo.

echo 已检测到的环境：!DETECTED_ENV!
echo.
echo 可部署的项目：
echo.

set "COUNT=0"

if "!DETECTED_ENV!" neq "" (
    echo !COUNT!. 查看所有项目
    set /a COUNT+=1
)

if "!DETECTED_ENV!" contains "node" (
    echo !COUNT!. 前端项目 ^(Vue/React/Next.js^) - 需要 Node.js
    set /a COUNT+=1
)

if "!DETECTED_ENV!" contains "python" (
    echo !COUNT!. Python Web ^(FastAPI/Django/Flask^) - 需要 Python
    set /a COUNT+=1
)

if "!DETECTED_ENV!" contains "node" (
    echo !COUNT!. Node.js 后端 ^(Express/NestJS^) - 需要 Node.js
    set /a COUNT+=1
)

if "!DETECTED_ENV!" contains "java" (
    echo !COUNT!. Java 项目 ^(Spring Boot^) - 需要 Java
    set /a COUNT+=1
)

if "!DETECTED_ENV!" contains "go" (
    echo !COUNT!. Go 项目 ^(Gin^) - 需要 Go
    set /a COUNT+=1
)

echo.
set /p CHOICE="请输入选项 (0-!COUNT!): "

if "!CHOICE!"=="0" goto all_projects

if "!DETECTED_ENV!" contains "node" (
    set /a NODE_START=1
    if "!CHOICE!"=="!NODE_START!" goto frontend
)

if "!DETECTED_ENV!" contains "python" (
    set /a PY_START=2
    if defined NODE_START set /a PY_START+=1
    if "!CHOICE!"=="!PY_START!" goto python
)

if "!DETECTED_ENV!" contains "node" (
    set /a NODEJS_START=3
    if defined NODE_START set /a NODEJS_START+=1
    if defined PY_START if "!DETECTED_ENV!" contains "node" set /a NODEJS_START+=1
    if "!CHOICE!"=="!NODEJS_START!" goto nodejs
)

echo 无效选项！
pause
exit /b

:all_projects
echo.
echo ========================================
echo     所有可用项目
echo ========================================
echo.
echo   1. 前端项目 ^(Vue/React/Next.js^)
echo   2. Python Web ^(FastAPI/Django/Flask^)
echo   3. Node.js 后端 ^(Express/NestJS^)
echo   4. Java 项目 ^(Spring Boot^)
echo   5. Go 项目
echo.

set /p FULL_CHOICE="请输入选项 (1-5): "

if "!FULL_CHOICE!"=="1" goto frontend
if "!FULL_CHOICE!"=="2" goto python
if "!FULL_CHOICE!"=="3" goto nodejs
if "!FULL_CHOICE!"=="4" goto java
if "!FULL_CHOICE!"=="5" goto go

echo 无效选项！
pause
exit /b

:frontend
set "PROJECT_NAME=vue3"
set "GIT_URL=https://github.com/vuejs/create-vue.git"
set "INSTALL_CMD=npm install"
set "DEV_CMD=npm run dev"
set "REQUIRE_TOOLS=node"
goto deploy_project

:python
set "PROJECT_NAME=fastapi"
set "GIT_URL=https://github.com/tiangolo/fastapi.git"
set "INSTALL_CMD=pip install -r requirements.txt"
set "DEV_CMD=uvicorn main:app --reload"
set "REQUIRE_TOOLS=python"
goto deploy_project

:nodejs
set "PROJECT_NAME=express"
set "GIT_URL=https://github.com/expressjs/express.git"
set "INSTALL_CMD=npm install"
set "DEV_CMD=node index.js"
set "REQUIRE_TOOLS=node"
goto deploy_project

:java
set "PROJECT_NAME=springboot"
set "GIT_URL=https://github.com/spring-projects/spring-boot.git"
set "INSTALL_CMD=mvn install -DskipTests"
set "DEV_CMD=mvn spring-boot:run"
set "REQUIRE_TOOLS=java"
goto deploy_project

:go
set "PROJECT_NAME=gin"
set "GIT_URL=https://github.com/gin-gonic/gin.git"
set "INSTALL_CMD=go mod download"
set "DEV_CMD=go run main.go"
set "REQUIRE_TOOLS=go"
goto deploy_project

:deploy_project
echo.
echo ========================================
echo 已选择：!PROJECT_NAME!
echo ========================================
echo.

echo 请选择安装目录（建议选择非系统盘）
echo 例如：D:\Projects
echo.

set /p INSTALL_DIR="请输入安装路径: "

if "!INSTALL_DIR!"=="" (
    echo 安装路径不能为空！
    pause
    exit /b
)

echo.
echo 正在克隆项目到 !INSTALL_DIR! ...
echo.

where git >nul 2>nul
if !errorlevel! neq 0 (
    call :install_git_quiet
)

if exist "!INSTALL_DIR!" (
    echo 目录已存在，跳过克隆
) else (
    git clone "!GIT_URL!" "!INSTALL_DIR!" 2>nul
    if !errorlevel! neq 0 (
        echo 克隆失败！请检查网络连接
        pause
        exit /b
    )
)

echo.
echo 正在安装依赖...
echo 执行命令：!INSTALL_CMD!
echo.

cd /d "!INSTALL_DIR!"
!INSTALL_CMD! 2>nul

if !errorlevel! neq 0 (
    echo.
    echo 依赖安装失败，请手动安装
) else (
    echo.
    echo 依赖安装成功！
)

echo.
echo 正在生成启动脚本...

(
echo @echo off
echo chcp 65001 ^>nul
echo title !PROJECT_NAME! 项目
echo cd /d "%%~dp0"
echo.
echo echo ========================================
echo echo      正在启动 !PROJECT_NAME! 项目...
echo echo ========================================
echo.
echo !DEV_CMD!
echo.
echo pause
) > "!INSTALL_DIR!\start.bat"

echo.
echo ========================================
echo         部署完成！
echo ========================================
echo.
echo 项目路径：!INSTALL_DIR!
echo 启动命令：双击 start.bat
echo.

pause
exit /b

:install_git_quiet
echo   [!] Git 未安装，正在安装...
echo.

set "GIT_EXE=%TEMP%\git-installer.exe"
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe' -OutFile '%GIT_EXE%'}" 2>nul

if exist "!GIT_EXE!" (
    !GIT_EXE! /VERYSILENT /NORESTART >nul 2>nul
    echo   [√] Git 安装完成
) else (
    echo   [!] Git 安装失败，请手动安装
)

exit /b
