#!/bin/bash

# 🔒 Secure Solana Vanity Wallet Bot Starter
echo "🔒 Starting Secure Solana Vanity Wallet Bot..."
echo "================================================"

# Security checks
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    exit 1
fi

# Set secure permissions
chmod 600 .env 2>/dev/null

# Check token
if ! grep -q "TELEGRAM_TOKEN=" .env; then
    echo "❌ Error: TELEGRAM_TOKEN not found"
    exit 1
fi

# Load environment
export $(cat .env | grep -v '^#' | xargs)

echo "✅ Environment configured"
echo "🌐 Network: ${SOLANA_NETWORK:-devnet} (Safe Mode)"
echo "📏 Max Prefix: ${MAX_PREFIX_LENGTH:-6}"
echo "🛡️ Security: No logging of sensitive data"
echo ""

# Create secure log directory
mkdir -p logs
chmod 700 logs 2>/dev/null

# Start bot with security
echo "🤖 Starting secure bot..."
python3 bot.py
