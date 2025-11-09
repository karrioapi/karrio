@echo off
echo Checking for Windows SDK...
echo.

dir /b "C:\Program Files (x86)\Windows Kits\10\Include" 2>nul
if errorlevel 1 (
    echo ERROR: Windows SDK not found at C:\Program Files ^(x86^)\Windows Kits\10\Include
    echo.
    echo You need to install the Windows 10 SDK.
) else (
    echo Windows SDK 10 found!
    echo Available SDK versions:
    dir /b "C:\Program Files (x86)\Windows Kits\10\Include"
)

echo.
echo Checking registry for SDK...
reg query "HKLM\SOFTWARE\Microsoft\Windows Kits\Installed Roots" /v KitsRoot10 2>nul

echo.
pause
