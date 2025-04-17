import requests

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

def get_weather_tool_schema():
    return {
        "type": "function",
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
