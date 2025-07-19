#!/bin/bash

# Solana Vanity Wallet Telegram Bot Startup Script

echo "🚀 Starting Solana Vanity Wallet Telegram Bot..."
echo "================================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your bot token."
    echo "Run: cp .env.example .env"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import telegram, solana, base58" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Start the bot
echo "🤖 Starting bot..."
python3 bot.py