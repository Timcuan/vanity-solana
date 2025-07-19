# Solana Vanity Generator - Telegram Mini App

A fully functional Telegram Mini App that generates Solana vanity addresses with custom prefixes. This app runs directly within Telegram and provides a seamless user experience for generating custom Solana addresses.

## 🚀 Features

### Core Functionality
- **Real Solana Address Generation** - Generates actual Solana keypairs with custom prefixes
- **Multiple Network Support** - Devnet, Testnet, and Mainnet
- **Progress Tracking** - Real-time generation progress with attempts and rate
- **History Management** - Local storage of generation history
- **Secure Keypair Download** - Download generated keypairs as JSON files

### Telegram Integration
- **Native Telegram UI** - Follows Telegram's design guidelines
- **Theme Support** - Automatically adapts to light/dark themes
- **Responsive Design** - Works perfectly on mobile and desktop
- **Telegram Web App API** - Full integration with Telegram's features
- **Main Button & Back Button** - Proper navigation controls

### User Experience
- **Modern Interface** - Clean, intuitive design
- **Real-time Feedback** - Toast notifications and progress updates
- **Input Validation** - Smart validation with helpful error messages
- **Copy to Clipboard** - Easy address copying
- **Network Selection** - Visual network indicators

## 📱 Screenshots

The app includes several screens:
1. **Welcome Screen** - Introduction and feature overview
2. **Generator Screen** - Input form with network selection
3. **Progress Screen** - Real-time generation progress
4. **Results Screen** - Generated address with download options
5. **History Screen** - Past generation records

## 🛠️ Technical Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables and responsive design
- **Vanilla JavaScript** - No frameworks, optimized for Telegram Web App
- **Telegram Web App API** - Native Telegram integration

### Backend
- **Node.js** - Server runtime
- **Express.js** - Web framework
- **@solana/web3.js** - Solana blockchain integration
- **CORS** - Cross-origin resource sharing

### Key Technologies
- **Web Workers** - Background processing (planned)
- **Local Storage** - Client-side data persistence
- **Fetch API** - Modern HTTP requests
- **Blob API** - File downloads

## 🚀 Quick Start

### 1. Prerequisites
- Node.js 16+ 
- npm or yarn
- A Telegram bot token (from @BotFather)

### 2. Installation
```bash
# Clone the repository
git clone <repository-url>
cd solana-vanity-telegram

# Install dependencies
npm install

# Install additional server dependencies
npm install express cors
```

### 3. Configuration
```bash
# Copy environment file
cp .env.example .env

# Edit .env file with your bot token
TELEGRAM_TOKEN=your_bot_token_here
PORT=3000
```

### 4. Running the App
```bash
# Start the server
npm run server

# Or for development with auto-restart
npm run dev-server
```

### 5. Setting up Telegram Bot
1. Message @BotFather on Telegram
2. Create a new bot with `/newbot`
3. Get your bot token
4. Set up the menu button:
   ```
   /setmenubutton
   ```
   Choose your bot and set:
   - Type: `web_app`
   - Text: `Generate Address`
   - URL: `https://your-domain.com`

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Serve the Mini App
- `GET /api/health` - Health check
- `POST /api/generate` - Generate vanity address (synchronous)
- `POST /api/generate/start` - Start generation (asynchronous)
- `GET /api/generate/:id/status` - Get generation progress
- `POST /api/generate/:id/stop` - Stop generation

### Request Examples
```javascript
// Start generation
const response = await fetch('/api/generate/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        prefix: 'SOL',
        network: 'devnet',
        maxAttempts: 1000000
    })
});

// Check progress
const status = await fetch(`/api/generate/${generationId}/status`);
```

## 🎨 Customization

### Styling
The app uses CSS variables for easy theming:
```css
:root {
    --primary-color: #2481cc;
    --tg-theme-bg-color: #ffffff;
    --tg-theme-text-color: #000000;
    /* ... more variables */
}
```

### Configuration
Edit `telegram-config.json` to customize:
- App name and description
- Supported networks
- Maximum prefix length
- Security settings

## 🔒 Security Features

### Data Protection
- **No Server Logging** - Private keys never logged
- **Secure Delivery** - Keys only sent to user
- **HTTPS Required** - All connections encrypted
- **Input Validation** - Strict validation on all inputs

### Best Practices
- Private keys generated client-side when possible
- No persistent storage of sensitive data
- Regular cleanup of old generation sessions
- Rate limiting on API endpoints

## 📊 Performance

### Generation Speed
- **2-3 characters**: 1-60 seconds
- **4 characters**: 1-10 minutes  
- **5 characters**: 10-60 minutes
- **6+ characters**: Hours or more

### Optimization
- Batch processing for faster generation
- Efficient Solana keypair generation
- Minimal API calls
- Optimized UI updates

## 🧪 Testing

### Manual Testing
```bash
# Start the server
npm run server

# Open in browser
open http://localhost:3000

# Test in Telegram
# 1. Set up bot with menu button
# 2. Open bot in Telegram
# 3. Click menu button to launch Mini App
```

### API Testing
```bash
# Health check
curl http://localhost:3000/api/health

# Generate address
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prefix":"SOL","network":"devnet"}'
```

## 🚀 Deployment

### Local Development
```bash
npm run dev-server
```

### Production Deployment
1. **Deploy to hosting service** (Vercel, Netlify, Heroku)
2. **Set environment variables**
3. **Configure HTTPS**
4. **Update bot web app URL**

### Environment Variables
```bash
TELEGRAM_TOKEN=your_bot_token
PORT=3000
NODE_ENV=production
```

## 📱 Telegram Mini App Guidelines

### Compliance
- ✅ Follows Telegram's design guidelines
- ✅ Uses Telegram Web App API properly
- ✅ Implements proper navigation
- ✅ Handles theme changes
- ✅ Responsive design

### Best Practices
- Fast loading times
- Minimal external dependencies
- Proper error handling
- User-friendly interface
- Secure data handling

## 🔧 Troubleshooting

### Common Issues

**1. Bot not responding**
- Check bot token in .env
- Verify server is running
- Check Telegram bot settings

**2. Generation not working**
- Ensure @solana/web3.js is installed
- Check network connectivity
- Verify API endpoints

**3. UI not loading**
- Check file paths
- Verify static file serving
- Check browser console for errors

**4. Telegram integration issues**
- Verify web app URL in bot settings
- Check HTTPS requirement
- Ensure proper CORS configuration

### Debug Mode
```javascript
// Enable debug logging
localStorage.setItem('debug', 'true');
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Use responsibly and at your own risk.

## ⚠️ Disclaimer

This app generates real Solana keypairs. Users are responsible for:
- Securing their private keys
- Using appropriate networks (devnet for testing)
- Understanding Solana address generation
- Following security best practices

## 🆘 Support

For support:
- Check the troubleshooting section
- Review Telegram Mini App documentation
- Open an issue on GitHub
- Contact the development team

---

**Happy Generating! 🚀**