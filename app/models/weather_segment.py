from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.location import Location
from app.models.weather_info import WeatherInfo
from app.models.weather_risk import WeatherRisk


class WeatherSegment(BaseModel):
    """
    Weather and risk information for a sampled point along a road segment.
    """

    origin: Location
    destination: Location

    latitude: float
    longitude: float

    weather: Optional[WeatherInfo] = None

    forecast_time: Optional[datetime] = None

    risk: Optional[WeatherRisk] = None