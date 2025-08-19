#!/usr/bin/env python3
"""
OSINT Tool Auto Installer
Automatically installs all required dependencies for the OSINT tool
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DARK = '\033[90m'
    GREEN_BG = '\033[42m'
    RED_BG = '\033[41m'
    BLINK = '\033[5m'

def print_banner():
    banner = f"""
{Colors.RED_BG}{Colors.BOLD}{Colors.HEADER}
╔══════════════════════════════════════════════════════════════╗
║                OSINT TOOL AUTO INSTALLER                     ║
║                    Dependency Manager                        ║
║                     [ WE ARE LEGION ]                        ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print(f"{Colors.OKCYAN}[+] Checking Python version...{Colors.ENDC}")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"{Colors.FAIL}[-] Python 3.8+ required. Current version: {version.major}.{version.minor}{Colors.ENDC}")
        return False
    print(f"{Colors.OKGREEN}[+] Python version: {version.major}.{version.minor}.{version.micro}{Colors.ENDC}")
    return True

def check_pip():
    """Check if pip is available"""
    print(f"{Colors.OKCYAN}[+] Checking pip...{Colors.ENDC}")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print(f"{Colors.OKGREEN}[+] pip is available{Colors.ENDC}")
        return True
    except subprocess.CalledProcessError:
        print(f"{Colors.FAIL}[-] pip not found{Colors.ENDC}")
        return False

def upgrade_pip():
    """Upgrade pip to latest version"""
    print(f"{Colors.OKCYAN}[+] Upgrading pip...{Colors.ENDC}")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True)
        print(f"{Colors.OKGREEN}[+] pip upgraded successfully{Colors.ENDC}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.WARNING}[!] Failed to upgrade pip: {e}{Colors.ENDC}")
        return False

def install_package(package, description=""):
    """Install a single package"""
    try:
        print(f"{Colors.OKCYAN}[+] Installing {package}...{Colors.ENDC}")
        if description:
            print(f"{Colors.DARK}  {description}{Colors.ENDC}")
        
        result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{Colors.OKGREEN}[+] {package} installed successfully{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.FAIL}[-] Failed to install {package}: {result.stderr}{Colors.ENDC}")
            return False
    except Exception as e:
        print(f"{Colors.FAIL}[-] Error installing {package}: {e}{Colors.ENDC}")
        return False

def install_from_requirements():
    """Install packages from requirements.txt"""
    print(f"{Colors.OKCYAN}[+] Installing from requirements.txt...{Colors.ENDC}")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print(f"{Colors.FAIL}[-] requirements.txt not found{Colors.ENDC}")
        return False
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{Colors.OKGREEN}[+] All packages from requirements.txt installed successfully{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.WARNING}[!] Some packages failed to install: {result.stderr}{Colors.ENDC}")
            return False
    except Exception as e:
        print(f"{Colors.FAIL}[-] Error installing from requirements.txt: {e}{Colors.ENDC}")
        return False

def install_optional_tools():
    """Install optional tools that might be useful"""
    print(f"\n{Colors.OKCYAN}[+] Installing optional tools...{Colors.ENDC}")
    
    optional_tools = [
        ("nmap", "Network scanner (if not already installed)"),
        ("git", "Version control (for cloning repositories)"),
    ]
    
    system = platform.system().lower()
    
    if system == "windows":
        print(f"{Colors.WARNING}[!] On Windows, you may need to install nmap manually{Colors.ENDC}")
        print(f"{Colors.DARK}  Download from: https://nmap.org/download.html{Colors.ENDC}")
    elif system == "linux":
        print(f"{Colors.OKCYAN}[+] On Linux, you can install nmap with: sudo apt-get install nmap{Colors.ENDC}")
    elif system == "darwin":  # macOS
        print(f"{Colors.OKCYAN}[+] On macOS, you can install nmap with: brew install nmap{Colors.ENDC}")

def check_installed_packages():
    """Check which packages are already installed"""
    print(f"\n{Colors.OKCYAN}[+] Checking installed packages...{Colors.ENDC}")
    
    packages_to_check = [
        "whois", "dnspython", "requests", "sublist3r", "scrapy", 
        "beautifulsoup4", "lxml", "python-nmap", "paramiko"
    ]
    
    installed = []
    not_installed = []
    
    for package in packages_to_check:
        try:
            __import__(package.replace("-", "_"))
            installed.append(package)
            print(f"{Colors.OKGREEN}[+] {package} - Installed{Colors.ENDC}")
        except ImportError:
            not_installed.append(package)
            print(f"{Colors.WARNING}[-] {package} - Not installed{Colors.ENDC}")
    
    return installed, not_installed

def create_launcher_script():
    """Create a launcher script for easy execution"""
    print(f"\n{Colors.OKCYAN}[+] Creating launcher script...{Colors.ENDC}")
    
    if platform.system().lower() == "windows":
        launcher_content = """@echo off
echo Starting OSINT Tool...
python OSINT.py %*
pause
"""
        with open("run_osint.bat", "w") as f:
            f.write(launcher_content)
        print(f"{Colors.OKGREEN}[+] Created run_osint.bat{Colors.ENDC}")
    else:
        launcher_content = """#!/bin/bash
echo "Starting OSINT Tool..."
python3 OSINT.py "$@"
"""
        with open("run_osint.sh", "w") as f:
            f.write(launcher_content)
        os.chmod("run_osint.sh", 0o755)
        print(f"{Colors.OKGREEN}[+] Created run_osint.sh{Colors.ENDC}")

def main():
    print_banner()
    
    print(f"{Colors.BOLD}{Colors.OKGREEN}OSINT Tool Auto Installer{Colors.ENDC}")
    print(f"{Colors.DARK}{'='*60}{Colors.ENDC}")
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        print(f"{Colors.FAIL}[-] pip is required but not found{Colors.ENDC}")
        sys.exit(1)
    
    # Upgrade pip
    upgrade_pip()
    
    # Check current installations
    installed, not_installed = check_installed_packages()
    
    if not not_installed:
        print(f"\n{Colors.OKGREEN}[+] All required packages are already installed!{Colors.ENDC}")
    else:
        print(f"\n{Colors.OKCYAN}[+] Installing missing packages...{Colors.ENDC}")
        
        # Install from requirements.txt first
        install_from_requirements()
        
        # Install any remaining packages individually
        for package in not_installed:
            if package == "python-nmap":
                install_package("python-nmap", "Python nmap library")
            elif package == "sublist3r":
                install_package("sublist3r", "Subdomain enumeration tool")
            elif package == "scrapy":
                install_package("scrapy", "Web crawling framework")
            elif package == "paramiko":
                install_package("paramiko", "SSH library")
            else:
                install_package(package)
    
    # Install optional tools
    install_optional_tools()
    
    # Create launcher script
    create_launcher_script()
    
    # Final check
    print(f"\n{Colors.OKCYAN}[+] Final verification...{Colors.ENDC}")
    installed, not_installed = check_installed_packages()
    
    if not_installed:
        print(f"\n{Colors.WARNING}[!] Some packages could not be installed:{Colors.ENDC}")
        for package in not_installed:
            print(f"  {Colors.WARNING}- {package}{Colors.ENDC}")
        print(f"\n{Colors.DARK}You can try installing them manually:{Colors.ENDC}")
        for package in not_installed:
            print(f"  {Colors.DARK}pip install {package}{Colors.ENDC}")
    else:
        print(f"\n{Colors.OKGREEN}[+] All packages installed successfully!{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}Installation Complete!{Colors.ENDC}")
    print(f"{Colors.DARK}{'='*60}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[+] You can now run the OSINT tool with:{Colors.ENDC}")
    print(f"  {Colors.OKBLUE}python OSINT.py{Colors.ENDC}")
    
    if platform.system().lower() == "windows":
        print(f"  {Colors.OKBLUE}run_osint.bat{Colors.ENDC}")
    else:
        print(f"  {Colors.OKBLUE}./run_osint.sh{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Example usage:{Colors.ENDC}")
    print(f"  {Colors.DARK}python OSINT.py example.com{Colors.ENDC}")
    print(f"  {Colors.DARK}python OSINT.py{Colors.ENDC} (interactive mode)")
    
    print(f"\n{Colors.RED_BG}{Colors.BOLD}WE ARE LEGION{Colors.ENDC} 🔥")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Installation interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)
