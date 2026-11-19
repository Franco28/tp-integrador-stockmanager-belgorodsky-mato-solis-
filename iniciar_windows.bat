@echo off
setlocal
cd /d "%~dp0"

if not exist "scripts\iniciar_local.py" (
    echo No se encontro scripts\iniciar_local.py.
    echo Coloca el iniciador en la raiz de PROYECTO_COMPLETO.
    pause
    exit /b 1
)

set "PYTHON="
where py >nul 2>nul
if not errorlevel 1 (
    py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if not errorlevel 1 set "PYTHON=py -3"
)
if not defined PYTHON (
    where python >nul 2>nul
    if not errorlevel 1 (
        python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
        if not errorlevel 1 set "PYTHON=python"
    )
)
if not defined PYTHON (
    echo No se encontro Python 3.10 o superior. Instalalo desde python.org.
    pause
    exit /b 1
)

%PYTHON% "scripts\iniciar_local.py"
set "CODIGO=%ERRORLEVEL%"
if not "%CODIGO%"=="0" (
    echo.
    echo La ejecucion termino con error %CODIGO%. Revisa el mensaje anterior.
    pause
)
exit /b %CODIGO%
