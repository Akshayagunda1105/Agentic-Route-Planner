from app.services.route_plan_builder import (
    RoutePlanBuilder
)

from app.state.route_planner_state import (
    RoutePlannerState
)


builder = RoutePlanBuilder()


def builder_node(
    state: RoutePlannerState
):

    route_plan = builder.build(

        state.start_location,

        state.destination_location,

        state.waypoint_locations

    )

    state.route_plan = route_plan

    return state