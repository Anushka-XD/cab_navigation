"""Uber-specific cab booking agent."""

import logging
from agents.base_agent import BaseCabAgent
from models.ride_preferences import RidePreferences
from models.price_info import PriceInfo

logger = logging.getLogger("cab_navigation.uber")


class UberAgent(BaseCabAgent):
    """Agent for Uber cab booking."""
    
    def __init__(self, config=None):
        """Initialize Uber agent."""
        super().__init__(
            app_name="Uber",
            package_name="com.ubercab",
            config=config
        )
    
    def _build_price_goal(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences
    ) -> str:
        """Build Uber-specific price extraction goal."""
        
        ride_type_uber = self._map_ride_type(preferences.ride_type)
        
        goal = f"""
Open Uber app and get the fare estimate:

STEP-BY-STEP INSTRUCTIONS:
1. Make sure Uber app is open and ready
2. Look for the destination input field (usually says "Where to?" or has a search icon)
3. Tap on the destination/search field
4. Type the destination: {destination}
5. Wait for suggestions to appear and tap the first matching result
6. The fare estimate screen will show
7. Look for the {ride_type_uber} ride type in the list of options
8. Extract the fare information

INFORMATION TO EXTRACT:
- Ride type name (e.g., "UberGo", "Uber Auto")
- Estimated fare/price in rupees
- Estimated time (minutes)
- Distance (km) if visible
- Any surge pricing or extra charges

RETURN:
The app_name should be "Uber"
The estimated_price should be a number
The estimated_time should be like "7 mins"
        """
        
        return goal.strip()
    
    def _build_booking_goal(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences,
        price_info: PriceInfo
    ) -> str:
        """Build Uber-specific booking goal."""
        
        goal = f"""
        Complete the Uber ride booking with the following details:
        
        - Pickup: {pickup_location}
        - Destination: {destination}
        - Ride Type: {price_info.ride_type}
        - Estimated Fare: ₹{price_info.estimated_price}
        - Passengers: {preferences.passengers}
        
        Steps:
        1. Enter pickup location or confirm current location
        2. Enter destination: {destination}
        3. Select ride type: {price_info.ride_type}
        4. Proceed to payment/confirmation
        5. Complete the booking
        
        Extract and return:
        - Booking ID
        - Confirmation status
        - Driver details if available
        - Final estimated fare
        - ETA
        """
        
        return goal.strip()
    
    def _map_ride_type(self, preference: str) -> str:
        """Map ride preference to Uber ride types."""
        mapping = {
            'car': 'UberGo',
            'rickshaw': 'Uber Auto',
            'bike': 'Uber Moto',
            'premium': 'Uber XL',
            'auto': 'Uber Auto'
        }
        return mapping.get(preference.lower(), 'UberGo')
