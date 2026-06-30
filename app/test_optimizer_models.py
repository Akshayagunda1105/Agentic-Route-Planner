from app.models.location import Location
from app.models.route_plan import RoutePlan
from app.models.optimization_result import OptimizationResult


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

print(plan)

result = OptimizationResult(

    route=[

        start,

        destination

    ],

    total_distance=137.2,

    strategy="Nearest Neighbor",

    execution_time=0.0034

)

print()

print(result)