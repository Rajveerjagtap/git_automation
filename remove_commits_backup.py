#!/usr/bin/env python3
"""
GitHub Commit Remover
Removes automated commits created by the create_commits.py script.
"""

import os
import subprocess
import json
from datetime import datetime

class GitCommitRemover:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.commit_log_file = os.path.join(repo_path, '.commit_automation_log.json')
        
    def run_git_command(self, command):
        """Run git command"""
        try:
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
    
    def load_automation_log(self):
        """Load automation log to get commit information"""
        try:
            if not os.path.exists(self.commit_log_file):
                print(f"❌ Automation log file not found: {self.commit_log_file}")
                print("This file is created when you run create_commits.py")
                return None
            
            with open(self.commit_log_file, 'r') as f:
                log_data = json.load(f)
            
            print("📋 Found automation log:")
            print(f"  Date range: {log_data.get('date_range', 'Unknown')}")
            print(f"  Total commits: {log_data.get('total_commits', 'Unknown')}")
            print(f"  Target file: {log_data.get('target_file', 'Unknown')}")
            print(f"  Created at: {log_data.get('created_at', 'Unknown')}")
            
            return log_data
        except Exception as e:
            print(f"Error loading automation log: {e}")
            return None
    
    def get_commit_count_to_remove(self, start_commit):
        """Get the number of commits to remove from start_commit to HEAD"""
        try:
            success, output = self.run_git_command(f"git rev-list --count {start_commit}..HEAD")
            if success:
                return int(output.strip())
            return 0
        except:
            return 0
    
    def reset_to_commit(self, commit_hash, hard_reset=False):
        """Reset repository to a specific commit"""
        reset_type = "--hard" if hard_reset else "--soft"
        success, output = self.run_git_command(f"git reset {reset_type} {commit_hash}")
        return success
    
    def remove_automation_commits_safe(self, log_data):
        """Safely remove automation commits using soft reset"""
        start_commit = log_data.get('start_commit')
        if not start_commit:
            print("❌ No start commit found in log data")
            return False
        
        # Count commits to be removed
        commits_to_remove = self.get_commit_count_to_remove(start_commit)
        print(f"📊 Commits to remove: {commits_to_remove}")
        
        if commits_to_remove == 0:
            print("✅ No commits to remove (already at starting point)")
            return True
        
        print(f"\n🔄 Removing {commits_to_remove} automated commits...")
        print(f"Resetting to commit: {start_commit}")
        
        # Perform soft reset to preserve working directory changes
        if self.reset_to_commit(start_commit, hard_reset=False):
            print("✅ Commits removed successfully (soft reset)")
            print("📝 Your working directory changes are preserved")
            return True
        else:
            print("❌ Failed to remove commits")
            return False
    
    def remove_automation_commits_hard(self, log_data):
        """Remove automation commits using hard reset (WARNING: loses changes)"""
        start_commit = log_data.get('start_commit')
        if not start_commit:
            print("❌ No start commit found in log data")
            return False
        
        # Count commits to be removed
        commits_to_remove = self.get_commit_count_to_remove(start_commit)
        print(f"📊 Commits to remove: {commits_to_remove}")
        
        if commits_to_remove == 0:
            print("✅ No commits to remove (already at starting point)")
            return True
        
        print(f"\n⚠️  HARD RESET: This will permanently delete {commits_to_remove} commits!")
        print(f"⚠️  All uncommitted changes will be lost!")
        confirm = input("Type 'DELETE' to confirm hard reset: ")
        
        if confirm != "DELETE":
            print("❌ Hard reset cancelled")
            return False
        
        print(f"🔄 Performing hard reset to commit: {start_commit}")
        
        # Perform hard reset
        if self.reset_to_commit(start_commit, hard_reset=True):
            print("✅ Hard reset completed successfully")
            print("⚠️  All automated commits and uncommitted changes have been removed")
            return True
        else:
            print("❌ Failed to perform hard reset")
            return False
    
    def clean_target_file(self, log_data):
        """Clean the target file that was modified during automation"""
        target_file = log_data.get('target_file')
        if not target_file:
            print("❌ No target file found in log data")
            return False
        
        file_path = os.path.join(self.repo_path, target_file)
        
        if not os.path.exists(file_path):
            print(f"❌ Target file not found: {target_file}")
            return False
        
        print(f"\n🧹 Cleaning target file: {target_file}")
        
        try:
            # Remove automation comments and restore original content
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Filter out automation comments
            original_lines = []
            for line in lines:
                # Skip lines that contain automation markers
                if not any(marker in line for marker in [
                    "# Automated commit", "// Automated commit", "<!-- Automated commit",
                    "# Auto-generated", "// Auto-generated", "<!-- Auto-generated"
                ]):
                    original_lines.append(line)
            
            # Write back the cleaned content
            with open(file_path, 'w') as f:
                f.writelines(original_lines)
            
            print(f"✅ File cleaned: {target_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error cleaning file {target_file}: {e}")
            return False
    
    def display_removal_options(self):
        """Display removal options to user"""
        print("\n🔧 Removal Options:")
        print("1. 🔄 Safe Removal (Soft Reset)")
        print("   - Removes automated commits")
        print("   - Preserves uncommitted changes")
        print("   - Recommended for most cases")
        print()
        print("2. ⚠️  Complete Removal (Hard Reset)")
        print("   - Removes automated commits")
        print("   - Deletes ALL uncommitted changes")
        print("   - Use only if you want to lose all changes")
        print()
        print("3. 🧹 File Cleaning + Soft Reset")
        print("   - Removes automated commits (soft reset)")
        print("   - Cleans automation comments from target file")
        print("   - Preserves other uncommitted changes")
        print()
        print("4. ❌ Cancel")
        print()
    
    def remove_automation_log(self):
        """Remove the automation log file"""
        try:
            if os.path.exists(self.commit_log_file):
                os.remove(self.commit_log_file)
                print(f"✅ Removed automation log: {os.path.basename(self.commit_log_file)}")
                return True
            return True
        except Exception as e:
            print(f"❌ Error removing automation log: {e}")
            return False
            return False
        
        # Count commits to be removed
        commits_to_remove = self.get_commit_count_to_remove(start_commit)
        print(f"📊 Commits to remove: {commits_to_remove}")
        
        if commits_to_remove == 0:
            print("✅ No commits to remove (already at starting point)")
            return True
        
        print(f"\n🔄 Removing {commits_to_remove} automated commits...")
        print(f"Resetting to commit: {start_commit}")
        print("⚠️  WARNING: This will permanently delete all changes!")
        
        # Perform hard reset
        if self.reset_to_commit(start_commit, hard_reset=True):
            print("✅ Commits removed successfully (hard reset)")
            print("🗑️  All automated changes have been permanently deleted")
            return True
        else:
            print("❌ Failed to remove commits")
            return False
    
    def clean_target_file(self, target_file):
        """Remove automation comments from target file"""
        if not target_file:
            return False
        
        file_path = os.path.join(self.repo_path, target_file)
        if not os.path.exists(file_path):
            print(f"Target file not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Remove lines that look like automation comments
            cleaned_lines = []
            for line in lines:
                line_stripped = line.strip()
                # Check for various comment patterns
                is_automation_comment = any([
                    'Auto-generated comment' in line_stripped,
                    'Modified on 20' in line_stripped,
                    'Commit #' in line_stripped and 'Auto-generated' in line_stripped,
                    line_stripped.endswith('refactor') and ('Update:' in line_stripped),
                    line_stripped.endswith('optimize') and ('Update:' in line_stripped),
                    line_stripped.endswith('cleanup') and ('Update:' in line_stripped),
                    line_stripped.endswith('enhance') and ('Update:' in line_stripped),
                    'Version:' in line_stripped and line_stripped.count('.') == 1,
                    'Build:' in line_stripped and any(char.isdigit() for char in line_stripped[-4:]),
                    'Feature:' in line_stripped and any(word in line_stripped for word in ['improvement', 'bugfix', 'enhancement', 'maintenance']),
                    'Automation commit' in line_stripped and any(char.isdigit() for char in line_stripped)
                ])
                
                if not is_automation_comment:
                    cleaned_lines.append(line)
            
            # Write cleaned content back
            with open(file_path, 'w') as f:
                f.writelines(cleaned_lines)
            
            print(f"🧹 Cleaned automation comments from {target_file}")
            return True
        except Exception as e:
            print(f"Error cleaning target file: {e}")
            return False
    
    def remove_log_file(self):
        """Remove the automation log file"""
        try:
            if os.path.exists(self.commit_log_file):
                os.remove(self.commit_log_file)
                print(f"🗑️  Removed automation log file")
            return True
        except Exception as e:
            print(f"Error removing log file: {e}")
            return False
    
    def interactive_removal(self):
        """Interactive commit removal process"""
        print("🔍 Checking repository status...")
        
        if not self.run_git_command("git status")[0]:
            print("❌ Not in a git repository or git not configured")
            return False
        
        # Load automation log
        log_data = self.load_automation_log()
        if not log_data:
            return False
        
        print(f"\n🎯 Removal Options:")
        print("1. Safe removal (soft reset - preserves working directory)")
        print("2. Complete removal (hard reset - removes all changes)")
        print("3. Clean file only (remove automation comments)")
        print("4. Cancel")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            print("\n🛡️  SAFE REMOVAL MODE")
            print("This will remove commits but preserve your working directory changes.")
            confirm = input("Continue? (y/N): ")
            if confirm.lower() == 'y':
                success = self.remove_automation_commits_safe(log_data)
                if success:
                    # Also clean the file
                    self.clean_target_file(log_data)
                    self.remove_automation_log()
                return success
                
        elif choice == "2":
            print("\n⚠️  COMPLETE REMOVAL MODE")
            print("🚨 WARNING: This will permanently delete ALL changes!")
            print("🚨 This includes any work you may have done after automation!")
            print("🚨 Make sure you have a backup!")
            confirm = input("Continue? (y/N): ")
            if confirm.lower() == 'y':
                success = self.remove_automation_commits_hard(log_data)
                if success:
                    self.remove_automation_log()
                return success
                
        elif choice == "3":
            print("\n🧹 FILE CLEANING MODE")
            print("This will only remove automation comments from the target file.")
            confirm = input("Continue? (y/N): ")
            if confirm.lower() == 'y':
                success = self.clean_target_file(log_data)
                if success:
                    print("✅ File cleaned successfully")
                return success
                
        elif choice == "4":
            print("❌ Operation cancelled")
            return False
            
        else:
            print("❌ Invalid choice")
            return False
            
        return False
            
            confirm1 = input("\nAre you sure you want to proceed? (y/N): ")
            if confirm1.lower() != 'y':
                print("Cancelled.")
                return False
                
            confirm2 = input("Type 'DELETE ALL' to confirm complete removal: ")
            if confirm2 != 'DELETE ALL':
                print("Cancelled for safety.")
                return False
                
            success = self.remove_automation_commits_hard(log_data)
            if success:
                self.remove_log_file()
            return success
            
        elif choice == "3":
            print("\n🧹 FILE CLEANING MODE")
            print("This will only remove automation comments from the target file.")
            confirm = input("Continue? (y/N): ")
            if confirm.lower() == 'y':
                return self.clean_target_file(log_data.get('target_file'))
                
        elif choice == "4":
            print("Cancelled.")
            return False
        else:
            print("Invalid choice.")
            return False
    
    def show_commit_history(self, limit=10):
        """Show recent commit history"""
        print(f"\n📝 Recent commit history (last {limit} commits):")
        success, output = self.run_git_command(f"git log --oneline -n {limit}")
        if success:
            print(output)
        else:
            print("Could not retrieve commit history")

def get_repo_info():
    """Get repository path and check if it's a git repository"""
    repo_path = os.getcwd()
    
    # Check if we're in a git repository
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("❌ Error: Current directory is not a git repository!")
        print("Please run this script from inside a git repository.")
        return None
    
    return repo_path

def main():
    print("🗑️  GitHub Commit Remover")
    print("=" * 50)
    
    # Get repository information
    repo_path = get_repo_info()
    if repo_path is None:
        return
    
    print(f"Repository: {repo_path}")
    print("=" * 50)
    
    remover = GitCommitRemover(repo_path)
    
    # Show current status
    remover.show_commit_history()
    
    print("\nThis tool will help you remove automated commits created by create_commits.py")
    print("⚠️  Always make sure you have a backup before removing commits!")
    
    success = remover.interactive_removal()
    
    if success:
        print("\n🎉 COMMIT REMOVAL COMPLETED!")
        print("🔄 Your repository has been cleaned up.")
        
        # Ask about pushing changes
        push_response = input("\n🚀 Do you want to force push to remote? (y/N): ")
        if push_response.lower() == 'y':
            print("⚠️  Force pushing to remote repository...")
            print("🚨 This will rewrite remote history!")
            
            final_confirm = input("Type 'FORCE PUSH' to confirm: ")
            if final_confirm == 'FORCE PUSH':
                if remover.run_git_command("git push --force origin main")[0]:
                    print("✅ Force push completed!")
                elif remover.run_git_command("git push --force origin master")[0]:
                    print("✅ Force push completed!")
                else:
                    print("❌ Force push failed. Try manually:")
                    print("  git push --force origin main")
                    print("  git push --force origin master")
            else:
                print("Force push cancelled.")
        
        print("\n💡 Note: If you pushed to remote, it may take a few minutes for GitHub to update.")
    else:
        print("\n❌ Commit removal was not completed.")

if __name__ == "__main__":
    main()
