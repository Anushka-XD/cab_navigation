#!/usr/bin/env python
"""Test script to verify Pydantic models are Gemini-compatible."""

import os
import sys
from pydantic import BaseModel
import json

# Set API key
os.environ["GOOGLE_API_KEY"] = "your gemini key"

# Import models
sys.path.insert(0, '/Users/anushka/cab_navigation')
from models.price_info import PriceInfo
from models.booking_info import BookingInfo
from models.ride_preferences import RidePreferences

def test_schema(model_class, name):
    """Test if model schema is Gemini-compatible."""
    print(f"\n🔍 Testing {name}...")
    schema = model_class.model_json_schema()
    
    # Check for problematic fields
    schema_str = json.dumps(schema)
    if "additional_properties" in schema_str:
        print(f"  ❌ Found 'additional_properties' in schema")
        print(f"  Full schema: {json.dumps(schema, indent=2)}")
        return False
    else:
        print(f"  ✅ Schema is clean (no additional_properties)")
        print(f"  Fields: {list(schema.get('properties', {}).keys())}")
        return True

def main():
    print("=" * 50)
    print("GEMINI COMPATIBILITY TEST")
    print("=" * 50)
    
    results = []
    results.append(test_schema(PriceInfo, "PriceInfo"))
    results.append(test_schema(BookingInfo, "BookingInfo"))
    results.append(test_schema(RidePreferences, "RidePreferences"))
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All models are Gemini-compatible!")
        return 0
    else:
        print("❌ Some models have issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())
