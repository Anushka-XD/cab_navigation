#!/bin/bash

# Cab Navigation System - Setup Script
# This script sets up the development environment

set -e

echo "🚗 Cab Navigation System - Setup"
echo "=================================="

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null

# Create directories
echo "📁 Creating project directories..."
mkdir -p logs
mkdir -p config/app_cards

# Check adb
echo "📱 Checking Android Device Connection..."
if command -v adb &> /dev/null; then
    device_count=$(adb devices | grep -c "device$" || true)
    if [ "$device_count" -gt 0 ]; then
        echo "✓ Android device(s) found:"
        adb devices | grep "device$" || true
    else
        echo "⚠️  No Android devices found. Please connect a device and ensure adb is configured."
    fi
else
    echo "⚠️  adb not found. Please install Android SDK tools."
fi

# Setup .env file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Update .env with your API keys:"
    echo "   - GOOGLE_API_KEY or OPENAI_API_KEY"
else
    echo "✓ .env file already exists"
fi

# Verify imports
echo "🔍 Verifying imports..."
python3 -c "
from config import get_droidrun_config
from orchestrator import CabComparisonOrchestrator
from models import RidePreferences, PriceInfo, BookingInfo
from agents import UberAgent, OlaAgent, RapidoAgent
print('✓ All imports successful')
" || exit 1

echo ""
echo "=================================="
echo "✅ Setup completed successfully!"
echo "=================================="
echo ""
echo "📖 Next steps:"
echo "1. Update .env with your LLM API keys"
echo "2. Connect your Android device or emulator"
echo "3. Run: python main.py"
echo ""
echo "📚 For help: python main.py  (then type 'help')"
echo ""
