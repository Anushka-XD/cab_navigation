"""
API Reference for Cab Navigation System

This file documents all public APIs and classes available in the system.
"""

# ============================================================================
# MODELS (Data Classes)
# ============================================================================

"""
models.RidePreferences
- destination: str - Destination address
- ride_type: str - Type of ride (car, rickshaw, bike, premium)
- vehicle_type: Optional[str] - Specific vehicle type
- passengers: int - Number of passengers
- luggage: bool - Whether luggage is needed
- ac_preference: Optional[bool] - AC preference
- budget_constraint: Optional[float] - Maximum budget in INR

Example:
    from models import RidePreferences
    
    prefs = RidePreferences(
        destination="Airport",
        ride_type="rickshaw",
        passengers=1,
        ac_preference=True
    )
"""

"""
models.PriceInfo
- app_name: str - Cab service app name
- ride_type: str - Type of ride offered
- estimated_price: float - Fare in INR
- estimated_time: str - ETA (e.g., "5 mins")
- distance: Optional[str] - Distance in km
- currency: str - Currency code (default: INR)
- extra_charges: Optional[dict] - Additional charges
- available: bool - Availability status

Example:
    from models import PriceInfo
    
    price = PriceInfo(
        app_name="Uber",
        ride_type="UberGo",
        estimated_price=250.0,
        estimated_time="7 mins",
        distance="4.2 km"
    )
"""

"""
models.BookingInfo
- booking_id: str - Unique booking ID
- app_name: str - App name (Uber, Ola, Rapido)
- ride_type: str - Ride type booked
- estimated_price: float - Final fare
- estimated_arrival: str - Driver ETA
- driver_name: Optional[str] - Driver name
- driver_rating: Optional[float] - Driver rating (1-5)
- vehicle_details: Optional[str] - Vehicle info
- status: str - Booking status
- pickup_location: Optional[str] - Pickup address
- destination: Optional[str] - Destination address

Example:
    from models import BookingInfo
    
    booking = BookingInfo(
        booking_id="UBER123456",
        app_name="Uber",
        ride_type="UberGo",
        estimated_price=250.0,
        estimated_arrival="5 mins",
        driver_name="John Doe",
        driver_rating=4.8
    )
"""

# ============================================================================
# AGENTS (App Controllers)
# ============================================================================

"""
agents.BaseCabAgent - Abstract base class
Methods:
    async open_app() -> bool
        Open the cab booking app
        Returns: True if successful
    
    async get_price(pickup_location, destination, preferences) -> Optional[PriceInfo]
        Get fare estimate from app
        Args:
            pickup_location: str - Starting location
            destination: str - Destination address
            preferences: RidePreferences - User preferences
        Returns: PriceInfo object or None
    
    async book_ride(pickup_location, destination, preferences, price_info) -> Optional[BookingInfo]
        Book a ride on the app
        Args:
            pickup_location: str - Starting location
            destination: str - Destination address
            preferences: RidePreferences - User preferences
            price_info: PriceInfo - Pricing information
        Returns: BookingInfo object or None
    
    async close_app() -> bool
        Close the app gracefully

Example:
    from agents import UberAgent
    from config import get_droidrun_config
    
    agent = UberAgent(get_droidrun_config())
    success = await agent.open_app()
"""

"""
agents.UberAgent(BaseCabAgent)
Uber-specific implementation for Uber cab bookings.

Example:
    from agents import UberAgent
    agent = UberAgent()
"""

"""
agents.OlaAgent(BaseCabAgent)
Ola-specific implementation for Ola cab bookings.

Example:
    from agents import OlaAgent
    agent = OlaAgent()
"""

"""
agents.RapidoAgent(BaseCabAgent)
Rapido-specific implementation for Rapido cab bookings.

Example:
    from agents import RapidoAgent
    agent = RapidoAgent()
"""

# ============================================================================
# ORCHESTRATOR (Main Coordinator)
# ============================================================================

"""
orchestrator.CabComparisonOrchestrator
Main orchestrator for price comparison and booking.

Methods:
    __init__(config: Optional[DroidrunConfig])
        Initialize orchestrator
        Args: config - Optional DroidrunConfig
    
    async parse_user_input(user_input: str) -> RidePreferences
        Parse natural language user input
        Args: user_input - User's input string
        Returns: RidePreferences object
        
        Examples supported:
        - "Go to airport as rickshaw"
        - "Take me to Times Square by car"
        - "Head to station, 2 people, AC auto"
    
    async compare_prices(pickup_location, destination, preferences, apps) -> ComparisonResult
        Compare prices across multiple apps
        Args:
            pickup_location: str - Starting location
            destination: str - Destination
            preferences: RidePreferences - User preferences
            apps: Optional[List[str]] - Apps to compare (default: all)
        Returns: ComparisonResult with pricing from all apps
    
    async book_cheapest(pickup_location, destination, preferences, comparison) -> Optional[BookingInfo]
        Book the cheapest ride
        Args:
            pickup_location: str - Starting location
            destination: str - Destination
            preferences: RidePreferences - User preferences
            comparison: Optional[ComparisonResult] - Previous comparison (runs new if None)
        Returns: BookingInfo or None
    
    get_last_comparison_summary() -> Optional[str]
        Get formatted summary of last comparison
        Returns: Formatted string summary
    
    get_last_booking_summary() -> Optional[str]
        Get formatted summary of last booking
        Returns: Formatted string summary

Example:
    from orchestrator import CabComparisonOrchestrator
    from config import get_droidrun_config
    
    orch = CabComparisonOrchestrator(get_droidrun_config())
    
    # Parse user input
    prefs = await orch.parse_user_input("Go to airport as rickshaw")
    
    # Compare prices
    comparison = await orch.compare_prices(
        "Current Location",
        "Airport",
        prefs
    )
    
    print(comparison.comparison_summary)
    
    # Book cheapest
    booking = await orch.book_cheapest(
        "Current Location",
        "Airport",
        prefs,
        comparison
    )
"""

# ============================================================================
# CUSTOM TOOLS (Helper Functions)
# ============================================================================

"""
tools.nlp_parser
Functions:
    parse_ride_preferences(user_input: str) -> str
        Parse natural language to preferences
        Args: user_input - User's text input
        Returns: JSON string of RidePreferences
    
    compare_prices(prices_json: str) -> str
        Compare prices from list
        Args: prices_json - JSON string of prices
        Returns: Comparison summary string
    
    validate_location(location: str) -> str
        Validate and normalize location
        Args: location - Location name/address
        Returns: Validated location string
"""

"""
tools.location_handler
Functions:
    get_current_location() -> str
        Get current device location
        Returns: Location string
    
    format_location_pair(pickup: str, destination: str) -> str
        Format pickup and destination
        Returns: Formatted string
    
    estimate_distance(pickup: str, destination: str) -> str
        Estimate distance between locations
        Returns: Distance estimation
"""

"""
tools.price_comparator
Functions:
    filter_by_ride_type(prices: List, ride_type: str) -> str
        Filter prices by ride type
        Returns: Filtered prices JSON
    
    find_cheapest(prices: List) -> str
        Find cheapest option
        Returns: Cheapest option details JSON
    
    apply_budget_filter(prices: List, budget: float) -> str
        Filter prices by budget
        Returns: Filtered prices JSON
"""

# ============================================================================
# UTILITIES
# ============================================================================

"""
utils
Functions:
    format_currency(amount: float, currency: str = "INR") -> str
        Format amount as currency
        Example: "₹250.00"
    
    format_time_estimate(minutes: str) -> str
        Format time estimate
        Example: "5-10 min"
    
    normalize_location(location: str) -> str
        Normalize location string
    
    calculate_eta_in_minutes(eta_string: str) -> Optional[int]
        Extract minutes from ETA string
    
    save_comparison_to_file(comparison_data, filepath)
        Save comparison results to JSON
    
    save_booking_to_file(booking_info, filepath)
        Save booking details to JSON
    
    FareHistory - Class for tracking fare history
        add_comparison(comparison_data)
        get_average_price(app, ride_type)
        to_dict()
"""

# ============================================================================
# CONFIGURATION
# ============================================================================

"""
config.get_droidrun_config() -> DroidrunConfig
    Get configured DroidrunConfig instance
    Returns: DroidrunConfig with default/env settings

Environment Variables:
    CAB_NAV_DEBUG - Enable debug mode (true/false)
    ANDROID_DEVICE_SERIAL - Device serial for connection
    USE_TCP - Use TCP connection (true/false)
    PLATFORM - Platform type (android/ios)
    GOOGLE_API_KEY - Google API key for LLMs
    OPENAI_API_KEY - OpenAI API key for LLMs
    ANTHROPIC_API_KEY - Anthropic API key for LLMs
"""

# ============================================================================
# COMPLETE WORKFLOW EXAMPLE
# ============================================================================

"""
Complete workflow example:

    import asyncio
    from orchestrator import CabComparisonOrchestrator
    from config import get_droidrun_config
    
    async def main():
        # Initialize
        config = get_droidrun_config()
        orch = CabComparisonOrchestrator(config)
        
        # Get user input
        user_input = "Go to airport as rickshaw"
        
        # Parse preferences
        preferences = await orch.parse_user_input(user_input)
        print(f"Preferences: {preferences}")
        
        # Compare prices
        comparison = await orch.compare_prices(
            pickup_location="Current Location",
            destination="Airport",
            preferences=preferences,
            apps=["uber", "ola", "rapido"]
        )
        
        # Display comparison
        print(comparison.comparison_summary)
        
        # Book cheapest
        booking = await orch.book_cheapest(
            pickup_location="Current Location",
            destination="Airport",
            preferences=preferences,
            comparison=comparison
        )
        
        if booking:
            print(f"Booked: {booking.booking_id}")
            print(f"Driver: {booking.driver_name}")
            print(f"ETA: {booking.estimated_arrival}")
        else:
            print("Booking failed")
    
    asyncio.run(main())
"""

# ============================================================================
# ERROR HANDLING
# ============================================================================

"""
Common Exceptions:

    ValueError
        - Raised when required data is missing
        - Example: No prices could be fetched from any app
    
    TimeoutError
        - Raised when operation exceeds timeout
        - Increased via config.COMPARISON_TIMEOUT, BOOKING_TIMEOUT
    
    Exception (generic)
        - Device connectivity issues
        - App not installed
        - LLM API errors
        - Network failures

All exceptions are logged with full context in logs/.
"""

# ============================================================================
# TESTING
# ============================================================================

"""
Testing individual components:

    # Test parsing
    from tools.nlp_parser import parse_ride_preferences
    result = parse_ride_preferences("Go to airport as rickshaw")
    
    # Test agent
    from agents import UberAgent
    agent = UberAgent()
    success = await agent.open_app()
    
    # Test orchestrator
    from orchestrator import CabComparisonOrchestrator
    orch = CabComparisonOrchestrator()
    comparison = await orch.compare_prices(...)

See DEVELOPMENT.md for detailed testing guide.
"""
