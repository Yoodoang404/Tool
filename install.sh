#!/bin/bash

# OSINT Tool Auto Installer for Linux/macOS
# Automatically installs all required dependencies

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Banner
echo -e "${RED}${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                OSINT TOOL AUTO INSTALLER                     ║"
echo "║                    Dependency Manager                        ║"
echo "║                     [ WE ARE LEGION ]                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}[*] Starting OSINT Tool Auto Installer...${NC}"
echo -e "${CYAN}[*] This will install all required dependencies${NC}"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3 is not installed${NC}"
    echo -e "${YELLOW}[INFO] Please install Python 3.8+ first${NC}"
    echo -e "${YELLOW}  Ubuntu/Debian: sudo apt-get install python3 python3-pip${NC}"
    echo -e "${YELLOW}  CentOS/RHEL: sudo yum install python3 python3-pip${NC}"
    echo -e "${YELLOW}  macOS: brew install python3${NC}"
    exit 1
fi

echo -e "${GREEN}[+] Python3 found${NC}"
python3 --version

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}[ERROR] pip3 is not available${NC}"
    echo -e "${YELLOW}[INFO] Please install pip3${NC}"
    exit 1
fi

echo -e "${GREEN}[+] pip3 found${NC}"

# Upgrade pip
echo -e "${CYAN}[*] Upgrading pip...${NC}"
python3 -m pip install --upgrade pip

# Install from requirements.txt
echo -e "${CYAN}[*] Installing dependencies from requirements.txt...${NC}"
python3 -m pip install -r requirements.txt

# Install additional packages if needed
echo -e "${CYAN}[*] Installing additional packages...${NC}"
python3 -m pip install python-nmap paramiko

# Check if nmap is installed
if ! command -v nmap &> /dev/null; then
    echo -e "${YELLOW}[!] nmap is not installed${NC}"
    echo -e "${CYAN}[*] Installing nmap...${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y nmap
        elif command -v yum &> /dev/null; then
            sudo yum install -y nmap
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y nmap
        else
            echo -e "${YELLOW}[!] Please install nmap manually${NC}"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install nmap
        else
            echo -e "${YELLOW}[!] Please install Homebrew and then: brew install nmap${NC}"
        fi
    fi
else
    echo -e "${GREEN}[+] nmap found${NC}"
fi

# Create launcher script
echo -e "${CYAN}[*] Creating launcher script...${NC}"
cat > run_osint.sh << 'EOF'
#!/bin/bash
echo "Starting OSINT Tool..."
python3 OSINT.py "$@"
EOF

chmod +x run_osint.sh

echo
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    INSTALLATION COMPLETE                     ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo
echo -e "${GREEN}[+] All dependencies installed successfully!${NC}"
echo
echo -e "${CYAN}[*] You can now run the OSINT tool with:${NC}"
echo -e "    ${BLUE}python3 OSINT.py${NC}"
echo -e "    ${BLUE}./run_osint.sh${NC}"
echo
echo -e "${CYAN}[*] Example usage:${NC}"
echo -e "    ${BLUE}python3 OSINT.py example.com${NC}"
echo -e "    ${BLUE}python3 OSINT.py${NC} (interactive mode)"
echo
echo -e "${RED}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}${BOLD}║                     WE ARE LEGION                            ║${NC}"
echo -e "${RED}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo
