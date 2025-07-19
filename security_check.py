#!/usr/bin/env python3
"""
Security Check Script for Solana Vanity Wallet Bot
This script checks for potential security issues in the codebase.
"""

import os
import re
import sys
from pathlib import Path

def check_file_for_sensitive_data(file_path: str) -> list:
    """Check a file for potential security issues."""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for actual private key exposure in logs/prints
        dangerous_patterns = [
            # Private keys in print statements
            (r'print.*secret_key\.hex\(\)', 'Private key printed to console'),
            (r'print.*keypair\.secret', 'Private key printed to console'),
            (r'print.*private_key', 'Private key printed to console'),
            
            # Private keys in logging
            (r'logger.*secret_key', 'Private key logged'),
            (r'logger.*keypair\.secret', 'Private key logged'),
            (r'logger.*private_key', 'Private key logged'),
            
            # Personal info in logs
            (r'logger.*first_name', 'Personal info logged'),
            (r'logger.*username', 'Personal info logged'),
            (r'logger.*last_name', 'Personal info logged'),
            
            # Hardcoded tokens
            (r'TELEGRAM_TOKEN\s*=\s*["\'][0-9]{8,}:[A-Za-z0-9_-]{35}["\']', 'Hardcoded Telegram token'),
        ]
        
        line_number = 0
        for line in content.split('\n'):
            line_number += 1
            
            # Skip comments and docstrings
            stripped_line = line.strip()
            if stripped_line.startswith('#') or stripped_line.startswith('"""') or stripped_line.startswith("'''"):
                continue
                
            # Check each dangerous pattern
            for pattern, description in dangerous_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(f"Line {line_number}: {description}")
                    
    except Exception as e:
        issues.append(f"Error reading file: {e}")
    
    return issues

def check_env_file():
    """Check if .env file exists and contains sensitive data."""
    issues = []
    
    if os.path.exists('.env'):
        issues.append("⚠️  .env file exists - make sure it's not committed to version control")
        
        # Check if .env is in .gitignore
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                gitignore_content = f.read()
                if '.env' not in gitignore_content:
                    issues.append("❌ .env file is not in .gitignore")
                else:
                    issues.append("✅ .env file is properly ignored")
    else:
        issues.append("ℹ️  .env file not found - this is normal for fresh installations")
    
    return issues

def check_security_features():
    """Check for implemented security features."""
    features = []
    
    # Check for secure file handling
    if os.path.exists('bot.py'):
        with open('bot.py', 'r') as f:
            content = f.read()
            if 'os.unlink(' in content:
                features.append("✅ Temporary files are deleted after use")
            if 'send_wallet_files' in content:
                features.append("✅ Wallet files sent via DM only")
            if 'format_keypair_info_secure' in content:
                features.append("✅ Secure keypair formatting (no private keys in chat)")
    
    # Check for secure logging
    if os.path.exists('vanity_generator.py'):
        with open('vanity_generator.py', 'r') as f:
            content = f.read()
            if 'logger.info' in content and 'print(' not in content:
                features.append("✅ Secure logging (no print statements)")
    
    return features

def main():
    """Main security check function."""
    print("🔒 Security Check for Solana Vanity Wallet Bot")
    print("=" * 50)
    
    # Files to check
    files_to_check = [
        'bot.py',
        'vanity_generator.py',
        'config.py',
        'test_bot.py',
        'requirements.txt',
    ]
    
    all_issues = []
    
    # Check each file
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"\n🔍 Checking {file_path}...")
            issues = check_file_for_sensitive_data(file_path)
            
            if issues:
                print(f"❌ Found {len(issues)} potential security issues:")
                for issue in issues:
                    print(f"   {issue}")
                all_issues.extend(issues)
            else:
                print(f"✅ No security issues found")
        else:
            print(f"⚠️  {file_path} not found")
    
    # Check .env file
    print(f"\n🔍 Checking .env file...")
    env_issues = check_env_file()
    for issue in env_issues:
        print(f"   {issue}")
    
    # Check .gitignore
    print(f"\n🔍 Checking .gitignore...")
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' in gitignore_content:
                print("✅ .env is properly ignored")
            else:
                print("❌ .env is not in .gitignore")
                all_issues.append(".env file not in .gitignore")
    else:
        print("❌ .gitignore file not found")
        all_issues.append("No .gitignore file")
    
    # Check security features
    print(f"\n🔍 Checking security features...")
    features = check_security_features()
    for feature in features:
        print(f"   {feature}")
    
    # Summary
    print(f"\n" + "=" * 50)
    print("📊 Security Check Summary")
    print("=" * 50)
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} potential security issues:")
        for issue in all_issues:
            print(f"   • {issue}")
        print(f"\n🚨 Please review and fix these issues before deployment!")
        return False
    else:
        print(f"✅ No security issues found!")
        print(f"🔒 Bot appears to be secure for deployment")
        print(f"\nImplemented security features:")
        for feature in features:
            print(f"   • {feature}")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)