#!/bin/bash

echo "📊 Solana Vanity Generator Mini App Status"
echo "=========================================="

# Check Python version
echo "🐍 Python Version:"
python3 --version

# Check dependencies
echo -e "\n📦 Dependencies:"
if pip3 list | grep -q "python-telegram-bot"; then
    echo "✅ python-telegram-bot: Installed"
else
    echo "❌ python-telegram-bot: Not installed"
fi

if pip3 list | grep -q "solders"; then
    echo "✅ solders: Installed"
else
    echo "❌ solders: Not installed"
fi

if pip3 list | grep -q "aiohttp"; then
    echo "✅ aiohttp: Installed"
else
    echo "❌ aiohttp: Not installed"
fi

# Check configuration
echo -e "\n🔧 Configuration:"
if [ -f .env ]; then
    echo "✅ .env file: Exists"
    if grep -q "TELEGRAM_TOKEN=your_telegram_bot_token_here" .env; then
        echo "⚠️  TELEGRAM_TOKEN: Not configured"
    else
        echo "✅ TELEGRAM_TOKEN: Configured"
    fi
else
    echo "❌ .env file: Missing"
fi

# Check files
echo -e "\n�� Files:"
files=("telegram_mini_app.py" "vanity_generator.py" "config.py" "requirements.txt")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file: Exists"
    else
        echo "❌ $file: Missing"
    fi
done

# Check if server is running
echo -e "\n🌐 Web Server:"
if lsof -i :8080 > /dev/null 2>&1; then
    echo "✅ Server: Running on port 8080"
else
    echo "❌ Server: Not running"
fi

echo -e "\n🎯 Ready to use!"
echo "   • Test server: ./run_test_server.sh"
echo "   • Full mini app: ./run_mini_app.sh"
echo "   • Demo: python3 demo.py"
