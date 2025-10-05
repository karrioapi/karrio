# Karrio Development Environment Setup Guide for Windows

This guide documents the steps required to set up the Karrio development environment on Windows with Git Bash (MINGW64).

## Prerequisites

- Windows 10/11
- Git Bash (MINGW64) installed
- Python 3.12.x installed
- Visual Studio 2022 Build Tools with C++ workload
- MSYS2 (for GTK runtime libraries)

---

## Initial Issues Encountered and Solutions

### Issue 1: Python3 Command Not Found
**Problem:** Windows doesn't create a `python3` executable by default, only `python.exe`.

**Solution:** Created a wrapper script for `python3`:
```bash
mkdir -p ~/bin
echo '#!/bin/bash' > ~/bin/python3
echo 'exec /c/Python312/python.exe "$@"' >> ~/bin/python3
chmod +x ~/bin/python3
export PATH="$HOME/bin:$PATH"
```

### Issue 2: Windows Store Python Alias Conflict
**Problem:** Windows App Execution Aliases for Python redirect to Microsoft Store.

**Solution:**
1. Open Windows Settings
2. Go to **Apps → Advanced app settings → App execution aliases**
3. Turn OFF both:
   - `App Installer python.exe`
   - `App Installer python3.exe`

### Issue 3: Virtual Environment Path Differences
**Problem:** Windows uses `Scripts/activate` while Unix uses `bin/activate`.

**Solution:** Modified `bin/create-new-env` to handle both paths:
```bash
# Handle both Unix (bin) and Windows (Scripts) paths
if [[ -f "${ROOT:?}/$ENV_DIR/$BASE_DIR/Scripts/activate" ]]; then
    source "${ROOT:?}/$ENV_DIR/$BASE_DIR/Scripts/activate"
else
    source "${ROOT:?}/$ENV_DIR/$BASE_DIR/bin/activate"
fi
```

### Issue 4: Pip Self-Upgrade Fails on Windows
**Problem:** Running `pip install pip --upgrade` fails on Windows.

**Solution:** Modified `bin/create-new-env` to use:
```bash
run_command "python -m pip install pip --upgrade" "Failed to upgrade pip" "Upgrading pip..." || exit $?
```

### Issue 5: Pyzint Compilation Requires C++ Compiler
**Problem:** `pyzint==0.1.10` requires compilation with Microsoft Visual C++ 14.0 or greater.

**Solution:**
1. Install Visual Studio 2022 Build Tools
2. Install **Desktop development with C++** workload (includes Windows 10 SDK)
3. Create batch scripts that load VS environment before running Python setup

### Issue 6: WeasyPrint Requires GTK Libraries
**Problem:** WeasyPrint (used for PDF generation) cannot load `libgobject-2.0-0` and other GTK libraries on Windows.

**Error:**
```
OSError: cannot load library 'libgobject-2.0-0': error 0x7e
```

**Solution:** Install GTK3 runtime via MSYS2:

1. Install MSYS2 from https://www.msys2.org/
2. Open **MSYS2 MINGW64** terminal
3. Install GTK packages:
   ```bash
   pacman -S --noconfirm \
     mingw-w64-x86_64-gtk3 \
     mingw-w64-x86_64-pango \
     mingw-w64-x86_64-gdk-pixbuf2 \
     mingw-w64-x86_64-librsvg \
     mingw-w64-x86_64-cairo
   ```
4. Add `C:\msys64\mingw64\bin` to Windows PATH environment variable
5. Add to `~/.bashrc` for persistence:
   ```bash
   echo 'export PATH="/c/msys64/mingw64/bin:$PATH"' >> ~/.bashrc
   ```
6. Restart terminal and verify:
   ```bash
   python -c "import weasyprint; print('Success!')"
   ```

**Alternative:** Use Docker for development (GTK pre-installed in containers)

---

## Setup Steps

### Step 1: Install Visual Studio 2022 Build Tools

1. Download Visual Studio Installer from: https://visualstudio.microsoft.com/downloads/
2. Install **Visual Studio 2022 Build Tools**
3. During installation, select the **Desktop development with C++** workload
   - This includes:
     - MSVC v143 C++ compiler
     - Windows 10 SDK
     - CMake tools for Windows
4. **Restart your computer** after installation

### Step 2: Verify C++ Compiler Installation

Open a Command Prompt and run:
```cmd
cd C:\Users\princ\Ashish\karrio
bin\check-vs-install.bat
```

**Expected output:**
```
SUCCESS: C++ compiler found!
Microsoft (R) C/C++ Optimizing Compiler Version 19.XX...
```

### Step 3: Verify Windows SDK Installation

```cmd
bin\check-windows-sdk.bat
```

**Expected output:**
```
Windows SDK 10 found!
Available SDK versions:
10.0.xxxxx.x
```

### Step 4: Set Up Python3 Wrapper (Git Bash)

In Git Bash:
```bash
mkdir -p ~/bin
echo '#!/bin/bash' > ~/bin/python3
echo 'exec /c/Python312/python.exe "$@"' >> ~/bin/python3
chmod +x ~/bin/python3
export PATH="$HOME/bin:$PATH"
```

**Add to your `~/.bashrc` for persistence:**
```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
```

### Step 5: Install Pyzint

From Command Prompt:
```cmd
cd C:\Users\princ\Ashish\karrio
bin\install-pyzint-fixed.bat
```

This script:
- Loads Visual Studio 2022 environment
- Sets `DISTUTILS_USE_SDK=1` and `MSSdk=1`
- Installs pyzint with `--no-build-isolation` flag

**Expected output:**
```
SUCCESS: pyzint installed successfully!
```

### Step 6: Run Full Server Environment Setup

From Command Prompt:
```cmd
bin\setup-with-vs.bat
```

This script:
- Loads Visual Studio 2022 environment
- Runs `bin/setup-server-env` in Git Bash
- Installs all Python dependencies
- Creates virtual environment at `.venv/karrio`
- Logs output to `setup-output.log`

**Note:** This takes several minutes. Watch the output or check `setup-output.log`.

### Step 7: Install GTK for WeasyPrint

**Follow the instructions in:** `bin/setup-gtk-msys2.md`

Quick summary:
1. Install MSYS2 from https://www.msys2.org/
2. Open **MSYS2 MINGW64** terminal and run:
   ```bash
   pacman -S --noconfirm mingw-w64-x86_64-gtk3 mingw-w64-x86_64-pango mingw-w64-x86_64-gdk-pixbuf2 mingw-w64-x86_64-librsvg mingw-w64-x86_64-cairo
   ```
3. Add `C:\msys64\mingw64\bin` to Windows PATH
4. Add to `~/.bashrc`:
   ```bash
   echo 'export PATH="/c/msys64/mingw64/bin:$PATH"' >> ~/.bashrc
   ```

### Step 8: Activate Python Environment

In Git Bash:
```bash
export PATH="$HOME/bin:$PATH"
export PATH="/c/msys64/mingw64/bin:$PATH"  # For GTK libraries
source .venv/karrio/Scripts/activate
```

---

## Files Modified/Created

### Modified Files
- `bin/create-new-env` - Added Windows `Scripts/activate` path handling and fixed pip upgrade command

### Created Helper Scripts
- `bin/check-vs-install.bat` - Verifies C++ compiler installation
- `bin/check-windows-sdk.bat` - Verifies Windows SDK installation
- `bin/install-pyzint-fixed.bat` - Installs pyzint with proper VS environment
- `bin/setup-with-vs.bat` - Runs full setup with VS 2022 environment
- `bin/setup-gtk-msys2.md` - Instructions for installing GTK via MSYS2
- `~/bin/python3` - Wrapper script to make `python3` command available

---

## Troubleshooting

### Terminal Crashes During Setup
**Symptom:** Command Prompt closes unexpectedly during `pyzint` compilation.

**Solution:**
- Ensure you've restarted your computer after installing VS Build Tools
- Run from a fresh Command Prompt (not from within VS Code terminal)
- Check `setup-output.log` for error details

### "Microsoft Visual C++ 14.0 or greater is required"
**Symptom:** Error during pyzint installation.

**Causes:**
1. C++ workload not installed in Visual Studio
2. Windows SDK not installed
3. VS environment not loaded before running pip

**Solution:** Follow Steps 1-3 above, then restart and retry.

### "Cannot open include file: 'stdio.h'"
**Symptom:** Compiler can't find standard C headers.

**Cause:** Windows 10 SDK is missing.

**Solution:**
1. Open Visual Studio Installer
2. Modify VS 2022 Build Tools
3. Go to **Individual components** tab
4. Check **Windows 10 SDK (latest version)**
5. Install and restart computer

### "Cannot load library 'libgobject-2.0-0'"
**Symptom:** WeasyPrint fails to import with GTK library error when running `karrio migrate`.

**Cause:** GTK runtime libraries not installed on Windows.

**Solution:** Follow Step 7 to install GTK via MSYS2, or use Docker for development.

### Dashboard "Invalid URL" Error
**Symptom:** Dashboard logs show `TypeError: Invalid URL` with `input: 'undefined'` when trying to load metadata.

**Error:**
```
loadMetadata TypeError: Invalid URL
{
  code: 'ERR_INVALID_URL',
  input: 'undefined'
}
```

**Cause:** The dashboard's `.env` file is missing. The `apps/dashboard/.env.sample` file is not automatically copied to `.env` during setup.

**Solution:**
1. Copy the sample file:
   ```bash
   cp apps/dashboard/.env.sample apps/dashboard/.env
   ```
2. Verify the file contains the correct API URL (default is already configured):
   ```
   KARRIO_URL=http://localhost:5002
   NEXT_PUBLIC_KARRIO_PUBLIC_URL=http://localhost:5002
   ```
3. Restart the dashboard server

---

## Next Steps After Setup

Once setup completes successfully:

1. **Verify WeasyPrint installation:**
   ```bash
   python -c "import weasyprint; print('WeasyPrint OK')"
   ```

2. **Run database migrations:**
   ```bash
   karrio migrate
   ```

3. **Create superuser:**
   ```bash
   karrio createsuperuser
   ```

4. **Collect static files:**
   ```bash
   karrio collectstatic --noinput
   ```

5. **Create dashboard .env file (if not already created):**
   ```bash
   cp apps/dashboard/.env.sample apps/dashboard/.env
   ```
   **Note:** The setup script should create this automatically, but sometimes it doesn't. This file is required for the dashboard to connect to the API.

6. **Start development servers:**
   ```bash
   ./bin/dev up
   ```

---

## Summary of Key Learnings

1. **Windows-specific challenges:**
   - Different executable names (`python` vs `python3`)
   - Different virtual environment paths (`Scripts` vs `bin`)
   - Pip self-upgrade requires `python -m pip`
   - C/C++ compilation requires proper Visual Studio environment

2. **Compilation requirements for pyzint:**
   - Visual Studio Build Tools with C++ workload
   - Windows 10 SDK for C standard library headers
   - Environment variables must be set: `DISTUTILS_USE_SDK=1`, `MSSdk=1`
   - Use `--no-build-isolation` to preserve VS environment

3. **Environment inheritance issues:**
   - Batch scripts can load VS environment
   - Git Bash must be launched from the batch environment
   - Python subprocesses inherit environment when `--no-build-isolation` is used

4. **WeasyPrint/GTK dependencies:**
   - WeasyPrint requires GTK runtime (Pango, Cairo, GObject)
   - Not available on Windows by default
   - MSYS2 provides compatible GTK binaries for Windows
   - Must add MSYS2 bin directory to PATH for DLL discovery

---

## Quick Reference Commands

### Verify Setup
```cmd
bin\check-vs-install.bat
bin\check-windows-sdk.bat
```

### Install Dependencies
```cmd
bin\install-pyzint-fixed.bat
bin\setup-with-vs.bat
```

### Activate Environment (Git Bash)
```bash
export PATH="$HOME/bin:$PATH"
export PATH="/c/msys64/mingw64/bin:$PATH"
source .venv/karrio/Scripts/activate
```

### Run Migrations
```bash
karrio migrate
```

### Start Development
```bash
./bin/dev up
```

---

**Setup Date:** October 5, 2025
**Python Version:** 3.12.4
**Visual Studio:** 2022 Build Tools
**Platform:** Windows 10/11 with Git Bash (MINGW64)
