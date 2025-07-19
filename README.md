# Solana Vanity Wallet Telegram Bot

A Telegram bot that generates Solana vanity addresses with custom prefixes. This bot allows users to create Solana keypairs with addresses that start with their desired prefix.

## Features

- 🚀 Generate Solana vanity addresses with custom prefixes
- 🔒 Real Solana keypairs (public and private keys)
- ⏱️ Real-time generation progress updates
- 📊 Generation statistics (attempts, time, rate)
- 🛡️ Input validation and error handling
- 📱 User-friendly Telegram interface
- ⚡ Fast generation for short prefixes
- 🔧 Configurable settings

## Commands

- `/start` - Show welcome message and available commands
- `/generate <prefix>` - Generate a vanity address with custom prefix
- `/help` - Show detailed help information
- `/status` - Check bot status and configuration

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- A Telegram account
- A Telegram bot token (get from @BotFather)

### 2. Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and add your Telegram bot token:
   ```
   TELEGRAM_TOKEN=your_actual_bot_token_here
   SOLANA_NETWORK=devnet
   ```

### 4. Getting a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token provided by BotFather
5. Paste it in your `.env` file

### 5. Running the Bot

```bash
python bot.py
```

## Usage Examples

### Basic Usage

```
/generate SOL
```
Generates a Solana address starting with "SOL"

### Short Prefixes (Fast)
```
/generate A
/generate 123
/generate SOL
```
These generate quickly (seconds to minutes)

### Longer Prefixes (Slower)
```
/generate SOLANA
/generate 123456
```
These may take longer (minutes to hours)

## Security Considerations

⚠️ **Important Security Notes:**

1. **Private Key Security**: The bot generates real Solana keypairs. Keep private keys secure and never share them.

2. **Offline Storage**: Store generated private keys offline in a secure location.

3. **Hardware Wallets**: For large amounts, consider transferring to a hardware wallet.

4. **Network Selection**: The bot defaults to devnet for safety. Change to mainnet-beta only when ready for real transactions.

5. **Bot Access**: Only share your bot with trusted users.

## Technical Details

### Vanity Address Generation

The bot uses a brute-force approach to generate vanity addresses:

1. Generates random Solana keypairs
2. Checks if the public key starts with the desired prefix
3. Continues until a match is found or max attempts reached

### Performance

- **2-3 character prefixes**: ~1-60 seconds
- **4 character prefixes**: ~1-10 minutes
- **5 character prefixes**: ~10-60 minutes
- **6+ character prefixes**: Hours or more

### Configuration Options

Edit `config.py` to customize:

- `MAX_ATTEMPTS`: Maximum generation attempts
- `MAX_PREFIX_LENGTH`: Maximum allowed prefix length
- `SOLANA_NETWORK`: Target Solana network

## File Structure

```
├── bot.py                 # Main bot application
├── config.py              # Configuration and messages
├── vanity_generator.py    # Core vanity address generator
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your environment variables (create this)
└── README.md             # This file
```

## Troubleshooting

### Common Issues

1. **"TELEGRAM_TOKEN not found"**
   - Make sure you created a `.env` file
   - Verify your bot token is correct

2. **"Invalid characters in prefix"**
   - Only use alphanumeric characters
   - Avoid special characters and spaces

3. **Generation taking too long**
   - Try a shorter prefix
   - Check your internet connection

4. **Bot not responding**
   - Verify the bot is running
   - Check the console for error messages

### Error Logs

The bot logs all activities to the console. Check for error messages if something goes wrong.

## Contributing

Feel free to contribute to this project by:

1. Reporting bugs
2. Suggesting new features
3. Submitting pull requests
4. Improving documentation

## License

This project is open source. Use responsibly and at your own risk.

## Disclaimer

This bot generates real Solana keypairs. Users are responsible for the security of their generated keys and any transactions made with them. The developers are not responsible for any loss of funds or security issues.

## Support

For support or questions:
- Check the `/help` command in the bot
- Review this README
- Check the console logs for errors
