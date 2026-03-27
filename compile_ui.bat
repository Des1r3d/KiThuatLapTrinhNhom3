@echo off
chcp 65001 > nul
echo ============================================
echo   Compile UI: .ui -^> .py (pyuic6)
echo ============================================
echo.

set UI_DIR=%~dp0Ui Qt

set ERRORS=0
set COUNT=0

for %%f in ("%UI_DIR%\*.ui") do (
    set /a COUNT+=1
    set "INPUT=%%f"
    set "OUTPUT=%%~dpnf.py"
    echo [%%~nf] Compiling...
    pyuic6 -x "%%f" -o "%%~dpnf.py"
    if errorlevel 1 (
        echo   [FAILED] %%~nf.ui
        set /a ERRORS+=1
    ) else (
        echo   [OK]     %%~nxf -^> %%~nf.py
    )
)

echo.
echo ============================================
if %ERRORS%==0 (
    echo   Done! %COUNT% file(s) compiled successfully.
) else (
    echo   Done with errors: %ERRORS% failed / %COUNT% total.
)
echo ============================================
pause
