import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import ValidationError
from models.checklist import Checklist
import requests

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_trip_info(user_input: str) -> dict:

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
            print("Open-Meteo response:", data)

            current_weather = data.get("current_weather", {})
            temperature = current_weather.get("temperature")
            wind_speed = current_weather.get("windspeed")

            return {
                "temperature_c": temperature,
                "wind_speed_kph": wind_speed
            }

        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current temperature and wind speed for a given latitude and longitude.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "number",
                            "description": "Latitude of the location, e.g. 48.8566"
                        },
                        "longitude": {
                            "type": "number",
                            "description": "Longitude of the location, e.g. 2.3522"
                        }
                    },
                    "required": ["latitude", "longitude"],
                    "additionalProperties": False
                }
            }
        }
    ]


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


    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools = tools
    )

    print(completion.model_dump())

    def call_function(name, args):
        if name == "get_weather":
            return get_weather(**args)


    for tool_call in completion.choices[0].message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        messages.append(completion.choices[0].message)

        result = call_function(name, args)
        messages.append(
            {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
        )


    return result
