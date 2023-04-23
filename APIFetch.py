from dotenv import load_dotenv, find_dotenv
import requests
from os import getenv


def get_weather_data():
    load_dotenv(find_dotenv())

    # San Marcos: 29.89* N, -97.94* W
    weather_forecast = requests.get(
        "https://api.openweathermap.org/data/3.0/onecall",
        params={
            "lat": "29.89",
            "lon": "-97.94",
            "appid": getenv("WEATHER_API_KEY"),
            "units": "imperial",
        },
    )

    return weather_forecast.json()


def get_daily_forecast():
    weather_data = get_weather_data()
    try:
        daily_forecast = weather_data["current"]["temp"]
    except:
        return 404
        # If this temperatue pops up, either it's the end of the world, or the API fetch failed
    finally:
        return daily_forecast


print(get_daily_forecast())
