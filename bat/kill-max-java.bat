@echo off
setlocal enabledelayedexpansion

set max_mem=9000000
set target_pid=

echo 正在扫描Java进程内存占用...
echo ======================================
for /f "tokens=2,5" %%a in ('tasklist /fi "imagename eq java.exe" /nh 2^>nul') do (
    set pid=%%a
    set mem=%%b
    set mem=!mem: K=!
    set mem=!mem:,=!
    set /a mem_kb=!mem! 
    set /a mem_mb=!mem!/1024
    echo PID:!pid!  内存:!mem_kb!KB[!mem_mb!MB]
    if !mem! gtr !max_mem! (
        set max_mem=!mem!
        set target_pid=!pid!
    )
    @REM echo !max_mem!
)

REM 终止目标进程
if defined target_pid (
    echo 正在终止ֹPID [!target_pid!]（内存使用: !max_mem!KB）
    @REM taskkill /pid !target_pid! /f
) else (
    echo 没有找到Java进程
)

endlocal