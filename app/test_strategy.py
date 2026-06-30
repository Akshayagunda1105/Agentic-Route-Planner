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

destination = Location(
    name="Suryapet",
    district="Suryapet",
    subdistrict="Suryapet",
    latitude=17.11,
    longitude=79.73
)

plan = RoutePlan(
    start=start,
    destinations=[destination]
)

strategy = NearestNeighborStrategy()

result = strategy.optimize(plan)

print(result)