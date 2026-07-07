from app.state.route_planner_state import (
    RoutePlannerState
)

from app.graph.parser_node import (
    parser_node
)

from app.graph.retriever_node import (
    retriever_node
)

from app.graph.builder_node import (
    builder_node
)

from app.graph.optimizer_node import (
    optimizer_node
)

state = RoutePlannerState(

    query="I am in Hyderabad and want to visit Kodad"

)

state = parser_node(state)

state = retriever_node(state)

state = builder_node(state)

state = optimizer_node(state)

print(state)