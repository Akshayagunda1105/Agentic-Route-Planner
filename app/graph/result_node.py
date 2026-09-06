from app.state.route_planner_state import (
    RoutePlannerState
)

from app.models.route_planning_result import (
    RoutePlanningResult
)


def result_node(
    state: RoutePlannerState
):

    # -----------------------------------
    # User clarification required
    # -----------------------------------

    if state.pending_locations:

        result = RoutePlanningResult(

            success=False,

            pending_locations=state.pending_locations,

            errors=[]

        )

        state.result = result

        return state

    # -----------------------------------
    # Successful route planning
    # -----------------------------------

    result = RoutePlanningResult(

        success=state.reflection.approved,

        optimization=state.optimization,

        weather=state.weather,

        reflection=state.reflection,

        pending_locations=[],

        errors=[]

    )

    state.result = result

    return state