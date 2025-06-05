# Basic Usage Examples

## Example 1: Quick Start (Last 30 Days)

The simplest way to get started with GitHub Green:

```bash
# Navigate to your repository
cd /path/to/your/repository

# Set up GitHub Green
./setup_automation.sh

# Run the commit creator
python3 create_commits.py
```

**Interactive choices:**
- Choose option **1** (Last 30 days)
- Select a target file from the list
- Confirm to proceed
- Choose **y** to push (optional)

**Expected result:** Your GitHub contribution graph will show activity for the last 30 days.

---

## Example 2: Fill a Complete Year

Perfect for making your profile look consistently active:

```bash
python3 create_commits.py
```

**Interactive choices:**
- Choose option **4** (Specific year)
- Enter **2024** (or any year you want)
- Select target file: choose **1** (usually a Python or JavaScript file)
- Confirm to proceed

**Expected result:** ~800-1200 commits spread throughout 2024.

---

## Example 3: Custom Date Range

For precise control over the time period:

```bash
python3 create_commits.py
```

**Interactive choices:**
- Choose option **5** (Custom date range)
- Start date: **2023-06-01**
- End date: **2023-12-31**
- Select your preferred target file

**Expected result:** Activity from June 1st to December 31st, 2023.

---

## Example 4: Safe Experimentation

Test GitHub Green safely before committing to larger changes:

```bash
# Create a small test period
python3 create_commits.py
# Choose option 1 (last 30 days)

# Check your GitHub profile
# Visit: https://github.com/yourusername

# If satisfied, keep the commits
# If not satisfied, remove them:
python3 remove_commits.py
# Choose option 1 (safe removal)
```

---

## Example 5: Multiple Repositories

Using GitHub Green across different projects:

```bash
# Repository 1: Personal portfolio
cd ~/projects/portfolio
/path/to/github-green/setup_automation.sh
python3 create_commits.py  # Fill 2024

# Repository 2: Learning project  
cd ~/projects/learning-python
python3 create_commits.py  # Fill last 90 days

# Repository 3: Open source contribution
cd ~/projects/open-source-project
python3 create_commits.py  # Fill last 30 days
```

---

## Example Outputs

### Successful Commit Creation
```
🚀 GitHub Commit Creator
==================================================
Repository: /home/user/my-project
Target file: src/main.py
==================================================

📊 Selected period: 2024-01-01 to 2024-12-31
Expected commits: ~1095

⚠️  WARNING: This will create many automated commits!
⚠️  Make sure you have a backup of your repository!

Do you want to proceed? (y/N): y

🎯 Starting commit generation...
Creating 3 commits for 2024-01-01
  ✓ Commit 1/3 created at 2024-01-01 14:23:15
  ✓ Commit 2/3 created at 2024-01-01 16:45:32
  ✓ Commit 3/3 created at 2024-01-01 19:12:07
  → Successfully created 3/3 commits for 2024-01-01

...

📊 Summary:
Total days with commits: 245
Total commits created: 847
Average commits per active day: 3.5

📝 Automation log saved to: .commit_automation_log.json

🚀 Do you want to push commits to remote repository? (y/N): y
⏳ Pushing commits to remote repository...
✓ All commits pushed successfully!

🎉 COMMIT CREATION COMPLETED SUCCESSFULLY!
🟢 Your GitHub contribution graph should now show activity for the selected period!
```

### Successful Commit Removal
```
🗑️  GitHub Commit Remover
==================================================
Repository: /home/user/my-project
==================================================

📋 Found automation log:
  Date range: 2024-01-01 to 2024-12-31
  Total commits: 847
  Target file: src/main.py
  Created at: 2025-06-05T10:30:45

📊 Commits to remove: 847

🔧 Removal Options:
1. 🔄 Safe Removal (Soft Reset)
2. ⚠️  Complete Removal (Hard Reset)  
3. 🧹 File Cleaning + Soft Reset
4. ❌ Cancel

Select removal option (1-4): 1

🔄 Removing 847 automated commits...
✅ Commits removed successfully (soft reset)
📝 Your working directory changes are preserved

🎉 COMMIT REMOVAL COMPLETED!
```

## Tips for Success

1. **Start Small**: Test with 30 days first
2. **Choose Appropriate Files**: Pick files you actually work with
3. **Backup First**: Always have a backup before automation
4. **Review Results**: Check your GitHub profile after changes
5. **Use Responsibly**: Be transparent about automation in professional contexts
