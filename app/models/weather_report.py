from pydantic import BaseModel

from app.models.weather_info import WeatherInfo
from app.models.weather_risk import WeatherRisk


class WeatherReport(BaseModel):

    weather: WeatherInfo

    risk: WeatherRisk