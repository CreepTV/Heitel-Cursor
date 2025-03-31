@echo off
:: Set the script and output paths
set SCRIPT_PATH=c:\Users\MaRe\HeitelCursors\Heitel-Cursors\HeitelCursor.py
set OUTPUT_DIR=c:\Users\MaRe\HeitelCursors\Heitel-Cursors\dist

:: Ensure pyinstaller is installed
echo Checking for PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller is not installed. Installing now...
    pip install pyinstaller
)

:: Build the executable
echo Building HeitelCursor executable...
pyinstaller --onefile --noconsole --icon=c:\Users\MaRe\HeitelCursors\Heitel-Cursors\recources\HeitelCursorLogoNew.ico --distpath %OUTPUT_DIR% %SCRIPT_PATH%

:: Notify the user
if %errorlevel% equ 0 (
    echo Build successful! Executable is located in %OUTPUT_DIR%.
) else (
    echo Build failed. Check the output for errors.
)

pause
