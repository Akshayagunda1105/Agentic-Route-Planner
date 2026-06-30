from app.models.location import Location

from app.services.distance_service import (
    DistanceService
)

loc1 = Location(

    name="Hyderabad",

    district="Hyderabad",

    subdistrict="Shaikpet",

    latitude=17.42,

    longitude=78.47

)

loc2 = Location(

    name="Suryapet",

    district="Suryapet",

    subdistrict="Suryapet",

    latitude=17.11,

    longitude=79.73

)

distance = DistanceService.calculate(

    loc1,

    loc2

)

print(distance)