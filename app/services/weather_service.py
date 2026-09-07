from datetime import datetime, timezone

import requests

from app.config.settings import OPENWEATHER_API_KEY
from app.models.location import Location
from app.models.weather_info import WeatherInfo


class WeatherService:

    CURRENT_WEATHER_URL = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    FORECAST_URL = (
        "https://api.openweathermap.org/data/2.5/forecast"
    )

    WIND_SPEED_UNIT = "m/s"

    @classmethod
    def get_weather(
        cls,
        location: Location,
    ) -> WeatherInfo:

        params = {
            "lat": location.latitude,
            "lon": location.longitude,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }

        response = requests.get(
            cls.CURRENT_WEATHER_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        observation_timestamp = data.get("dt")

        forecast_time = None

        if observation_timestamp is not None:
            forecast_time = datetime.fromtimestamp(
                observation_timestamp,
                tz=timezone.utc,
            )

        return cls._weather_info_from_current_response(
            location,
            data,
            forecast_time=forecast_time,
        )

    @classmethod
    def get_weather_at(
        cls,
        location: Location,
        target_time: datetime,
    ) -> WeatherInfo:
        """
        Return the forecast closest to the requested arrival time.

        OpenWeather's standard forecast endpoint provides forecasts
        at discrete time intervals. The forecast point closest to
        target_time is selected.
        """

        if target_time.tzinfo is None:
            raise ValueError(
                "target_time must be timezone-aware."
            )

        target_time_utc = target_time.astimezone(timezone.utc)

        params = {
            "lat": location.latitude,
            "lon": location.longitude,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }

        response = requests.get(
            cls.FORECAST_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        forecast = cls._select_closest_forecast(
            data.get("list", []),
            target_time_utc,
        )

        if forecast is None:
            raise ValueError(
                "No weather forecast is available near "
                f"{target_time.isoformat()}."
            )

        forecast_timestamp = forecast.get("dt")

        if forecast_timestamp is None:
            raise ValueError(
                "Selected weather forecast has no timestamp."
            )

        forecast_time = datetime.fromtimestamp(
            forecast_timestamp,
            tz=timezone.utc,
        )

        return cls._weather_info_from_forecast(
            location,
            forecast,
            forecast_time=forecast_time,
        )

    @staticmethod
    def _select_closest_forecast(
        forecasts: list[dict],
        target_time: datetime,
    ) -> dict | None:

        if not forecasts:
            return None

        closest_forecast = None
        closest_difference = None

        for forecast in forecasts:
            timestamp = forecast.get("dt")

            if timestamp is None:
                continue

            forecast_time = datetime.fromtimestamp(
                timestamp,
                tz=timezone.utc,
            )

            difference = abs(
                (
                    forecast_time - target_time
                ).total_seconds()
            )

            if (
                closest_difference is None
                or difference < closest_difference
            ):
                closest_difference = difference
                closest_forecast = forecast

        return closest_forecast

    @staticmethod
    def _weather_info_from_current_response(
        location: Location,
        data: dict,
        forecast_time: datetime | None = None,
    ) -> WeatherInfo:

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
            forecast_time=forecast_time,
        )

    @staticmethod
    def _weather_info_from_forecast(
        location: Location,
        data: dict,
        forecast_time: datetime,
    ) -> WeatherInfo:

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
            forecast_time=forecast_time,
        )