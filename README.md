# GitHub Commit Automation Scripts

A pair of Python scripts to automate commit creation and removal for GitHub contribution graphs.

## 📁 Files

- `create_commits.py` - Creates automated commits for any date range
- `remove_commits.py` - Safely removes automated commits
- `setup_automation.sh` - Sets up the scripts in any git repository

## 🚀 Quick Setup

1. **Copy this folder to any location on your system**
2. **Navigate to any git repository where you want to add commits**
3. **Run the setup script:**
   ```bash
   /path/to/git_automation/setup_automation.sh
   ```

This will copy the automation scripts to your current repository.

## 📖 Usage

### Creating Commits

```bash
python3 create_commits.py
```

**Features:**
- Automatically detects the current git repository
- Shows available files and lets you choose a target file
- Multiple date range options:
  - Last 30/90/365 days
  - Specific year (e.g., 2023)
  - Custom date range
- Creates realistic commit patterns
- Saves automation log for safe removal
- Optional push to remote

### Removing Commits

```bash
python3 remove_commits.py
```

**Features:**
- Reads automation log to know exactly what to remove
- Three removal modes:
  - **Safe removal** (soft reset) - preserves working changes
  - **Complete removal** (hard reset) - removes everything
  - **File cleaning only** - removes automation comments
- Shows commit history before removal
- Optional force push to remote

## 🔧 How It Works

1. **Create Script:**
   - Detects current repository automatically
   - Lets you select target file from available files
   - Creates commits with backdated timestamps
   - Adds harmless comments to the target file
   - Saves log file (`.commit_automation_log.json`)

2. **Remove Script:**
   - Reads the log file to know what to remove
   - Uses git reset to remove commits safely
   - Cleans automation comments from files
   - Removes log file after successful removal

## 📋 Example Workflow

```bash
# Go to any git repository
cd /path/to/your/repo

# Set up automation scripts
/path/to/git_automation/setup_automation.sh

# Create commits for 2023
python3 create_commits.py
# Choose option 4 (specific year) and enter 2023

# Later, remove all automated commits
python3 remove_commits.py
# Choose option 1 (safe removal)
```

## 🛡️ Safety Features

- **Automatic backups**: Always creates log files for safe removal
- **Multiple confirmations**: Destructive operations require multiple confirmations
- **Soft reset default**: Preserves your work by default
- **Repository detection**: Won't run outside git repositories
- **File creation**: Creates target file if it doesn't exist

## ⚠️ Important Notes

- **Always backup your repository** before using these scripts
- The scripts detect comment syntax based on file extension
- Automation log is stored as `.commit_automation_log.json`
- GitHub may take 5-10 minutes to update contribution graphs
- Force pushing rewrites remote history - use with caution

## 🎯 Supported File Types

The scripts automatically detect the correct comment syntax for:

- **Python** (`.py`) - `#` comments
- **JavaScript/TypeScript** (`.js`, `.ts`) - `//` comments  
- **Java** (`.java`) - `//` comments
- **C/C++** (`.c`, `.cpp`) - `//` comments
- **Go** (`.go`) - `//` comments
- **Rust** (`.rs`) - `//` comments
- **PHP** (`.php`) - `//` comments
- **Shell** (`.sh`) - `#` comments
- **YAML** (`.yml`, `.yaml`) - `#` comments
- **And more...**

## 🤝 Contributing

Feel free to modify these scripts for your needs. The code is designed to be readable and modifiable.

## ⚖️ Disclaimer

These scripts are for educational purposes. Use responsibly and in accordance with GitHub's terms of service.
# git_automation
