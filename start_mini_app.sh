#!/bin/bash
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
