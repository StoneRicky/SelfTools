@echo off
setlocal enabledelayedexpansion

:: ================================================:: 自动请求管理员权限
:: ================================================:: 检查是否已管理员身份运行
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 正在请求管理员权限 ...
    powershell -Command "Start-Process '%~s0' -Verb RunAs"
    exit /b
)

:: ================================================:: 数据库备份脚本
:: 功能： 自动备份MySQL数据库，保留7天历史备份
:: 特点：WinRAR压缩、并行执行、错误日志、权限控制:: 配置日期：2025-07-22
:: ================================================

:: ------------------------------
:: 配置区域（根据实际环境修改）:: 初始化变量
:: ------------------------------
set "MYSQL_BIN=D:\Server\SERVER1\mysql\mysql-5.7.27-winx64\bin\mysqldump"
set "DATABASE_USER=root"
set "DATABASE_PASSWORD=123456"
set "DATABASE_PORT=3366"
set "BACKUP_ROOT=%~dp0"
set "DATABASES=mysql"

:: 使用更可靠的日期获取方式
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "Ymd=%dt:~0,8%"

:: 日志目录
set "LOG_DIR=%BACKUP_ROOT%logs"
:: 备份日志文件（统一使用反斜杠）
set "LOGFILE=%BACKUP_ROOT%logs\backup_%Ymd%.log"
set ERROR_FLAG=0

:: 创建日志目录
if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
)

:: 写入日志文件头
if not exist "%LOGFILE%" (
    echo ================================================================================= >> "%LOGFILE%"
    echo ===================================== >> "%LOGFILE%"
)

echo [%date% %time%] === 备份开始 === >> "%LOGFILE%"

:: ------------------------------
:: 目录检查与创建
:: ------------------------------
for /l %%i in (1,1,7) do (
    if not exist "%BACKUP_ROOT%D%%i" (
        mkdir "%BACKUP_ROOT%D%%i"
        echo [%date% %time%] 提示：创建目录: D%%i >> "%LOGFILE%"
    )
)

:: ------------------------------
:: 清理旧备份（保留7天）
:: ------------------------------
if exist "%BACKUP_ROOT%\D1\*.sql" (
    del /Q "%BACKUP_ROOT%\D1\*.sql" >> "%LOGFILE%" 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo [%date% %time%] 错误: 删除D1旧备份失败 >> "%LOGFILE%"
        set ERROR_FLAG=1
    )
) else (
    echo [%date% %time%] 警告: D1无SQL文件可删除 >> "%LOGFILE%"
)

:: ------------------------------
:: 目录轮转
:: ------------------------------
for /l %%i in (2,1,7) do (
    set /a j=%%i-1
    if exist "%BACKUP_ROOT%D%%i\*.sql" (
        move /Y "%BACKUP_ROOT%D%%i\*.sql" "%BACKUP_ROOT%D!j!\" >> "%LOGFILE%" 2>&1
        if !ERRORLEVEL! NEQ 0 (
            echo [%date% %time%] 错误: 移动D%%i到D!j!失败（错误码: !ERRORLEVEL!） >> "%LOGFILE%"
            set ERROR_FLAG=1
        )
    ) else (
        echo [%date% %time%] 警告: D%%i无SQL文件可移动 >> "%LOGFILE%"
    )
)

:: ------------------------------
:: 顺序备份数据库
:: ------------------------------
for %%d in (%DATABASES%) do (
    echo [%date% %time%] 开始备份数据库: %%d >> "%LOGFILE%"
    :: 执行备份 - 使用--password参数兼容MySQL 5.7，添加推荐参数
    "%MYSQL_BIN%" -u%DATABASE_USER% --password=%DATABASE_PASSWORD% --port=%DATABASE_PORT% --single-transaction --skip-ssl --routines --triggers --events %%d > "%BACKUP_ROOT%D7\%%d_%Ymd%.sql"
    :: 错误检查
    if !ERRORLEVEL! NEQ 0 (
        echo [%date% %time%] 严重错误: 数据库 %%d 备份失败 >> "%LOGFILE%"
        set ERROR_FLAG=1
    ) else (
        echo [%date% %time%] 数据库成功备份: %%d >> "%LOGFILE%"
    )
)

:: ------------------------------
:: 最终状态检查
:: ------------------------------
if %ERROR_FLAG% NEQ 0 (
    echo [%date% %time%] === 备份完成（有错误）=== >> "%LOGFILE%"
    exit /b 1
) else (
    echo [%date% %time%] === 备份完成（成功）=== >> "%LOGFILE%"
    exit /b 0
)

endlocal