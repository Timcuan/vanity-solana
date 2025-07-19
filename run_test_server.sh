#!/bin/bash

echo "🧪 Starting Test Web Server..."

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip3 install -r requirements.txt

# Start the test server
echo "🚀 Starting test server on http://localhost:8080"
echo "📱 Open your browser and navigate to the URL above"
echo "🛑 Press Ctrl+C to stop"

python3 test_web_server.py
