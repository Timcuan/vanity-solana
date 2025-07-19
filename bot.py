import asyncio
import logging
import json
import tempfile
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from config import (
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, WELCOME_MESSAGE, HELP_MESSAGE, STATUS_MESSAGE,
    SOLANA_NETWORK, MAX_ATTEMPTS, MAX_PREFIX_LENGTH
)
from vanity_generator import SolanaVanityGenerator

# Configure logging - SECURE: No sensitive data
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the vanity generator
vanity_generator = SolanaVanityGenerator(max_attempts=MAX_ATTEMPTS)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    # SECURE: Only log user ID, not personal info
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    
    # Send minimal notification to admin
    notification = f"🚀 **Bot Started**\n\n👤 User ID: {user_id}\n💬 Chat: {chat_type}\n⏰ Time: {update.message.date}"
    await send_notification(context, notification)
    
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    await update.message.reply_text(HELP_MESSAGE, parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /status command."""
    status_text = STATUS_MESSAGE.format(
        network=SOLANA_NETWORK,
        max_attempts=MAX_ATTEMPTS,
        max_prefix_length=MAX_PREFIX_LENGTH
    )
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /generate command."""
    if not context.args:
        await update.message.reply_text(
            "❌ Please provide a prefix for the vanity address.\n\n"
            "**Usage:** `/generate <prefix>`\n"
            "**Example:** `/generate SOL`",
            parse_mode='Markdown'
        )
        return
    
    prefix = context.args[0].upper()
    
    # Validate the prefix
    is_valid, error_message = vanity_generator.validate_prefix(prefix)
    if not is_valid:
        await update.message.reply_text(f"❌ {error_message}")
        return
    
    # SECURE: Only log user ID and prefix, no personal info
    user_id = update.effective_user.id
    generation_notification = f"🔍 **Generation Request**\n\n👤 User ID: {user_id}\n🎯 Prefix: `{prefix}`\n⏱️ Estimated: {vanity_generator.estimate_generation_time(prefix)}"
    await send_notification(context, generation_notification)
    
    # Send initial message
    status_message = await update.message.reply_text(
        f"🔍 **Generating vanity address...**\n\n"
        f"**Prefix:** `{prefix}`\n"
        f"**Estimated time:** {vanity_generator.estimate_generation_time(prefix)}\n\n"
        f"⏳ Please wait, this may take a while...",
        parse_mode='Markdown'
    )
    
    try:
        # Generate the vanity address
        keypair, attempts, time_taken = vanity_generator.generate_vanity_address(prefix)
        
        if keypair:
            # SECURE: Don't include private keys in result text
            result_text = vanity_generator.format_keypair_info_secure(keypair, attempts, time_taken)
            
            # SECURE: Only send success notification with minimal info
            success_notification = f"✅ **Generation Success**\n\n👤 User ID: {user_id}\n🎯 Prefix: `{prefix}`\n📊 Attempts: {attempts:,}\n⏱️ Time: {time_taken:.2f}s"
            await send_notification(context, success_notification)
            
            # Update the status message with the result
            await status_message.edit_text(result_text, parse_mode='Markdown')
            
            # SECURE: Send wallet files to user via DM only
            try:
                await send_wallet_files(context, update.effective_user.id, keypair, prefix, attempts, time_taken, user_id)
            except Exception as e:
                # SECURE: Don't log user ID in error
                logger.error(f"Failed to send files to user: {e}")
                await update.message.reply_text(
                    "⚠️ **Note:** Could not send wallet files via DM. Please make sure you have started a conversation with the bot.\n\n"
                    "To receive wallet files, please:\n"
                    "1. Send `/start` to the bot in a private message\n"
                    "2. Try generating again",
                    parse_mode='Markdown'
                )
            
        else:
            # SECURE: Send failure notification with minimal info
            failure_notification = f"❌ **Generation Failed**\n\n👤 User ID: {user_id}\n🎯 Prefix: `{prefix}`\n📊 Attempts: {attempts:,}\n⏱️ Time: {time_taken:.2f}s"
            await send_notification(context, failure_notification)
            
            await status_message.edit_text(
                f"❌ **Generation Failed**\n\n"
                f"Could not find a vanity address starting with `{prefix}` "
                f"after {attempts:,} attempts.\n\n"
                f"Try a shorter prefix or try again later.",
                parse_mode='Markdown'
            )
    
    except Exception as e:
        # SECURE: Don't log sensitive data in errors
        logger.error(f"Error generating vanity address: {e}")
        await status_message.edit_text(
            f"❌ **Error occurred**\n\n"
            f"An error occurred while generating the vanity address.\n"
            f"Please try again later or contact support.",
            parse_mode='Markdown'
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle non-command messages."""
    await update.message.reply_text(
        "🤖 I'm a Solana vanity wallet generator bot!\n\n"
        "Use `/start` to see available commands or `/help` for more information.",
        parse_mode='Markdown'
    )

async def send_notification(context: ContextTypes.DEFAULT_TYPE, message: str):
    """Send notification to the configured chat ID."""
    try:
        await context.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")

async def create_wallet_json(keypair, prefix: str, attempts: int, time_taken: float, user_id: int):
    """Create a JSON file with wallet information."""
    wallet_data = {
        "wallet_info": {
            "prefix": prefix,
            "generated_at": datetime.now().isoformat(),
            "network": SOLANA_NETWORK,
            "generation_stats": {
                "attempts": attempts,
                "time_taken_seconds": time_taken,
                "rate_per_second": attempts / time_taken if time_taken > 0 else 0
            },
            "user_id": user_id
        },
        "keys": {
            "public_key": str(keypair.public_key),
            "private_key": str(keypair.secret_key.hex()),
            "private_key_base58": str(keypair.secret_key)
        },
        "security_warning": {
            "message": "Keep your private key secure and never share it with anyone",
            "recommendations": [
                "Store private key offline in a secure location",
                "Use hardware wallet for large amounts",
                "Never share private key via unsecured channels",
                "Make multiple secure backups"
            ]
        }
    }
    
    # Create temporary JSON file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(wallet_data, temp_file, indent=2)
    temp_file.close()
    
    return temp_file.name

async def send_wallet_files(context: ContextTypes.DEFAULT_TYPE, chat_id: int, keypair, prefix: str, attempts: int, time_taken: float, user_id: int):
    """Send wallet JSON file and private key file to user."""
    try:
        # Create JSON file
        json_file_path = await create_wallet_json(keypair, prefix, attempts, time_taken, user_id)
        
        # Send JSON file
        with open(json_file_path, 'rb') as json_file:
            await context.bot.send_document(
                chat_id=chat_id,
                document=json_file,
                filename=f"solana_wallet_{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                caption=f"🔐 **Solana Wallet JSON File**\n\n🎯 Prefix: `{prefix}`\n📊 Attempts: {attempts:,}\n⏱️ Time: {time_taken:.2f}s\n\n⚠️ Keep this file secure!"
            )
        
        # Create private key file
        private_key_content = f"""Solana Private Key File
Generated: {datetime.now().isoformat()}
Prefix: {prefix}
Network: {SOLANA_NETWORK}

PRIVATE KEY (HEX):
{str(keypair.secret_key.hex())}

PRIVATE KEY (BASE58):
{str(keypair.secret_key)}

PUBLIC KEY:
{str(keypair.public_key)}

SECURITY WARNING:
- Keep this file secure and never share it
- Store offline in a secure location
- Use hardware wallet for large amounts
- Make multiple secure backups
"""
        
        # Create temporary private key file
        private_key_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        private_key_file.write(private_key_content)
        private_key_file.close()
        
        # Send private key file
        with open(private_key_file.name, 'rb') as pk_file:
            await context.bot.send_document(
                chat_id=chat_id,
                document=pk_file,
                filename=f"private_key_{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                caption=f"🔑 **Private Key File**\n\n🎯 Prefix: `{prefix}`\n\n⚠️ **CRITICAL SECURITY WARNING**\n• Keep this file absolutely secure\n• Never share with anyone\n• Store offline only\n• Use hardware wallet for large amounts"
            )
        
        # Clean up temporary files
        os.unlink(json_file_path)
        os.unlink(private_key_file.name)
        
        # Send additional security message
        await context.bot.send_message(
            chat_id=chat_id,
            text="🔒 **Security Reminder**\n\n✅ Files have been sent to your DM\n⚠️ Delete these files from Telegram after downloading\n💾 Store them securely offline\n🔐 Consider using a hardware wallet for large amounts",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Failed to send wallet files: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ Error creating wallet files. Please try again or contact support."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "❌ An error occurred. Please try again later or contact support."
        )

def main():
    """Start the bot."""
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not found in environment variables!")
        return
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("generate", generate_command))
    
    # Add message handler for non-command messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting Solana Vanity Wallet Bot...")
    
    # Send startup notification
    async def send_startup_notification():
        try:
            await application.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text="🚀 **Solana Vanity Bot Started**\n\n✅ Bot is now online and ready to generate vanity addresses!\n🌐 Network: " + SOLANA_NETWORK,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Failed to send startup notification: {e}")
    
    # Run startup notification and then start polling
    application.job_queue.run_once(send_startup_notification, 1)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()