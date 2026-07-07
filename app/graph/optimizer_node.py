from app.agents.optimizer_agent import (
    OptimizerAgent
)

from app.state.route_planner_state import (
    RoutePlannerState
)


optimizer = OptimizerAgent()


def optimizer_node(
    state: RoutePlannerState
):

    optimization = optimizer.optimize(
        state.route_plan
    )

    state.optimization = optimization

    return state