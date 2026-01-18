# Quick Start Guide

## 5-Minute Setup

### 1. Install
```bash
bash setup.sh
```

### 2. Configure API Keys
```bash
# Copy template
cp .env.example .env

# Edit .env and add ONE of these:
# - GOOGLE_API_KEY (recommended - faster)
# - OPENAI_API_KEY
# - ANTHROPIC_API_KEY
```

### 3. Connect Device
```bash
# List devices
adb devices

# Ensure Uber, Ola, Rapido are installed
```

### 4. Run
```bash
python main.py
```

### 5. Try It!
```
→ Go to airport as rickshaw

[System compares prices from all 3 apps...]

→ Book the cheapest ride? (yes/no): yes

✅ Ride booked!
```

---

## Usage Examples

### Command-Line Examples

```bash
# Standard booking
python main.py

# With debug logging
CAB_NAV_DEBUG=true python main.py

# Specify device
ANDROID_DEVICE_SERIAL=emulator-5554 python main.py
```

### Programmatic Examples

```python
import asyncio
from orchestrator import CabComparisonOrchestrator
from models import RidePreferences
from config import get_droidrun_config

async def quick_book():
    # Setup
    orch = CabComparisonOrchestrator(get_droidrun_config())
    
    # Create preferences
    prefs = RidePreferences(
        destination="Airport",
        ride_type="rickshaw",
        passengers=1
    )
    
    # Compare and book
    booking = await orch.book_cheapest(
        "Current Location",
        "Airport",
        prefs
    )
    
    print(f"✅ Booked on {booking.app_name}!")

asyncio.run(quick_book())
```

---

## Natural Language Examples

The system understands various ways to express your preferences:

```
"Go to airport as rickshaw"
↓
destination=Airport, ride_type=rickshaw

"Take me to Times Square in a premium car"
↓
destination=Times Square, ride_type=premium

"Head to central station, 2 people, need AC"
↓
destination=central station, passengers=2, ac_preference=True

"Go to the station with luggage on a bike"
↓
destination=station, luggage=True, ride_type=bike

"Take me to office, budget is 500 rupees"
↓
destination=office, budget_constraint=500
```

---

## Troubleshooting

### Apps not detected
```bash
# Check device is connected
adb devices

# Set correct device
export ANDROID_DEVICE_SERIAL=your-device-id

# Verify apps are installed
adb shell pm list packages | grep -E "ubercab|olacabs|rapido"
```

### API key errors
```bash
# Verify API key is set
echo $GOOGLE_API_KEY

# Test LLM connection
python -c "from llama_index.llms.gemini import Gemini; print('OK')"
```

### Price extraction failing
```bash
# Enable debug mode to see screenshots
export CAB_NAV_DEBUG=true
python main.py

# Check trajectories folder for UI screenshots
ls -la trajectories/
```

---

## Project Structure

```
cab_navigation/
├── agents/              # App-specific agents
│   ├── base_agent.py    # Abstract base class
│   ├── uber_agent.py    # Uber implementation
│   ├── ola_agent.py     # Ola implementation
│   └── rapido_agent.py  # Rapido implementation
│
├── models/              # Pydantic data models
│   ├── ride_preferences.py
│   ├── price_info.py
│   └── booking_info.py
│
├── tools/               # Custom utilities
│   ├── nlp_parser.py
│   ├── location_handler.py
│   └── price_comparator.py
│
├── config/              # Configuration & guides
│   ├── app_cards.json
│   ├── uber.md
│   ├── ola.md
│   └── rapido.md
│
├── orchestrator.py      # Main coordinator
├── config.py            # Configuration
├── main.py              # CLI entry point
├── utils.py             # Utilities
├── requirements.txt     # Dependencies
├── setup.sh             # Setup script
├── Makefile             # Task automation
│
├── README.md            # Full documentation
├── DEVELOPMENT.md       # Developer guide
├── API_REFERENCE.md     # API docs
└── QUICK_START.md       # This file
```

---

## Key Features

✅ **Multi-App Comparison** - Parallel price fetching from Uber, Ola, Rapido
✅ **Natural Language** - Parse user preferences from text
✅ **Automatic Booking** - Books the cheapest option
✅ **Modular Design** - Easy to extend with new apps
✅ **Production Ready** - Logging, error handling, configuration
✅ **Type Safe** - Pydantic models for data validation
✅ **Flexible** - Support for ride types, preferences, budgets

---

## Common Tasks

### Make Commands
```bash
make help       # Show all commands
make run        # Run the app
make debug      # Run with debug mode
make setup      # Setup project
make clean      # Clean cache
make lint       # Check code style
make format     # Format code
```

### Check Device Connection
```bash
adb devices -l
```

### View Logs
```bash
tail -f logs/*.log
```

### Test Individual Agent
```python
from agents import UberAgent
agent = UberAgent()
await agent.open_app()
```

---

## API Keys Setup

### Option 1: Google (Recommended)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project
3. Enable Gemini API
4. Create API key
5. Add to .env: `GOOGLE_API_KEY=your-key`

### Option 2: OpenAI
1. Go to [OpenAI](https://platform.openai.com/api-keys)
2. Create API key
3. Add to .env: `OPENAI_API_KEY=your-key`

### Option 3: Anthropic
1. Go to [Anthropic](https://console.anthropic.com)
2. Get API key
3. Add to .env: `ANTHROPIC_API_KEY=your-key`

---

## Device Setup

### Android Emulator
```bash
# If using emulator
emulator -avd your-emulator-name

# Get serial
adb devices
# emulator-5554 is typical default
```

### Physical Android Device
```bash
# Enable USB debugging
# Settings > Developer Options > USB Debugging

# Connect via USB
adb devices

# View device serial
```

### Verify Cab Apps Installed
```bash
adb shell pm list packages | grep -E "ubercab|olacabs|rapido"

# If not installed, install via:
# adb install app.apk
# Or install manually from Play Store
```

---

## Performance Tips

1. **Use WiFi** - Stable connection improves extraction
2. **Keep Device Clean** - Close background apps
3. **Set Brightness** - Some apps need good lighting
4. **Use Emulator** - More stable than physical device for automation
5. **Cache Results** - Implement caching for frequently checked routes

---

## Next Steps

1. ✅ Run `bash setup.sh`
2. ✅ Configure `.env` with API key
3. ✅ Connect Android device
4. ✅ Run `python main.py`
5. 📚 Check `README.md` for full documentation
6. 🔧 See `DEVELOPMENT.md` for extending the system
7. 📖 Check `API_REFERENCE.md` for programmatic usage

---

## Support

- **Issue**: Check [README.md](README.md#troubleshooting)
- **Code Help**: See [API_REFERENCE.md](API_REFERENCE.md)
- **Development**: See [DEVELOPMENT.md](DEVELOPMENT.md)
- **Questions**: Review [README.md](README.md)

Happy booking! 🚗
