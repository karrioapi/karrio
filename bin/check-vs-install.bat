@echo off
echo Checking Visual Studio 2022 installation...
echo.

call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

echo Checking for cl.exe (C++ compiler):
where cl.exe
if errorlevel 1 (
    echo.
    echo ERROR: cl.exe not found!
    echo The C++ compiler is not installed.
    echo.
    echo You need to install the "Desktop development with C++" workload.
    echo.
    echo Run this command to install it:
    echo vs_buildtools.exe --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended
    echo.
    echo Or download Visual Studio Installer from:
    echo https://visualstudio.microsoft.com/downloads/
    echo Then modify VS 2019 BuildTools and add "Desktop development with C++"
) else (
    echo.
    echo SUCCESS: C++ compiler found!
    cl.exe 2>&1 | findstr /C:"Version"
)

echo.
pause
