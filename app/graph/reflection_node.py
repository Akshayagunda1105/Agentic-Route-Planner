from app.agents.reflection_agent import (
    ReflectionAgent
)

from app.state.route_planner_state import (
    RoutePlannerState
)


reflection_agent = ReflectionAgent()


def reflection_node(
    state: RoutePlannerState
):

    reflection = reflection_agent.evaluate(

        state.optimization,

        state.weather,

        replan_attempt=state.replan_attempt

    )

    state.reflection = reflection

    return state