#!/usr/bin/env node

const readline = require('readline');
const fs = require('fs');
const path = require('path');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

console.log('🤖 Telegram Mini App Setup Wizard');
console.log('==================================\n');

// Questions for setup
const questions = [
    {
        name: 'botToken',
        question: 'Enter your Telegram bot token (from @BotFather): ',
        required: true
    },
    {
        name: 'webAppUrl',
        question: 'Enter your web app URL (e.g., https://your-domain.com): ',
        required: true
    },
    {
        name: 'port',
        question: 'Enter port number for local development (default: 3000): ',
        default: '3000'
    }
];

async function askQuestion(question) {
    return new Promise((resolve) => {
        rl.question(question.question, (answer) => {
            if (question.required && !answer.trim()) {
                console.log('❌ This field is required!');
                return askQuestion(question);
            }
            resolve(answer.trim() || question.default);
        });
    });
}

async function setupBot() {
    console.log('📋 Let\'s set up your Telegram bot for the Mini App...\n');
    
    const answers = {};
    
    for (const q of questions) {
        answers[q.name] = await askQuestion(q);
    }
    
    console.log('\n📝 Creating configuration files...');
    
    // Create .env file
    const envContent = `TELEGRAM_TOKEN=${answers.botToken}
PORT=${answers.port}
NODE_ENV=development
`;
    
    fs.writeFileSync('.env', envContent);
    console.log('✅ Created .env file');
    
    // Update telegram-config.json
    const configPath = path.join(__dirname, 'telegram-config.json');
    if (fs.existsSync(configPath)) {
        const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        config.telegram.bot_token = answers.botToken;
        config.telegram.web_app_url = answers.webAppUrl;
        
        fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
        console.log('✅ Updated telegram-config.json');
    }
    
    console.log('\n🎉 Configuration complete!');
    console.log('\n📋 Next steps:');
    console.log('1. Start the server: npm run server');
    console.log('2. Set up your bot menu button:');
    console.log('   - Message @BotFather');
    console.log('   - Use /setmenubutton');
    console.log('   - Select your bot');
    console.log('   - Set type to: web_app');
    console.log('   - Set text to: Generate Address');
    console.log('   - Set URL to:', answers.webAppUrl);
    console.log('\n3. Test your Mini App in Telegram!');
    
    rl.close();
}

function showInstructions() {
    console.log('\n📚 Manual Setup Instructions');
    console.log('============================\n');
    
    console.log('1. Create a Telegram Bot:');
    console.log('   - Message @BotFather on Telegram');
    console.log('   - Send /newbot');
    console.log('   - Follow the instructions');
    console.log('   - Save your bot token\n');
    
    console.log('2. Set up the Menu Button:');
    console.log('   - Message @BotFather again');
    console.log('   - Send /setmenubutton');
    console.log('   - Select your bot');
    console.log('   - Choose "web_app" type');
    console.log('   - Set text: "Generate Address"');
    console.log('   - Set URL: your web app URL\n');
    
    console.log('3. Configure Environment:');
    console.log('   - Copy .env.example to .env');
    console.log('   - Add your bot token');
    console.log('   - Set your web app URL\n');
    
    console.log('4. Deploy your app:');
    console.log('   - Deploy to hosting service (Vercel, Netlify, etc.)');
    console.log('   - Update web app URL in bot settings');
    console.log('   - Ensure HTTPS is enabled\n');
    
    console.log('5. Test the Mini App:');
    console.log('   - Open your bot in Telegram');
    console.log('   - Click the menu button');
    console.log('   - The Mini App should open!\n');
}

function showHelp() {
    console.log('\n❓ Help & Support');
    console.log('==================\n');
    
    console.log('🔗 Useful Links:');
    console.log('- Telegram Bot API: https://core.telegram.org/bots/api');
    console.log('- Telegram Web App: https://core.telegram.org/bots/webapps');
    console.log('- Solana Web3.js: https://docs.solana.com/developing/clients/javascript-api');
    console.log('- This project: https://github.com/your-repo/solana-vanity-telegram\n');
    
    console.log('🐛 Common Issues:');
    console.log('- Bot not responding: Check token and server status');
    console.log('- Mini App not loading: Verify HTTPS and CORS settings');
    console.log('- Generation failing: Check Solana network connectivity');
    console.log('- UI issues: Ensure Telegram Web App API is loaded\n');
    
    console.log('📞 Support:');
    console.log('- Check the troubleshooting section in README');
    console.log('- Open an issue on GitHub');
    console.log('- Review Telegram Mini App documentation\n');
}

// Main menu
async function showMenu() {
    console.log('\n🔧 Setup Options:');
    console.log('1. Automated Setup (Recommended)');
    console.log('2. Manual Instructions');
    console.log('3. Help & Support');
    console.log('4. Exit');
    
    const choice = await askQuestion({
        question: '\nSelect an option (1-4): ',
        required: true
    });
    
    switch (choice) {
        case '1':
            await setupBot();
            break;
        case '2':
            showInstructions();
            rl.close();
            break;
        case '3':
            showHelp();
            rl.close();
            break;
        case '4':
            console.log('👋 Goodbye!');
            rl.close();
            break;
        default:
            console.log('❌ Invalid option. Please try again.');
            await showMenu();
    }
}

// Start the setup wizard
if (require.main === module) {
    showMenu().catch(console.error);
}

module.exports = {
    setupBot,
    showInstructions,
    showHelp
};