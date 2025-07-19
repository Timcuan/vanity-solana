#!/bin/bash

# Solana Vanity Wallet Telegram Bot Deployment Script
echo "🚀 Deploying Solana Vanity Wallet Telegram Bot..."
echo "================================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your Telegram bot token"
    exit 1
fi

# Check if TELEGRAM_TOKEN is set and not placeholder
if ! grep -q "TELEGRAM_TOKEN=" .env; then
    echo "❌ Error: TELEGRAM_TOKEN not found in .env file"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if token is valid (not placeholder)
if [ "$TELEGRAM_TOKEN" = "your_telegram_bot_token_here" ] || [ -z "$TELEGRAM_TOKEN" ]; then
    echo "❌ Error: Please set a valid TELEGRAM_TOKEN in .env file"
    exit 1
fi

echo "✅ Environment configured"
echo "🌐 Network: ${SOLANA_NETWORK:-mainnet-beta}"
echo "📏 Max Prefix Length: ${MAX_PREFIX_LENGTH:-8}"
echo ""

# Check dependencies
echo "🔍 Checking dependencies..."
python3 -c "import telegram, solders, base58, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: Required packages not installed"
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt
fi

echo "✅ Dependencies check passed"
echo ""

# Start the bot
echo "🤖 Starting Solana Vanity Wallet Telegram Bot..."
echo "�� Bot will be available on Telegram"
echo "🛑 Press Ctrl+C to stop"
echo "================================================"

python3 bot.py
