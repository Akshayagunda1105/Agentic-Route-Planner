from langgraph.graph import StateGraph, START, END

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

from app.graph.weather_node import (
    weather_node
)

from app.graph.reflection_node import (
    reflection_node
)

from app.graph.result_node import (
    result_node
)

# -----------------------------------
# Create Graph
# -----------------------------------

builder = StateGraph(RoutePlannerState)

# -----------------------------------
# Register Nodes
# -----------------------------------

builder.add_node("parser", parser_node)

builder.add_node("retriever", retriever_node)

builder.add_node("builder", builder_node)

builder.add_node("optimizer", optimizer_node)

builder.add_node("weather", weather_node)

builder.add_node("reflection", reflection_node)

builder.add_node("result", result_node)

# -----------------------------------
# Connect Nodes
# -----------------------------------

builder.add_edge(START, "parser")

builder.add_edge("parser", "retriever")

builder.add_edge("retriever", "builder")

builder.add_edge("builder", "optimizer")

builder.add_edge("optimizer", "weather")

builder.add_edge("weather", "reflection")

builder.add_edge("reflection", "result")

builder.add_edge("result", END)

# -----------------------------------
# Compile Graph
# -----------------------------------

route_graph = builder.compile()