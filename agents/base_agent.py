"""Base agent class for cab booking apps."""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from droidrun import DroidAgent, DroidrunConfig
from models.price_info import PriceInfo
from models.booking_info import BookingInfo
from models.ride_preferences import RidePreferences
from config import get_droidrun_config

logger = logging.getLogger("cab_navigation")


class BaseCabAgent(ABC):
    """Abstract base class for cab booking agents."""
    
    def __init__(self, app_name: str, package_name: str, config: Optional[DroidrunConfig] = None):
        """
        Initialize base cab agent.
        
        Args:
            app_name: Human-readable app name (e.g., "Uber")
            package_name: Android package name (e.g., "com.ubercab")
            config: DroidrunConfig instance
        """
        self.app_name = app_name
        self.package_name = package_name
        self.config = config or get_droidrun_config()
        self.logger = logging.getLogger(f"cab_navigation.{app_name.lower()}")
        
    async def open_app(self) -> bool:
        """
        Open the cab booking app.
        
        Returns:
            True if app opened successfully, False otherwise
        """
        try:
            self.logger.info(f"Opening {self.app_name}")
            goal = f"Open {self.app_name} app"
            
            agent = DroidAgent(
                goal=goal,
                config=self.config,
                timeout=90  # Increased from 30 to allow for device init and LLM inference
            )
            
            result = await agent.run()
            
            if result.success:
                self.logger.info(f"{self.app_name} opened successfully")
                return True
            else:
                self.logger.error(f"Failed to open {self.app_name}: {result.reason}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error opening app: {str(e)}")
            return False
    
    async def get_price(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences
    ) -> Optional[PriceInfo]:
        """
        Get pricing information from the app.
        
        Args:
            pickup_location: Starting location
            destination: Destination location
            preferences: Ride preferences
        
        Returns:
            PriceInfo object or None if failed
        """
        try:
            self.logger.info(
                f"Getting price for {pickup_location} -> {destination} "
                f"(ride_type: {preferences.ride_type})"
            )
            
            goal = self._build_price_goal(pickup_location, destination, preferences)
            
            agent = DroidAgent(
                goal=goal,
                config=self.config,
                output_model=PriceInfo,
                timeout=180  # Increased from 120 for destination entry and navigation
            )
            
            result = await agent.run()
            
            if result.success and result.structured_output:
                price_info: PriceInfo = result.structured_output
                self.logger.info(
                    f"Price retrieved: {price_info.ride_type} - ₹{price_info.estimated_price}"
                )
                return price_info
            else:
                self.logger.warning(f"Could not extract price: {result.reason}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting price: {str(e)}")
            return None
    
    async def book_ride(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences,
        price_info: PriceInfo
    ) -> Optional[BookingInfo]:
        """
        Book a ride on the app.
        
        Args:
            pickup_location: Starting location
            destination: Destination location
            preferences: Ride preferences
            price_info: Pricing information
        
        Returns:
            BookingInfo object or None if failed
        """
        try:
            self.logger.info(
                f"Booking {price_info.ride_type} on {self.app_name} "
                f"for ₹{price_info.estimated_price}"
            )
            
            goal = self._build_booking_goal(pickup_location, destination, preferences, price_info)
            
            agent = DroidAgent(
                goal=goal,
                config=self.config,
                output_model=BookingInfo,
                timeout=120
            )
            
            result = await agent.run()
            
            if result.success and result.structured_output:
                booking_info: BookingInfo = result.structured_output
                self.logger.info(f"Ride booked successfully: {booking_info.booking_id}")
                return booking_info
            else:
                self.logger.error(f"Failed to book ride: {result.reason}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error booking ride: {str(e)}")
            return None
    
    @abstractmethod
    def _build_price_goal(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences
    ) -> str:
        """Build goal prompt for price extraction."""
        pass
    
    @abstractmethod
    def _build_booking_goal(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences,
        price_info: PriceInfo
    ) -> str:
        """Build goal prompt for booking."""
        pass
    
    async def close_app(self) -> bool:
        """Close the app gracefully."""
        try:
            self.logger.info(f"Closing {self.app_name}")
            # Implement app-specific close logic if needed
            return True
        except Exception as e:
            self.logger.error(f"Error closing app: {str(e)}")
            return False
