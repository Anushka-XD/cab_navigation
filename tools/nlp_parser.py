"""Utility tools for cab navigation."""

import logging
from typing import Dict, Any

logger = logging.getLogger("cab_navigation")


def _match_destination(user_input: str) -> str:
    """
    Smart destination matching using common destinations.
    
    First looks for keyword matches in COMMON_DESTINATIONS.
    If multiple matches found, uses more precise keywords to disambiguate.
    
    Args:
        user_input: User input string
    
    Returns:
        Matched destination or extracted text
    """
    from config import COMMON_DESTINATIONS
    
    user_lower = user_input.lower()
    
    # Find all matching destinations based on keywords
    matches = {}
    for dest_full_name, keywords in COMMON_DESTINATIONS.items():
        matching_keywords = [kw for kw in keywords if kw in user_lower]
        if matching_keywords:
            matches[dest_full_name] = len(matching_keywords)
    
    # If no matches, return extracted destination
    if not matches:
        return None
    
    # If single match, return it
    if len(matches) == 1:
        return list(matches.keys())[0]
    
    # If multiple matches (e.g., both sec 62 and sec 128 jaypee)
    # Look for disambiguating keywords
    if len(matches) > 1:
        logger.info(f"Multiple destination matches found: {list(matches.keys())}")
        
        # Look for more precise keywords
        for dest_full_name, keywords in COMMON_DESTINATIONS.items():
            if dest_full_name not in matches:
                continue
            
            # Check for highly specific keywords (e.g., "sec 62" vs "sec 128")
            specific_keywords = [kw for kw in keywords if len(kw) > 3 and kw.isdigit() or "sec" in kw or "sector" in kw]
            specific_matches = [kw for kw in specific_keywords if kw in user_lower]
            
            if specific_matches:
                logger.info(f"Disambiguated to: {dest_full_name} using keywords: {specific_matches}")
                return dest_full_name
        
        # If still ambiguous, return the one with most keyword matches
        best_match = max(matches.items(), key=lambda x: x[1])[0]
        logger.info(f"Using best match: {best_match}")
        return best_match
    
    return None


def parse_ride_preferences(user_input: str, **kwargs) -> str:
    """
    Parse natural language user input to extract ride preferences.
    
    Args:
        user_input: Natural language input from user (e.g., "Go to airport in a rickshaw")
    
    Returns:
        JSON-formatted string with extracted preferences
    """
    try:
        import re
        from models.ride_preferences import RidePreferences
        
        logger.info(f"Parsing ride preferences from: {user_input}")
        
        # Try smart destination matching first
        destination = _match_destination(user_input)
        
        # If no common destination matched, extract using regex
        if not destination:
            destination_match = re.search(
                r'(?:to|go to|take me to|head to|towards?|near)\s+([a-zA-Z\s]+?)(?:\s+(?:in|by|using|with|as|please|now))?',
                user_input.lower()
            )
            destination = destination_match.group(1).strip() if destination_match else "current location"
        
        logger.info(f"Destination matched: {destination}")
        
        # Detect ride type from keywords
        ride_type = "car"
        if any(word in user_input.lower() for word in ['rick', 'rickshaw', 'auto-rickshaw']):
            ride_type = "rickshaw"
        elif any(word in user_input.lower() for word in ['bike', 'motorcycle', 'two-wheeler']):
            ride_type = "bike"
        elif any(word in user_input.lower() for word in ['auto', 'auto rickshaw']):
            ride_type = "auto"
        elif any(word in user_input.lower() for word in ['premium', 'comfortable', 'xl', 'suv']):
            ride_type = "premium"
        
        # Detect AC preference
        ac_preference = None
        if 'ac' in user_input.lower() or 'air' in user_input.lower():
            ac_preference = True
        elif any(word in user_input.lower() for word in ['no ac', 'without ac', 'non-ac']):
            ac_preference = False
        
        # Detect luggage requirement
        luggage = any(word in user_input.lower() for word in ['luggage', 'bag', 'baggage', 'suitcase'])
        
        # Detect passenger count
        passengers = 1
        if 'we' in user_input.lower() or 'us' in user_input.lower():
            # Try to extract number
            num_match = re.search(r'(\d+)\s+(?:of us|people|passengers|persons)', user_input.lower())
            if num_match:
                passengers = int(num_match.group(1))
        
        # Create preferences object
        prefs = RidePreferences(
            destination=destination,
            ride_type=ride_type,
            passengers=passengers,
            luggage=luggage,
            ac_preference=ac_preference
        )
        
        logger.info(f"Extracted preferences: {prefs.model_dump()}")
        return prefs.model_dump_json()
        
    except Exception as e:
        logger.error(f"Error parsing preferences: {str(e)}")
        return f"Error: {str(e)}"


def compare_prices(prices_json: str, **kwargs) -> str:
    """
    Compare prices from different cab services and return sorted list.
    
    Args:
        prices_json: JSON string containing list of PriceInfo objects
    
    Returns:
        String with comparison results
    """
    try:
        import json
        
        logger.info("Comparing prices from all services")
        prices_data = json.loads(prices_json)
        
        if not prices_data:
            return "No prices available to compare"
        
        # Sort by price
        sorted_prices = sorted(
            prices_data,
            key=lambda x: x.get('estimated_price', float('inf'))
        )
        
        comparison = "Price Comparison:\n"
        for i, price in enumerate(sorted_prices, 1):
            comparison += f"{i}. {price['app_name']} - {price['ride_type']}: ₹{price['estimated_price']} ({price['estimated_time']})\n"
        
        logger.info(f"Price comparison completed. Cheapest: {sorted_prices[0]['app_name']}")
        return comparison
        
    except Exception as e:
        logger.error(f"Error comparing prices: {str(e)}")
        return f"Error: {str(e)}"


def validate_location(location: str, **kwargs) -> str:
    """
    Validate and normalize location string.
    
    Args:
        location: Location name or address
    
    Returns:
        Validated location string
    """
    try:
        logger.info(f"Validating location: {location}")
        
        # Basic normalization
        location = location.strip()
        
        # Check if it's a common location or needs clarification
        common_locations = {
            'airport': 'Indira Gandhi International Airport',
            'igai': 'Indira Gandhi International Airport',
            'railway station': 'New Delhi Railway Station',
            'station': 'New Delhi Railway Station',
            'home': 'Home',
            'office': 'Office'
        }
        
        location_lower = location.lower()
        normalized = common_locations.get(location_lower, location)
        
        logger.info(f"Location validated: {normalized}")
        return normalized
        
    except Exception as e:
        logger.error(f"Error validating location: {str(e)}")
        return f"Error: {str(e)}"
