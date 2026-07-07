from app.agents.retriever_agent import (
    RetrieverAgent
)

from app.state.route_planner_state import (
    RoutePlannerState
)


retriever = RetrieverAgent()


def retriever_node(
    state: RoutePlannerState
):

    request = state.request

    # Resolve start
    start = retriever.resolve_location(
        request.start
    )

    if not start.resolved:
        raise Exception(start.message)

    # Resolve destination
    destination = retriever.resolve_location(
        request.destination
    )

    if not destination.resolved:
        raise Exception(destination.message)

    # Resolve waypoints
    waypoints = []

    for waypoint in request.waypoints:

        result = retriever.resolve_location(
            waypoint
        )

        if not result.resolved:
            raise Exception(result.message)

        waypoints.append(
            result.location
        )

    state.start_location = start.location

    state.destination_location = (
        destination.location
    )

    state.waypoint_locations = waypoints

    return state