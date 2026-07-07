from app.graph.parser_node import parser_node
from app.graph.retriever_node import retriever_node

from app.state.route_planner_state import (
    RoutePlannerState
)

state = RoutePlannerState(

    query="I am in Hyderabad and want to visit Kodad"

)

state = parser_node(state)

state = retriever_node(state)

print(state)