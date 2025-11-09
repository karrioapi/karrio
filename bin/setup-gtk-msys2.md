# Installing GTK for WeasyPrint on Windows

## Quick Install via MSYS2

1. **Install MSYS2** (if not already installed):
   - Download from: https://www.msys2.org/
   - Run the installer (default location: `C:\msys64`)

2. **Open MSYS2 MINGW64 terminal** (not Git Bash)

3. **Install GTK3 and dependencies**:
   ```bash
   pacman -S --noconfirm \
     mingw-w64-x86_64-gtk3 \
     mingw-w64-x86_64-pango \
     mingw-w64-x86_64-gdk-pixbuf2 \
     mingw-w64-x86_64-librsvg \
     mingw-w64-x86_64-cairo
   ```

4. **Add MSYS2 binaries to Windows PATH**:
   - Open System Environment Variables
   - Add `C:\msys64\mingw64\bin` to PATH
   - Restart Command Prompt/Git Bash

5. **Test**:
   ```bash
   export PATH="/c/msys64/mingw64/bin:$PATH"
   source .venv/karrio/Scripts/activate
   python -c "import weasyprint; print('Success!')"
   ```

6. **Make permanent** - Add to `~/.bashrc`:
   ```bash
   echo 'export PATH="/c/msys64/mingw64/bin:$PATH"' >> ~/.bashrc
   ```
