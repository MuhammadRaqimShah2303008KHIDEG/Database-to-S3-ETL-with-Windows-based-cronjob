@echo off
setlocal

REM --- Set date in YYYY-MM-DD format ---
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set day=%%a
    set month=%%b
    set year=%%c
)

REM Handle regional date formats
if "%day:~2,1%"=="" (
    REM Possible format: DD/MM/YYYY
    for /f "tokens=1-3 delims=/" %%a in ('date /t') do (
        set day=%%a
        set month=%%b
        set year=%%c
    )
)

set LOGDATE=%year%-%month%-%day%

REM --- Define log path ---
set LOGPATH=C:\Collection_Daily_Data\collection_daily_logs\run_log_%LOGDATE%.txt

REM --- Run Python script and log output ---
echo [%date% %time%] Starting script... >> "%LOGPATH%"
"C:\Program Files\Python312\python.exe" "C:\Collection_Daily_Data\main.py" >> "%LOGPATH%" 2>&1
echo [%date% %time%] Script finished. >> "%LOGPATH%"
echo Log saved to: %LOGPATH%

endlocal
