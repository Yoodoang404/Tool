@echo off
title OSINT Tool Auto Installer
color 0a

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                OSINT TOOL AUTO INSTALLER                     ║
echo ║                    Dependency Manager                        ║
echo ║                     [ WE ARE LEGION ]                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [*] Starting OSINT Tool Auto Installer...
echo [*] This will install all required dependencies
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [INFO] Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [+] Python found
python --version

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available
    echo [INFO] Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo [+] pip found

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip

REM Install from requirements.txt
echo [*] Installing dependencies from requirements.txt...
python -m pip install -r requirements.txt

REM Install additional packages if needed
echo [*] Installing additional packages...
python -m pip install python-nmap paramiko

REM Create launcher script
echo [*] Creating launcher script...
echo @echo off > run_osint.bat
echo echo Starting OSINT Tool... >> run_osint.bat
echo python OSINT.py %%* >> run_osint.bat
echo pause >> run_osint.bat

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    INSTALLATION COMPLETE                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo [+] All dependencies installed successfully!
echo.
echo [*] You can now run the OSINT tool with:
echo     python OSINT.py
echo     run_osint.bat
echo.
echo [*] Example usage:
echo     python OSINT.py example.com
echo     python OSINT.py (interactive mode)
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                     WE ARE LEGION                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause
