# Cab Navigation System - Production-Ready Agent

An intelligent, modular Python system that automatically compares cab fares across multiple apps (Uber, Ola, Rapido) and books the cheapest option.

## Features

✅ **Multi-App Price Comparison** - Simultaneously fetch and compare prices from Uber, Ola, and Rapido
✅ **Natural Language Processing** - Parse user requests like "Go to airport as rickshaw"
✅ **Automatic Booking** - Books the cheapest ride with a single command
✅ **Modular Architecture** - Each app has its own agent, easy to extend
✅ **Structured Data Extraction** - Uses Pydantic models for type-safe data
✅ **Production Ready** - Comprehensive error handling, logging, and configuration
✅ **Flexible Preferences** - Support for ride types (car, rickshaw, bike, premium), passengers, luggage, AC, budget

## Project Structure

```
cab_navigation/
├── agents/                 # App-specific agents
│   ├── base_agent.py      # Abstract base class with common logic
│   ├── uber_agent.py      # Uber implementation
│   ├── ola_agent.py       # Ola implementation
│   └── rapido_agent.py    # Rapido implementation
├── models/                 # Pydantic data models
│   ├── ride_preferences.py # User preferences
│   ├── price_info.py      # Pricing data
│   └── booking_info.py    # Booking confirmation
├── tools/                  # Custom utilities
│   ├── nlp_parser.py      # NLP and text processing
│   ├── location_handler.py # Location utilities
│   └── price_comparator.py # Price comparison logic
├── orchestrator.py        # Main coordinator
├── config.py              # Configuration & settings
├── main.py                # CLI entry point
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.8+
- Android device or emulator with adb connection
- Uber, Ola, and Rapido apps installed on device

### Setup

1. **Clone/Create project:**
   ```bash
   cd /Users/anushka/cab_navigation
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure LLM API keys:**
   ```bash
   export GOOGLE_API_KEY="your-google-api-key"
   # or
   export OPENAI_API_KEY="your-openai-api-key"
   ```

5. **Set Android device (if not auto-detected):**
   ```bash
   export ANDROID_DEVICE_SERIAL="your-device-serial"
   ```

## Usage

### Command-Line Interface

```bash
python main.py
```

### Example Interactions

```
→ Go to airport as rickshaw
✓ Preferences extracted:
   Destination: Airport
   Ride Type: rickshaw
   Passengers: 1

🚀 Comparing prices across Uber, Ola, and Rapido...
   From: Current Location
   To: Airport

💰 Price Comparison Results:
==================================================

🥇 #1 OLA
   Ride Type: Ola Auto
   Fare: ₹450
   ETA: 5 mins
   Distance: 15 km

🥈 #2 RAPIDO
   Ride Type: Auto
   Fare: ₹480
   ETA: 6 mins
   Distance: 15 km

🥉 #3 UBER
   Ride Type: Uber Auto
   Fare: ₹520
   ETA: 8 mins
   Distance: 15 km

==================================================
✅ Cheapest Option: OLA (₹450)

🎯 Book the cheapest ride? (yes/no): yes

📱 Booking on OLA...
✅ Ride Booked Successfully!
   App: Ola
   Booking ID: OLA123456789
   Ride Type: Ola Auto
   Fare: ₹450
   Driver: Rajesh Kumar (4.8⭐)
   ETA: 4 mins
   Vehicle: DL01AB1234, White Auto
```

## Supported Ride Types

- **car** / economy - Standard sedan
- **rickshaw** / auto-rickshaw / auto - Auto-rickshaw (three-wheeler)
- **bike** / two-wheeler / motorcycle - Bike/motorcycle
- **premium** / comfort / xl - Premium/comfortable vehicles

## Supported Apps

- **Uber** - Comprehensive ride options
- **Ola** - India's leading cab service
- **Rapido** - Bike and auto focus

## Configuration

### Environment Variables

```bash
# Debug mode (more logs, trajectory saving)
export CAB_NAV_DEBUG=true

# Device configuration
export ANDROID_DEVICE_SERIAL=device-serial
export USE_TCP=true  # Use TCP instead of USB
export PLATFORM=android  # or "ios"

# LLM Configuration
export GOOGLE_API_KEY=your-key
export OPENAI_API_KEY=your-key
```

### Python Configuration

Edit `config.py` to customize:

- Agent behavior (`max_steps`, `reasoning` mode)
- Timeouts (`COMPARISON_TIMEOUT`, `BOOKING_TIMEOUT`)
- Default apps to compare
- Logging level and output

## Architecture

### Data Models

**RidePreferences** - Parsed from user input
- destination
- ride_type (car, rickshaw, bike, premium)
- passengers
- luggage (boolean)
- ac_preference
- budget_constraint

**PriceInfo** - Extracted from app
- app_name
- ride_type
- estimated_price
- estimated_time
- distance
- extra_charges

**BookingInfo** - Confirmation data
- booking_id
- driver details
- vehicle info
- estimated fare & arrival

### Agent Pattern

Each app agent inherits from `BaseCabAgent`:

1. **Open App** - Launch the cab service
2. **Get Price** - Extract fare estimates using Droidrun + Pydantic structured output
3. **Book Ride** - Complete the booking workflow
4. **Close App** - Clean shutdown

App-specific agents override goal builders to handle UI differences.

### Custom Tools

- **nlp_parser.py** - Parse natural language, compare prices
- **location_handler.py** - Location validation and formatting
- **price_comparator.py** - Filter and compare fares

## Advanced Usage

### Programmatic Usage

```python
import asyncio
from orchestrator import CabComparisonOrchestrator
from models.ride_preferences import RidePreferences
from config import get_droidrun_config

async def book_ride():
    orchestrator = CabComparisonOrchestrator(get_droidrun_config())
    
    # Define preferences
    prefs = RidePreferences(
        destination="Airport",
        ride_type="car",
        passengers=1
    )
    
    # Compare prices
    comparison = await orchestrator.compare_prices(
        pickup_location="Times Square",
        destination="Airport",
        preferences=prefs
    )
    
    print(comparison.comparison_summary)
    
    # Book cheapest
    booking = await orchestrator.book_cheapest(
        pickup_location="Times Square",
        destination="Airport",
        preferences=prefs,
        comparison=comparison
    )
    
    if booking:
        print(f"Booked on {booking.app_name}: {booking.booking_id}")

asyncio.run(book_ride())
```

### Extending for New Apps

1. Create new agent class inheriting from `BaseCabAgent`:

```python
from agents import BaseCabAgent
from models import RidePreferences, PriceInfo

class NewAppAgent(BaseCabAgent):
    def __init__(self, config=None):
        super().__init__(app_name="NewApp", package_name="com.newapp", config=config)
    
    def _build_price_goal(self, pickup, destination, prefs):
        # Customize goal for your app
        return f"Get price from {pickup} to {destination}"
    
    def _build_booking_goal(self, pickup, destination, prefs, price):
        return f"Book {prefs.ride_type} for ₹{price.estimated_price}"
```

2. Register in orchestrator:

```python
orchestrator.agents['newapp'] = NewAppAgent(config)
```

## Error Handling

The system includes comprehensive error handling:

- **Device Connectivity** - Checks if device is connected
- **App Availability** - Validates apps are installed
- **Network Errors** - Handles API/network failures
- **Extraction Failures** - Falls back gracefully if data extraction fails
- **Timeout Handling** - Manages long-running operations

## Performance

- **Parallel Fetching** - Fetches prices from all apps simultaneously
- **Timeout Protection** - Prevents hanging on slow responses
- **Smart Retries** - Implements backoff for transient failures
- **Memory Efficient** - Closes apps after each operation

## Troubleshooting

### Apps not detected

```bash
# Check connected devices
adb devices

# Set specific device
export ANDROID_DEVICE_SERIAL=emulator-5554
```

### Price extraction failing

- Ensure apps are in English
- Check device screen brightness (some apps require it)
- Enable `CAB_NAV_DEBUG=true` for trajectory logs

### LLM API errors

```bash
# Verify API keys
echo $GOOGLE_API_KEY
echo $OPENAI_API_KEY

# Test connection
python -c "from llama_index.llms.gemini import Gemini; Gemini().complete('test')"
```

### Booking timeout

- Increase `BOOKING_TIMEOUT` in config.py
- Ensure device has good internet
- Check if app has network issues

## Logging

Logs are saved to `logs/` directory:

```bash
tail -f logs/cab_navigation.log
```

Enable detailed logs:

```bash
export CAB_NAV_DEBUG=true
python main.py
```

## Production Deployment

For production use:

1. **Use environment-based config**
   ```python
   from config import get_droidrun_config
   config = get_droidrun_config()
   ```

2. **Implement persistent storage** for bookings/history
3. **Add rate limiting** if running as a service
4. **Set up monitoring/alerting** for failures
5. **Use credentials manager** for API keys
6. **Run on dedicated device** or emulator

## Performance Metrics

- **Price Comparison**: ~30-60 seconds (parallel across 3 apps)
- **Single App Query**: ~15-25 seconds
- **Booking**: ~30-90 seconds
- **Memory**: ~150-200MB typical

## Security Considerations

- API keys never logged (use environment variables)
- Device credentials handled securely by Droidrun
- User preferences stored only in memory
- Booking IDs should be stored securely in production

## Contributing

Areas for improvement:

- Add support for more cab services
- Improve NLP parsing (integrate spaCy/BERT)
- Add booking history/favorites
- Implement user preferences caching
- Add real-time tracking
- Multi-language support

## License

MIT License - See LICENSE file

## Support

For issues or questions:

1. Check troubleshooting section above
2. Enable debug mode and check logs
3. Verify device connection and apps
4. Test individual agents separately

## Future Enhancements

- [ ] Real-time tracking post-booking
- [ ] Saved addresses and preferences
- [ ] Historical fare data analysis
- [ ] Predictive pricing
- [ ] Multi-passenger coordination
- [ ] Integration with calendar (for scheduled rides)
- [ ] Automatic ride scheduling
- [ ] Bill splitting functionality
- [ ] Corporate ride management
- [ ] AI-powered driver ratings and reviews
