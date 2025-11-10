@echo off
REM Setup script that loads Visual Studio 2022 environment then runs bash setup

echo Loading Visual Studio 2022 Build Tools environment...
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

if errorlevel 1 (
    echo ERROR: Failed to load Visual Studio 2022 environment
    echo Make sure the C++ workload is installed for VS 2022
    pause
    exit /b 1
)

echo.
echo Visual Studio 2022 environment loaded successfully
echo Starting bash setup script...
echo.

REM Change to project directory
cd /d "%~dp0\.."

REM Run the setup in Git Bash with the VS environment variables
"C:\Program Files\Git\usr\bin\bash.exe" --login -i -c "export PATH=\"$HOME/bin:$PATH\" && source ./bin/setup-server-env --verbose" 2>&1 | "C:\Program Files\Git\usr\bin\tee.exe" setup-output.log

echo.
echo Setup complete. Check setup-output.log for details.
pause
