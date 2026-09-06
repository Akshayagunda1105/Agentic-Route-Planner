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

    def resolve(location_query):
        selected = state.selections.get(location_query)
        if selected:
            from app.models.retrieval_result import RetrievalResult
            return RetrievalResult(
                resolved=True,
                location=selected,
                message="User-selected location."
            )
        return retriever.resolve_location(location_query)

    # Resolve start
    start = resolve(request.start)

    if not start.resolved:

        state.pending_locations = [start]

        return state

    # Resolve destination
    destination = resolve(request.destination)

    if not destination.resolved:

        state.pending_locations = [destination]

        return state

    # Resolve waypoints
    waypoints = []

    for waypoint in request.waypoints:

        result = resolve(waypoint)

        if not result.resolved:

            state.pending_locations = [result]

            return state

        waypoints.append(
            result.location
        )

    state.start_location = start.location

    state.destination_location = (
        destination.location
    )

    state.waypoint_locations = waypoints

    return state
