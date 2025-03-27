:: filepath: C:\Users\MaRe\HeitelCursors\Heitel-Cursors\Heitel Cursor Installer
@echo off
echo Building the executable for HeitelCursorInstaller.py...

:: Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller is not installed. Installing it now...
    pip install pyinstaller
)

:: Build the .exe with PyInstaller
pyinstaller --onefile --noconsole --icon="C:\Users\MaRe\HeitelCursors\Heitel-Cursors\recources\HeitelCursorsInstallerIcon.ico" ^
    "C:\Users\MaRe\HeitelCursors\Heitel-Cursors\Heitel Cursor Installer\HeitelCursorInstaller.py"

echo Build complete. Check the "dist" folder for the .exe file.
pause