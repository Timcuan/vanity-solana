// Telegram Web App API
let tg = window.Telegram.WebApp;

// App State
let appState = {
    currentSection: 'welcome',
    selectedNetwork: 'devnet',
    isGenerating: false,
    generationInterval: null,
    currentGeneration: null,
    history: []
};

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeTelegramApp();
    setupEventListeners();
    loadHistory();
    updateNetworkBadge();
});

// Initialize Telegram Web App
function initializeTelegramApp() {
    // Expand the app to full height
    tg.expand();
    
    // Set the header color
    tg.setHeaderColor('#2481cc');
    
    // Set the background color
    tg.setBackgroundColor('#ffffff');
    
    // Enable closing confirmation
    tg.enableClosingConfirmation();
    
    // Set up theme change handler
    tg.onEvent('themeChanged', function() {
        updateTheme();
    });
    
    // Set up viewport change handler
    tg.onEvent('viewportChanged', function() {
        tg.expand();
    });
    
    // Show the main button
    tg.MainButton.setText('Generate Address');
    tg.MainButton.onClick(function() {
        if (appState.currentSection === 'welcome') {
            showGenerator();
        } else if (appState.currentSection === 'generator') {
            startGeneration();
        }
    });
    
    // Show the back button when needed
    tg.BackButton.onClick(function() {
        if (appState.currentSection === 'generator') {
            showWelcome();
        } else if (appState.currentSection === 'results') {
            showGenerator();
        } else if (appState.currentSection === 'history') {
            showWelcome();
        }
    });
    
    // Update theme initially
    updateTheme();
}

// Update theme based on Telegram's theme
function updateTheme() {
    const isDark = tg.colorScheme === 'dark';
    document.body.classList.toggle('dark-theme', isDark);
    
    // Update CSS variables
    if (isDark) {
        document.documentElement.style.setProperty('--tg-theme-bg-color', '#1a1a1a');
        document.documentElement.style.setProperty('--tg-theme-text-color', '#ffffff');
        document.documentElement.style.setProperty('--tg-theme-hint-color', '#888888');
        document.documentElement.style.setProperty('--tg-theme-secondary-bg-color', '#2a2a2a');
    } else {
        document.documentElement.style.setProperty('--tg-theme-bg-color', '#ffffff');
        document.documentElement.style.setProperty('--tg-theme-text-color', '#000000');
        document.documentElement.style.setProperty('--tg-theme-hint-color', '#999999');
        document.documentElement.style.setProperty('--tg-theme-secondary-bg-color', '#f1f1f1');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Prefix input
    const prefixInput = document.getElementById('prefixInput');
    if (prefixInput) {
        prefixInput.addEventListener('input', function() {
            updateCharCount();
            validateInput();
        });
        
        prefixInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                startGeneration();
            }
        });
    }
    
    // Network selector
    const networkBtns = document.querySelectorAll('.network-btn');
    networkBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            selectNetwork(this.dataset.network);
        });
    });
}

// Update character count
function updateCharCount() {
    const input = document.getElementById('prefixInput');
    const count = document.getElementById('charCount');
    if (input && count) {
        const length = input.value.length;
        count.textContent = length;
        count.style.color = length > 6 ? '#dc3545' : '#999999';
    }
}

// Validate input
function validateInput() {
    const input = document.getElementById('prefixInput');
    const generateBtn = document.getElementById('generateBtn');
    
    if (!input || !generateBtn) return;
    
    const value = input.value.trim();
    const isValid = /^[A-Za-z0-9]+$/.test(value) && value.length > 0 && value.length <= 8;
    
    generateBtn.disabled = !isValid || appState.isGenerating;
}

// Select network
function selectNetwork(network) {
    appState.selectedNetwork = network;
    
    // Update UI
    document.querySelectorAll('.network-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.network === network);
    });
    
    updateNetworkBadge();
    showToast(`Network changed to ${network}`, 'info');
}

// Update network badge
function updateNetworkBadge() {
    const badge = document.getElementById('networkBadge');
    if (badge) {
        const dot = badge.querySelector('.network-dot');
        const text = badge.querySelector('span:last-child') || badge.lastChild;
        
        if (dot) {
            dot.className = `network-dot ${appState.selectedNetwork}`;
        }
        
        if (text && text.nodeType === Node.TEXT_NODE) {
            text.textContent = appState.selectedNetwork.charAt(0).toUpperCase() + appState.selectedNetwork.slice(1);
        }
    }
}

// Navigation functions
function showSection(section) {
    // Hide all sections
    document.querySelectorAll('section').forEach(s => s.classList.add('hidden'));
    
    // Show target section
    const targetSection = document.getElementById(section + 'Section');
    if (targetSection) {
        targetSection.classList.remove('hidden');
    }
    
    // Update navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const activeBtn = document.querySelector(`[onclick="showSection('${section}')"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
    
    // Update app state
    appState.currentSection = section;
    
    // Update Telegram buttons
    updateTelegramButtons();
}

function showWelcome() {
    showSection('welcome');
    tg.MainButton.setText('Generate Address');
    tg.MainButton.show();
    tg.BackButton.hide();
}

function showGenerator() {
    showSection('generator');
    tg.MainButton.setText('Generate Address');
    tg.MainButton.show();
    tg.BackButton.show();
}

function showResults() {
    showSection('results');
    tg.MainButton.hide();
    tg.BackButton.show();
}

function showHistory() {
    showSection('history');
    tg.MainButton.hide();
    tg.BackButton.show();
}

// Update Telegram buttons
function updateTelegramButtons() {
    switch (appState.currentSection) {
        case 'welcome':
            tg.MainButton.setText('Generate Address');
            tg.MainButton.show();
            tg.BackButton.hide();
            break;
        case 'generator':
            tg.MainButton.setText('Generate Address');
            tg.MainButton.show();
            tg.BackButton.show();
            break;
        case 'results':
        case 'history':
            tg.MainButton.hide();
            tg.BackButton.show();
            break;
    }
}

// Generation functions
async function startGeneration() {
    const prefix = document.getElementById('prefixInput').value.trim().toUpperCase();
    
    if (!prefix) {
        showToast('Please enter a prefix', 'error');
        return;
    }
    
    if (!/^[A-Z0-9]+$/.test(prefix)) {
        showToast('Prefix can only contain letters and numbers', 'error');
        return;
    }
    
    if (prefix.length > 8) {
        showToast('Prefix cannot be longer than 8 characters', 'error');
        return;
    }
    
    // Start generation
    appState.isGenerating = true;
    appState.currentGeneration = {
        prefix: prefix,
        network: appState.selectedNetwork,
        startTime: Date.now(),
        attempts: 0,
        isRunning: true
    };
    
    // Update UI
    updateGenerationUI();
    showProgress();
    
    // Start generation process
    await generateVanityAddress(prefix);
}

async function generateVanityAddress(prefix) {
    const generation = appState.currentGeneration;
    
    try {
        // Start generation on server
        const startResponse = await fetch('/api/generate/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prefix: prefix,
                network: appState.selectedNetwork,
                maxAttempts: 1000000
            })
        });
        
        if (!startResponse.ok) {
            throw new Error('Failed to start generation');
        }
        
        const startData = await startResponse.json();
        const generationId = startData.generationId;
        
        // Poll for progress
        const progressInterval = setInterval(async () => {
            if (!generation.isRunning) {
                clearInterval(progressInterval);
                return;
            }
            
            try {
                const statusResponse = await fetch(`/api/generate/${generationId}/status`);
                if (!statusResponse.ok) {
                    throw new Error('Failed to get status');
                }
                
                const statusData = await statusResponse.json();
                const status = statusData.data;
                
                // Update progress
                generation.attempts = status.attempts;
                updateProgress();
                
                // Check if generation is complete
                if (!status.isRunning) {
                    clearInterval(progressInterval);
                    
                    if (status.result && status.result.success) {
                        generationSuccess(prefix, status.result.attempts, status.result.timeTaken, status.result);
                    } else {
                        generationFailed(prefix, status.result.attempts, status.result.timeTaken);
                    }
                }
                
            } catch (error) {
                console.error('Status check error:', error);
                clearInterval(progressInterval);
                generationFailed(prefix, generation.attempts, Date.now() - generation.startTime);
            }
        }, 500);
        
        appState.generationInterval = progressInterval;
        
    } catch (error) {
        console.error('Generation error:', error);
        generationFailed(prefix, 0, 0);
    }
}

function generationSuccess(prefix, attempts, timeTaken, result) {
    const generation = appState.currentGeneration;
    generation.isRunning = false;
    
    // Save to history
    const historyItem = {
        id: Date.now(),
        prefix: prefix,
        address: result.publicKey,
        privateKey: result.privateKey,
        network: appState.selectedNetwork,
        attempts: attempts,
        timeTaken: timeTaken,
        timestamp: new Date().toISOString()
    };
    
    appState.history.unshift(historyItem);
    saveHistory();
    
    // Update UI
    showResults();
    displayResults(historyItem);
    
    // Reset state
    appState.isGenerating = false;
    appState.currentGeneration = null;
    
    showToast('Address generated successfully!', 'success');
}

function generationFailed(prefix, attempts, timeTaken) {
    const generation = appState.currentGeneration;
    generation.isRunning = false;
    
    // Reset state
    appState.isGenerating = false;
    appState.currentGeneration = null;
    
    updateGenerationUI();
    hideProgress();
    
    showToast('Generation failed. Try a shorter prefix.', 'error');
}

function generateFakeSolanaAddress(prefix) {
    // Generate a fake Solana address that starts with the prefix
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let address = prefix;
    
    // Fill the rest with random characters
    for (let i = prefix.length; i < 44; i++) {
        address += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    
    return address;
}

function stopGeneration() {
    if (appState.currentGeneration) {
        appState.currentGeneration.isRunning = false;
    }
    
    if (appState.generationInterval) {
        clearInterval(appState.generationInterval);
        appState.generationInterval = null;
    }
    
    appState.isGenerating = false;
    appState.currentGeneration = null;
    
    updateGenerationUI();
    hideProgress();
    
    showToast('Generation stopped', 'info');
}

// UI update functions
function updateGenerationUI() {
    const generateBtn = document.getElementById('generateBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const btnLoading = generateBtn.querySelector('.btn-loading');
    
    if (appState.isGenerating) {
        btnText.classList.add('hidden');
        btnLoading.classList.remove('hidden');
        generateBtn.disabled = true;
    } else {
        btnText.classList.remove('hidden');
        btnLoading.classList.add('hidden');
        generateBtn.disabled = false;
    }
}

function showProgress() {
    const progressSection = document.getElementById('progressSection');
    if (progressSection) {
        progressSection.classList.remove('hidden');
    }
}

function hideProgress() {
    const progressSection = document.getElementById('progressSection');
    if (progressSection) {
        progressSection.classList.add('hidden');
    }
}

function updateProgress() {
    const generation = appState.currentGeneration;
    if (!generation) return;
    
    const attemptsEl = document.getElementById('attemptsCount');
    const timeEl = document.getElementById('timeElapsed');
    const rateEl = document.getElementById('generationRate');
    
    if (attemptsEl) {
        attemptsEl.textContent = generation.attempts.toLocaleString();
    }
    
    if (timeEl) {
        const timeTaken = Math.floor((Date.now() - generation.startTime) / 1000);
        timeEl.textContent = `${timeTaken}s`;
    }
    
    if (rateEl) {
        const timeTaken = (Date.now() - generation.startTime) / 1000;
        const rate = timeTaken > 0 ? Math.floor(generation.attempts / timeTaken) : 0;
        rateEl.textContent = `${rate}/s`;
    }
}

function displayResults(historyItem) {
    const addressEl = document.getElementById('generatedAddress');
    const prefixEl = document.getElementById('generatedPrefix');
    const attemptsEl = document.getElementById('finalAttempts');
    const timeEl = document.getElementById('finalTime');
    
    if (addressEl) {
        const addressText = addressEl.querySelector('.address-text');
        if (addressText) {
            addressText.textContent = historyItem.address;
        }
    }
    
    if (prefixEl) {
        prefixEl.textContent = historyItem.prefix;
    }
    
    if (attemptsEl) {
        attemptsEl.textContent = historyItem.attempts.toLocaleString();
    }
    
    if (timeEl) {
        timeEl.textContent = `${Math.floor(historyItem.timeTaken / 1000)}s`;
    }
}

// History functions
function loadHistory() {
    const saved = localStorage.getItem('solanaVanityHistory');
    if (saved) {
        try {
            appState.history = JSON.parse(saved);
        } catch (e) {
            appState.history = [];
        }
    }
    updateHistoryDisplay();
}

function saveHistory() {
    localStorage.setItem('solanaVanityHistory', JSON.stringify(appState.history));
    updateHistoryDisplay();
}

function updateHistoryDisplay() {
    const historyList = document.getElementById('historyList');
    if (!historyList) return;
    
    historyList.innerHTML = '';
    
    if (appState.history.length === 0) {
        historyList.innerHTML = '<p style="text-align: center; color: var(--tg-theme-hint-color);">No generation history yet</p>';
        return;
    }
    
    appState.history.slice(0, 10).forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <div class="history-info">
                <div class="history-prefix">${item.prefix}</div>
                <div class="history-details">
                    ${item.attempts.toLocaleString()} attempts • ${Math.floor(item.timeTaken / 1000)}s • ${item.network}
                </div>
                <div class="history-address">${item.address}</div>
            </div>
        `;
        historyList.appendChild(historyItem);
    });
}

// Utility functions
function generateNew() {
    showGenerator();
    document.getElementById('prefixInput').value = '';
    updateCharCount();
    validateInput();
}

function copyToClipboard(type) {
    let text = '';
    
    if (type === 'address') {
        const addressText = document.querySelector('.address-text');
        if (addressText) {
            text = addressText.textContent;
        }
    }
    
    if (text) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            showToast('Failed to copy', 'error');
        });
    }
}

function downloadKeypair() {
    const addressText = document.querySelector('.address-text');
    if (!addressText) return;
    
    const address = addressText.textContent;
    const prefix = document.getElementById('generatedPrefix').textContent;
    
    // Find the current result in history
    const currentResult = appState.history.find(item => item.address === address);
    if (!currentResult) {
        showToast('Keypair data not found', 'error');
        return;
    }
    
    // Create the keypair JSON with real data
    const keypair = {
        publicKey: currentResult.address,
        privateKey: currentResult.privateKey,
        prefix: prefix,
        network: appState.selectedNetwork,
        attempts: currentResult.attempts,
        timeTaken: currentResult.timeTaken,
        generatedAt: currentResult.timestamp
    };
    
    const blob = new Blob([JSON.stringify(keypair, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `solana-keypair-${prefix}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showToast('Keypair downloaded!', 'success');
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

// Global functions for HTML onclick handlers
window.showSection = showSection;
window.showGenerator = showGenerator;
window.startGeneration = startGeneration;
window.stopGeneration = stopGeneration;
window.generateNew = generateNew;
window.copyToClipboard = copyToClipboard;
window.downloadKeypair = downloadKeypair;