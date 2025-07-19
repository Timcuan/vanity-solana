#!/bin/bash

echo "🚀 Starting Solana Vanity Generator Mini App..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please run deploy_mini_app.py first"
    exit 1
fi

# Check if TELEGRAM_TOKEN is set
if ! grep -q "TELEGRAM_TOKEN=your_telegram_bot_token_here" .env; then
    echo "✅ TELEGRAM_TOKEN is configured"
else
    echo "⚠️  Please configure TELEGRAM_TOKEN in .env file"
    echo "   Get a bot token from @BotFather on Telegram"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip3 install -r requirements.txt

# Start the mini app
echo "🚀 Starting mini app..."
python3 telegram_mini_app.py
