@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Memory Check

echo ========================================
echo         Memory Usage Check
echo ========================================
echo.

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
    set /a USED_GB=!USED_MB! / 1024
    set /a FREE_GB=!FREE_MB! / 1024
    if !TOTAL_MB! gtr 0 (
        set /a USED_PERCENT=!USED_MB! * 100 / !TOTAL_MB!
    )
)

echo ========================================
echo [1] Physical Memory (OS Reported)
echo ========================================
echo   Total:      !TOTAL_MB! MB ^(!TOTAL_GB! GB^)
echo   Used:       !USED_MB! MB ^(!USED_GB! GB^) - !USED_PERCENT!%%
echo   Available:  !FREE_MB! MB ^(!FREE_GB! GB^)
echo.

echo ========================================
echo [2] System Memory (Kernel/Cache)
echo ========================================

for /f "delims=" %%a in ('powershell -Command "$c = Get-Counter '\Memory\Pool Nonpaged Bytes' -ErrorAction SilentlyContinue; if($c){[math]::Round($c.CounterSamples[0].CookedValue/1MB,0)}"') do set NONPAGED_MB=%%a

for /f "delims=" %%a in ('powershell -Command "$c = Get-Counter '\Memory\Pool Paged Bytes' -ErrorAction SilentlyContinue; if($c){[math]::Round($c.CounterSamples[0].CookedValue/1MB,0)}"') do set PAGED_MB=%%a

for /f "delims=" %%a in ('powershell -Command "$c = Get-Counter '\Memory\Cache Bytes' -ErrorAction SilentlyContinue; if($c){[math]::Round($c.CounterSamples[0].CookedValue/1MB,0)}"') do set CACHE_MB=%%a

if defined NONPAGED_MB echo   Non-paged Pool:  !NONPAGED_MB! MB
if defined PAGED_MB echo   Paged Pool:       !PAGED_MB! MB
if defined CACHE_MB echo   System Cache:     !CACHE_MB! MB

set /a KERNEL_MB=0
if defined NONPAGED_MB set /a KERNEL_MB+=!NONPAGED_MB!
if defined PAGED_MB set /a KERNEL_MB+=!PAGED_MB!
if defined CACHE_MB set /a KERNEL_MB+=!CACHE_MB!
echo   Subtotal Kernel:  !KERNEL_MB! MB
echo.

echo ========================================
echo [3] Page File
echo ========================================
for /f "skip=1 tokens=1" %%a in ('wmic pagefile get AllocatedBaseSize') do (
    if not "%%a"=="" set "PAGE_TOTAL=%%a"
)
for /f "skip=1 tokens=1" %%a in ('wmic pagefile get CurrentUsage') do (
    if not "%%a"=="" set "PAGE_USED=%%a"
)

if defined PAGE_TOTAL if defined PAGE_USED (
    set /a PAGE_PERCENT=!PAGE_USED! * 100 / !PAGE_TOTAL!
    echo   Total:  !PAGE_TOTAL! MB
    echo   Used:   !PAGE_USED! MB ^(!PAGE_PERCENT!%%^)
)
echo.

echo ========================================
echo [4] Process Memory Top 15
echo ========================================

for /f "delims=" %%a in ('powershell -Command "$total=0; Get-Process | ForEach-Object { $total += $_.WorkingSet }; [math]::Round($total/1MB,0)"') do set PROC_TOTAL=%%a

powershell -Command "Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 15 | ForEach-Object { Write-Host ('{0,-30} {1,6} MB' -f $_.ProcessName, [math]::Round($_.WorkingSet/1MB,0)) }"

echo   ----------------------------------------
echo   All Processes Total: !PROC_TOTAL! MB
echo.

echo ========================================
echo [5] Memory Balance Check
echo ========================================
echo   OS Used Memory:      !USED_MB! MB
echo   Kernel/Cache:       !KERNEL_MB! MB
echo   All Processes:      !PROC_TOTAL! MB
set /a CHECK_SUM=!KERNEL_MB! + !PROC_TOTAL!
echo   Sum (Kernal+Proc):  !CHECK_SUM! MB
set /a DIFFERENCE=!USED_MB! - !CHECK_SUM!
echo   Difference:         !DIFFERENCE! MB
echo.
