from app.orchestrators.route_planner import (
    RoutePlanner
)

planner = RoutePlanner()

result = planner.plan(

    "I am in Hyderabad and want to visit Kodad and Nalgonda before reaching Suryapet."

)

print(result)