"""Main orchestrator for cab comparison and booking."""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from droidrun import DroidrunConfig
from models.ride_preferences import RidePreferences
from models.price_info import PriceInfo
from models.booking_info import BookingInfo
from agents import UberAgent, OlaAgent, RapidoAgent
from tools.nlp_parser import parse_ride_preferences
from config import get_droidrun_config

logger = logging.getLogger("cab_navigation.orchestrator")


@dataclass
class ComparisonResult:
    """Result of price comparison."""
    prices: Dict[str, PriceInfo]
    cheapest_app: str
    cheapest_price: float
    comparison_summary: str


class CabComparisonOrchestrator:
    """Orchestrates price comparison and booking across multiple cab apps."""
    
    def __init__(self, config: Optional[DroidrunConfig] = None):
        """
        Initialize orchestrator.
        
        Args:
            config: Optional DroidrunConfig for all agents
        """
        self.config = config or get_droidrun_config()
        self.logger = logging.getLogger("cab_navigation.orchestrator")
        
        # Initialize agents for each app
        self.agents = {
            'uber': UberAgent(self.config),
            'ola': OlaAgent(self.config),
            'rapido': RapidoAgent(self.config)
        }
        
        self.last_comparison = None
        self.last_booking = None
    
    async def parse_user_input(self, user_input: str) -> RidePreferences:
        """
        Parse natural language user input to extract preferences.
        
        Args:
            user_input: User's natural language input (e.g., "Go to airport as rickshaw")
        
        Returns:
            RidePreferences object
        """
        try:
            self.logger.info(f"Parsing user input: {user_input}")
            
            # Use NLP parser to extract preferences
            prefs_json = parse_ride_preferences(user_input)
            
            # Parse JSON response back to RidePreferences
            import json
            prefs_dict = json.loads(prefs_json)
            preferences = RidePreferences(**prefs_dict)
            
            self.logger.info(f"Preferences extracted: {preferences}")
            return preferences
            
        except Exception as e:
            self.logger.error(f"Error parsing user input: {str(e)}")
            raise
    
    async def compare_prices(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences,
        apps: Optional[List[str]] = None
    ) -> ComparisonResult:
        """
        Compare prices across multiple cab apps.
        
        Args:
            pickup_location: Starting location
            destination: Destination location
            preferences: Ride preferences
            apps: List of apps to compare (default: all)
        
        Returns:
            ComparisonResult with pricing info from all apps
        """
        if apps is None:
            apps = list(self.agents.keys())
        
        self.logger.info(f"Starting price comparison across {apps}")
        self.logger.info(f"Route: {pickup_location} -> {destination}")
        
        prices = {}
        tasks = []
        
        # Launch concurrent price fetching from all apps
        for app_name in apps:
            if app_name in self.agents:
                task = self._fetch_price_from_app(
                    app_name,
                    pickup_location,
                    destination,
                    preferences
                )
                tasks.append(task)
        
        # Wait for all price fetches to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, app_name in enumerate(apps):
            if app_name in self.agents:
                try:
                    result = results[i]
                    if isinstance(result, Exception):
                        self.logger.warning(f"Error fetching price from {app_name}: {result}")
                        continue
                    if result:
                        prices[app_name] = result
                        self.logger.info(
                            f"{app_name}: {result.ride_type} - ₹{result.estimated_price} "
                            f"({result.estimated_time})"
                        )
                except Exception as e:
                    self.logger.error(f"Unexpected error processing {app_name}: {str(e)}")
        
        # Find cheapest option
        if not prices:
            raise ValueError("Could not fetch prices from any app")
        
        cheapest_app = min(prices.keys(), key=lambda k: prices[k].estimated_price)
        cheapest_price = prices[cheapest_app].estimated_price
        
        # Build comparison summary
        summary = self._build_comparison_summary(prices, cheapest_app)
        
        comparison_result = ComparisonResult(
            prices=prices,
            cheapest_app=cheapest_app,
            cheapest_price=cheapest_price,
            comparison_summary=summary
        )
        
        self.last_comparison = comparison_result
        return comparison_result
    
    async def book_cheapest(
        self,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences,
        comparison: Optional[ComparisonResult] = None
    ) -> Optional[BookingInfo]:
        """
        Book the cheapest ride from the comparison.
        
        Args:
            pickup_location: Starting location
            destination: Destination
            preferences: Ride preferences
            comparison: Optional ComparisonResult (if None, will run comparison first)
        
        Returns:
            BookingInfo if successful, None otherwise
        """
        try:
            # Run comparison if not provided
            if comparison is None:
                comparison = await self.compare_prices(
                    pickup_location,
                    destination,
                    preferences
                )
            
            cheapest_app = comparison.cheapest_app
            price_info = comparison.prices[cheapest_app]
            
            self.logger.info(
                f"Booking on {cheapest_app} at ₹{price_info.estimated_price}"
            )
            
            # Book on the cheapest app
            agent = self.agents[cheapest_app]
            booking = await agent.book_ride(
                pickup_location,
                destination,
                preferences,
                price_info
            )
            
            if booking:
                self.logger.info(f"Booking successful: {booking.booking_id}")
                self.last_booking = booking
            
            return booking
            
        except Exception as e:
            self.logger.error(f"Error booking ride: {str(e)}")
            return None
    
    async def _fetch_price_from_app(
        self,
        app_name: str,
        pickup_location: str,
        destination: str,
        preferences: RidePreferences
    ) -> Optional[PriceInfo]:
        """Fetch price from a single app."""
        try:
            agent = self.agents[app_name]
            
            # Open app
            if not await agent.open_app():
                self.logger.warning(f"Could not open {app_name}")
                return None
            
            # Get price
            price = await agent.get_price(pickup_location, destination, preferences)
            
            # Close app
            await agent.close_app()
            
            return price
            
        except Exception as e:
            self.logger.error(f"Error fetching price from {app_name}: {str(e)}")
            return None
    
    def _build_comparison_summary(self, prices: Dict[str, PriceInfo], cheapest_app: str) -> str:
        """Build a human-readable comparison summary."""
        summary = "💰 Price Comparison Results:\n"
        summary += "=" * 50 + "\n\n"
        
        # Sort by price
        sorted_prices = sorted(prices.items(), key=lambda x: x[1].estimated_price)
        
        for rank, (app_name, price_info) in enumerate(sorted_prices, 1):
            emoji = "🥇" if app_name == cheapest_app else "🥈" if rank == 2 else "🥉"
            summary += f"{emoji} #{rank} {app_name.upper()}\n"
            summary += f"   Ride Type: {price_info.ride_type}\n"
            summary += f"   Fare: ₹{price_info.estimated_price}\n"
            summary += f"   ETA: {price_info.estimated_time}\n"
            if price_info.distance:
                summary += f"   Distance: {price_info.distance}\n"
            if price_info.extra_charges:
                summary += f"   Extra Charges: {price_info.extra_charges}\n"
            summary += "\n"
        
        summary += "=" * 50 + "\n"
        summary += f"✅ Cheapest Option: {cheapest_app.upper()} (₹{prices[cheapest_app].estimated_price})\n"
        
        return summary
    
    def get_last_comparison_summary(self) -> Optional[str]:
        """Get the summary of last comparison."""
        if self.last_comparison:
            return self.last_comparison.comparison_summary
        return None
    
    def get_last_booking_summary(self) -> Optional[str]:
        """Get the summary of last booking."""
        if self.last_booking:
            return (
                f"✅ Ride Booked Successfully!\n"
                f"   App: {self.last_booking.app_name}\n"
                f"   Booking ID: {self.last_booking.booking_id}\n"
                f"   Ride Type: {self.last_booking.ride_type}\n"
                f"   Fare: ₹{self.last_booking.estimated_price}\n"
                f"   Driver: {self.last_booking.driver_name} ({self.last_booking.driver_rating}⭐)\n"
                f"   ETA: {self.last_booking.estimated_arrival}\n"
                f"   Vehicle: {self.last_booking.vehicle_details}"
            )
        return None
