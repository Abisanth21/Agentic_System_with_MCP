import requests
import os

# EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY", "your_exchangerateapi_key")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

def convert_currency(amount: float, from_currency: str, to_currency: str):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["result"] != "success":
            return {"error": data.get("error-type", "API error")}

        converted_amount = data["conversion_result"]
        return {
            "result": f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
        }

    except Exception as e:
        return {"error": str(e)}
