"""Price information extracted from cab apps."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal


class PriceInfo(BaseModel):
    """Pricing information from a single cab service."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "app_name": "Uber",
                "ride_type": "UberGo",
                "estimated_price": 250.0,
                "estimated_time": "7 mins",
                "distance": "4.2 km",
                "currency": "INR",
                "extra_charges": "Surge pricing applied",
                "available": True
            }
        }
    )
    
    app_name: str = Field(
        description="Name of the cab service app (Uber, Ola, Rapido)"
    )
    ride_type: str = Field(
        description="Type of ride offered (economy, comfort, rickshaw, etc.)"
    )
    estimated_price: float = Field(
        description="Estimated fare in INR"
    )
    estimated_time: str = Field(
        description="Estimated arrival time (e.g., '5 mins', '7-10 mins')"
    )
    distance: Optional[str] = Field(
        default=None,
        description="Estimated distance in km"
    )
    currency: str = Field(
        default="INR",
        description="Currency code"
    )
    extra_charges: Optional[str] = Field(
        default=None,
        description="Any extra charges (surge, toll, etc.)"
    )
    available: bool = Field(
        default=True,
        description="Whether this ride type is currently available"
    )
