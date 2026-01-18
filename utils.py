"""Utility functions and helpers for cab navigation system."""

import logging
from typing import Optional, Dict, Any
import json
from datetime import datetime

logger = logging.getLogger("cab_navigation.utils")


def setup_logging(debug: bool = False, log_file: Optional[str] = None):
    """
    Setup logging configuration.
    
    Args:
        debug: Enable debug logging
        log_file: Optional log file path
    """
    import logging.handlers
    
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Root logger
    root_logger = logging.getLogger("cab_navigation")
    root_logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)


def format_currency(amount: float, currency: str = "INR") -> str:
    """Format amount as currency string."""
    if currency == "INR":
        return f"₹{amount:,.2f}"
    else:
        return f"{currency} {amount:,.2f}"


def format_time_estimate(minutes: str) -> str:
    """Parse and format time estimate string."""
    try:
        # Handle formats like "5 mins", "7-10 mins", "10 mins away"
        import re
        match = re.search(r'(\d+)(?:-(\d+))?\s+(?:mins?|minutes?)?', minutes.lower())
        if match:
            start = int(match.group(1))
            end = int(match.group(2)) if match.group(2) else start
            
            if start == end:
                return f"~{start} min"
            else:
                return f"{start}-{end} min"
    except Exception as e:
        logger.warning(f"Could not parse time: {minutes} - {e}")
    
    return minutes


def parse_fare_range(fare_string: str) -> Optional[tuple]:
    """Parse fare range string and return (min, max) as floats."""
    try:
        import re
        # Handle formats like "₹100-150", "100-150", "$100"
        numbers = re.findall(r'\d+(?:\.\d+)?', fare_string)
        if numbers:
            if len(numbers) >= 2:
                return (float(numbers[0]), float(numbers[1]))
            else:
                return (float(numbers[0]), float(numbers[0]))
    except Exception as e:
        logger.warning(f"Could not parse fare: {fare_string} - {e}")
    
    return None


def save_comparison_to_file(comparison_data: Dict[str, Any], filepath: str):
    """Save comparison results to JSON file."""
    try:
        data = {
            "timestamp": datetime.now().isoformat(),
            "comparison": {
                app: {
                    "ride_type": price.ride_type,
                    "estimated_price": price.estimated_price,
                    "estimated_time": price.estimated_time,
                    "distance": price.distance,
                    "available": price.available
                }
                for app, price in comparison_data.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Comparison saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving comparison: {str(e)}")


def save_booking_to_file(booking_info, filepath: str):
    """Save booking details to JSON file."""
    try:
        data = {
            "timestamp": datetime.now().isoformat(),
            "booking": booking_info.model_dump()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Booking saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving booking: {str(e)}")


def validate_phone_number(phone: str) -> bool:
    """Validate Indian phone number."""
    import re
    # Indian phone format: +91 or 0 followed by 10 digits
    pattern = r'^(?:\+91|0)?[6-9]\d{9}$'
    return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))


def validate_email(email: str) -> bool:
    """Validate email address."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def normalize_location(location: str) -> str:
    """Normalize location string."""
    # Trim whitespace
    location = location.strip()
    
    # Convert to title case
    location = location.title()
    
    # Common location mappings
    location_map = {
        "Airport": "Indira Gandhi International Airport",
        "Station": "New Delhi Railway Station",
        "T1": "Terminal 1, IGI Airport",
        "T2": "Terminal 2, IGI Airport",
        "T3": "Terminal 3, IGI Airport",
        "Igia": "Indira Gandhi International Airport"
    }
    
    return location_map.get(location, location)


def calculate_eta_in_minutes(eta_string: str) -> Optional[int]:
    """Extract number of minutes from ETA string."""
    try:
        import re
        match = re.search(r'(\d+)', eta_string)
        if match:
            return int(match.group(1))
    except Exception as e:
        logger.warning(f"Could not parse ETA: {eta_string} - {e}")
    
    return None


def get_best_deal(prices_dict: Dict[str, 'PriceInfo']) -> tuple:
    """
    Find the best deal from multiple prices.
    
    Returns:
        (app_name, price_info, savings_dict)
    """
    if not prices_dict:
        return None, None, {}
    
    # Find cheapest
    cheapest_app = min(prices_dict.keys(), key=lambda k: prices_dict[k].estimated_price)
    cheapest_price = prices_dict[cheapest_app].estimated_price
    
    # Calculate savings
    savings = {}
    for app, price in prices_dict.items():
        if app != cheapest_app:
            savings[app] = price.estimated_price - cheapest_price
    
    return cheapest_app, prices_dict[cheapest_app], savings


def print_comparison_table(prices_dict: Dict[str, 'PriceInfo']):
    """Print price comparison as formatted table."""
    if not prices_dict:
        print("No prices to display")
        return
    
    from tabulate import tabulate
    
    data = []
    for app, price in sorted(prices_dict.items(), key=lambda x: x[1].estimated_price):
        data.append([
            app,
            price.ride_type,
            format_currency(price.estimated_price),
            price.estimated_time,
            price.distance or "—"
        ])
    
    headers = ["App", "Ride Type", "Price", "ETA", "Distance"]
    print(tabulate(data, headers=headers, tablefmt="grid"))


class FareHistory:
    """Track fare history for comparisons."""
    
    def __init__(self, max_entries: int = 100):
        """Initialize fare history tracker."""
        self.history = []
        self.max_entries = max_entries
    
    def add_comparison(self, comparison_data: Dict[str, Any]):
        """Add a comparison to history."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "data": comparison_data
        }
        
        self.history.append(entry)
        
        # Keep only latest entries
        if len(self.history) > self.max_entries:
            self.history = self.history[-self.max_entries:]
    
    def get_average_price(self, app: str, ride_type: str) -> Optional[float]:
        """Get average price for specific app/ride type from history."""
        prices = [
            entry["data"][app].estimated_price
            for entry in self.history
            if app in entry["data"] and entry["data"][app].ride_type == ride_type
        ]
        
        return sum(prices) / len(prices) if prices else None
    
    def to_dict(self) -> Dict:
        """Convert history to dictionary."""
        return {"history": self.history, "total_entries": len(self.history)}
