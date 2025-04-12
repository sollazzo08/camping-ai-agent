import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import ValidationError
from models.trip import Trip

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_trip_info(user_input: str) -> Trip:
    system_prompt = (
        "You are a helpful assistant that extracts structured camping trip details "
        "from user messages. Return all dates in full ISO format: YYYY-MM-DD."

    )

    function_schema = {
        "name": "extract_trip_info",
        "description": "Extract camping trip details from user input.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "start_date": {"type": "string", "format": "date"},
                "end_date": {"type": "string", "format": "date"},
                "group_size": {"type": "integer"},
                "activities": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "include_weather": {"type": "boolean"}
            },
            "required": ["location"]
        }
    }

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        tools=[{"type": "function", "function": function_schema}],
        tool_choice={"type": "function", "function": {"name": "extract_trip_info"}}
    )

    try:
        tool_call = response.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        trip = Trip(**arguments)
        return trip
    except (KeyError, IndexError, json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Failed to extract Trip data: {e}")
