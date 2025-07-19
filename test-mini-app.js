const { Keypair } = require('@solana/web3.js');

// Test Solana keypair generation
function testKeypairGeneration() {
    console.log('🧪 Testing Solana keypair generation...');
    
    const keypair = Keypair.generate();
    const publicKey = keypair.publicKey.toString();
    const privateKey = Buffer.from(keypair.secretKey).toString('base64');
    
    console.log('✅ Keypair generated successfully!');
    console.log(`📝 Public Key: ${publicKey}`);
    console.log(`🔐 Private Key: ${privateKey.substring(0, 20)}...`);
    console.log(`📏 Length: ${publicKey.length} characters`);
    
    return { publicKey, privateKey };
}

// Test vanity address generation
function testVanityGeneration(prefix) {
    console.log(`\n🔍 Testing vanity generation for prefix: "${prefix}"`);
    
    const startTime = Date.now();
    let attempts = 0;
    const maxAttempts = 10000; // Limit for testing
    
    while (attempts < maxAttempts) {
        attempts++;
        
        const keypair = Keypair.generate();
        const publicKey = keypair.publicKey.toString();
        
        if (publicKey.startsWith(prefix)) {
            const timeTaken = Date.now() - startTime;
            console.log(`✅ Found vanity address after ${attempts} attempts!`);
            console.log(`📝 Address: ${publicKey}`);
            console.log(`⏱️ Time taken: ${timeTaken}ms`);
            console.log(`⚡ Rate: ${Math.floor(attempts / (timeTaken / 1000))}/s`);
            return { success: true, publicKey, attempts, timeTaken };
        }
    }
    
    const timeTaken = Date.now() - startTime;
    console.log(`❌ No vanity address found after ${attempts} attempts`);
    console.log(`⏱️ Time taken: ${timeTaken}ms`);
    return { success: false, attempts, timeTaken };
}

// Test API endpoints
async function testAPIEndpoints() {
    console.log('\n🌐 Testing API endpoints...');
    
    try {
        // Test health endpoint
        const healthResponse = await fetch('http://localhost:3000/api/health');
        const healthData = await healthResponse.json();
        console.log('✅ Health endpoint:', healthData.status);
        
        // Test generation endpoint
        const generateResponse = await fetch('http://localhost:3000/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prefix: 'SOL', network: 'devnet' })
        });
        
        if (generateResponse.ok) {
            const generateData = await generateResponse.json();
            console.log('✅ Generation endpoint working');
            console.log(`📝 Generated address: ${generateData.data.publicKey}`);
        } else {
            console.log('❌ Generation endpoint failed');
        }
        
    } catch (error) {
        console.log('❌ API test failed:', error.message);
    }
}

// Main test function
async function runTests() {
    console.log('🚀 Starting Telegram Mini App Tests\n');
    
    // Test 1: Basic keypair generation
    testKeypairGeneration();
    
    // Test 2: Vanity generation (short prefix)
    testVanityGeneration('SOL');
    
    // Test 3: API endpoints (if server is running)
    await testAPIEndpoints();
    
    console.log('\n✅ All tests completed!');
}

// Run tests if this file is executed directly
if (require.main === module) {
    runTests().catch(console.error);
}

module.exports = {
    testKeypairGeneration,
    testVanityGeneration,
    testAPIEndpoints,
    runTests
};