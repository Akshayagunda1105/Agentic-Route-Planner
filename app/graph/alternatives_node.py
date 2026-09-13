from app.agents.optimizer_agent import OptimizerAgent
from app.agents.weather_agent import WeatherAgent
from app.models.route_planning_result import RoutePlanningOption
from app.state.route_planner_state import RoutePlannerState


optimizer_agent = OptimizerAgent()
weather_agent = WeatherAgent()


def alternatives_node(
    state: RoutePlannerState,
):
    """
    Generate and evaluate an alternative route when critical
    weather risk has been detected.

    This node is intentionally human-in-the-loop:

    - The primary route is preserved as Route A.
    - A distinct alternative route is generated when possible.
    - Weather risk is calculated independently for Route B.
    - Route B is presented as a lower-weather-risk alternative
      only when its deterministic risk score is actually lower.
    - The user's preferences are never silently changed.
    """

    if state.route_plan is None:
        raise ValueError(
            "Route plan is required before generating alternatives."
        )

    if state.optimization is None:
        raise ValueError(
            "Primary optimization is required before generating alternatives."
        )

    primary_optimization = state.optimization
    primary_weather = state.weather

    # The current optimizer can generate a distinct candidate by
    # changing waypoint ordering. If that is not possible, there
    # is no alternative route to present.
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

    alternative_optimization = optimizer_agent.generate_alternative(
        state.route_plan,
        objective=objective,
        weather_sensitive=weather_sensitive,
        weather_weight=weather_weight,
        departure_time=departure_time,
    )

    # Always preserve the primary route as Route A.
    primary_risk_score = (
        primary_weather.overall_risk.score
        if primary_weather is not None
        and primary_weather.overall_risk is not None
        else None
    )

    options = [
        RoutePlanningOption(
            option_id="route_a",
            label="Route A — Requested Route",
            description=(
                "The primary route generated from your requested "
                "preferences."
            ),
            optimization=primary_optimization,
            weather=primary_weather,
            weather_risk_score=primary_risk_score,
        )
    ]

    # No distinct candidate could be generated.
    if alternative_optimization is None:
        state.options = options
        state.selection_required = False
        return state

    # Analyze weather independently for the alternative route.
    alternative_weather = weather_agent.analyze(
        alternative_optimization
    )

    alternative_risk_score = (
        alternative_weather.overall_risk.score
        if alternative_weather.overall_risk is not None
        else None
    )

    # Only present Route B as a lower-weather-risk alternative when
    # the deterministic weather score actually proves that it is lower.
    if (
        primary_risk_score is not None
        and alternative_risk_score is not None
        and alternative_risk_score < primary_risk_score
    ):
        options.append(
            RoutePlanningOption(
                option_id="route_b",
                label="Route B — Lower-Weather-Risk Alternative",
                description=(
                    "A different route with a lower deterministic "
                    "weather-risk score than Route A."
                ),
                optimization=alternative_optimization,
                weather=alternative_weather,
                weather_risk_score=alternative_risk_score,
            )
        )

        state.selection_required = True
    else:
        state.selection_required = False

    state.options = options

    return state