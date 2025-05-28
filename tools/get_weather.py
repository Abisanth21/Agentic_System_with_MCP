import requests
import os

# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your_weatherapi_key")  # fallback
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
def get_weather(city: str):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "aqi": "no"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            return {"error": data.get("error", {}).get("message", "Unknown error")}

        condition = data["current"]["condition"]["text"]
        temp_c = data["current"]["temp_c"]
        return {
            "result": f"Weather in {city}: {condition}, {temp_c}°C"
        }

    except Exception as e:
        return {"error": str(e)}
