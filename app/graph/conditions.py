from app.state.route_planner_state import (
    RoutePlannerState
)


def retriever_condition(
    state: RoutePlannerState
):

    if state.pending_locations:

        return "pending"

    return "continue"