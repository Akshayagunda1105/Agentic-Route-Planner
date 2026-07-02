from app.models.location import Location

from app.models.weather_info import WeatherInfo


location = Location(

    name="Kodad",

    district="Suryapet",

    subdistrict="Kodad",

    latitude=16.97,

    longitude=79.99

)

weather = WeatherInfo(

    location=location,

    temperature=28.5,

    condition="Sunny",

    humidity=60,

    wind_speed=10,

    risk="Low"

)

print(weather)