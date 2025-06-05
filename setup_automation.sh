#!/bin/bash
# GitHub Commit Automation Setup Script
# This script copies the automation scripts to any git repository

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 GitHub Commit Automation Setup${NC}"
echo "=================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Error: Current directory is not a git repository!${NC}"
    echo "Please run this script from inside a git repository."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if automation scripts exist
if [ ! -f "$SCRIPT_DIR/create_commits.py" ] || [ ! -f "$SCRIPT_DIR/remove_commits.py" ]; then
    echo -e "${RED}❌ Error: Automation scripts not found!${NC}"
    echo "Please make sure create_commits.py and remove_commits.py are in the same directory as this script."
    exit 1
fi

# Current repository path
REPO_PATH=$(pwd)
echo -e "${GREEN}📁 Repository: ${REPO_PATH}${NC}"

# Copy scripts to current repository
echo -e "${YELLOW}📋 Copying automation scripts...${NC}"

cp "$SCRIPT_DIR/create_commits.py" ./
cp "$SCRIPT_DIR/remove_commits.py" ./

# Make scripts executable
chmod +x create_commits.py remove_commits.py

echo -e "${GREEN}✅ Scripts copied successfully!${NC}"
echo ""
echo "📝 Available scripts:"
echo "  • create_commits.py  - Creates automated commits"
echo "  • remove_commits.py  - Removes automated commits"
echo ""
echo "🚀 Usage:"
echo "  python3 create_commits.py   # To create commits"
echo "  python3 remove_commits.py   # To remove commits"
echo ""
echo "⚠️  Important notes:"
echo "  • Always backup your repository before using these scripts"
echo "  • The scripts work with the current directory as the repository"
echo "  • A log file will be created to track automation for safe removal"
echo ""
echo -e "${GREEN}🎉 Setup complete! You can now run the automation scripts.${NC}"
