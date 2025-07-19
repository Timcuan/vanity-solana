#!/usr/bin/env python3
"""
Deployment script for Solana Vanity Generator Mini App
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def setup_environment():
    """Setup environment variables"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# Telegram Bot Configuration
TELEGRAM_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Solana Configuration
SOLANA_NETWORK=devnet

# Web Server Configuration
WEB_SERVER_HOST=localhost
WEB_SERVER_PORT=8080
WEB_SERVER_URL=http://localhost:8080

# Vanity Generator Configuration
MAX_ATTEMPTS=1000000
MAX_PREFIX_LENGTH=8
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")

def create_static_directory():
    """Create static directory for assets"""
    static_dir = Path("static")
    if not static_dir.exists():
        static_dir.mkdir()
        print("✅ Static directory created")
    else:
        print("✅ Static directory already exists")

def create_startup_script():
    """Create startup script"""
    script_content = """#!/bin/bash
# Startup script for Solana Vanity Generator Mini App

echo "🚀 Starting Solana Vanity Generator Mini App..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please run deploy_mini_app.py first"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip3 install -r requirements.txt

# Start the mini app
echo "🚀 Starting mini app..."
python3 telegram_mini_app.py
"""
    
    with open("start_mini_app.sh", "w") as f:
        f.write(script_content)
    
    # Make executable
    os.chmod("start_mini_app.sh", 0o755)
    print("✅ Startup script created (start_mini_app.sh)")

def print_setup_instructions():
    """Print setup instructions"""
    instructions = """
🎉 **Setup Complete!**

**Next Steps:**

1. **Configure Telegram Bot:**
   - Get a bot token from @BotFather on Telegram
   - Edit .env file and add your TELEGRAM_TOKEN

2. **Configure Web Server URL:**
   - For local development: Keep WEB_SERVER_URL=http://localhost:8080
   - For production: Update WEB_SERVER_URL to your domain

3. **Start the Mini App:**
   - Local: python3 telegram_mini_app.py
   - Script: ./start_mini_app.sh

4. **Configure BotFather:**
   - Send /newapp to @BotFather
   - Set the Web App URL to your server URL
   - Configure bot commands:
     /start - Open mini app
     /help - Show help
     /status - Check status

**Security Notes:**
- Keep TELEGRAM_TOKEN secure
- Use HTTPS in production
- Regularly update dependencies
- Monitor server logs

**Support:**
- Check logs for errors
- Verify .env configuration
- Test bot commands
- Monitor web server status
"""
    print(instructions)

def main():
    """Main deployment function"""
    print("🚀 Solana Vanity Generator Mini App Deployment")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    setup_environment()
    
    # Create static directory
    create_static_directory()
    
    # Create startup script
    create_startup_script()
    
    print("\n" + "=" * 50)
    print_setup_instructions()

if __name__ == "__main__":
    main()
