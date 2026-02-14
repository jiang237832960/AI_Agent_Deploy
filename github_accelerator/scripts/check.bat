@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title GitHub 访问状态检测

echo.
echo ========================================
echo       GitHub 访问状态检测
echo ========================================
echo.
echo 正在检测 GitHub 访问状态，请稍候...
echo.

echo 【主要域名检测】
echo.

echo 检测 github.com...
curl -s -o nul -w "%%{http_code} %%{time_total}" --connect-timeout 10 https://github.com >tmp.txt 2>nul
set /p RESULT=<tmp.txt
del tmp.txt >nul 2>nul

if "!RESULT!"=="" (
    echo   状态：无法访问
) else (
    echo   状态：可访问
    echo   HTTP码：!RESULT!
)

echo.
echo 检测 raw.githubusercontent.com...
curl -s -o nul -w "%%{http_code} %%{time_total}" --connect-timeout 10 https://raw.githubusercontent.com >tmp.txt 2>nul
set /p RESULT=<tmp.txt
del tmp.txt >nul 2>nul

if "!RESULT!"=="" (
    echo   状态：无法访问
) else (
    echo   状态：可访问
    echo   HTTP码：!RESULT!
)

echo.
echo 【镜像源检测】
echo.

echo 检测 ghproxy.com...
curl -s -o nul -w "%%{http_code} %%{time_total}" --connect-timeout 10 https://ghproxy.com/ >tmp.txt 2>nul
set /p RESULT=<tmp.txt
del tmp.txt >nul 2>nul

if "!RESULT!"=="" (
    echo   状态：无法访问
) else (
    echo   状态：可访问
    echo   HTTP码：!RESULT!
)

echo.
echo 检测 fastgit.org...
curl -s -o nul -w "%%{http_code} %%{time_total}" --connect-timeout 10 https://fastgit.org/ >tmp.txt 2>nul
set /p RESULT=<tmp.txt
del tmp.txt >nul 2>nul

if "!RESULT!"=="" (
    echo   状态：无法访问
) else (
    echo   状态：可访问
    echo   HTTP码：!RESULT!
)

echo.
echo ========================================
echo       检测完成！
echo ========================================
echo.

pause
