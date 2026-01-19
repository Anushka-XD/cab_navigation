#!/bin/bash

# Cab Navigation System - Setup Script
# This script sets up the environment and configures Droidrun

set -e

echo "╔════════════════════════════════════════╗"
echo "║  CAB NAVIGATION SYSTEM - SETUP         ║"
echo "╚════════════════════════════════════════╝"
echo ""

# 1. Set the API key
echo "📝 Step 1: Setting Google API Key..."
export GOOGLE_API_KEY="your gemini key"
echo "✓ API Key set"
echo ""

# 2. Activate virtual environment
echo "🐍 Step 2: Activating virtual environment..."
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# 3. Verify dependencies
echo "📦 Step 3: Verifying dependencies..."
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt
echo "✓ Dependencies verified"
echo ""

# 4. Verify Droidrun config
echo "⚙️  Step 4: Checking Droidrun configuration..."
if [ ! -f "$HOME/.droidrun/config.yaml" ]; then
    echo "⚠️  Warning: ~/.droidrun/config.yaml not found"
    echo "Please ensure Droidrun is properly configured"
else
    echo "✓ Droidrun config found"
fi
echo ""

# 5. Create logs directory
echo "📁 Step 5: Creating logs directory..."
mkdir -p logs
echo "✓ Logs directory ready"
echo ""

echo "✅ Setup complete!"
echo ""
echo "📌 To run the cab navigation system:"
echo "   python main.py"
echo ""
echo "🔑 Environment variable reminder:"
echo "   export GOOGLE_API_KEY=your_gemini_key"
echo ""
