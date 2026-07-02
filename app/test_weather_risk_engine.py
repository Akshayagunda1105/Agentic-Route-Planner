from app.models.location import Location

from app.models.weather_info import WeatherInfo

from app.services.weather_risk_engine import (
    WeatherRiskEngine
)

location = Location(

    name="Kodad",

    district="Suryapet",

    subdistrict="Kodad",

    latitude=16.97,

    longitude=79.99

)

weather = WeatherInfo(

    location=location,

    temperature=28,

    condition="Rain",

    humidity=92,

    wind_speed=18,

    risk="Unknown"

)

risk = WeatherRiskEngine.calculate_risk(
    weather
)

print(risk)