import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import ValidationError
from models.checklist import Checklist  # your Pydantic model

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        current_weather = data.get("current_weather", {})
        return {
            "temperature_c": current_weather.get("temperature"),
            "wind_speed_kph": current_weather.get("windspeed")
        }
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def generate_checklist(user_input: dict) -> Checklist:
    # Step 1: Fetch weather data
    weather = get_weather(user_input["latitude"], user_input["longitude"])

    # Step 2: Define the system prompt
    system_prompt = """You are a helpful assistant that generates personalized camping packing checklists.

You will receive structured input containing:
- The campsite location and weather forecast
- Trip start and end dates
- Group size
- Whether a dog is coming
- A list of planned activities

Your job is to generate a concise, well-organized packing list tailored to the user’s trip.

Consider:
- The number of people (e.g., 3 sleeping bags for 3 people)
- The weather forecast (e.g., rain gear, cold-weather layers, sun protection)
- Any pets included in the trip
- The selected activities (e.g., swimming → swimsuit, fishing → gear)

Only include relevant, practical items. Avoid duplicates across categories."""

    # Step 3: Compile structured input to send to LLM
    structured_input = {
        "location": user_input["location"],
        "start_date": user_input["start_date"],
        "end_date": user_input["end_date"],
        "group_size": user_input["group_size"],
        "has_dog": user_input["has_dog"],
        "activities": user_input["activities"],
        "weather": weather
    }

    input = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(structured_input)}
    ]

    # Step 4: Call OpenAI with structured JSON response
    completion = client.responses.create(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Generate a camping checklist based on the trip details."},
        {"role": "user", "content": json.dumps({
            "location": "Little Pond Campground, NY",
            "start_date": "2025-06-15",
            "end_date": "2025-06-17",
            "group_size": 2,
            "has_dog": True,
            "activities": ["hiking", "campfire cooking"],
            "weather": {
                "temperature_c": 16.4,
                "wind_speed_kph": 8.7
            }
        })}
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "camping_checklist",
            "schema": {
                "type": "object",
                "properties": {
                    "Shelter": {"type": "array", "items": {"type": "string"}},
                    "Clothing": {"type": "array", "items": {"type": "string"}},
                    "Cooking": {"type": "array", "items": {"type": "string"}},
                    "Hygiene": {"type": "array", "items": {"type": "string"}},
                    "Safety": {"type": "array", "items": {"type": "string"}},
                    "Miscellaneous": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["Shelter", "Clothing", "Cooking", "Hygiene", "Safety", "Miscellaneous"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

    raw_output = completion.output

    return raw_output

