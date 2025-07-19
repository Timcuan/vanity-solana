#!/usr/bin/env python3
"""
Security Check Script for Solana Vanity Wallet Bot
"""

import os
import re
from dotenv import load_dotenv

def check_log_files():
    """Check log files for sensitive data"""
    print("🔍 Checking log files for sensitive data...")
    
    log_files = ['bot.log', 'bot_secure.log', 'debug.log']
    sensitive_patterns = [
        r'[1-9A-HJ-NP-Za-km-z]{87,88}',  # Private keys
        r'[1-9A-HJ-NP-Za-km-z]{32,44}',  # Public keys
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"📄 Checking {log_file}...")
            try:
                with open(log_file, 'r') as f:
                    content = f.read()
                    
                for pattern in sensitive_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        print(f"❌ WARNING: Found {len(matches)} potential sensitive data")
                    else:
                        print(f"✅ No sensitive data found")
                        
            except Exception as e:
                print(f"⚠️ Error reading {log_file}: {e}")
        else:
            print(f"ℹ️ {log_file} not found")

def check_environment():
    """Check environment configuration"""
    print("\n🔍 Checking environment configuration...")
    
    load_dotenv()
    
    # Check network setting
    network = os.getenv('SOLANA_NETWORK', 'devnet')
    if network == 'devnet':
        print("✅ Using devnet (safe for testing)")
    elif network == 'mainnet-beta':
        print("⚠️ WARNING: Using mainnet-beta (real addresses)")
    else:
        print(f"ℹ️ Using {network}")
    
    # Check security settings
    max_attempts = int(os.getenv('MAX_ATTEMPTS', '500000'))
    max_prefix = int(os.getenv('MAX_PREFIX_LENGTH', '6'))
    rate_limit = int(os.getenv('RATE_LIMIT_PER_USER', '10'))
    
    print(f"✅ Max attempts: {max_attempts}")
    print(f"✅ Max prefix length: {max_prefix}")
    print(f"✅ Rate limit: {rate_limit}/hour")

def main():
    """Run security check"""
    print("🔒 Security Check for Solana Vanity Wallet Bot")
    print("=" * 50)
    
    check_log_files()
    check_environment()
    
    print("\n" + "=" * 50)
    print("📋 Security Recommendations:")
    print("✅ Use devnet for testing")
    print("✅ Set file permissions to 600")
    print("✅ Monitor log files regularly")
    print("✅ Never commit .env files")
    print("✅ Use rate limiting")

if __name__ == "__main__":
    main()
