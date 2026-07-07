from app.state.route_planner_state import (
    RoutePlannerState
)

from app.models.route_planning_result import (
    RoutePlanningResult
)


def result_node(
    state: RoutePlannerState
):

    result = RoutePlanningResult(

        success=state.reflection.approved,

        optimization=state.optimization,

        weather=state.weather,

        reflection=state.reflection

    )

    state.result = result

    return state