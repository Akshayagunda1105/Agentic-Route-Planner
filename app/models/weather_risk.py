from pydantic import BaseModel


class WeatherRisk(BaseModel):

    score: int

    level: str

    recommendation: str