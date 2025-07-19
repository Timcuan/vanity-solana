import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Solana Configuration
SOLANA_NETWORK = os.getenv('SOLANA_NETWORK', 'devnet')  # devnet, testnet, mainnet-beta

# Vanity Wallet Configuration
MAX_ATTEMPTS = 1000000  # Maximum attempts to find a vanity address
DEFAULT_PREFIX_LENGTH = 4  # Default prefix length for vanity addresses
MAX_PREFIX_LENGTH = 8  # Maximum allowed prefix length

# Bot Messages
WELCOME_MESSAGE = """
🚀 **Solana Vanity Wallet Generator Bot**

Welcome! I can help you generate Solana vanity addresses with custom prefixes.

**Available Commands:**
• `/start` - Show this welcome message
• `/generate <prefix>` - Generate a vanity address with custom prefix
• `/help` - Show help information
• `/status` - Check bot status

**Example:**
`/generate SOL` - Generates an address starting with "SOL"

**Note:** Longer prefixes take more time to generate. Maximum prefix length is 8 characters.
"""

HELP_MESSAGE = """
📖 **Help Guide**

**How to use:**
1. Use `/generate <prefix>` to create a vanity address
2. The bot will generate a Solana keypair with your desired prefix
3. You'll receive both the public key and private key

**Tips:**
• Shorter prefixes (2-4 chars) generate faster
• Longer prefixes (5-8 chars) may take several minutes
• Only use alphanumeric characters for prefixes
• Keep your private keys secure!

**Safety:**
⚠️ Never share your private keys with anyone
⚠️ This bot generates real Solana keypairs
⚠️ Store private keys securely offline
"""

STATUS_MESSAGE = """
🤖 **Bot Status**

✅ Bot is running
🌐 Network: {network}
🔧 Max attempts: {max_attempts:,}
📏 Max prefix length: {max_prefix_length}
"""