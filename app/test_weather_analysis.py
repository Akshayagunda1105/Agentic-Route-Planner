from app.models.location import Location
from app.models.weather_info import WeatherInfo
from app.models.weather_analysis import WeatherAnalysis

location = Location(
    name="Kodad",
    district="Suryapet",
    subdistrict="Kodad",
    latitude=16.97,
    longitude=79.99
)

weather = WeatherInfo(
    location=location,
    temperature=26,
    condition="Heavy Rain",
    humidity=92,
    wind_speed=18,
    risk="High"
)

analysis = WeatherAnalysis(
    reports=[weather],
    overall_risk="High",
    recommendation="Heavy rain expected. Consider delaying travel."
)

print(analysis)