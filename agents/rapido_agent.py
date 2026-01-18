"""Rapido-specific cab booking agent."""

import logging
from agents.base_agent import BaseCabAgent
from models.ride_preferences import RidePreferences
from models.price_info import PriceInfo

logger = logging.getLogger("cab_navigation.rapido")


class RapidoAgent(BaseCabAgent):
    """Agent for Rapido cab booking."""
    
    def __init__(self, config=None):
        """Initialize Rapido agent."""
        super().__init__(
            app_name="Rapido",
            package_name="com.rapido.android",
            config=config
        )
    
    def _build_price_goal(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences
    ) -> str:
        """Build Rapido-specific price extraction goal."""
        
        ride_type_rapido = self._map_ride_type(preferences.ride_type)
        
        goal = f"""
Open Rapido app and get the fare estimate:

STEP-BY-STEP INSTRUCTIONS:
1. Make sure Rapido app is open
2. Look for the destination field at the top of the screen
3. Tap on the destination input field
4. Type the destination: {destination}
5. Wait for search results/suggestions to appear
6. Select the destination from the suggestions that appear
7. The app will show available ride options with fares
8. Find the {ride_type_rapido} ride type
9. Extract the fare information

INFORMATION TO EXTRACT:
- Ride type (e.g., "Rapido Auto", "Rapido Bike")
- Estimated fare in rupees
- Estimated time to arrive (minutes)
- Distance if shown
- Any extra charges

RETURN:
The app_name should be "Rapido"
The estimated_price should be a number
The estimated_time should be like "4 mins"
        """
        
        return goal.strip()
    
    def _build_booking_goal(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences,
        price_info: PriceInfo
    ) -> str:
        """Build Rapido-specific booking goal."""
        
        goal = f"""
        Complete the Rapido ride booking with the following details:
        
        - Pickup: {pickup_location}
        - Destination: {destination}
        - Ride Type: {price_info.ride_type}
        - Estimated Fare: ₹{price_info.estimated_price}
        - Passengers: {preferences.passengers}
        
        Steps:
        1. Set pickup location to: {pickup_location}
        2. Enter destination: {destination}
        3. Select {price_info.ride_type} ride type
        4. Review fare details: ₹{price_info.estimated_price}
        5. Proceed with booking
        
        Extract and return:
        - Booking confirmation number/ID
        - Driver details (name, rating, vehicle)
        - Time to pickup
        - Final ride fare
        - Trip status
        """
        
        return goal.strip()
    
    def _map_ride_type(self, preference: str) -> str:
        """Map ride preference to Rapido ride types."""
        mapping = {
            'car': 'Auto',
            'rickshaw': 'Auto',
            'bike': 'Bike',
            'premium': 'Auto',
            'auto': 'Auto'
        }
        return mapping.get(preference.lower(), 'Auto')
