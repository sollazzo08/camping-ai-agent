import requests

def lookup_location(location: str) -> dict:
    """
    Uses OpenStreetMap's Nominatim API to look up the location and return cleaned data.
    Returns:
        {
            "display_name": "...",
            "lat": "...",
            "lon": "...",
            "address": {...}
        }
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }

    headers = {
        "User-Agent": "camping-ai-agent/1.0"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError(f"Location not found for '{location}'")

    result = data[0]
    address = result.get("address", {})
    return {
        "display_name": result["display_name"],
        "lat": float(result["lat"]),
        "lon": float(result["lon"]),
        "address": result.get("address", {}),
        "zip": address.get("postcode")

    }
