from app.models.route_request import RouteRequest
from app.services.route_plan_builder import RoutePlanBuilder

request = RouteRequest(
    start="Hyderabad",
    destination="Suryapet",
    waypoints=[
        "Kodad",
        "Nalgonda"
    ]
)

builder = RoutePlanBuilder()

route_plan = builder.build(request)

print(route_plan)