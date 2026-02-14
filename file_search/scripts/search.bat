@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title 文件搜索（Everything）

echo.
echo ========================================
echo       文件搜索（Everything）
echo ========================================
echo.

set "ES_PATH=%~dp0..\..\tools\Everything\es.exe"

if not exist "!ES_PATH!" (
    set "ES_PATH=%~dp0..\tools\Everything\es.exe"
)

if not exist "!ES_PATH!" (
    set "ES_PATH=C:\Program Files\Everything\es.exe"
)

if not exist "!ES_PATH!" (
    call :download_everything
)

if not exist "!ES_PATH!" (
    echo 错误：无法获取 Everything
    pause
    exit /b
)

echo Everything 路径：!ES_PATH!
echo.

echo 请选择搜索方式：
echo.
echo   1. 按文件名搜索
echo   2. 按扩展名搜索
echo   3. 按大小搜索
echo.

set /p CHOICE="请输入选项 (1-3): "

if "!CHOICE!"=="1" goto search_filename
if "!CHOICE!"=="2" goto search_extension
if "!CHOICE!"=="3" goto search_size

echo 无效选项！
pause
exit /b

:search_filename
echo.
set /p KEYWORD="请输入搜索关键词： "

if "!KEYWORD!"=="" (
    echo 关键词不能为空！
    pause
    exit /b
)

echo.
echo 正在搜索：!KEYWORD! ...
echo.

"!ES_PATH!" "!KEYWORD!" -n 100 >tmp_search.txt

goto show_results

:search_extension
echo.
set /p EXT="请输入扩展名（如：py, js, txt）： "

if "!EXT!"=="" (
    echo 扩展名不能为空！
    pause
    exit /b
)

echo.
echo 正在搜索 *.!EXT! 文件...
echo.

"!ES_PATH!" "* .!EXT!" -n 100 >tmp_search.txt

goto show_results

:search_size
echo.
echo 大小条件示例：
echo   gt10MB   - 大于 10MB
echo   lt100KB  - 小于 100KB
echo   1MB-10MB - 1MB 到 10MB 之间
echo.

set /p SIZE_COND="请输入大小条件： "

if "!SIZE_COND!"=="" (
    echo 大小条件不能为空！
    pause
    exit /b
)

echo.
echo 正在搜索符合条件的文件...
echo.

"!ES_PATH!" "size:!SIZE_COND!" -n 100 >tmp_search.txt

goto show_results

:show_results
echo ========================================
echo         搜索结果
echo ========================================
echo.

findstr /v "^$" tmp_search.txt >tmp_results.txt
set /a COUNT=0

for /f "tokens=* delims=" %%a in (tmp_results.txt) do (
    set /a COUNT+=1
    echo !COUNT!. %%a
)

del tmp_search.txt >nul 2>nul
del tmp_results.txt >nul 2>nul

echo.
echo ========================================
echo       搜索完成！共 !COUNT! 个结果
echo ========================================
echo.

pause
exit /b

:download_everything
echo   [!] 未找到 Everything，正在下载...
echo.

set "ES_DIR=%~dp0..\..\tools\Everything"
if not exist "!ES_DIR!" mkdir "!ES_DIR!"

set "ES_ZIP=%TEMP%\Everything.zip"

echo 正在下载 Everything 便携版...
echo.

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.voidtools.com/Everything-1.4a.zip' -OutFile '%ES_ZIP%'}"

if not exist "!ES_ZIP!" (
    echo [!] 下载失败，正在尝试备用方案...
    powershell -Command "Start-Process 'https://www.voidtools.com/zh-cn/downloads/'"
    exit /b
)

echo 下载完成，正在解压...
echo.

powershell -Command "Expand-Archive -Path '!ES_ZIP!' -DestinationPath '!ES_DIR!' -Force"

del /f /q "!ES_ZIP!" 2>nul

set "ES_PATH=!ES_DIR!\Everything.exe"

if exist "!ES_PATH!" (
    echo   [√] Everything 下载完成
    echo   路径：!ES_PATH!
    echo.
    echo 提示：首次运行会建立索引，请稍候...
) else (
    echo [!] 解压失败，请手动下载
)

echo.
exit /b
