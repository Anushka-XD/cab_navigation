# 🚗 Cab Navigation System - Setup Guide

## Prerequisites

1. **Droidrun installed** and configured at `~/.droidrun/config.yaml`
2. **Python 3.11+**
3. **Android device or emulator** connected via ADB

## Quick Start - Terminal Commands

### 1️⃣ Set Environment Variable

```bash
export GOOGLE_API_KEY="your gemini key"
```

### 2️⃣ Create Virtual Environment

```bash
cd /Users/anushka/cab_navigation
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Verify Droidrun Configuration

Your `~/.droidrun/config.yaml` should have:

```yaml
llm_profiles:
  codeact:
    provider: GoogleGenAI
    model: models/gemini-2.5-flash
    temperature: 0.2
    
  manager:
    provider: GoogleGenAI
    model: models/gemini-2.5-pro
    temperature: 0.2
    
  executor:
    provider: GoogleGenAI
    model: models/gemini-2.5-flash
    temperature: 0.1

device:
  platform: android
  serial: null  # auto-detect

agent:
  max_steps: 20
  reasoning: true
```

### 5️⃣ Run the Application

```bash
python main.py
```

## Usage

Once running, enter commands like:

```
→ Go to airport
→ Take me to JIIT as auto-rickshaw
→ Head to metro station with 2 people, need AC
→ Go home
```

## How It Works

1. **Parses your input** using NLP to extract:
   - Destination
   - Ride type (car, auto-rickshaw, bike)
   - Special requirements (luggage, AC, passengers)

2. **Compares prices** across:
   - 🚕 Uber
   - 🏎️ Ola
   - 🏍️ Rapido

3. **Books the cheapest** option automatically

## Troubleshooting

### "Missing key inputs argument" Error

```bash
# Solution: Set the API key before running
export GOOGLE_API_KEY=your_gemini_key
python main.py
```

### "Could not fetch prices from any app"

```bash
# 1. Check device connection
adb devices

# 2. Verify Droidrun is installed
pip list | grep droidrun

# 3. Check ~/.droidrun/config.yaml exists and is valid
cat ~/.droidrun/config.yaml
```

### Device not detected

```bash
# 1. List connected devices
adb devices

# 2. If emulator: start it first
emulator -avd <device_name>

# 3. Verify ADB connection
adb shell echo "test"
```

## Configuration Files

- **`config.py`** - Project settings, loads DroidrunConfig from `~/.droidrun/config.yaml`
- **`models/`** - Pydantic data models for Price, Booking, Preferences
- **`agents/`** - App-specific agents (Uber, Ola, Rapido)
- **`tools/`** - Utilities for NLP, location, price comparison

## Project Structure

```
cab_navigation/
├── main.py                 # Entry point
├── config.py              # Configuration (loads ~/.droidrun/config.yaml)
├── orchestrator.py        # Main orchestration logic
├── agents/                # App-specific agents
│   ├── base_agent.py      # Abstract base class
│   ├── uber_agent.py
│   ├── ola_agent.py
│   └── rapido_agent.py
├── models/                # Pydantic models
├── tools/                 # Utilities
└── logs/                  # Application logs
```

## Next Steps

1. Ensure `~/.droidrun/config.yaml` is properly configured
2. Connect your Android device
3. Set the environment variable and run!

For more help: Check DEVELOPMENT.md and API_REFERENCE.md
