"""Configuration for cab navigation system."""

import os
from pathlib import Path
from droidrun import DroidrunConfig

# Set API key before Droidrun initializes
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "AIzaSyAgmAmBrQfVOHgM41RDbpUNA6E8PLFgFBE")

# Project root
PROJECT_ROOT = Path(__file__).parent

# Get from environment or use defaults
DEBUG = os.getenv("CAB_NAV_DEBUG", "false").lower() == "true"
DEVICE_SERIAL = os.getenv("ANDROID_DEVICE_SERIAL", None)
PLATFORM = os.getenv("PLATFORM", "android")  # "android" or "ios"
USE_TCP = os.getenv("USE_TCP", "false").lower() == "true"

# Logging
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# App package names
APP_PACKAGES = {
    "uber": "com.ubercab",
    "ola": "com.olacabs.customer",
    "rapido": "com.rapido.passenger"
}

# Common destinations with keywords for smart matching
COMMON_DESTINATIONS = {
    "work": ["work", "office", "workplace", "company"],
    "home": ["home", "house", "apartment", "residence"],
    "jaypee institute of information technology sec 62 noida": [
        "jaypee", "jiit", "sec 62", "sector 62", "noida"
    ],
    "jaypee institute of information technology sec 128 jaypee wishtown noida": [
        "jaypee", "jiit", "sec 128", "sector 128", "wishtown", "noida"
    ]
}

# Droidrun configuration - loads from ~/.droidrun/config.yaml
def get_droidrun_config() -> DroidrunConfig:
    """
    Get DroidrunConfig which loads from ~/.droidrun/config.yaml.
    
    The ~/.droidrun/config.yaml file should contain:
    - LLM profiles (manager, executor, codeact, etc.)
    - Device configuration
    - Logging settings
    - App cards configuration
    
    Returns:
        DroidrunConfig instance
    """
    # DroidrunConfig() automatically loads from ~/.droidrun/config.yaml
    # Ensure GOOGLE_API_KEY is set in environment before initialization
    config = DroidrunConfig()
    return config


# UI/UX Configuration
COMPARISON_TIMEOUT = 180  # seconds
BOOKING_TIMEOUT = 300    # seconds
DEFAULT_APPS = ["uber", "ola", "rapido"]

# Messages
WELCOME_MESSAGE = """
╔════════════════════════════════════════╗
║     🚗 CAB NAVIGATION SYSTEM 🚗        ║
║                                        ║
║  Automatically compare prices and     ║
║  book the cheapest cab ride!          ║
╚════════════════════════════════════════╝
"""

HELP_MESSAGE = """
USAGE EXAMPLES:
  • "Go to airport as rickshaw"
  • "Take me to Times Square by car"
  • "Go to central station, need AC auto"
  • "Head to station, 2 people, rickshaw preferred"
  • "Go to airport with luggage, premium car"

COMMON DESTINATIONS:
  > work
  > home
  > jaypee institute of information technology sec 62 noida
  > jaypee institute of information technology sec 128, jaypee wishtown noida

SUPPORTED RIDE TYPES:
  • car / economy
  • rickshaw / auto-rickshaw / auto
  • bike / two-wheeler
  • premium / comfort / xl

APPS SUPPORTED:
  ✓ Uber
  ✓ Ola
  ✓ Rapido
"""
