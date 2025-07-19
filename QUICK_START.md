# 🚀 Quick Start Guide - Solana Vanity Generator Mini App

## 📋 Overview

This is a modern Telegram Mini App that generates Solana vanity addresses with custom prefixes through a beautiful web interface.

## ⚡ Quick Start (5 minutes)

### 1. Test the App (No Setup Required)

```bash
# Run the demo to see it in action
python3 demo.py

# Start the test web server
./run_test_server.sh
```

Then open your browser to `http://localhost:8080`

### 2. Full Setup (With Telegram Bot)

```bash
# Run deployment script
python3 deploy_mini_app.py

# Configure your bot token in .env file
# Get token from @BotFather on Telegram

# Start the full mini app
./run_mini_app.sh
```

## 🎯 What You Get

### Features
- ✅ **Modern Web Interface**: Beautiful, responsive design
- ✅ **Real-time Generation**: Live progress tracking
- ✅ **Fast Generation**: Optimized for short prefixes
- ✅ **Real Solana Keypairs**: Actual public and private keys
- ✅ **Dark Mode Support**: Adapts to Telegram theme
- ✅ **One-click Copy**: Easy key copying
- ✅ **Input Validation**: Prevents invalid prefixes

### Files Created
- `telegram_mini_app.py` - Main mini app with bot and web server
- `vanity_generator.py` - Core Solana address generation
- `config.py` - Configuration and messages
- `demo.py` - Demo script for testing
- `test_web_server.py` - Test web server (no bot required)
- `run_mini_app.sh` - Script to run full mini app
- `run_test_server.sh` - Script to run test server
- `status.sh` - Check system status

## 🧪 Testing

### Demo Mode
```bash
python3 demo.py
```
Shows prefix validation, time estimation, and actual generation.

### Test Web Server
```bash
./run_test_server.sh
```
Opens web interface at `http://localhost:8080` without requiring bot token.

### Status Check
```bash
./status.sh
```
Shows system status, dependencies, and configuration.

## 🔧 Configuration

### Environment Variables (.env)
```env
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
SOLANA_NETWORK=devnet
WEB_SERVER_HOST=localhost
WEB_SERVER_PORT=8080
WEB_SERVER_URL=http://localhost:8080
MAX_ATTEMPTS=1000000
MAX_PREFIX_LENGTH=8
```

### Bot Setup
1. Message @BotFather on Telegram
2. Send `/newbot` command
3. Follow instructions to create bot
4. Copy the token to `.env` file
5. Send `/newapp` to set up mini app
6. Set Web App URL to your server URL

## 📊 Performance

| Prefix Length | Estimated Time | Success Rate |
|---------------|----------------|--------------|
| 1-2 chars     | ~1-60 seconds  | Very High    |
| 3-4 chars     | ~1-10 minutes  | High         |
| 5 chars       | ~10-60 minutes | Medium       |
| 6+ chars      | Hours+         | Low          |

## 🔒 Security

- Generated private keys are real and can hold funds
- Never share private keys
- Store keys securely offline
- Use hardware wallets for large amounts

## 🐛 Troubleshooting

### Common Issues
1. **"Module not found"** - Run `pip3 install -r requirements.txt`
2. **"TELEGRAM_TOKEN not found"** - Configure token in `.env` file
3. **"Server not starting"** - Check port 8080 is available
4. **"Generation slow"** - Try shorter prefixes

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📱 Usage

### Web Interface
1. Enter desired prefix (1-8 characters)
2. Click "Generate Vanity Address"
3. Wait for generation to complete
4. Copy public and private keys

### Telegram Bot
1. Send `/start` to bot
2. Click "Open Vanity Generator"
3. Use the web interface
4. Copy generated keys

## 🎉 Success!

You now have a fully functional Solana Vanity Generator Mini App!

- **Test Mode**: `./run_test_server.sh`
- **Full Mode**: `./run_mini_app.sh`
- **Demo**: `python3 demo.py`
- **Status**: `./status.sh`

---

**Made with ❤️ for the Solana community**
