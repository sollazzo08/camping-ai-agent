import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import ValidationError
from models.trip import Trip
from tools.weather import get_weather_tool_schema, get_weather

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_trip_info(user_input: str) -> dict:
    system_prompt = (
        "You are a helpful assistant that extracts structured camping trip details from user messages.\n"
        "Standardize the 'location' field to match what mapping tools would understand.\n"
        "Also return the latitude and longitude of the location.\n"
        "Return all dates in full ISO format: YYYY-MM-DD."
    )

    function_schema = {
        "name": "extract_trip_info",
        "description": "Extract camping trip details from user input.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
                "start_date": {"type": "string", "format": "date"},
                "end_date": {"type": "string", "format": "date"},
                "group_size": {"type": "integer"},
                "activities": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "include_weather": {"type": "boolean"}
            },
            "required": ["location", "latitude", "longitude"]
        }
    }

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        tools = [
            {"type": "function", "function": function_schema},
            {"type": "function", "function": get_weather_tool_schema()}
        ],
        tool_choice="auto"
    )

    tool_calls = response.choices[0].message.tool_calls
    print(response.model_dump())
    trip_data = None
    weather_data = None

    for tool_call in tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        if name == "extract_trip_info":
            trip = Trip(**args)
            trip_data = trip.model_dump()

            if trip.include_weather:
                print(f"Calling get_weather for lat: {trip.latitude}, lon: {trip.longitude}")
                weather_data = get_weather(trip.latitude, trip.longitude)

        elif name == "get_weather":
            weather_data = get_weather(**args)

    return {
        "trip": trip_data,
        "weather": weather_data
    }
