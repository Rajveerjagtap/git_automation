#!/bin/bash

# GitHub Green Quick Installer
# Downloads and sets up GitHub Green in any git repository

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${GREEN}${BOLD}🟢 GitHub Green Quick Installer${NC}"
echo "=================================="
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Error: This must be run from inside a git repository${NC}"
    echo "Please navigate to your git repository and run this script again."
    exit 1
fi

echo -e "${BLUE}ℹ${NC} Current repository: $(pwd)"
echo ""

# Download method selection
echo "📦 Choose installation method:"
echo "1. Download from GitHub (latest release)"
echo "2. Clone repository (development version)"
echo "3. Cancel"
echo ""

read -p "Select option (1-3): " choice

case $choice in
    1)
        echo ""
        echo -e "${YELLOW}⏳${NC} Downloading GitHub Green from latest release..."
        
        # Download the latest release
        LATEST_URL="https://api.github.com/repos/yourusername/github-green/releases/latest"
        DOWNLOAD_URL=$(curl -s $LATEST_URL | grep "tarball_url" | cut -d '"' -f 4)
        
        if [ -z "$DOWNLOAD_URL" ]; then
            echo -e "${RED}❌ Error: Could not fetch latest release${NC}"
            exit 1
        fi
        
        # Download and extract
        curl -L "$DOWNLOAD_URL" | tar -xz --strip-components=1
        ;;
        
    2)
        echo ""
        echo -e "${YELLOW}⏳${NC} Cloning GitHub Green repository..."
        
        # Clone to temporary directory
        git clone https://github.com/yourusername/github-green.git /tmp/github-green-temp
        
        # Copy files
        cp /tmp/github-green-temp/*.py .
        cp /tmp/github-green-temp/*.sh .
        cp /tmp/github-green-temp/*.md .
        
        # Cleanup
        rm -rf /tmp/github-green-temp
        ;;
        
    3)
        echo "Installation cancelled."
        exit 0
        ;;
        
    *)
        echo -e "${RED}❌ Invalid option${NC}"
        exit 1
        ;;
esac

# Make scripts executable
chmod +x *.py *.sh

echo -e "${GREEN}✓${NC} GitHub Green installed successfully!"
echo ""
echo "📋 Available commands:"
echo "  ${BOLD}python3 create_commits.py${NC} - Create commits to fill your contribution graph"
echo "  ${BOLD}python3 remove_commits.py${NC} - Safely remove automated commits"
echo "  ${BOLD}./demo.sh${NC} - Run a quick demonstration"
echo ""
echo "🚀 Quick start:"
echo "  python3 create_commits.py"
echo ""
echo -e "${BLUE}ℹ${NC} For full documentation, see README.md"
echo -e "${YELLOW}⚠${NC} Always backup your repository before automation!"
echo ""
echo -e "${GREEN}🎉 Happy coding!${NC}"
