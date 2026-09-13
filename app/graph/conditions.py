from app.state.route_planner_state import (
    RoutePlannerState
)


def retriever_condition(
    state: RoutePlannerState
):
    """
    Decide whether location retrieval is complete.

    If unresolved locations remain, the graph returns a pending
    result so the user can provide a selection.
    """

    if state.pending_locations:
        return "pending"

    return "continue"


def reflection_condition(
    state: RoutePlannerState
):
    """
    Decide what should happen after deterministic reflection.

    Critical weather is intentionally handled separately from
    normal validation failures.

    - Invalid route/data -> retry
    - Critical weather -> generate alternatives
    - Everything else -> result
    """

    if state.reflection is None:
        return "result"

    # Critical weather is a human-in-the-loop condition.
    # Do not automatically replan or change the user's preferences.
    if (
        state.reflection.replan_reason
        == "CRITICAL_WEATHER_RISK"
    ):
        return "alternatives"

    # Other deterministic validation failures may still
    # request another planning attempt.
    if state.reflection.should_retry:
        return "retry"

    return "result"