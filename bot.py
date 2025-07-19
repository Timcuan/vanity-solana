import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from config import (
    TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, WELCOME_MESSAGE, HELP_MESSAGE, STATUS_MESSAGE,
    SOLANA_NETWORK, MAX_ATTEMPTS, MAX_PREFIX_LENGTH
)
from vanity_generator import SolanaVanityGenerator

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the vanity generator
vanity_generator = SolanaVanityGenerator(max_attempts=MAX_ATTEMPTS)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    user_info = f"👤 User: {update.effective_user.first_name} (@{update.effective_user.username})"
    chat_info = f"💬 Chat: {update.effective_chat.type} (ID: {update.effective_chat.id})"
    
    # Send notification to admin
    notification = f"🚀 **Bot Started**\n\n{user_info}\n{chat_info}\n⏰ Time: {update.message.date}"
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
    
    # Send notification to admin about generation request
    user_info = f"👤 User: {update.effective_user.first_name} (@{update.effective_user.username})"
    generation_notification = f"🔍 **Generation Request**\n\n{user_info}\n🎯 Prefix: `{prefix}`\n⏱️ Estimated: {vanity_generator.estimate_generation_time(prefix)}"
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
            # Format the result
            result_text = vanity_generator.format_keypair_info(keypair, attempts, time_taken)
            
            # Send success notification to admin
            success_notification = f"✅ **Generation Success**\n\n{user_info}\n🎯 Prefix: `{prefix}`\n📊 Attempts: {attempts:,}\n⏱️ Time: {time_taken:.2f}s\n🔑 Address: `{str(keypair.public_key)[:20]}...`"
            await send_notification(context, success_notification)
            
            # Update the status message with the result
            await status_message.edit_text(result_text, parse_mode='Markdown')
            
            # Send a separate message with just the keys for easy copying
            keys_text = f"""
📋 **Quick Copy Keys:**

🔑 **Public Key:**
`{str(keypair.public_key)}`

🔐 **Private Key:**
`{str(keypair.secret_key.hex())}`
"""
            await update.message.reply_text(keys_text, parse_mode='Markdown')
            
        else:
            # Send failure notification to admin
            failure_notification = f"❌ **Generation Failed**\n\n{user_info}\n🎯 Prefix: `{prefix}`\n📊 Attempts: {attempts:,}\n⏱️ Time: {time_taken:.2f}s"
            await send_notification(context, failure_notification)
            
            await status_message.edit_text(
                f"❌ **Generation Failed**\n\n"
                f"Could not find a vanity address starting with `{prefix}` "
                f"after {attempts:,} attempts.\n\n"
                f"Try a shorter prefix or try again later.",
                parse_mode='Markdown'
            )
    
    except Exception as e:
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