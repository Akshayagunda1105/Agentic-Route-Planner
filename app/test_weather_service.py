from app.models.location import Location

from app.services.weather_service import WeatherService


location = Location(

    name="Hyderabad",

    district="Hyderabad",

    subdistrict="Bandlaguda",

    latitude=17.40030329999287,

    longitude=78.47703451108815

)

weather = WeatherService.get_weather(location)

print(weather)