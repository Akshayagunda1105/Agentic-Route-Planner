from app.graph.route_graph import (
    route_graph
)

from app.state.route_planner_state import (
    RoutePlannerState
)

state = RoutePlannerState(

    query="I am in Hyderabad and want to visit Kodad"

)

result = route_graph.invoke(state)

print(result)

print("\nFinal Result:\n")

print(result["result"])