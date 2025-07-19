# Solana Vanity Generator Mini App

A modern Telegram Mini App that generates Solana vanity addresses with custom prefixes through a beautiful web interface.

## 🌟 Features

- **📱 Modern Web Interface**: Beautiful, responsive design optimized for mobile
- **🚀 Real-time Generation**: Live progress tracking with attempt counters
- **⚡ Fast Generation**: Optimized for short prefixes (2-4 characters)
- **🔒 Real Solana Keypairs**: Generates actual Solana public and private keys
- **📊 Progress Tracking**: Real-time updates during generation
- **🎨 Dark Mode Support**: Automatically adapts to Telegram's theme
- **📋 One-click Copy**: Easy copying of generated keys
- **🛡️ Input Validation**: Prevents invalid prefixes and provides helpful feedback
- **🌐 Cross-platform**: Works on all devices through Telegram

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Telegram account
- Telegram bot token (from @BotFather)

### 2. Automated Setup

```bash
# Run the deployment script
python3 deploy_mini_app.py
```

This will:
- ✅ Check Python version
- 📦 Install dependencies
- 📝 Create .env file
- 🔧 Create startup scripts

### 3. Configure Bot

1. **Get Bot Token**:
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` command
   - Follow instructions to create your bot
   - Copy the token provided

2. **Edit .env file**:
   ```env
   TELEGRAM_TOKEN=your_actual_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   SOLANA_NETWORK=devnet
   WEB_SERVER_URL=https://your-domain.com
   ```

3. **Configure BotFather**:
   - Send `/newapp` to @BotFather
   - Set the Web App URL to your server URL
   - Configure bot commands:
     ```
     /start - Open mini app
     /help - Show help
     /status - Check status
     ```

### 4. Start the Mini App

**Option 1: Direct Python**
```bash
python3 telegram_mini_app.py
```

**Option 2: Startup Script**
```bash
./start_mini_app.sh
```

## 🏗️ Architecture

### Components

1. **Telegram Bot** (`telegram_mini_app.py`)
   - Handles bot commands and interactions
   - Provides mini app launch button
   - Manages user sessions

2. **Web Server** (aiohttp)
   - Serves the mini app HTML interface
   - Provides REST API for generation
   - Handles real-time status updates

3. **Vanity Generator** (`vanity_generator.py`)
   - Core Solana address generation logic
   - Prefix validation and estimation
   - Keypair formatting

4. **Mini App Interface** (HTML/CSS/JS)
   - Modern, responsive web interface
   - Real-time progress tracking
   - Telegram Web App integration

### API Endpoints

- `GET /` - Mini app HTML interface
- `POST /api/generate` - Start vanity address generation
- `GET /api/status/{task_id}` - Check generation status

## 🎨 User Interface

### Features

- **Responsive Design**: Works on all screen sizes
- **Dark Mode**: Automatically adapts to Telegram theme
- **Progress Bar**: Visual feedback during generation
- **Copy Buttons**: One-click copying of keys
- **Error Handling**: Clear error messages and validation
- **Loading States**: Smooth transitions and feedback

## 🔧 Configuration

### Environment Variables

```env
# Telegram Bot
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Solana Network
SOLANA_NETWORK=devnet  # devnet, testnet, mainnet-beta

# Web Server
WEB_SERVER_HOST=localhost
WEB_SERVER_PORT=8080
WEB_SERVER_URL=https://your-domain.com

# Generator Settings
MAX_ATTEMPTS=1000000
MAX_PREFIX_LENGTH=8
```

## 📊 Performance

### Generation Times

| Prefix Length | Estimated Time | Success Rate |
|---------------|----------------|--------------|
| 1 character   | ~1-10 seconds  | Very High    |
| 2 characters  | ~10-60 seconds | High         |
| 3 characters  | ~1-10 minutes  | Medium       |
| 4 characters  | ~10-60 minutes | Medium       |
| 5 characters  | ~1-10 hours    | Low          |
| 6+ characters | Hours+         | Very Low     |

## 🔒 Security Considerations

### Bot Security
- Keep `TELEGRAM_TOKEN` secure and private
- Use HTTPS in production
- Regularly update dependencies
- Monitor bot usage and logs

### Key Security
- Generated private keys are real and can hold funds
- Never share private keys
- Store keys securely offline
- Consider hardware wallets for large amounts

## 🐛 Troubleshooting

### Common Issues

1. **"TELEGRAM_TOKEN not found"**
   - Check .env file exists and has correct token
   - Verify token is valid with @BotFather

2. **"Web App not loading"**
   - Check web server is running
   - Verify WEB_SERVER_URL is correct
   - Check firewall and port settings

3. **"Generation taking too long"**
   - Try shorter prefix
   - Check server resources
   - Verify internet connection

4. **"Copy to clipboard not working"**
   - This is normal in some browsers
   - Manual copy is always available

### Debug Mode

Enable debug logging:

```python
# In telegram_mini_app.py
logging.basicConfig(level=logging.DEBUG)
```

## 📄 License

This project is open source. Use responsibly and at your own risk.

## ⚠️ Disclaimer

This mini app generates real Solana keypairs that can hold funds. Users are responsible for:
- Securing their private keys
- Any transactions made with generated addresses
- Compliance with local regulations

The developers are not responsible for any loss of funds or security issues.

## 🆘 Support

For support:
- Check this README
- Review troubleshooting section
- Check logs for errors
- Open an issue on GitHub

---

**Made with ❤️ for the Solana community**
