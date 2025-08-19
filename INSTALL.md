# 🚀 OSINT Tool Installation Guide

## 📋 Prerequisites

- **Python 3.8+** - [Download Python](https://python.org)
- **pip** - Usually comes with Python
- **Internet connection** - For downloading packages

## 🎯 Quick Installation

### Windows Users
```bash
# Method 1: Double-click installer
install.bat

# Method 2: Command line
python install.py

# Method 3: Manual
pip install -r requirements.txt
pip install python-nmap paramiko
```

### Linux/macOS Users
```bash
# Method 1: Shell script
chmod +x install.sh
./install.sh

# Method 2: Python script
python3 install.py

# Method 3: Manual
pip3 install -r requirements.txt
pip3 install python-nmap paramiko
```

## 🔧 System Dependencies

### Windows
- **Nmap**: Download from [nmap.org](https://nmap.org/download.html)
- Add nmap to your PATH environment variable

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install nmap
```

### Linux (CentOS/RHEL)
```bash
sudo yum install nmap
# or
sudo dnf install nmap
```

### macOS
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install nmap
brew install nmap
```

## 📦 Manual Installation

### Step 1: Install Python Dependencies
```bash
# Core dependencies
pip install whois dnspython requests

# Advanced dependencies
pip install sublist3r scrapy beautifulsoup4 lxml

# Network scanning
pip install python-nmap

# SSH connections
pip install paramiko

# Or install all at once
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
python -c "import whois, dns.resolver, requests, sublist3r, scrapy, nmap, paramiko; print('All packages installed successfully!')"
```

## 🚨 Troubleshooting

### Common Issues

#### 1. "pip not found"
```bash
# Windows
python -m ensurepip --upgrade

# Linux/macOS
sudo apt-get install python3-pip  # Ubuntu/Debian
sudo yum install python3-pip      # CentOS/RHEL
```

#### 2. "Permission denied"
```bash
# Use user installation
pip install --user -r requirements.txt

# Or use virtual environment
python -m venv osint_env
source osint_env/bin/activate  # Linux/macOS
osint_env\Scripts\activate     # Windows
```

#### 3. "nmap not found"
- Windows: Download and install nmap manually
- Linux: `sudo apt-get install nmap`
- macOS: `brew install nmap`

#### 4. "Module not found" errors
```bash
# Reinstall specific package
pip uninstall package_name
pip install package_name

# Or upgrade all packages
pip install --upgrade -r requirements.txt
```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv osint_env

# Activate (Windows)
osint_env\Scripts\activate

# Activate (Linux/macOS)
source osint_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tool
python OSINT.py example.com

# Deactivate when done
deactivate
```

## ✅ Verification

After installation, test the tool:

```bash
# Test basic functionality
python OSINT.py --help

# Test with a domain
python OSINT.py example.com

# Check if all modules work
python -c "
import whois
import dns.resolver
import requests
import sublist3r
import scrapy
import nmap
import paramiko
print('✅ All modules imported successfully!')
"
```

## 🎉 Success!

If everything is installed correctly, you should see:
- All packages installed without errors
- `run_osint.bat` (Windows) or `run_osint.sh` (Linux/macOS) created
- Tool runs without import errors

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure Python 3.8+ is installed
3. Try installing packages individually
4. Use virtual environment for isolation

---

**WE ARE LEGION** 🔥
