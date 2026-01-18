"""Price comparison and filtering utilities."""

import logging
from typing import List, Dict, Any

logger = logging.getLogger("cab_navigation")


def filter_by_ride_type(prices: List[Dict], ride_type: str, **kwargs) -> str:
    """
    Filter prices by specific ride type.
    
    Args:
        prices: List of price info dictionaries
        ride_type: Ride type to filter by (car, rickshaw, bike, etc.)
    
    Returns:
        Filtered prices JSON string
    """
    try:
        import json
        
        logger.info(f"Filtering prices for ride type: {ride_type}")
        
        # Map ride type to app-specific equivalents
        ride_type_mapping = {
            'car': ['UberGo', 'Ola Prime', 'Rapido Bike', 'economy'],
            'rickshaw': ['Auto', 'Ola Auto', 'Rickshaw'],
            'bike': ['Rapido', 'UberMoto', 'Bike'],
            'premium': ['UberX', 'Comfort+', 'Premium']
        }
        
        ride_types_to_match = ride_type_mapping.get(ride_type.lower(), [ride_type])
        
        filtered = [
            p for p in prices 
            if any(rt.lower() in p.get('ride_type', '').lower() for rt in ride_types_to_match)
            or p.get('ride_type', '').lower() == ride_type.lower()
        ]
        
        logger.info(f"Filtered {len(filtered)} prices from {len(prices)} total")
        return json.dumps(filtered)
        
    except Exception as e:
        logger.error(f"Error filtering by ride type: {str(e)}")
        return f"Error: {str(e)}"


def find_cheapest(prices: List[Dict], **kwargs) -> str:
    """
    Find the cheapest option from prices list.
    
    Args:
        prices: List of price info dictionaries
    
    Returns:
        Cheapest option details
    """
    try:
        import json
        
        logger.info("Finding cheapest option")
        
        if not prices:
            return "No prices available"
        
        cheapest = min(prices, key=lambda x: x.get('estimated_price', float('inf')))
        
        logger.info(f"Cheapest option: {cheapest['app_name']} at ₹{cheapest['estimated_price']}")
        return json.dumps(cheapest)
        
    except Exception as e:
        logger.error(f"Error finding cheapest: {str(e)}")
        return f"Error: {str(e)}"


def apply_budget_filter(prices: List[Dict], budget: float, **kwargs) -> str:
    """
    Filter prices by budget constraint.
    
    Args:
        prices: List of price info dictionaries
        budget: Maximum budget in INR
    
    Returns:
        Prices within budget
    """
    try:
        import json
        
        logger.info(f"Filtering prices with budget constraint: ₹{budget}")
        
        filtered = [
            p for p in prices 
            if p.get('estimated_price', float('inf')) <= budget
        ]
        
        if not filtered:
            logger.warning(f"No options available within budget ₹{budget}")
        
        logger.info(f"Found {len(filtered)} options within budget")
        return json.dumps(filtered)
        
    except Exception as e:
        logger.error(f"Error applying budget filter: {str(e)}")
        return f"Error: {str(e)}"
