from pydantic import BaseModel

from app.models.location import Location


class WeatherInfo(BaseModel):

    location: Location

    temperature: float

    condition: str

    humidity: int

    wind_speed: float
