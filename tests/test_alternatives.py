from unittest.mock import patch

import pytest

from app.models.location import Location
from app.models.optimization_result import OptimizationResult
from app.models.route_plan import RoutePlan
from app.models.route_request import RouteRequest
from app.models.weather_analysis import WeatherAnalysis
from app.graph import alternatives_node as alternatives_module
from app.state.route_planner_state import RoutePlannerState
from app.models.weather_risk import WeatherRisk


def route_plan():
    start = Location(
        name="Start",
        latitude=28.6139,
        longitude=77.2090,
        district="New Delhi",
        subdistrict="New Delhi",
    )

    waypoint_1 = Location(
        name="Waypoint 1",
        latitude=28.6200,
        longitude=77.2100,
        district="New Delhi",
        subdistrict="New Delhi",
    )

    waypoint_2 = Location(
        name="Waypoint 2",
        latitude=28.6300,
        longitude=77.2200,
        district="New Delhi",
        subdistrict="New Delhi",
    )

    destination = Location(
        name="Destination",
        latitude=28.6400,
        longitude=77.2300,
        district="New Delhi",
        subdistrict="New Delhi",
    )

    return RoutePlan(
        start=start,
        destination=destination,
        waypoints=[waypoint_1, waypoint_2],
    )


def optimization_result(route, strategy="Test"):
    return OptimizationResult(
        route=route,
        total_distance=10.0,
        total_duration=20.0,
        strategy=strategy,
        execution_time=0.01,
    )


def weather_analysis(score: float):
    return WeatherAnalysis(
        reports=[],
        overall_risk=WeatherRisk(
            score=score,
            level="Test",
            recommendation="Test recommendation",
        ),
        recommendation="Test recommendation",
    )

class FakeOptimizerAgent:
    def __init__(self, alternative=None):
        self.alternative = alternative
        self.calls = []

    def generate_alternative(
        self,
        route_plan,
        objective="duration",
        weather_sensitive=False,
        weather_weight=0.3,
        departure_time=None,
    ):
        self.calls.append(
            {
                "route_plan": route_plan,
                "objective": objective,
                "weather_sensitive": weather_sensitive,
                "weather_weight": weather_weight,
                "departure_time": departure_time,
            }
        )

        return self.alternative


class FakeWeatherAgent:
    def __init__(self, alternative_score):
        self.alternative_score = alternative_score
        self.calls = []

    def analyze(self, optimization):
        self.calls.append(optimization)

        if optimization.strategy == "Alternative":
            return weather_analysis(self.alternative_score)

        raise AssertionError(
            "Primary weather should come from state.weather, "
            "not from WeatherAgent.analyze()."
        )


def test_alternatives_node_presents_lower_weather_risk_route():
    plan = route_plan()

    primary = optimization_result(
        [
            plan.start,
            plan.waypoints[0],
            plan.waypoints[1],
            plan.destination,
        ],
        strategy="Primary",
    )

    alternative = optimization_result(
        [
            plan.start,
            plan.waypoints[1],
            plan.waypoints[0],
            plan.destination,
        ],
        strategy="Alternative",
    )

    fake_optimizer = FakeOptimizerAgent(alternative)
    fake_weather = FakeWeatherAgent(alternative_score=50)

    state = RoutePlannerState(
        query="Test route",
        route_plan=plan,
        optimization=primary,
        weather=weather_analysis(90),
    )

    with patch.object(
        alternatives_module,
        "optimizer_agent",
        fake_optimizer,
    ), patch.object(
        alternatives_module,
        "weather_agent",
        fake_weather,
    ):
        result = alternatives_module.alternatives_node(state)

    assert result.selection_required is True
    assert len(result.options) == 2

    assert result.options[0].option_id == "route_a"
    assert result.options[1].option_id == "route_b"

    assert result.options[1].label == (
        "Route B — Lower-Weather-Risk Alternative"
    )

    assert result.options[0].weather_risk_score == 90
    assert result.options[1].weather_risk_score == 50


def test_alternatives_node_does_not_present_higher_risk_route():
    plan = route_plan()

    primary = optimization_result(
        [
            plan.start,
            plan.waypoints[0],
            plan.waypoints[1],
            plan.destination,
        ],
        strategy="Primary",
    )

    alternative = optimization_result(
        [
            plan.start,
            plan.waypoints[1],
            plan.waypoints[0],
            plan.destination,
        ],
        strategy="Alternative",
    )

    fake_optimizer = FakeOptimizerAgent(alternative)
    fake_weather = FakeWeatherAgent(alternative_score=80)

    state = RoutePlannerState(
        query="Test route",
        route_plan=plan,
        optimization=primary,
        weather=weather_analysis(50),
    )

    with patch.object(
        alternatives_module,
        "optimizer_agent",
        fake_optimizer,
    ), patch.object(
        alternatives_module,
        "weather_agent",
        fake_weather,
    ):
        result = alternatives_module.alternatives_node(state)

    assert result.selection_required is False
    assert len(result.options) == 1
    assert result.options[0].option_id == "route_a"


def test_alternatives_node_does_not_present_equal_risk_route():
    plan = route_plan()

    primary = optimization_result(
        [
            plan.start,
            plan.waypoints[0],
            plan.waypoints[1],
            plan.destination,
        ],
        strategy="Primary",
    )

    alternative = optimization_result(
        [
            plan.start,
            plan.waypoints[1],
            plan.waypoints[0],
            plan.destination,
        ],
        strategy="Alternative",
    )

    fake_optimizer = FakeOptimizerAgent(alternative)
    fake_weather = FakeWeatherAgent(alternative_score=70)

    state = RoutePlannerState(
        query="Test route",
        route_plan=plan,
        optimization=primary,
        weather=weather_analysis(70),
    )

    with patch.object(
        alternatives_module,
        "optimizer_agent",
        fake_optimizer,
    ), patch.object(
        alternatives_module,
        "weather_agent",
        fake_weather,
    ):
        result = alternatives_module.alternatives_node(state)

    assert result.selection_required is False
    assert len(result.options) == 1
    assert result.options[0].option_id == "route_a"


def test_alternatives_node_keeps_primary_route_when_no_alternative_exists():
    plan = route_plan()

    primary = optimization_result(
        [
            plan.start,
            plan.waypoints[0],
            plan.waypoints[1],
            plan.destination,
        ],
        strategy="Primary",
    )

    fake_optimizer = FakeOptimizerAgent(None)
    fake_weather = FakeWeatherAgent(alternative_score=50)

    state = RoutePlannerState(
        query="Test route",
        route_plan=plan,
        optimization=primary,
        weather=weather_analysis(90),
    )

    with patch.object(
        alternatives_module,
        "optimizer_agent",
        fake_optimizer,
    ), patch.object(
        alternatives_module,
        "weather_agent",
        fake_weather,
    ):
        result = alternatives_module.alternatives_node(state)

    assert result.selection_required is False
    assert len(result.options) == 1
    assert result.options[0].option_id == "route_a"


def test_alternatives_node_passes_request_preferences_to_optimizer():
    plan = route_plan()

    primary = optimization_result(
        [
            plan.start,
            plan.waypoints[0],
            plan.waypoints[1],
            plan.destination,
        ],
        strategy="Primary",
    )

    alternative = optimization_result(
        [
            plan.start,
            plan.waypoints[1],
            plan.waypoints[0],
            plan.destination,
        ],
        strategy="Alternative",
    )

    fake_optimizer = FakeOptimizerAgent(alternative)
    fake_weather = FakeWeatherAgent(alternative_score=50)

    request = RouteRequest(
        start="Start",
        destination="Destination",
        waypoints=["Waypoint 1", "Waypoint 2"],
        objective="weather_aware",
        weather_sensitive=True,
        weather_weight=0.8,
        departure_time="2026-09-13T10:00:00",
    )

    state = RoutePlannerState(
        query="Test route",
        request=request,
        route_plan=plan,
        optimization=primary,
        weather=weather_analysis(90),
    )

    with patch.object(
        alternatives_module,
        "optimizer_agent",
        fake_optimizer,
    ), patch.object(
        alternatives_module,
        "weather_agent",
        fake_weather,
    ):
        alternatives_module.alternatives_node(state)

    assert len(fake_optimizer.calls) == 1

    call = fake_optimizer.calls[0]

    assert call["route_plan"] is plan
    assert call["objective"] == "weather_aware"
    assert call["weather_sensitive"] is True
    assert call["weather_weight"] == 0.8
    assert call["departure_time"] == "2026-09-13T10:00:00"


def test_alternatives_node_requires_route_plan():
    primary = optimization_result([])

    state = RoutePlannerState(
        query="Test route",
        optimization=primary,
    )

    fake_optimizer = FakeOptimizerAgent(None)

    with patch.object(
        alternatives_module,
        "optimizer_agent",
        fake_optimizer,
    ):
        with pytest.raises(
            ValueError,
            match="Route plan is required before generating alternatives",
        ):
            alternatives_module.alternatives_node(state)

    assert fake_optimizer.calls == []


def test_alternatives_node_requires_primary_optimization():
    plan = route_plan()

    state = RoutePlannerState(
        query="Test route",
        route_plan=plan,
    )

    fake_optimizer = FakeOptimizerAgent(None)

    with patch.object(
        alternatives_module,
        "optimizer_agent",
        fake_optimizer,
    ):
        with pytest.raises(
            ValueError,
            match="Primary optimization is required before generating alternatives",
        ):
            alternatives_module.alternatives_node(state)

    assert fake_optimizer.calls == []