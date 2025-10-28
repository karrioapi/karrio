@echo off
echo Installing pyzint with Visual Studio 2022 compiler...
echo.

REM Load VS 2022 environment
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

if errorlevel 1 (
    echo ERROR: Failed to load Visual Studio 2022 environment
    echo Make sure the C++ workload is installed for VS 2022
    pause
    exit /b 1
)

REM Set distutils to use MSVC
set DISTUTILS_USE_SDK=1
set MSSdk=1

REM Change to project directory
cd /d "%~dp0\.."

REM Activate Python virtual environment
echo Activating Python environment...
call .venv\karrio\Scripts\activate.bat

echo.
echo Environment variables set:
echo DISTUTILS_USE_SDK=%DISTUTILS_USE_SDK%
echo MSSdk=%MSSdk%

echo.
echo Installing pyzint with --no-build-isolation...
python -m pip install --no-build-isolation pyzint==0.1.10 -v

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install pyzint
    pause
    exit /b 1
)

echo.
echo SUCCESS: pyzint installed successfully!
pause
