"""Ola-specific cab booking agent."""

import logging
from agents.base_agent import BaseCabAgent
from models.ride_preferences import RidePreferences
from models.price_info import PriceInfo

logger = logging.getLogger("cab_navigation.ola")


class OlaAgent(BaseCabAgent):
    """Agent for Ola cab booking."""
    
    def __init__(self, config=None):
        """Initialize Ola agent."""
        super().__init__(
            app_name="Ola",
            package_name="com.olacabs.app",
            config=config
        )
    
    def _build_price_goal(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences
    ) -> str:
        """Build Ola-specific price extraction goal."""
        
        ride_type_ola = self._map_ride_type(preferences.ride_type)
        
        goal = f"""
Open Ola app and get the fare estimate:

STEP-BY-STEP INSTRUCTIONS:
1. Make sure Ola app is open and ready
2. Look for the destination input field (usually says "Where to?" at the top)
3. Tap on the destination input field
4. Type the destination: {destination}
5. Wait for suggestions/autocomplete to appear
6. Tap on the first matching suggestion from the dropdown
7. The fare estimate screen will appear
8. Find the {ride_type_ola} ride type option
9. Extract the fare information

INFORMATION TO EXTRACT:
- Ride type (e.g., "Ola Prime", "Ola Auto", "Ola Share")
- Estimated fare/price in rupees
- Estimated arrival time (minutes)
- Distance if shown
- Any charges or discounts

RETURN:
The app_name should be "Ola"
The estimated_price should be a number
The estimated_time should be like "5 mins"
        """
        
        return goal.strip()
    
    def _build_booking_goal(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences,
        price_info: PriceInfo
    ) -> str:
        """Build Ola-specific booking goal."""
        
        goal = f"""
        Complete the Ola ride booking with the following details:
        
        - Pickup: {pickup_location}
        - Destination: {destination}
        - Ride Category: {price_info.ride_type}
        - Estimated Fare: ₹{price_info.estimated_price}
        - Passengers: {preferences.passengers}
        
        Steps:
        1. Confirm or set pickup location
        2. Enter destination: {destination}
        3. Select ride category: {price_info.ride_type}
        4. Apply any available offers/coupons if visible
        5. Proceed to booking confirmation
        6. Complete the booking
        
        Extract and return:
        - Booking/Ride ID
        - Driver name and rating
        - Vehicle details (plate number, model, color)
        - Estimated arrival time
        - Final fare
        """
        
        return goal.strip()
    
    def _map_ride_type(self, preference: str) -> str:
        """Map ride preference to Ola ride types."""
        mapping = {
            'car': 'Ola Prime',
            'rickshaw': 'Ola Auto',
            'bike': 'Ola Bike',
            'premium': 'Ola Plus',
            'auto': 'Ola Auto'
        }
        return mapping.get(preference.lower(), 'Ola Prime')
