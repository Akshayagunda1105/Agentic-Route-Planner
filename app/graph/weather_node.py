from app.agents.weather_agent import (
    WeatherAgent
)

from app.state.route_planner_state import (
    RoutePlannerState
)


weather_agent = WeatherAgent()


def weather_node(
    state: RoutePlannerState
):

    weather = weather_agent.analyze(
        state.optimization
    )

    state.weather = weather

    return state