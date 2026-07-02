from app.models.location import Location
from app.models.weather_info import WeatherInfo
from app.models.weather_risk import WeatherRisk
from app.models.weather_report import WeatherReport


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

risk = WeatherRisk(

    score=65,

    level="High",

    recommendation="Delay travel if possible."

)

report = WeatherReport(

    weather=weather,

    risk=risk

)

print(report)