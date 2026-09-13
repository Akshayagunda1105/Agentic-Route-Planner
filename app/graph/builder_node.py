from app.services.route_plan_builder import (
    RoutePlanBuilder
)

from app.state.route_planner_state import (
    RoutePlannerState
)


route_plan_builder = RoutePlanBuilder()


def builder_node(
    state: RoutePlannerState
):

    if state.start_location is None:

        raise ValueError(
            "Start location is required before building the route plan."
        )

    if state.destination_location is None:

        raise ValueError(
            "Destination location is required before building the route plan."
        )

    state.route_plan = route_plan_builder.build(
        start=state.start_location,
        destination=state.destination_location,
        waypoints=state.waypoint_locations,
    )

    return state