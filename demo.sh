#!/bin/bash

# GitHub Green Demo Script
# Demonstrates the basic functionality of GitHub Green

echo "🟢 GitHub Green Demo Script"
echo "=========================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "This demo must be run from inside a git repository"
    echo "Creating a temporary demo repository..."
    
    # Create temporary demo repository
    mkdir -p github_green_demo
    cd github_green_demo
    
    git init
    echo "# GitHub Green Demo Repository" > README.md
    echo "This is a temporary repository for demonstrating GitHub Green." >> README.md
    git add README.md
    git commit -m "Initial commit"
    
    print_status "Created temporary demo repository"
fi

echo ""
print_info "This demo will:"
echo "  1. Show current repository status"
echo "  2. Create a few test commits for the last 7 days"
echo "  3. Display the results"
echo "  4. Clean up (remove the test commits)"
echo ""

read -p "Do you want to continue with the demo? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Demo cancelled."
    exit 0
fi

echo ""
print_info "Step 1: Current repository status"
git log --oneline -5
echo ""

print_info "Step 2: Creating test commits for demonstration..."

# Create a temporary target file
echo "# Demo file for GitHub Green" > demo_file.py
echo "# This file is used for demonstration purposes" >> demo_file.py

# Create a few commits for the last week
current_date=$(date '+%Y-%m-%d')
echo ""
print_status "Creating commits with GitHub Green pattern..."

# Simulate the commit creation (simplified version)
for i in {1..7}; do
    date_offset=$((i-1))
    commit_date=$(date -d "$current_date - $date_offset days" '+%Y-%m-%d')
    
    # Add a line to the demo file
    echo "# Demo comment for $commit_date" >> demo_file.py
    
    # Stage and commit
    git add demo_file.py
    git commit -m "Demo commit for $commit_date" --date="$commit_date 12:00:00" > /dev/null 2>&1
    
    print_status "Created commit for $commit_date"
done

echo ""
print_info "Step 3: Results - Recent commits:"
git log --oneline -10
echo ""

print_info "Step 4: Cleanup - Removing demo commits..."

# Count commits to remove (all commits after the initial demo setup)
initial_commit=$(git log --reverse --format="%H" | head -1)
commits_to_remove=$(git rev-list --count HEAD...$initial_commit 2>/dev/null || echo "7")

if [ "$commits_to_remove" -gt 0 ]; then
    # Reset to before our demo commits
    git reset --hard HEAD~$commits_to_remove > /dev/null 2>&1
    print_status "Removed $commits_to_remove demo commits"
else
    print_warning "No commits to remove"
fi

# Remove demo file
if [ -f "demo_file.py" ]; then
    rm demo_file.py
    print_status "Removed demo file"
fi

echo ""
print_info "Final repository status:"
git log --oneline -5
echo ""

print_status "Demo completed successfully!"
echo ""
echo "🟢 GitHub Green Features Demonstrated:"
echo "  ✓ Automated commit creation with realistic dates"
echo "  ✓ File modification and git operations"
echo "  ✓ Safe commit removal and cleanup"
echo ""
echo "📖 To use GitHub Green in your projects:"
echo "  1. Run: python3 create_commits.py"
echo "  2. Choose your date range and options"
echo "  3. Let GitHub Green fill your contribution graph!"
echo "  4. Use remove_commits.py if you want to undo"
echo ""
print_info "Visit the README.md for full documentation and examples"
