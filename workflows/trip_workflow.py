from agents.extract_trip import extract_trip_info
from tools.location_lookup import lookup_location

def run_trip_agent(user_input: str) -> dict:
    # 1. Extract trip info from GPT
    trip = extract_trip_info(user_input)

    # 2. Look up location info using OpenStreetMap
    try:
        location_data = lookup_location(trip.location)
    except Exception as e:
        location_data = {"error": str(e)}

    # 3. Combine both results
    return {
        "trip": trip.model_dump(),  # Pydantic to dict
        "location": location_data
    }
