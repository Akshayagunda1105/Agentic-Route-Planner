from app.models.location import Location
from app.services.distance_service import DistanceService

hyderabad = Location(
    name="Hyderabad",
    district="Hyderabad",
    subdistrict="Shaikpet",
    latitude=17.42,
    longitude=78.47
)

suryapet = Location(
    name="Suryapet",
    district="Suryapet",
    subdistrict="Suryapet",
    latitude=17.11,
    longitude=79.73
)

distance = DistanceService.calculate(
    hyderabad,
    suryapet
)

print(f"Distance: {distance:.2f} km")