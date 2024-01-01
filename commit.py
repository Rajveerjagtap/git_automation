import os
import random
import subprocess
from datetime import datetime, timedelta
import time

class GitCommitAutomator:
    def __init__(self, repo_path, target_file):
        self.repo_path = repo_path
        self.target_file = target_file
        self.commit_messages = [
            "Update code structure",
            "Fix minor issues", 
            "Refactor code",
            "Add improvements",
            "Update documentation",
            "Optimize performance",
            "Fix bugs",
            "Clean up code",
            "Add new features",
            "Update comments",
            "Improve UI",
            "Fix styling",
            "Update methods",
            "Add error handling",
            "Improve logic",
            "Code cleanup",
            "Minor updates",
            "Performance improvements",
            "Bug fixes",
            "Feature updates"
        ]
        
    def run_git_command(self, command, date_str=None):
        """Run git command with optional date"""
        try:
            if date_str:
                env = os.environ.copy()
                env['GIT_AUTHOR_DATE'] = date_str
                env['GIT_COMMITTER_DATE'] = date_str
                result = subprocess.run(command, shell=True, cwd=self.repo_path, 
                                      capture_output=True, text=True, env=env)
            else:
                result = subprocess.run(command, shell=True, cwd=self.repo_path,
                                      capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error running command: {command}")
                print(f"Error: {result.stderr}")
                return False
            return True
        except Exception as e:
            print(f"Exception running command {command}: {e}")
            return False
    
    def modify_file(self, commit_num, date_str):
        """Modify the target file - always add content to ensure commits work"""
        file_path = os.path.join(self.repo_path, self.target_file)
        
        try:
            # Always add content - this ensures every commit has changes
            
            # Add different types of modifications with 2023 context
            modifications = [
                f"// Modified on {date_str}",
                f"// Commit #{commit_num} - {comment}",
                f"// Update: {random.choice(['refactor', 'optimize', 'cleanup', 'enhance'])}",
                f"// Version: {random.randint(1, 100)}.{random.randint(0, 9)}",
                f"// Build: {random.randint(1000, 9999)}",
                f"// 2023 Update: {random.choice(['feature', 'bugfix', 'improvement', 'maintenance'])}",
                f"// Year 2023 - Build {random.randint(100, 999)}"
            ]
            
            selected_mod = random.choice(modifications)
            
            with open(file_path, 'a') as f:
                f.write(f"\n{selected_mod}\n")
            
            return True
        except Exception as e:
            print(f"Error modifying file: {e}")
            return False
    
    def check_for_changes(self):
        """Check if there are changes to commit"""
        try:
            result = subprocess.run("git diff --cached --name-only", 
                                  shell=True, cwd=self.repo_path,
                                  capture_output=True, text=True)
            return len(result.stdout.strip()) > 0
        except:
            return False
    
    def create_commits_for_date(self, target_date, num_commits):
        """Create specified number of commits for a given date"""
        date_str = target_date.strftime('%Y-%m-%d')
        print(f"Creating {num_commits} commits for {date_str}")
        
        successful_commits = 0
        
        for i in range(num_commits):
            # Randomize time within the day
            hour = random.randint(9, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_time = target_date.replace(hour=hour, minute=minute, second=second)
            git_date = commit_time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Modify the file
            if not self.modify_file(i + 1, date_str):
                print(f"  ✗ Failed to modify file for commit {i+1}")
                continue
            
            # Stage the file
            if not self.run_git_command(f"git add {self.target_file}"):
                print(f"  ✗ Failed to stage file for commit {i+1}")
                continue
            
            # Check if there are actually changes to commit
            if not self.check_for_changes():
                print(f"  ⚠ No changes to commit for commit {i+1}")
                continue
            
            # Commit with backdated timestamp
            commit_msg = random.choice(self.commit_messages)
            commit_command = f'git commit -m "{commit_msg}"'
            
            if self.run_git_command(commit_command, git_date):
                successful_commits += 1
                print(f"  ✓ Commit {successful_commits}/{num_commits} created at {git_date}")
            else:
                print(f"  ✗ Failed to create commit {i+1}")
            
            # Small delay to avoid issues
            time.sleep(0.1)
        
        print(f"  → Successfully created {successful_commits}/{num_commits} commits for {date_str}")
        return successful_commits
    
    def generate_commits_for_2023(self):
        """Generate commits specifically for the year 2023"""
        print("Starting commit generation for the FULL YEAR 2023...")
        print("This will create commits from Jan 1, 2023 to Dec 31, 2023")
        
        if not self.run_git_command("git status"):
            print("Error: Not in a git repository or git not configured")
            return False
        
        if not os.path.exists(os.path.join(self.repo_path, self.target_file)):
            print(f"Error: Target file {self.target_file} not found")
            return False
        
        ####MANUPLATE DATES HERE TO GENERATE COMMITS FOR THAT YEAR OR DATE LIMITS
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 3, 1)
        
        current_date = start_date
        total_commits = 0
        total_days = 0
        
        print(f"📅 Processing {(end_date - start_date).days + 1} days in 2023...")
        
        # Generate commits for each day in 2023
        while current_date <= end_date:
            # 65% chance of having commits on any given day (more active year)
            if random.random() < 0.65:
                # Vary commits by day of week (more commits on weekdays)
                if current_date.weekday() < 5:  # Monday-Friday
                    num_commits = random.randint(1, 8)
                else:  # Weekend
                    num_commits = random.randint(1, 4)
                
                commits_made = self.create_commits_for_date(current_date, num_commits)
                total_commits += commits_made
                if commits_made > 0:
                    total_days += 1
                
                # Special busy periods (simulate project deadlines)
                if random.random() < 0.05:  # 5% chance of very busy day
                    extra_commits = random.randint(5, 12)
                    extra_made = self.create_commits_for_date(current_date, extra_commits)
                    total_commits += extra_made
                    print(f"  🔥 BUSY DAY: Extra {extra_made} commits added!")
            
            current_date += timedelta(days=1)
        
        print(f"\n📊 2023 Summary:")
        print(f"Total days with commits: {total_days}")
        print(f"Total commits created: {total_commits}")
        print(f"Average commits per active day: {total_commits/total_days if total_days > 0 else 0:.1f}")
        
        # Push all commits
        print("\n🚀 Pushing ALL 2023 commits to remote repository...")
        print("⏳ This may take several minutes depending on your internet connection...")
        
        if self.run_git_command("git push origin main"):
            print("✓ All 2023 commits pushed successfully!")
        elif self.run_git_command("git push origin master"):
            print("✓ All 2023 commits pushed successfully!")
        else:
            print("✗ Error pushing commits.")
            print("Try manually with one of these commands:")
            print("  git push origin main")
            print("  git push origin master")
            print("  git push")
        
        return True

def main():
    REPO_PATH = "/home/rajveer/oibsip_task_3"  
    TARGET_FILE = "ATMinterface.java"  
    
    print("🚀 GitHub Commit Automator - 2023 FULL YEAR EDITION")
    print("=" * 60)
    print(f"Repository: {REPO_PATH}")
    print(f"Target file: {TARGET_FILE}")
    print(f"Target period: January 1, 2023 - December 31, 2023")
    print(f"Expected commits: ~800-1200 commits")
    print("=" * 60)
    
    print("⚠️  WARNING: This will create commits for ENTIRE YEAR 2023!")
    print("⚠️  This means hundreds of commits will be created!")
    print("⚠️  Make sure you have a backup of your repository!")
    print("⚠️  This process may take 10-30 minutes to complete!")
    
    response = input("\nDo you want to proceed with 2023 full year? (y/N): ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    print("\n🚨 FINAL WARNING:")
    print("This will modify your git history for the entire year 2023.")
    print("Your GitHub contribution graph will show activity for all of 2023.")
    confirm = input("Type 'YES 2023' to confirm you want to proceed: ")
    if confirm != 'YES 2023':
        print("Aborted for safety.")
        return
    
    print("\n🎯 Starting 2023 commit generation...")
    print("Grab a coffee ☕ - this will take a while!")
    
    automator = GitCommitAutomator(REPO_PATH, TARGET_FILE)
    success = automator.generate_commits_for_2023()
    
    if success:
        print("\n🎉 2023 AUTOMATION COMPLETED SUCCESSFULLY!")
        print("🟢 Your GitHub contribution panel for 2023 should now be completely green!")
        print("📈 You now have a full year of commit activity for 2023!")
        print("\n💡 Note: It may take 5-10 minutes for GitHub to update the contribution graph.")
        print("🔄 Refresh your GitHub profile page to see the changes.")
    else:
        print("\n❌ 2023 Automation failed. Please check the errors above.")

if __name__ == "__main__":
    main()

# Modified on 2025-01-02


# Update: optimize

# Version: 90.4

# Build: 8277


# Modified on 2025-01-02

# Automation commit 639

# Automation commit 159

# Modified on 2025-01-06

# Build: 1810

# Build: 1140

# Update: optimize

# Automation commit 822

# Update: cleanup

# Feature: enhancement

# Version: 57.1

# Feature: improvement

# Build: 9851


# Version: 2.8

# Update: refactor

# Feature: bugfix

# Version: 65.8

# Automation commit 345

# Version: 13.7

# Build: 7658

# Build: 6687

# Feature: improvement

# Automation commit 376

# Modified on 2025-01-08

# Feature: enhancement


# Update: enhance


# Automation commit 474

# Update: refactor

# Update: optimize

# Automation commit 652

# Build: 3743

# Automation commit 146

# Update: enhance

# Update: optimize

# Modified on 2025-01-16

# Automation commit 942


# Build: 2047

# Modified on 2025-01-16

# Automation commit 637

# Update: cleanup

# Automation commit 507

# Update: optimize

# Version: 1.7

# Version: 78.7


# Modified on 2025-01-19

# Modified on 2025-01-21

# Build: 3532

# Automation commit 152

# Build: 1723

# Feature: bugfix

# Update: enhance


# Build: 7376

# Automation commit 810

# Feature: bugfix

# Build: 1731


# Feature: improvement


# Modified on 2025-01-27

# Version: 26.7

# Version: 80.1

# Build: 3742

# Build: 7149

# Build: 7709


# Version: 20.9

# Update: enhance

# Build: 2436


# Version: 76.1

# Feature: enhancement

# Version: 50.0

# Version: 66.2

# Automation commit 159

# Update: refactor

# Build: 5832

# Modified on 2024-01-01
