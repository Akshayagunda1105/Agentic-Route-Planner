from app.models.location import Location
from app.models.route_plan import RoutePlan

from app.strategies.nearest_neighbor import (
    NearestNeighborStrategy
)

start = Location(
    name="Hyderabad",
    district="Hyderabad",
    subdistrict="Shaikpet",
    latitude=17.42,
    longitude=78.47
)

nalgonda = Location(
    name="Nalgonda",
    district="Nalgonda",
    subdistrict="Nalgonda",
    latitude=17.05,
    longitude=79.27
)

suryapet = Location(
    name="Suryapet",
    district="Suryapet",
    subdistrict="Suryapet",
    latitude=17.11,
    longitude=79.73
)

kodad = Location(
    name="Kodad",
    district="Suryapet",
    subdistrict="Kodad",
    latitude=17.00,
    longitude=79.97
)

plan = RoutePlan(
    start=start,
    destinations=[
        suryapet,
        kodad,
        nalgonda
    ]
)

strategy = NearestNeighborStrategy()

result = strategy.optimize(plan)

print(result)