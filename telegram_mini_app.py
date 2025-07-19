import asyncio
import logging
import json
import os
from datetime import datetime
from aiohttp import web, ClientSession
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SOLANA_NETWORK, MAX_ATTEMPTS, MAX_PREFIX_LENGTH
from vanity_generator import SolanaVanityGenerator

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the vanity generator
vanity_generator = SolanaVanityGenerator(max_attempts=MAX_ATTEMPTS)

# Store active generations
active_generations = {}

class TelegramMiniApp:
    def __init__(self):
        self.app = web.Application()
        self.setup_routes()
        
    def setup_routes(self):
        """Setup web routes for the mini app"""
        self.app.router.add_get('/', self.index_handler)
        self.app.router.add_post('/api/generate', self.generate_api_handler)
        self.app.router.add_get('/api/status/{task_id}', self.status_api_handler)
        self.app.router.add_static('/static', path='./static', name='static')
        
    async def index_handler(self, request):
        """Serve the main mini app HTML"""
        html_content = self.get_mini_app_html()
        return web.Response(text=html_content, content_type='text/html')
    
    async def generate_api_handler(self, request):
        """Handle vanity address generation API requests"""
        try:
            data = await request.json()
            prefix = data.get('prefix', '').upper()
            
            # Validate prefix
            is_valid, error_message = vanity_generator.validate_prefix(prefix)
            if not is_valid:
                return web.json_response({
                    'success': False,
                    'error': error_message
                })
            
            # Create task ID
            task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{prefix}"
            
            # Start generation in background
            asyncio.create_task(self.generate_vanity_address_async(task_id, prefix))
            
            return web.json_response({
                'success': True,
                'task_id': task_id,
                'estimated_time': vanity_generator.estimate_generation_time(prefix)
            })
            
        except Exception as e:
            logger.error(f"Error in generate API: {e}")
            return web.json_response({
                'success': False,
                'error': 'Internal server error'
            })
    
    async def status_api_handler(self, request):
        """Handle status check API requests"""
        task_id = request.match_info['task_id']
        
        if task_id in active_generations:
            status = active_generations[task_id]
            return web.json_response(status)
        else:
            return web.json_response({
                'success': False,
                'error': 'Task not found'
            })
    
    async def generate_vanity_address_async(self, task_id: str, prefix: str):
        """Generate vanity address asynchronously"""
        try:
            # Initialize task status
            active_generations[task_id] = {
                'status': 'generating',
                'prefix': prefix,
                'attempts': 0,
                'start_time': datetime.now().isoformat(),
                'progress': 0
            }
            
            # Generate the vanity address
            keypair, attempts, time_taken = vanity_generator.generate_vanity_address(prefix)
            
            if keypair:
                # Success
                active_generations[task_id] = {
                    'status': 'completed',
                    'prefix': prefix,
                    'attempts': attempts,
                    'time_taken': time_taken,
                    'public_key': str(keypair.public_key),
                    'private_key': vanity_generator.format_private_key(keypair),
                    'completion_time': datetime.now().isoformat()
                }
            else:
                # Failed
                active_generations[task_id] = {
                    'status': 'failed',
                    'prefix': prefix,
                    'attempts': attempts,
                    'time_taken': time_taken,
                    'error': 'Could not find vanity address within maximum attempts',
                    'completion_time': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error in async generation: {e}")
            active_generations[task_id] = {
                'status': 'failed',
                'prefix': prefix,
                'error': str(e),
                'completion_time': datetime.now().isoformat()
            }
    
    def get_mini_app_html(self):
        """Generate the HTML content for the mini app"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solana Vanity Generator</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 24px;
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 24px;
            margin-bottom: 8px;
        }}
        
        .header p {{
            color: #666;
            font-size: 14px;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }}
        
        .form-group input {{
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        
        .form-group input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .btn {{
            width: 100%;
            padding: 14px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
        }}
        
        .btn:disabled {{
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }}
        
        .status {{
            margin-top: 20px;
            padding: 16px;
            border-radius: 8px;
            display: none;
        }}
        
        .status.generating {{
            background: #e3f2fd;
            border: 1px solid #2196f3;
            color: #1976d2;
        }}
        
        .status.completed {{
            background: #e8f5e8;
            border: 1px solid #4caf50;
            color: #2e7d32;
        }}
        
        .status.failed {{
            background: #ffebee;
            border: 1px solid #f44336;
            color: #c62828;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e1e5e9;
            border-radius: 4px;
            overflow: hidden;
            margin: 12px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s;
        }}
        
        .result {{
            margin-top: 16px;
            padding: 16px;
            background: #f8f9fa;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            word-break: break-all;
        }}
        
        .copy-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 8px;
            font-size: 12px;
        }}
        
        .info {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 12px;
            border-radius: 8px;
            font-size: 14px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header">
                <h1>🚀 Solana Vanity Generator</h1>
                <p>Generate custom Solana addresses with your desired prefix</p>
            </div>
            
            <div class="info">
                <strong>💡 Tips:</strong> Shorter prefixes (2-4 chars) generate faster. 
                Maximum length is {MAX_PREFIX_LENGTH} characters.
            </div>
            
            <form id="generateForm">
                <div class="form-group">
                    <label for="prefix">Desired Prefix:</label>
                    <input type="text" id="prefix" name="prefix" 
                           placeholder="e.g., SOL, 123, ABC" 
                           maxlength="{MAX_PREFIX_LENGTH}" required>
                </div>
                
                <button type="submit" class="btn" id="generateBtn">
                    �� Generate Vanity Address
                </button>
            </form>
            
            <div id="status" class="status">
                <div id="statusText"></div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div id="progressText"></div>
            </div>
            
            <div id="result" class="result" style="display: none;">
                <div id="resultContent"></div>
            </div>
        </div>
    </div>

    <script>
        // Initialize Telegram WebApp
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();
        
        // Set theme
        if (tg.colorScheme === 'dark') {{
            document.body.style.background = 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)';
            document.querySelector('.card').style.background = '#34495e';
            document.querySelector('.card').style.color = '#ecf0f1';
        }}
        
        let currentTaskId = null;
        let statusCheckInterval = null;
        
        document.getElementById('generateForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            
            const prefix = document.getElementById('prefix').value.trim().toUpperCase();
            const generateBtn = document.getElementById('generateBtn');
            const status = document.getElementById('status');
            const statusText = document.getElementById('statusText');
            
            if (!prefix) {{
                alert('Please enter a prefix');
                return;
            }}
            
            // Disable form and show status
            generateBtn.disabled = true;
            generateBtn.textContent = '⏳ Generating...';
            status.className = 'status generating';
            status.style.display = 'block';
            statusText.textContent = 'Starting generation...';
            
            try {{
                const response = await fetch('/api/generate', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ prefix }})
                }});
                
                const data = await response.json();
                
                if (data.success) {{
                    currentTaskId = data.task_id;
                    statusText.textContent = `Generating address with prefix "${prefix}"...`;
                    
                    // Start polling for status
                    startStatusPolling();
                }} else {{
                    throw new Error(data.error);
                }}
                
            }} catch (error) {{
                status.className = 'status failed';
                statusText.textContent = `Error: ${{error.message}}`;
                generateBtn.disabled = false;
                generateBtn.textContent = '🔍 Generate Vanity Address';
            }}
        }});
        
        function startStatusPolling() {{
            if (statusCheckInterval) {{
                clearInterval(statusCheckInterval);
            }}
            
            statusCheckInterval = setInterval(async () => {{
                if (!currentTaskId) return;
                
                try {{
                    const response = await fetch(`/api/status/${{currentTaskId}}`);
                    const data = await response.json();
                    
                    if (data.success === false) {{
                        clearInterval(statusCheckInterval);
                        showError('Task not found');
                        return;
                    }}
                    
                    updateStatus(data);
                    
                    if (data.status === 'completed' || data.status === 'failed') {{
                        clearInterval(statusCheckInterval);
                        showResult(data);
                    }}
                    
                }} catch (error) {{
                    console.error('Status check error:', error);
                }}
            }}, 1000);
        }}
        
        function updateStatus(data) {{
            const statusText = document.getElementById('statusText');
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            
            if (data.status === 'generating') {{
                statusText.textContent = `Generating... (Attempts: ${{data.attempts || 0}})`;
                progressFill.style.width = '50%';
                progressText.textContent = 'Searching for matching address...';
            }}
        }}
        
        function showResult(data) {{
            const status = document.getElementById('status');
            const statusText = document.getElementById('statusText');
            const result = document.getElementById('result');
            const resultContent = document.getElementById('resultContent');
            const generateBtn = document.getElementById('generateBtn');
            
            generateBtn.disabled = false;
            generateBtn.textContent = '🔍 Generate Vanity Address';
            
            if (data.status === 'completed') {{
                status.className = 'status completed';
                statusText.textContent = `✅ Generated successfully in ${{data.time_taken.toFixed(2)}}s (${{data.attempts.toLocaleString()}} attempts)`;
                
                resultContent.innerHTML = `
                    <strong>🔑 Public Key:</strong><br>
                    <code>${{data.public_key}}</code>
                    <button class="copy-btn" onclick="copyToClipboard('${{data.public_key}}')">📋 Copy</button>
                    <br><br>
                    <strong>🔐 Private Key:</strong><br>
                    <code>${{data.private_key}}</code>
                    <button class="copy-btn" onclick="copyToClipboard('${{data.private_key}}')">📋 Copy</button>
                    <br><br>
                    <strong>⚠️ Security Warning:</strong><br>
                    Keep your private key secure and never share it!
                `;
                
            }} else {{
                status.className = 'status failed';
                statusText.textContent = `❌ Generation failed: ${{data.error}}`;
            }}
            
            result.style.display = 'block';
        }}
        
        function showError(message) {{
            const status = document.getElementById('status');
            const statusText = document.getElementById('statusText');
            const generateBtn = document.getElementById('generateBtn');
            
            status.className = 'status failed';
            statusText.textContent = `Error: ${{message}}`;
            generateBtn.disabled = false;
            generateBtn.textContent = '🔍 Generate Vanity Address';
        }}
        
        async function copyToClipboard(text) {{
            try {{
                await navigator.clipboard.writeText(text);
                tg.showAlert('Copied to clipboard!');
            }} catch (error) {{
                tg.showAlert('Failed to copy to clipboard');
            }}
        }}
    </script>
</body>
</html>
"""

# Telegram Bot Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command with mini app button"""
    keyboard = [
        [InlineKeyboardButton(
            "🚀 Open Vanity Generator", 
            web_app=WebAppInfo(url="https://your-domain.com/")
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🚀 **Solana Vanity Address Generator**\n\n"
        "Generate custom Solana addresses with your desired prefix!\n\n"
        "Click the button below to open the mini app:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    help_text = """
📖 **Solana Vanity Generator Help**

**How to use:**
1. Click "Open Vanity Generator" to launch the mini app
2. Enter your desired prefix (2-8 characters)
3. Wait for generation to complete
4. Copy your public and private keys

**Tips:**
• Shorter prefixes (2-4 chars) generate faster
• Only use alphanumeric characters
• Keep your private keys secure!

**Commands:**
• `/start` - Open the mini app
• `/help` - Show this help
• `/status` - Check bot status

⚠️ **Security:** Never share your private keys!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /status command"""
    status_text = f"""
🤖 **Bot Status**

✅ Bot is running
🌐 Network: {SOLANA_NETWORK}
🔧 Max attempts: {MAX_ATTEMPTS:,}
📏 Max prefix length: {MAX_PREFIX_LENGTH}
📱 Mini App: Available
"""
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle non-command messages"""
    keyboard = [
        [InlineKeyboardButton(
            "🚀 Open Vanity Generator", 
            web_app=WebAppInfo(url="https://your-domain.com/")
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 I'm a Solana vanity address generator!\n\n"
        "Click the button below to open the mini app:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "❌ An error occurred. Please try again later."
        )

def main():
    """Start the bot and web server"""
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not found in environment variables!")
        return
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Add message handler for non-command messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Create mini app
    mini_app = TelegramMiniApp()
    
    # Start the bot and web server
    logger.info("Starting Solana Vanity Generator Mini App...")
    
    # Run both the bot and web server
    async def run_both():
        # Start web server
        runner = web.AppRunner(mini_app.app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()
        logger.info("Web server started on http://localhost:8080")
        
        # Start bot
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    asyncio.run(run_both())

if __name__ == '__main__':
    main()
