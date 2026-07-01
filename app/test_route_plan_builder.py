from app.models.location import Location
from app.services.route_plan_builder import RoutePlanBuilder

start = Location(
    name="Hyderabad",
    district="Hyderabad",
    subdistrict="Hyderabad",
    latitude=17.40,
    longitude=78.47
)

destination = Location(
    name="Suryapet",
    district="Suryapet",
    subdistrict="Suryapet",
    latitude=17.11,
    longitude=79.73
)

waypoints = [

    Location(
        name="Kodad",
        district="Suryapet",
        subdistrict="Kodad",
        latitude=16.97,
        longitude=79.99
    ),

    Location(
        name="Nalgonda",
        district="Nalgonda",
        subdistrict="Nalgonda",
        latitude=16.91,
        longitude=79.19
    )

]

builder = RoutePlanBuilder()

route_plan = builder.build(
    start,
    destination,
    waypoints
)

print(route_plan)