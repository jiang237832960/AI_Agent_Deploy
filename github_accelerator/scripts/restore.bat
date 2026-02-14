@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title GitHub 加速配置还原

echo.
echo ========================================
echo    GitHub 加速配置还原
echo ========================================
echo.

set "BACKUP_DIR=%~dp0..\backup"

if not exist "!BACKUP_DIR!" (
    echo 未找到备份目录！
    echo.
    pause
    exit /b
)

echo 查找可用的备份文件...
echo.

dir /b "!BACKUP_DIR!\hosts.*.backup" 2>nul | findstr /v "没有" >tmp_files.txt
set /p HOSTS_BACKUP=<tmp_files.txt
del tmp_files.txt >nul 2>nul

dir /b "!BACKUP_DIR!\gitconfig.*.backup" 2>nul | findstr /v "没有" >tmp_files.txt
set /p GIT_BACKUP=<tmp_files.txt
del tmp_files.txt >nul 2>nul

echo 可用备份：
echo.

if not "!HOSTS_BACKUP!"=="" (
    echo   hosts: !HOSTS_BACKUP!
) else (
    echo   hosts: 无备份
)

if not "!GIT_BACKUP!"=="" (
    echo   gitconfig: !GIT_BACKUP!
) else (
    echo   gitconfig: 无备份
)

echo.
echo ========================================
echo 请选择还原内容：
echo ========================================
echo.
echo   1. 还原 hosts 文件
echo   2. 还原 Git 配置
echo   3. 全部还原
echo   4. 退出
echo.

set /p CHOICE="请输入选项 (1-4): "

if "!CHOICE!"=="1" goto restore_hosts
if "!CHOICE!"=="2" goto restore_git
if "!CHOICE!"=="3" goto restore_all
if "!CHOICE!"=="4" exit /b

:restore_hosts
if "!HOSTS_BACKUP!"=="" (
    echo   没有 hosts 备份，无法还原
    pause
    exit /b
)

echo.
echo 正在还原 hosts 文件...

copy "!BACKUP_DIR!\!HOSTS_BACKUP!" "C:\Windows\System32\drivers\etc\hosts" >nul 2>nul

if !errorlevel!==0 (
    echo   hosts 文件已还原
) else (
    echo   还原失败，可能需要管理员权限
)

goto done

:restore_git
if "!GIT_BACKUP!"=="" (
    echo   没有 Git 配置备份，无法还原
    pause
    exit /b
)

echo.
echo 正在还原 Git 配置...

for /f "tokens=2 delims==" %%a in ('type "!BACKUP_DIR!\!GIT_BACKUP!" ^| findstr /i "http.proxy https.proxy"') do (
    git config --global --unset %%a
)

echo   Git 配置已还原

goto done

:restore_all
echo.
echo 正在执行全部还原...

goto restore_hosts

:done
echo.
echo ========================================
echo       还原完成！
echo ========================================
echo.

pause
