from app.agents.optimizer_agent import OptimizerAgent
from app.state.route_planner_state import RoutePlannerState


optimizer = OptimizerAgent()


def optimizer_node(state: RoutePlannerState):
    if state.route_plan is None:
        raise ValueError(
            "Route plan is required before optimization."
        )

    request = state.request

    objective = "duration"
    weather_sensitive = False
    weather_weight = 0.3
    departure_time = None

    if request is not None:
        objective = request.objective
        weather_sensitive = request.weather_sensitive
        weather_weight = request.weather_weight
        departure_time = request.departure_time

    optimization = optimizer.optimize(
        state.route_plan,
        objective=objective,
        weather_sensitive=weather_sensitive,
        weather_weight=weather_weight,
        departure_time=departure_time,
    )

    state.optimization = optimization

    return state