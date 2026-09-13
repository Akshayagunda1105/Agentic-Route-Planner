from typing import List, Optional

from pydantic import BaseModel

from app.models.weather_report import WeatherReport
from app.models.weather_risk import WeatherRisk


class WeatherAnalysis(BaseModel):

    reports: List[WeatherReport]

    overall_risk: Optional[WeatherRisk] = None

    recommendation: str