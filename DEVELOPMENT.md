# Development / Testing Guide

## Quick Start for Development

```bash
# 1. Setup
bash setup.sh
source venv/bin/activate

# 2. Configure environment
cp .env.example .env
# Edit .env and add your API keys

# 3. Run
python main.py
```

## Testing Individual Agents

### Test Uber Agent

```python
import asyncio
from config import get_droidrun_config
from agents import UberAgent
from models import RidePreferences

async def test_uber():
    agent = UberAgent(get_droidrun_config())
    
    # Test opening app
    success = await agent.open_app()
    print(f"App opened: {success}")
    
    # Test getting price
    prefs = RidePreferences(
        destination="Times Square",
        ride_type="car"
    )
    
    price = await agent.get_price(
        "Current Location",
        "Times Square",
        prefs
    )
    
    if price:
        print(f"Price: ₹{price.estimated_price}")
    
    await agent.close_app()

asyncio.run(test_uber())
```

### Test Orchestrator

```python
import asyncio
from config import get_droidrun_config
from orchestrator import CabComparisonOrchestrator
from models import RidePreferences

async def test_comparison():
    orch = CabComparisonOrchestrator(get_droidrun_config())
    
    prefs = RidePreferences(
        destination="Airport",
        ride_type="rickshaw"
    )
    
    comparison = await orch.compare_prices(
        "Current Location",
        "Airport",
        prefs
    )
    
    print(comparison.comparison_summary)

asyncio.run(test_comparison())
```

## Running with Debug Mode

```bash
export CAB_NAV_DEBUG=true
export LOG_LEVEL=DEBUG
python main.py
```

This will:
- Save trajectory screenshots to `trajectories/`
- Print debug logs
- Disable timeout errors for easier debugging

## Testing NLP Parser

```python
from tools.nlp_parser import parse_ride_preferences
import json

inputs = [
    "Go to airport as rickshaw",
    "Take me to Times Square, need AC auto",
    "Head to station with luggage",
    "3 people need premium car to airport"
]

for user_input in inputs:
    result = parse_ride_preferences(user_input)
    prefs = json.loads(result)
    print(f"Input: {user_input}")
    print(f"Parsed: {prefs}\n")
```

## Performance Testing

```bash
# Time a single price comparison
time python -c "
import asyncio
from orchestrator import CabComparisonOrchestrator
from models import RidePreferences
from config import get_droidrun_config

async def benchmark():
    orch = CabComparisonOrchestrator(get_droidrun_config())
    prefs = RidePreferences(destination='Airport')
    await orch.compare_prices('Current', 'Airport', prefs)

asyncio.run(benchmark())
"
```

## Adding New Ride Type

Edit `agents/base_agent.py` and update `_map_ride_type()` in each agent:

```python
def _map_ride_type(self, preference: str) -> str:
    mapping = {
        'car': 'UberGo',
        'rickshaw': 'Uber Auto',
        'luxury': 'Uber Black',  # NEW
        ...
    }
    return mapping.get(preference.lower(), 'UberGo')
```

## Extending for New App

1. Create `new_app_agent.py`:

```python
from agents import BaseCabAgent
from models import RidePreferences, PriceInfo

class NewAppAgent(BaseCabAgent):
    def __init__(self, config=None):
        super().__init__(
            app_name="NewApp",
            package_name="com.newapp.package",
            config=config
        )
    
    def _build_price_goal(self, pickup, dest, prefs):
        return f"""
        Open NewApp and get fare from {pickup} to {dest}
        for {prefs.ride_type} ride type
        """
    
    def _build_booking_goal(self, pickup, dest, prefs, price):
        return f"Book {prefs.ride_type} for ₹{price.estimated_price}"
```

2. Register in `orchestrator.py`:

```python
from agents import NewAppAgent

self.agents['newapp'] = NewAppAgent(self.config)
```

3. Test with CLI:

```bash
python main.py
# Select new app when testing
```

## Debugging Failed Bookings

When a booking fails:

1. Check logs: `tail -f logs/*.log`
2. Enable debug mode: `export CAB_NAV_DEBUG=true`
3. Check screenshots: `ls -la trajectories/`
4. Review specific agent goal: Check agent's `_build_booking_goal()`
5. Verify UI elements haven't changed in app

## Common Issues & Solutions

### Issue: App not opening
**Solution**: 
- Verify app is installed: `adb shell pm list packages | grep uber`
- Clear app cache: `adb shell pm clear com.ubercab`
- Restart device: `adb reboot`

### Issue: Price not extracted
**Solution**:
- Check if UI layout changed
- Review trajectory screenshot
- Verify Pydantic model fields match extracted data
- Increase timeout in `config.py`

### Issue: Slow price fetching
**Solution**:
- Improve network connectivity
- Close background apps on device
- Reduce `max_steps` in `AgentConfig`
- Enable caching (custom implementation)

### Issue: LLM API errors
**Solution**:
- Verify API key is set: `echo $GOOGLE_API_KEY`
- Check account quota/limits
- Test with simple prompt: `python -c "from llama_index.llms.gemini import Gemini; print(Gemini().complete('test'))"`

## Integration Testing Checklist

- [ ] All three agents can open their respective apps
- [ ] Price extraction works for each app
- [ ] Booking completes successfully  
- [ ] Cheapest app is correctly identified
- [ ] NLP parser handles various input formats
- [ ] Error handling works (no crashes)
- [ ] Logs are generated properly
- [ ] Timeouts are respected

## CI/CD Considerations

For automated testing:

1. Use headless Android emulator
2. Mock LLM responses for unit tests
3. Test each agent independently first
4. Integration test full workflow
5. Monitor success rates

Example test:

```python
import unittest
from unittest.mock import patch, MagicMock
from orchestrator import CabComparisonOrchestrator

class TestOrchestrator(unittest.TestCase):
    def test_price_comparison(self):
        # Mock agents
        with patch('orchestrator.UberAgent') as mock_uber:
            # Setup mock
            mock_agent = MagicMock()
            mock_uber.return_value = mock_agent
            
            # Test
            orch = CabComparisonOrchestrator()
            # Assert...
```

## Performance Optimization Tips

1. **Parallel fetching**: Already implemented
2. **Agent caching**: Cache LLM responses for same routes
3. **Device optimization**: Keep device cache clean
4. **Network**: Use stable WiFi
5. **App preloading**: Keep apps open to skip launch time
