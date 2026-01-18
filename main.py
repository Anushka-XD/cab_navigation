"""Main entry point for cab navigation system."""

import asyncio
import logging
import sys
from typing import Optional
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import (
    get_droidrun_config, WELCOME_MESSAGE, HELP_MESSAGE,
    COMPARISON_TIMEOUT, BOOKING_TIMEOUT, DEFAULT_APPS, LOG_LEVEL
)
from orchestrator import CabComparisonOrchestrator, ComparisonResult
from models.ride_preferences import RidePreferences
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich import box

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("cab_navigation.main")

# Rich console for formatting
console = Console()


class CabNavigationCLI:
    """Command-line interface for cab navigation system."""
    
    def __init__(self):
        """Initialize CLI."""
        self.orchestrator = CabComparisonOrchestrator(get_droidrun_config())
        self.logger = logging.getLogger("cab_navigation.main")
    
    def _display_comparison(self, comparison: ComparisonResult) -> None:
        """
        Display price comparison in a nice table format.
        
        Args:
            comparison: ComparisonResult from orchestrator
        """
        # Create comparison table
        table = Table(title="💰 Price Comparison Results", box=box.ROUNDED)
        table.add_column("Rank", style="cyan", no_wrap=True)
        table.add_column("App", style="magenta", no_wrap=True)
        table.add_column("Fare (₹)", style="green", no_wrap=True)
        table.add_column("ETA", style="yellow")
        table.add_column("Distance", style="blue")
        table.add_column("Ride Type", style="white")
        
        # Sort prices
        sorted_apps = sorted(
            comparison.prices.items(),
            key=lambda x: x[1].estimated_price
        )
        
        for rank, (app_name, price_info) in enumerate(sorted_apps, 1):
            rank_emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
            app_display = f"[bold]{app_name.upper()}[/bold]" if app_name == comparison.cheapest_app else app_name.upper()
            fare_display = f"[bold green]₹{price_info.estimated_price}[/bold green]" if app_name == comparison.cheapest_app else f"₹{price_info.estimated_price}"
            
            distance_str = price_info.distance if price_info.distance else "N/A"
            
            table.add_row(
                f"{rank_emoji} #{rank}",
                app_display,
                fare_display,
                price_info.estimated_time or "N/A",
                distance_str,
                price_info.ride_type
            )
        
        console.print(table)
        
        # Show savings info
        if len(sorted_apps) > 1:
            cheapest = sorted_apps[0][1].estimated_price
            second_cheapest = sorted_apps[1][1].estimated_price
            savings = second_cheapest - cheapest
            savings_pct = (savings / second_cheapest * 100)
            
            savings_text = f"💡 You save ₹{savings:.0f} ({savings_pct:.1f}%) by choosing {comparison.cheapest_app.upper()}!"
            console.print(Panel(savings_text, style="green"))
    
    async def run(self):
        """Run the main CLI loop."""
        print(WELCOME_MESSAGE)
        
        while True:
            try:
                print("\n" + "=" * 50)
                user_input = input(
                    "\n📍 Enter your destination and preferences\n"
                    "   (or 'help' for examples, 'quit' to exit):\n\n→ "
                ).strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'quit':
                    print("\n👋 Thank you for using Cab Navigation System!")
                    break
                
                if user_input.lower() == 'help':
                    print(HELP_MESSAGE)
                    continue
                
                # Process the request
                await self._process_booking_request(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {str(e)}")
                print(f"\n❌ Error: {str(e)}")
                print("Please try again.")
    
    async def _process_booking_request(self, user_input: str):
        """Process a single booking request."""
        try:
            print("\n🔍 Analyzing your request...")
            
            # Parse user input to extract preferences
            preferences = await self.orchestrator.parse_user_input(user_input)
            
            print(f"\n✓ Preferences extracted:")
            print(f"   Destination: {preferences.destination}")
            print(f"   Ride Type: {preferences.ride_type}")
            if preferences.passengers > 1:
                print(f"   Passengers: {preferences.passengers}")
            if preferences.luggage:
                print(f"   Luggage: Required")
            if preferences.ac_preference is not None:
                print(f"   AC: {'Preferred' if preferences.ac_preference else 'Not needed'}")
            
            # Get pickup location
            pickup_location = input("\n📍 Confirm current pickup location (or press Enter for 'Current Location'): ").strip()
            if not pickup_location:
                pickup_location = "Current Location"
            
            destination = preferences.destination
            
            print(f"\n🚀 Comparing prices across Uber, Ola, and Rapido...")
            print(f"   From: {pickup_location}")
            print(f"   To: {destination}")
            
            # Compare prices
            comparison = await asyncio.wait_for(
                self.orchestrator.compare_prices(
                    pickup_location,
                    destination,
                    preferences,
                    DEFAULT_APPS
                ),
                timeout=COMPARISON_TIMEOUT
            )
            
            # Display comparison using rich table
            self._display_comparison(comparison)
            
            # Show recommendation
            print(f"\n✅ CHEAPEST OPTION: {comparison.cheapest_app.upper()} at ₹{comparison.cheapest_price}")
        
        except asyncio.TimeoutError:
            print("\n⏱️  Request timed out. Please try again.")
            self.logger.error("Request timed out")
        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}", exc_info=True)
            print(f"\n❌ Error: {str(e)}")


async def main():
    """Main entry point."""
    cli = CabNavigationCLI()
    await cli.run()


def run_sync():
    """Synchronous wrapper for running from command line."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Exiting gracefully...")
        return
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n❌ Unexpected error: {str(e)}")
        return


if __name__ == "__main__":
    run_sync()
