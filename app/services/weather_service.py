import requests

from app.config.settings import OPENWEATHER_API_KEY

from app.models.location import Location
from app.models.weather_info import WeatherInfo


class WeatherService:

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @classmethod
    def get_weather(
        cls,
        location: Location
    ) -> WeatherInfo:

        params = {

            "lat": location.latitude,

            "lon": location.longitude,

            "appid": OPENWEATHER_API_KEY,

            "units": "metric"

        }

        response = requests.get(

            cls.BASE_URL,

            params=params,

            timeout=10

        )

        response.raise_for_status()

        data = response.json()

        temperature = data["main"]["temp"]

        humidity = data["main"]["humidity"]

        wind_speed = data["wind"]["speed"]

        condition = data["weather"][0]["main"]

        return WeatherInfo(

            location=location,

            temperature=temperature,

            condition=condition,

            humidity=humidity,

            wind_speed=wind_speed,

            risk="Unknown"

        )