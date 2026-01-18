"""Booking confirmation information."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class BookingInfo(BaseModel):
    """Confirmation details after booking a ride."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "booking_id": "UBER123456",
                "app_name": "Uber",
                "ride_type": "UberGo",
                "estimated_price": 250.0,
                "estimated_arrival": "5 mins",
                "driver_name": "Rajesh Kumar",
                "driver_rating": 4.8,
                "vehicle_details": "DL01AB1234, White Hyundai i10",
                "status": "confirmed",
                "pickup_location": "Current Location",
                "destination": "Airport"
            }
        }
    )
    
    booking_id: str = Field(
        description="Unique booking/ride ID from the app"
    )
    app_name: str = Field(
        description="Which app the booking was made on"
    )
    ride_type: str = Field(
        description="Type of ride booked"
    )
    estimated_price: float = Field(
        description="Final estimated price in INR"
    )
    estimated_arrival: str = Field(
        description="Estimated driver arrival time"
    )
    driver_name: Optional[str] = Field(
        default=None,
        description="Driver name if available"
    )
    driver_rating: Optional[float] = Field(
        default=None,
        description="Driver rating (1-5)"
    )
    vehicle_details: Optional[str] = Field(
        default=None,
        description="Vehicle plate number, model, etc."
    )
    status: str = Field(
        default="confirmed",
        description="Booking status"
    )
    pickup_location: Optional[str] = Field(
        default=None,
        description="Confirmed pickup location"
    )
    destination: Optional[str] = Field(
        default=None,
        description="Confirmed destination"
    )
