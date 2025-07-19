const express = require('express');
const cors = require('cors');
const { Keypair } = require('@solana/web3.js');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('.')); // Serve static files

// In-memory storage for active generations (in production, use Redis or database)
const activeGenerations = new Map();

// Generate Solana vanity address
function generateVanityAddress(prefix, maxAttempts = 1000000) {
    const startTime = Date.now();
    let attempts = 0;
    
    while (attempts < maxAttempts) {
        attempts++;
        
        // Generate a new keypair
        const keypair = Keypair.generate();
        const publicKey = keypair.publicKey.toString();
        
        // Check if the public key starts with the desired prefix
        if (publicKey.startsWith(prefix)) {
            const timeTaken = Date.now() - startTime;
            return {
                success: true,
                publicKey: publicKey,
                privateKey: Buffer.from(keypair.secretKey).toString('base64'),
                attempts: attempts,
                timeTaken: timeTaken,
                rate: Math.floor(attempts / (timeTaken / 1000))
            };
        }
    }
    
    const timeTaken = Date.now() - startTime;
    return {
        success: false,
        attempts: attempts,
        timeTaken: timeTaken,
        rate: Math.floor(attempts / (timeTaken / 1000))
    };
}

// Routes
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// Generate vanity address endpoint
app.post('/api/generate', async (req, res) => {
    try {
        const { prefix, network = 'devnet', maxAttempts = 1000000 } = req.body;
        
        // Validate input
        if (!prefix || typeof prefix !== 'string') {
            return res.status(400).json({ error: 'Prefix is required' });
        }
        
        if (prefix.length > 8) {
            return res.status(400).json({ error: 'Prefix cannot be longer than 8 characters' });
        }
        
        if (!/^[A-Z0-9]+$/.test(prefix.toUpperCase())) {
            return res.status(400).json({ error: 'Prefix can only contain letters and numbers' });
        }
        
        const upperPrefix = prefix.toUpperCase();
        
        // Generate the vanity address
        const result = generateVanityAddress(upperPrefix, maxAttempts);
        
        if (result.success) {
            // Create response with keypair data
            const response = {
                success: true,
                data: {
                    publicKey: result.publicKey,
                    privateKey: result.privateKey,
                    prefix: upperPrefix,
                    network: network,
                    attempts: result.attempts,
                    timeTaken: result.timeTaken,
                    rate: result.rate,
                    generatedAt: new Date().toISOString()
                }
            };
            
            res.json(response);
        } else {
            res.json({
                success: false,
                error: 'Failed to generate address within maximum attempts',
                data: {
                    attempts: result.attempts,
                    timeTaken: result.timeTaken,
                    rate: result.rate
                }
            });
        }
        
    } catch (error) {
        console.error('Generation error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Start generation with progress tracking
app.post('/api/generate/start', async (req, res) => {
    try {
        const { prefix, network = 'devnet', maxAttempts = 1000000 } = req.body;
        
        // Validate input
        if (!prefix || typeof prefix !== 'string') {
            return res.status(400).json({ error: 'Prefix is required' });
        }
        
        if (prefix.length > 8) {
            return res.status(400).json({ error: 'Prefix cannot be longer than 8 characters' });
        }
        
        if (!/^[A-Z0-9]+$/.test(prefix.toUpperCase())) {
            return res.status(400).json({ error: 'Prefix can only contain letters and numbers' });
        }
        
        const upperPrefix = prefix.toUpperCase();
        const generationId = crypto.randomUUID();
        
        // Initialize generation tracking
        const generation = {
            id: generationId,
            prefix: upperPrefix,
            network: network,
            maxAttempts: maxAttempts,
            startTime: Date.now(),
            attempts: 0,
            isRunning: true,
            result: null
        };
        
        activeGenerations.set(generationId, generation);
        
        // Start generation in background
        setTimeout(() => {
            generateWithProgress(generationId);
        }, 100);
        
        res.json({
            success: true,
            generationId: generationId,
            message: 'Generation started'
        });
        
    } catch (error) {
        console.error('Start generation error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Get generation progress
app.get('/api/generate/:generationId/status', (req, res) => {
    try {
        const { generationId } = req.params;
        const generation = activeGenerations.get(generationId);
        
        if (!generation) {
            return res.status(404).json({ error: 'Generation not found' });
        }
        
        const timeElapsed = Date.now() - generation.startTime;
        const rate = timeElapsed > 0 ? Math.floor(generation.attempts / (timeElapsed / 1000)) : 0;
        
        res.json({
            success: true,
            data: {
                id: generation.id,
                prefix: generation.prefix,
                network: generation.network,
                attempts: generation.attempts,
                timeElapsed: timeElapsed,
                rate: rate,
                isRunning: generation.isRunning,
                result: generation.result
            }
        });
        
    } catch (error) {
        console.error('Status check error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Stop generation
app.post('/api/generate/:generationId/stop', (req, res) => {
    try {
        const { generationId } = req.params;
        const generation = activeGenerations.get(generationId);
        
        if (!generation) {
            return res.status(404).json({ error: 'Generation not found' });
        }
        
        generation.isRunning = false;
        generation.result = {
            success: false,
            reason: 'Stopped by user',
            attempts: generation.attempts,
            timeTaken: Date.now() - generation.startTime
        };
        
        res.json({
            success: true,
            message: 'Generation stopped'
        });
        
    } catch (error) {
        console.error('Stop generation error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Background generation function
function generateWithProgress(generationId) {
    const generation = activeGenerations.get(generationId);
    if (!generation) return;
    
    const startTime = Date.now();
    
    const interval = setInterval(() => {
        if (!generation.isRunning) {
            clearInterval(interval);
            return;
        }
        
        // Generate a batch of attempts
        const batchSize = 1000;
        for (let i = 0; i < batchSize; i++) {
            if (!generation.isRunning) break;
            
            generation.attempts++;
            
            // Generate a new keypair
            const keypair = Keypair.generate();
            const publicKey = keypair.publicKey.toString();
            
            // Check if the public key starts with the desired prefix
            if (publicKey.startsWith(generation.prefix)) {
                clearInterval(interval);
                
                const timeTaken = Date.now() - startTime;
                generation.result = {
                    success: true,
                    publicKey: publicKey,
                    privateKey: Buffer.from(keypair.secretKey).toString('base64'),
                    attempts: generation.attempts,
                    timeTaken: timeTaken,
                    rate: Math.floor(generation.attempts / (timeTaken / 1000))
                };
                
                generation.isRunning = false;
                return;
            }
        }
        
        // Check if max attempts reached
        if (generation.attempts >= generation.maxAttempts) {
            clearInterval(interval);
            
            const timeTaken = Date.now() - startTime;
            generation.result = {
                success: false,
                reason: 'Max attempts reached',
                attempts: generation.attempts,
                timeTaken: timeTaken,
                rate: Math.floor(generation.attempts / (timeTaken / 1000))
            };
            
            generation.isRunning = false;
        }
    }, 50); // Update every 50ms
}

// Clean up old generations (run every 5 minutes)
setInterval(() => {
    const now = Date.now();
    for (const [id, generation] of activeGenerations.entries()) {
        // Remove generations older than 1 hour
        if (now - generation.startTime > 3600000) {
            activeGenerations.delete(id);
        }
    }
}, 300000);

// Error handling middleware
app.use((error, req, res, next) => {
    console.error('Unhandled error:', error);
    res.status(500).json({ error: 'Internal server error' });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Not found' });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Solana Vanity Generator server running on port ${PORT}`);
    console.log(`📱 Telegram Mini App available at http://localhost:${PORT}`);
    console.log(`🔗 API endpoints:`);
    console.log(`   POST /api/generate - Generate vanity address`);
    console.log(`   POST /api/generate/start - Start generation with progress`);
    console.log(`   GET  /api/generate/:id/status - Get generation status`);
    console.log(`   POST /api/generate/:id/stop - Stop generation`);
    console.log(`   GET  /api/health - Health check`);
});

module.exports = app;