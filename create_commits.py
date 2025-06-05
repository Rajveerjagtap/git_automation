"""
GitHub Commit Creator
Creates automated commits for a specified date range to fill GitHub contribution graph.
"""

import os
import random
import subprocess
from datetime import datetime, timedelta
import time
import json

class GitCommitCreator:
    def __init__(self, repo_path, target_file):
        self.repo_path = repo_path
        self.target_file = target_file
        self.commit_log_file = os.path.join(repo_path, '.commit_automation_log.json')
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
                return False, result.stderr
            return True, result.stdout
        except Exception as e:
            print(f"Exception running command {command}: {e}")
            return False, str(e)
    
    def get_current_commit_hash(self):
        """Get the current commit hash"""
        success, output = self.run_git_command("git rev-parse HEAD")
        if success:
            return output.strip()
        return None
    
    def save_automation_log(self, start_commit, end_commit, total_commits, date_range):
        """Save automation log for removal script"""
        log_data = {
            'start_commit': start_commit,
            'end_commit': end_commit,
            'total_commits': total_commits,
            'date_range': date_range,
            'created_at': datetime.now().isoformat(),
            'target_file': self.target_file
        }
        
        try:
            with open(self.commit_log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
            print(f"📝 Automation log saved to: {self.commit_log_file}")
        except Exception as e:
            print(f"Warning: Could not save automation log: {e}")
    
    def modify_file(self, commit_num, date_str):
        """Modify the target file - always add content to ensure commits work"""
        file_path = os.path.join(self.repo_path, self.target_file)
        
        # Create the file if it doesn't exist
        if not os.path.exists(file_path):
            print(f"📄 Creating target file: {self.target_file}")
            with open(file_path, 'w') as f:
                f.write(f"# Automation Target File\n")
                f.write(f"# Created for commit automation\n\n")
        
        try:
            # Determine comment style based on file extension
            file_ext = os.path.splitext(self.target_file)[1].lower()
            if file_ext in ['.py', '.sh', '.yml', '.yaml', '.conf']:
                comment_prefix = "#"
            elif file_ext in ['.java', '.js', '.ts', '.cpp', '.c', '.cs', '.php', '.go', '.rs']:
                comment_prefix = "//"
            elif file_ext in ['.html', '.xml']:
                comment_prefix = "<!--"
                comment_suffix = "-->"
            else:
                comment_prefix = "#"  # Default to hash
            
            # Always add content - this ensures every commit has changes
            comment = f"{comment_prefix} Auto-generated comment {random.randint(1000, 9999)}"
            
            # Add different types of modifications
            modifications = [
                f"{comment_prefix} Modified on {date_str}",
                f"{comment_prefix} Commit #{commit_num} - {comment}",
                f"{comment_prefix} Update: {random.choice(['refactor', 'optimize', 'cleanup', 'enhance'])}",
                f"{comment_prefix} Version: {random.randint(1, 100)}.{random.randint(0, 9)}",
                f"{comment_prefix} Build: {random.randint(1000, 9999)}",
                f"{comment_prefix} Feature: {random.choice(['improvement', 'bugfix', 'enhancement', 'maintenance'])}",
                f"{comment_prefix} Automation commit {random.randint(100, 999)}"
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
            if not self.run_git_command(f"git add {self.target_file}")[0]:
                print(f"  ✗ Failed to stage file for commit {i+1}")
                continue
            
            # Check if there are actually changes to commit
            if not self.check_for_changes():
                print(f"  ⚠ No changes to commit for commit {i+1}")
                continue
            
            # Commit with backdated timestamp
            commit_msg = random.choice(self.commit_messages)
            commit_command = f'git commit -m "{commit_msg}"'
            
            if self.run_git_command(commit_command, git_date)[0]:
                successful_commits += 1
                print(f"  ✓ Commit {successful_commits}/{num_commits} created at {git_date}")
            else:
                print(f"  ✗ Failed to create commit {i+1}")
            
            # Small delay to avoid issues
            time.sleep(0.1)
        
        print(f"  → Successfully created {successful_commits}/{num_commits} commits for {date_str}")
        return successful_commits
    
    def generate_commits_for_period(self, start_date, end_date):
        """Generate commits for a specified period"""
        print(f"Starting commit generation from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
        
        if not self.run_git_command("git status")[0]:
            print("Error: Not in a git repository or git not configured")
            return False
        
        # Get starting commit hash
        start_commit = self.get_current_commit_hash()
        
        current_date = start_date
        total_commits = 0
        total_days = 0
        
        print(f"📅 Processing {(end_date - start_date).days + 1} days...")
        
        # Generate commits for each day in the period
        while current_date <= end_date:
            # 65% chance of having commits on any given day
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
        
        end_commit = self.get_current_commit_hash()
        
        print(f"\n📊 Summary:")
        print(f"Total days with commits: {total_days}")
        print(f"Total commits created: {total_commits}")
        print(f"Average commits per active day: {total_commits/total_days if total_days > 0 else 0:.1f}")
        
        # Save automation log
        date_range = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        self.save_automation_log(start_commit, end_commit, total_commits, date_range)
        
        push_response = input("\n🚀 Do you want to push commits to remote repository? (y/N): ")
        if push_response.lower() == 'y':
            print("⏳ Pushing commits to remote repository...")
            
            if self.run_git_command("git push origin main")[0]:
                print("✓ All commits pushed successfully!")
            elif self.run_git_command("git push origin master")[0]:
                print("✓ All commits pushed successfully!")
            else:
                print("✗ Error pushing commits.")
                print("Try manually with one of these commands:")
                print("  git push origin main")
                print("  git push origin master")
                print("  git push")
        
        return True

def get_repo_info():
    """Get repository path and suggest target files"""
    # Use current directory as repository path
    repo_path = os.getcwd()
    
    # Check if we're in a git repository
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("❌ Error: Current directory is not a git repository!")
        print("Please run this script from inside a git repository.")
        return None, None
    
    common_files = []
    for root, dirs, files in os.walk(repo_path):
        # Skip .git and other hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith(('.py', '.js', '.java', '.cpp', '.c', '.ts', '.php', '.rb', '.go', '.rs')):
                rel_path = os.path.relpath(os.path.join(root, file), repo_path)
                common_files.append(rel_path)
        
        if len(common_files) >= 20:
            break
    
    return repo_path, common_files[:20]  # Limit to first 20 files

def select_target_file(suggested_files):
    """Let user select or specify target file"""
    if not suggested_files:
        print("No suitable files found in repository.")
        target_file = input("Enter target file name (will be created if doesn't exist): ").strip()
        return target_file if target_file else "automation_target.txt"
    
    print("\n📁 Found these files in your repository:")
    for i, file in enumerate(suggested_files, 1):
        print(f"{i:2}. {file}")
    
    print(f"{len(suggested_files) + 1:2}. Specify custom file")
    
    while True:
        try:
            choice = input(f"\nSelect target file (1-{len(suggested_files) + 1}): ").strip()
            
            if choice == str(len(suggested_files) + 1):
                custom_file = input("Enter target file path: ").strip()
                return custom_file if custom_file else "automation_target.txt"
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(suggested_files):
                return suggested_files[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(suggested_files) + 1}")
        except ValueError:
            print("Please enter a valid number")

def main():
    print("🚀 GitHub Commit Creator")
    print("=" * 50)
    
    # Get repository information
    repo_path, suggested_files = get_repo_info()
    if repo_path is None:
        return
    
    # Get target file
    target_file = select_target_file(suggested_files)
    
    print(f"Repository: {repo_path}")
    print(f"Target file: {target_file}")
    print("=" * 50)
    
    # Get date range from user
    print("\n📅 Date Range Configuration:")
    print("1. Last 30 days")
    print("2. Last 90 days")
    print("3. Last 365 days (full year)")
    print("4. Specific year (e.g., 2023)")
    print("5. Custom date range")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    elif choice == "2":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
    elif choice == "3":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
    elif choice == "4":
        year = input("Enter year (e.g., 2023): ").strip()
        try:
            year = int(year)
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
        except ValueError:
            print("Invalid year. Using last 30 days.")
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
    elif choice == "5":
        try:
            start_str = input("Enter start date (YYYY-MM-DD): ").strip()
            end_str = input("Enter end date (YYYY-MM-DD): ").strip()
            start_date = datetime.strptime(start_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Using last 30 days.")
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
    else:
        print("Invalid choice. Using last 30 days.")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    
    print(f"\n📊 Selected period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    expected_commits = (end_date - start_date).days * 3  # Rough estimate
    print(f"Expected commits: ~{expected_commits}")
    
    print("\n⚠️  WARNING: This will create many automated commits!")
    print("⚠️  Make sure you have a backup of your repository!")
    
    response = input("\nDo you want to proceed? (y/N): ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    print("\n🎯 Starting commit generation...")
    
    creator = GitCommitCreator(repo_path, target_file)
    success = creator.generate_commits_for_period(start_date, end_date)
    
    if success:
        print("\n🎉 COMMIT CREATION COMPLETED SUCCESSFULLY!")
        print("🟢 Your GitHub contribution graph should now show activity for the selected period!")
        print("\n💡 Note: It may take 5-10 minutes for GitHub to update the contribution graph.")
        print("🔄 Refresh your GitHub profile page to see the changes.")
        print(f"\n📝 To remove these commits later, use the 'remove_commits.py' script.")
    else:
        print("\n❌ Commit creation failed. Please check the errors above.")

if __name__ == "__main__":
    main()
