@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title 系统环境检测

echo.
echo ========================================
echo         系统环境检测报告
echo ========================================
echo.

echo 【操作系统】
for /f "tokens=4-5 delims=. " %%a in ('ver') do set VERSION=%%a.%%b
echo   系统名称：Windows !VERSION!
echo   版本：!VERSION!

if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo   系统位性：64位
) else (
    echo   系统位性：32位
)

echo.
echo 【CPU 处理器】
for /f "skip=1 delims=" %%a in ('wmic cpu get Name') do (
    set "CPU_NAME=%%a"
    goto :cpu_name_done
)
:cpu_name_done
for /f "skip=1 delims=" %%a in ('wmic cpu get NumberOfCores') do (
    set "CPU_CORES=%%a"
    goto :cpu_cores_done
)
:cpu_cores_done
for /f "skip=1 delims=" %%a in ('wmic cpu get NumberOfLogicalProcessors') do (
    set "CPU_THREADS=%%a"
    goto :cpu_threads_done
)
:cpu_threads_done
for /f "skip=1 delims=" %%a in ('wmic cpu get MaxClockSpeed') do (
    set "CPU_SPEED=%%a"
    goto :cpu_speed_done
)
:cpu_speed_done
echo   型号：!CPU_NAME!
echo   核心数：!CPU_CORES!
echo   线程数：!CPU_THREADS!
echo   最大频率：!CPU_SPEED! MHz

echo.
echo 【内存】
for /f "skip=1 delims=" %%a in ('wmic OS get TotalVisibleMemorySize') do (
    set "TOTAL_MEM=%%a"
    goto :mem_total_done
)
:mem_total_done
for /f "skip=1 delims=" %%a in ('wmic OS get FreePhysicalMemory') do (
    set "FREE_MEM=%%a"
    goto :mem_free_done
)
:mem_free_done
if defined TOTAL_MEM if defined FREE_MEM (
    set /a TOTAL_MB=!TOTAL_MEM! / 1024
    set /a FREE_MB=!FREE_MEM! / 1024
    set /a USED_MB=!TOTAL_MB! - !FREE_MB!
    set /a TOTAL_GB=!TOTAL_MB! / 1024
    set /a FREE_GB=!FREE_MB! / 1024
    set /a USED_GB=!USED_MB! / 1024
    if !TOTAL_MB! gtr 0 (
        set /a USED_PERCENT=!USED_MB! * 100 / !TOTAL_MB!
        echo   总量：!TOTAL_MB! MB ^(!TOTAL_GB! GB^)
        echo   可用：!FREE_MB! MB ^(!FREE_GB! GB^)
        echo   已使用：!USED_MB! MB ^(!USED_GB! GB^)
        echo   使用率：!USED_PERCENT!%%
    )
) else (
    echo   内存信息获取失败
)

echo.
echo 【硬盘】
set DISK_NUM=0
for /f "skip=1 tokens=1-3" %%a in ('wmic logicaldisk where "DriveType=3" get DeviceID^,FreeSpace^,Size') do (
    set "DID=%%a"
    set "DFREE=%%b"
    set "DSIZE=%%c"
    if defined DID if defined DSIZE (
        set /a DISK_NUM+=1
        set "DISK_DEV!DISK_NUM!=!DID!"
        set "DISK_FREE!DISK_NUM!=!DFREE!"
        set "DISK_SIZE!DISK_NUM!=!DSIZE!"
    )
)
set VOL_NUM=0
for /f "skip=1 delims=" %%a in ('wmic logicaldisk where "DriveType=3" get VolumeName') do (
    set "TMP=%%a"
    call :trim TMP
    if defined TMP (
        set /a VOL_NUM+=1
        set "DISK_VOL!VOL_NUM!=!TMP!"
    )
)
for /L %%i in (1,1,!DISK_NUM!) do (
    set "DEV=!DISK_DEV%%i!"
    set "VOL=!DISK_VOL%%i!"
    set "DSIZE=!DISK_SIZE%%i!"
    set "DFREE=!DISK_FREE%%i!"
    call :calc_gb "!DSIZE!" SIZE_GB
    call :calc_gb "!DFREE!" FREE_GB
    set /a USED_GB=SIZE_GB - FREE_GB
    echo   !DEV! ^(!VOL!^)：约 !SIZE_GB! GB
    echo     已用：约 !USED_GB! GB / 可用：约 !FREE_GB! GB
)

echo.
echo 【显卡】
set GPU_COUNT=0
set IDX=0
for /f "skip=1 delims=" %%a in ('wmic path win32_VideoController get Name') do (
    set "TMP=%%a"
    call :trim TMP
    if defined TMP if not "!TMP!"=="" (
        set /a IDX+=1
        set "GPU_NAME!IDX!=!TMP!"
    )
)
set IDX2=0
for /f "skip=1 delims=" %%a in ('wmic path win32_VideoController get AdapterRAM') do (
    set "TMP=%%a"
    call :trim TMP
    if defined TMP if not "!TMP!"=="" (
        set /a IDX2+=1
        set "GPU_MEM!IDX2!=!TMP!"
    )
)
for /L %%i in (1,1,!IDX!) do (
    set "GNAME=!GPU_NAME%%i!"
    set "GMEM=!GPU_MEM%%i!"
    set /a GPU_COUNT+=1
    echo   显卡 !GPU_COUNT!：!GNAME!
    if defined GMEM (
        set "GMEM_STR=!GMEM!"
        set "GMEM_GB=!GMEM_STR:~0,1!"
        if "!GMEM_GB!"=="1" set GMEM_GB=1
        if "!GMEM_GB!"=="2" set GMEM_GB=2
        if "!GMEM_GB!"=="3" set GMEM_GB=3
        if "!GMEM_GB!"=="4" set GMEM_GB=4
        if "!GMEM_GB!"=="5" set GMEM_GB=5
        if "!GMEM_GB!"=="6" set GMEM_GB=6
        if "!GMEM_GB!"=="7" set GMEM_GB=7
        if "!GMEM_GB!"=="8" set GMEM_GB=8
        if "!GMEM_GB!"=="9" set GMEM_GB=9
        if "!GMEM_GB!"=="0" set GMEM_GB=0
        echo     显存大小：!GMEM_GB! GB
    )
)
if !GPU_COUNT!==0 echo   未检测到显卡信息

echo.
echo ========================================
echo         检测完成！
echo ========================================
echo.

pause
goto :eof

:calc_gb
setlocal enabledelayedexpansion
set "VAL=%~1"
set "LEN=0"
set "TMP=!VAL!"
:calc_len
if defined TMP (
    set "TMP=!TMP:~1!"
    set /a LEN+=1
    goto :calc_len
)
if !LEN! geq 12 (
    set /a GB=!VAL:~0,3!
) else if !LEN! geq 11 (
    set /a GB=!VAL:~0,3!
    set /a GB=GB*10/100
) else if !LEN! geq 10 (
    set /a GB=!VAL:~0,2!
) else (
    set GB=0
)
endlocal & set "%~2=%GB%"
goto :eof

:trim
setlocal enabledelayedexpansion
set "str=!%1!"
for /f "tokens=* delims= " %%a in ("!str!") do set "str=%%a"
for /l %%a in (1,1,100) do if "!str:~-1!"==" " set "str=!str:~0,-1!"
endlocal & set "%1=%str%"
goto :eof