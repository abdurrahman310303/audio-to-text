#!/bin/bash

echo "🎵 Starting Audio to Text Converter..."
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then run: source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment and start the app
echo "🚀 Activating virtual environment..."
source venv/bin/activate

echo "📱 Starting Flask application on port 8080..."
echo "🌐 Open your browser and go to: http://localhost:8080"
echo "⏹️  Press Ctrl+C to stop the application"
echo "======================================"

python app.py
