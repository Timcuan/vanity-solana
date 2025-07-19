#!/usr/bin/env python3
"""
Simple Telegram Bot for Solana Vanity Generator
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from vanity_generator import SolanaVanityGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
SOLANA_NETWORK = os.getenv('SOLANA_NETWORK', 'mainnet-beta')
MAX_ATTEMPTS = int(os.getenv('MAX_ATTEMPTS', '1000000'))
MAX_PREFIX_LENGTH = int(os.getenv('MAX_PREFIX_LENGTH', '8'))

# Initialize the vanity generator
vanity_generator = SolanaVanityGenerator(max_attempts=MAX_ATTEMPTS)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    welcome_text = f"""
🚀 **Solana Vanity Address Generator**

Selamat datang! Saya adalah bot untuk menghasilkan alamat Solana dengan prefix yang Anda inginkan.

✨ **Fitur:**
• Generate alamat Solana custom
• Interface yang indah dan modern
• Progress tracking real-time
• Keamanan tinggi

🌐 **Network:** {SOLANA_NETWORK}
📏 **Max Prefix:** {MAX_PREFIX_LENGTH} karakter

**Perintah:**
• `/generate <prefix>` - Generate alamat dengan prefix
• `/help` - Bantuan lengkap
• `/status` - Status bot

**Contoh:** `/generate ABC`

⚠️ **Security Warning:** Alamat yang dihasilkan adalah keypair Solana yang nyata!
"""
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /generate command"""
    if not context.args:
        await update.message.reply_text(
            "❌ **Error:** Harap berikan prefix yang diinginkan\n\n"
            "Contoh: `/generate ABC`",
            parse_mode='Markdown'
        )
        return
    
    prefix = context.args[0].upper()
    
    # Validate prefix
    is_valid, error_message = vanity_generator.validate_prefix(prefix)
    if not is_valid:
        await update.message.reply_text(
            f"❌ **Error:** {error_message}\n\n"
            "Gunakan hanya huruf dan angka (A-Z, a-z, 1-9)\n"
            "Hindari: 0, O, I, l",
            parse_mode='Markdown'
        )
        return
    
    # Send initial message
    status_message = await update.message.reply_text(
        f"🔍 **Generating vanity address...**\n\n"
        f"📝 **Prefix:** `{prefix}`\n"
        f"⏱️ **Estimated time:** {vanity_generator.estimate_generation_time(prefix)}\n"
        f"🔄 **Status:** Searching...",
        parse_mode='Markdown'
    )
    
    try:
        # Generate the vanity address
        keypair, attempts, time_taken = vanity_generator.generate_vanity_address(prefix)
        
        if keypair:
            # Success
            public_key = str(keypair.pubkey())
            private_key = vanity_generator.format_private_key(keypair)
            
            success_text = f"""
✅ **Vanity Address Generated Successfully!**

📝 **Prefix:** `{prefix}`
📊 **Attempts:** {attempts:,}
⏱️ **Time:** {time_taken:.2f} seconds
🌐 **Network:** {SOLANA_NETWORK}

🔑 **Public Key:**
`{public_key}`

🔐 **Private Key:**
`{private_key}`

⚠️ **Security Warning:**
• Jaga kerahasiaan private key Anda
• Jangan bagikan private key kepada siapapun
• Simpan di tempat yang aman
• Gunakan hardware wallet untuk jumlah besar
"""
            
            await status_message.edit_text(success_text, parse_mode='Markdown')
            
        else:
            # Failed
            await status_message.edit_text(
                f"❌ **Generation Failed**\n\n"
                f"📝 **Prefix:** `{prefix}`\n"
                f"📊 **Attempts:** {attempts:,}\n"
                f"⏱️ **Time:** {time_taken:.2f} seconds\n\n"
                f"Tidak dapat menemukan alamat dengan prefix tersebut dalam {MAX_ATTEMPTS:,} percobaan.\n"
                f"Coba dengan prefix yang lebih pendek.",
                parse_mode='Markdown'
            )
            
    except Exception as e:
        logger.error(f"Error in generation: {e}")
        await status_message.edit_text(
            f"❌ **Error occurred during generation**\n\n"
            f"Error: {str(e)}\n\n"
            f"Silakan coba lagi atau hubungi admin.",
            parse_mode='Markdown'
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    help_text = """
📖 **Solana Vanity Generator - Help**

**Cara Penggunaan:**
1. Gunakan `/generate <prefix>` untuk generate alamat
2. Tunggu proses selesai
3. Salin public dan private key yang dihasilkan

**Contoh Penggunaan:**
• `/generate ABC` - Generate alamat dengan prefix "ABC"
• `/generate 123` - Generate alamat dengan prefix "123"
• `/generate SOL` - Generate alamat dengan prefix "SOL"

**Tips untuk Generate Lebih Cepat:**
• Gunakan prefix pendek (2-4 karakter)
• Hanya gunakan huruf dan angka (A-Z, a-z, 1-9)
• Hindari karakter: 0, O, I, l

**Perkiraan Waktu:**
• 2 karakter: ~1-10 detik
• 3 karakter: ~10-60 detik
• 4 karakter: ~1-10 menit
• 5+ karakter: ~10+ menit

**Keamanan:**
• Private key adalah kunci rahasia yang nyata
• Jangan bagikan private key kepada siapapun
• Simpan di tempat yang aman
• Gunakan hardware wallet untuk jumlah besar

**Perintah:**
• `/start` - Pesan selamat datang
• `/generate <prefix>` - Generate alamat
• `/help` - Bantuan ini
• `/status` - Status bot

⚠️ **Peringatan:** Alamat yang dihasilkan adalah keypair Solana yang nyata!
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /status command"""
    status_text = f"""
🤖 **Bot Status**

✅ **Status:** Running
🌐 **Network:** {SOLANA_NETWORK}
🔧 **Max Attempts:** {MAX_ATTEMPTS:,}
📏 **Max Prefix Length:** {MAX_PREFIX_LENGTH}
📱 **Version:** 1.0.0

**Fitur Aktif:**
• ✅ Vanity address generation
• ✅ Prefix validation
• ✅ Real-time progress
• ✅ Security features

**Penggunaan:**
• `/generate <prefix>` - Generate alamat
• `/help` - Bantuan lengkap
"""
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle non-command messages"""
    await update.message.reply_text(
        "🤖 **Solana Vanity Generator**\n\n"
        "Saya adalah bot untuk generate alamat Solana custom.\n\n"
        "**Perintah yang tersedia:**\n"
        "• `/start` - Mulai bot\n"
        "• `/generate <prefix>` - Generate alamat\n"
        "• `/help` - Bantuan\n"
        "• `/status` - Status bot\n\n"
        "Contoh: `/generate ABC`",
        parse_mode='Markdown'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "❌ **Error occurred**\n\n"
            "Terjadi kesalahan. Silakan coba lagi atau gunakan `/help` untuk bantuan.",
            parse_mode='Markdown'
        )

def main():
    """Start the bot"""
    print("🔍 Debug: Starting bot initialization...")
    
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not found in environment variables!")
        print("❌ Error: TELEGRAM_TOKEN tidak ditemukan!")
        print("💡 Pastikan file .env berisi TELEGRAM_TOKEN yang valid")
        return
    
    print(f"✅ Token found: {TELEGRAM_TOKEN[:20]}...")
    print(f"🌐 Network: {SOLANA_NETWORK}")
    print(f"📏 Max Prefix Length: {MAX_PREFIX_LENGTH}")
    
    # Create the Application
    print("🔧 Creating Telegram application...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    print("📝 Adding command handlers...")
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("generate", generate_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Add message handler for non-command messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting Solana Vanity Generator Bot...")
    print("🚀 Starting Solana Vanity Generator Bot...")
    print(f"🌐 Network: {SOLANA_NETWORK}")
    print(f"📏 Max Prefix Length: {MAX_PREFIX_LENGTH}")
    print("🤖 Bot is ready! Send /start to begin")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    # Run the bot
    print("🔄 Starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
