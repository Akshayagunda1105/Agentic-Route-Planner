from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.location import Location


class WeatherInfo(BaseModel):

    location: Location

    temperature: float

    condition: str

    humidity: int

    wind_speed: float

    # Time represented by this weather observation/forecast.
    #
    # None is allowed for backward compatibility with the current-weather
    # endpoint and existing callers.
    forecast_time: Optional[datetime] = None