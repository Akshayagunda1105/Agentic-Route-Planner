from typing import List

from pydantic import BaseModel

from app.models.weather_report import WeatherReport


class WeatherAnalysis(BaseModel):

    reports: List[WeatherReport]

    overall_risk: str

    recommendation: str