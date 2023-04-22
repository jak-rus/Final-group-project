from dotenv import load_dotenv, find_dotenv
import requests
from os import getenv


def get_weather_forecast():
    load_dotenv(find_dotenv())

    # San Marcos: 29.89* N, -97.94* W
    weather_forecast = requests.get(
        "https://api.openweathermap.org/data/3.0/onecall",
        params={"lat": "29.89", "lon": "-97.94", "appid": getenv("WEATHER_API_KEY")},
    )

    return weather_forecast.json()


print(get_weather_forecast())
