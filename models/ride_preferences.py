"""Ride preference model - extracted from user input via NLP."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RidePreferences(BaseModel):
    """User's ride preferences extracted from natural language input."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "destination": "Airport",
                "ride_type": "rickshaw",
                "vehicle_type": None,
                "passengers": 1,
                "luggage": False,
                "ac_preference": None,
                "budget_constraint": 500
            }
        }
    )
    
    destination: str = Field(
        description="Destination address or location name"
    )
    ride_type: str = Field(
        default="car",
        description="Type of ride: 'car', 'rickshaw', 'bike', 'auto', 'premium'"
    )
    vehicle_type: Optional[str] = Field(
        default=None,
        description="Specific vehicle type if provided (e.g., 'economy', 'comfort', 'xl')"
    )
    passengers: int = Field(
        default=1,
        description="Number of passengers"
    )
    luggage: bool = Field(
        default=False,
        description="Whether luggage/extra space is needed"
    )
    ac_preference: Optional[bool] = Field(
        default=None,
        description="AC preference for rickshaw/auto (True=AC preferred, False=no AC, None=no preference)"
    )
    budget_constraint: Optional[float] = Field(
        default=None,
        description="Maximum budget in rupees if specified"
    )
