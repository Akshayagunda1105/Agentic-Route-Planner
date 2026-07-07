from app.state.route_planner_state import (
    RoutePlannerState
)

from app.agents.parser_agent import (
    ParserAgent
)


parser = ParserAgent()


def parser_node(
    state: RoutePlannerState
):

    request = parser.parse(
        state.query
    )

    state.request = request

    return state