import pytest

from app.agents.optimizer_agent import OptimizerAgent
from app.models.location import Location
from app.models.road_cost_matrix import RoadCostMatrix
from app.models.weather_info import WeatherInfo
from app.models.weather_risk import WeatherRisk
from app.services.route_plan_builder import RoutePlanBuilder
from app.services.routing_service import (
    RoutingProviderUnavailableError,
    RoutingService,
)
from app.strategies.nearest_neighbor import NearestNeighborStrategy


def location(name: str, latitude: float, longitude: float) -> Location:
    return Location(
        name=name,
        district="District",
        subdistrict="Subdistrict",
        latitude=latitude,
        longitude=longitude,
    )


def route_plan():
    start = location("Start", 0, 0)
    geographic_near = location("Geographic near", 0, 0.1)
    road_near = location("Road near", 0, 1)
    destination = location("Destination", 0, 2)

    return RoutePlanBuilder().build(
        start,
        destination,
        [geographic_near, road_near],
    )


def road_matrix() -> RoadCostMatrix:
    # Index order:
    # 0 = Start
    # 1 = Geographic near
    # 2 = Road near
    # 3 = Destination

    # The geographically farther waypoint is much faster by road.
    return RoadCostMatrix(
        distance_meters=[
            [0, 10_000, 2_000, 20_000],
            [10_000, 0, 1_000, 3_000],
            [2_000, 1_000, 0, 4_000],
            [20_000, 3_000, 4_000, 0],
        ],
        duration_seconds=[
            [0, 1_000, 20, 2_000],
            [1_000, 0, 50, 100],
            [20, 50, 0, 200],
            [2_000, 100, 200, 0],
        ],
    )


def test_road_cost_order_can_differ_from_haversine_order():
    plan = route_plan()
    strategy = NearestNeighborStrategy()

    geographic = strategy.optimize(plan)

    road = strategy.optimize(
        plan,
        road_matrix(),
        cost_metric="duration",
    )

    assert [place.name for place in geographic.route] == [
        "Start",
        "Geographic near",
        "Road near",
        "Destination",
    ]

    assert [place.name for place in road.route] == [
        "Start",
        "Road near",
        "Geographic near",
        "Destination",
    ]

    assert road.ordering_cost_source == "road_network"
    assert road.ordering_cost_metric == "duration"
    assert road.is_road_optimized is True


def test_road_cost_matrix_with_unreachable_waypoint_fails():
    matrix = road_matrix()

    matrix.duration_seconds[0][2] = None
    matrix.duration_seconds[0][1] = None

    with pytest.raises(ValueError, match="reachable"):
        NearestNeighborStrategy().optimize(
            route_plan(),
            matrix,
            cost_metric="duration",
        )


class RoadRoutingStub:
    matrix_calls = 0
    route_calls = 0

    @classmethod
    def get_road_cost_matrix(cls, locations):
        cls.matrix_calls += 1

        assert len(locations) == 4

        return road_matrix()

    @classmethod
    def get_route(cls, locations):
        cls.route_calls += 1

        assert [place.name for place in locations] == [
            "Start",
            "Road near",
            "Geographic near",
            "Destination",
        ]

        return {
            "distance_km": 6.0,
            "duration_minutes": 2.0,
            "geometry": [[0, 0], [1, 1]],
            "legs": [{"distance": 6_000}],
        }


def test_agent_uses_one_matrix_call_then_one_final_route_call():
    RoadRoutingStub.matrix_calls = 0
    RoadRoutingStub.route_calls = 0

    result = OptimizerAgent(
        routing_service=RoadRoutingStub
    ).optimize(route_plan())

    assert RoadRoutingStub.matrix_calls == 1
    assert RoadRoutingStub.route_calls == 1
    assert result.total_distance == 6.0
    assert result.total_duration == 2.0
    assert result.is_road_optimized is True
    assert result.geometry == [[0, 0], [1, 1]]


class UnavailableRoutingStub:
    route_calls = 0

    @classmethod
    def get_road_cost_matrix(cls, locations):
        raise RoutingProviderUnavailableError(
            "matrix service is unavailable"
        )

    @classmethod
    def get_route(cls, locations):
        cls.route_calls += 1

        raise AssertionError(
            "A fallback must not request final road geometry."
        )


def test_agent_marks_haversine_fallback_when_matrix_is_unavailable():
    result = OptimizerAgent(
        routing_service=UnavailableRoutingStub
    ).optimize(route_plan())

    assert result.is_road_optimized is False
    assert result.ordering_cost_source == "geographic"
    assert result.fallback_reason == "matrix service is unavailable"
    assert result.geometry is None
    assert UnavailableRoutingStub.route_calls == 0


def test_matrix_service_posts_all_locations_without_network(monkeypatch):
    class Response:
        ok = True

        @staticmethod
        def json():
            return {
                "distances": [[0, 12]],
                "durations": [[0, 34]],
            }

    captured = {}

    def fake_post(url, headers, json, timeout):
        captured.update(
            url=url,
            headers=headers,
            json=json,
            timeout=timeout,
        )

        return Response()

    monkeypatch.setattr(
        "app.services.routing_service.OPENROUTESERVICE_API_KEY",
        "test-key",
    )

    monkeypatch.setattr(
        "app.services.routing_service.requests.post",
        fake_post,
    )

    matrix = RoutingService.get_road_cost_matrix(
        route_plan().waypoints
    )

    assert captured["url"] == RoutingService.MATRIX_URL
    assert captured["json"]["metrics"] == [
        "distance",
        "duration",
    ]
    assert matrix.duration_seconds == [[0, 34]]


# -------------------------------------------------------------------
# Weather-aware optimization tests
# -------------------------------------------------------------------


class FakeWeatherService:
    calls = []

    @classmethod
    def get_weather(cls, location):
        cls.calls.append(location.name)

        return WeatherInfo(
            location=location,
            temperature=25.0,
            condition="Clear",
            humidity=50,
            wind_speed=2.0,
        )

    @classmethod
    def get_weather_at_coordinates(
        cls,
        latitude,
        longitude,
        target_time=None,
        name="Road sample",
    ):
        return WeatherInfo(
            location=Location(
                name=name,
                district="",
                subdistrict="",
                latitude=latitude,
                longitude=longitude,
                source="road_sample",
            ),
            temperature=25.0,
            condition="Clear",
            humidity=50,
            wind_speed=2.0,
            forecast_time=target_time,
        )


class FakeWeatherRiskEngine:
    @classmethod
    def calculate_risk(cls, weather):
        # Make "Road near" extremely risky.
        #
        # This lets the test prove that weather affects route ordering.
        if weather.location.name == "Road near":
            return WeatherRisk(
                score=100,
                level="high",
                reasons=["Severe weather"],
                recommendation="Avoid this location.",
            )

        return WeatherRisk(
            score=0,
            level="low",
            reasons=[],
            recommendation="Safe to travel.",
        )


class WeatherRoutingStub:
    matrix_calls = 0
    route_calls = 0
    routed_locations = []

    @classmethod
    def get_road_cost_matrix(cls, locations):
        cls.matrix_calls += 1

        return RoadCostMatrix(
            distance_meters=[
                [0, 10, 10, 10],
                [10, 0, 10, 10],
                [10, 10, 0, 10],
                [10, 10, 10, 0],
            ],
            duration_seconds=[
                [0, 9, 1, 1],
                [9, 0, 1, 1],
                [1, 8, 0, 1],
                [1, 1, 1, 0],
            ],
        )

    @classmethod
    def get_route(cls, locations):
        cls.route_calls += 1
        cls.routed_locations = locations

        return {
            "distance_km": 3.0,
            "duration_minutes": 1.0,
            "geometry": [[0, 0], [1, 1]],
            "legs": [],
        }


def test_weather_can_change_waypoint_order():
    """
    Without weather:

        Start -> Road near -> Geographic near -> Destination

    is cheaper by road duration.

    When Road near has severe weather, the weather-adjusted cost makes:

        Start -> Geographic near -> Road near -> Destination

    preferable.

    This proves weather participates in route selection.
    """

    FakeWeatherService.calls = []
    WeatherRoutingStub.matrix_calls = 0
    WeatherRoutingStub.route_calls = 0
    WeatherRoutingStub.routed_locations = []

    result = OptimizerAgent(
        routing_service=WeatherRoutingStub,
        weather_service=FakeWeatherService,
        weather_risk_engine=FakeWeatherRiskEngine,
    ).optimize(
        route_plan(),
        objective="weather_aware",
        weather_sensitive=True,
        weather_weight=0.3,
    )

    assert [place.name for place in result.route] == [
        "Start",
        "Geographic near",
        "Road near",
        "Destination",
    ]

    assert [
        place.name
        for place in WeatherRoutingStub.routed_locations
    ] == [
        "Start",
        "Geographic near",
        "Road near",
        "Destination",
    ]

    assert result.ordering_cost_source == (
        "weather_adjusted_road_network"
    )

    assert result.ordering_cost_metric == (
        "weather_adjusted_duration"
    )

    assert result.is_road_optimized is True


def test_weather_is_not_called_when_weather_sensitive_is_disabled():
    FakeWeatherService.calls = []

    OptimizerAgent(
        routing_service=RoadRoutingStub,
        weather_service=FakeWeatherService,
        weather_risk_engine=FakeWeatherRiskEngine,
    ).optimize(
        route_plan(),
        objective="duration",
        weather_sensitive=False,
    )

    assert FakeWeatherService.calls == []


def test_weather_is_called_for_all_route_locations():
    FakeWeatherService.calls = []

    OptimizerAgent(
        routing_service=WeatherRoutingStub,
        weather_service=FakeWeatherService,
        weather_risk_engine=FakeWeatherRiskEngine,
    ).optimize(
        route_plan(),
        objective="weather_aware",
        weather_sensitive=True,
        weather_weight=0.3,
    )

    assert FakeWeatherService.calls == [
        "Start",
        "Geographic near",
        "Road near",
        "Destination",
    ]


# -------------------------------------------------------------------
# Time-aware weather tests
# -------------------------------------------------------------------


class TimeAwareWeatherService:
    calls = []

    @classmethod
    def get_weather_at(cls, location, target_time):
        cls.calls.append(
            (location.name, target_time)
        )

        return WeatherInfo(
            location=location,
            temperature=25.0,
            condition="Clear",
            humidity=50,
            wind_speed=2.0,
            forecast_time=target_time,
        )

    @classmethod
    def get_weather_at_coordinates(
        cls,
        latitude,
        longitude,
        target_time=None,
        name="Road sample",
    ):
        return WeatherInfo(
            location=Location(
                name=name,
                district="",
                subdistrict="",
                latitude=latitude,
                longitude=longitude,
                source="road_sample",
            ),
            temperature=25.0,
            condition="Clear",
            humidity=50,
            wind_speed=2.0,
            forecast_time=target_time,
        )

    @classmethod
    def get_weather(cls, location):
        raise AssertionError(
            "Current weather should not be used when "
            "departure_time is provided."
        )


def test_departure_time_uses_arrival_time_weather_forecast():
    TimeAwareWeatherService.calls = []

    result = OptimizerAgent(
        routing_service=WeatherRoutingStub,
        weather_service=TimeAwareWeatherService,
        weather_risk_engine=FakeWeatherRiskEngine,
    ).optimize(
        route_plan(),
        objective="weather_aware",
        weather_sensitive=True,
        weather_weight=0.3,
        departure_time="2026-09-07T08:00:00+05:30",
    )

    assert result.is_road_optimized is True

    assert len(TimeAwareWeatherService.calls) == 4

    arrival_times = {
        location_name: target_time
        for location_name, target_time
        in TimeAwareWeatherService.calls
    }

    # Departure time at the starting location.
    assert arrival_times["Start"].isoformat() == (
        "2026-09-07T08:00:00+05:30"
    )

    # WeatherRoutingStub's provisional road route is:
    #
    # Start -> Road near -> Geographic near -> Destination
    #
    # Durations:
    # Start -> Road near = 1 second
    # Road near -> Geographic near = 8 seconds
    # Geographic near -> Destination = 1 second

    assert arrival_times["Road near"].isoformat() == (
        "2026-09-07T08:00:01+05:30"
    )

    assert arrival_times["Geographic near"].isoformat() == (
        "2026-09-07T08:00:09+05:30"
    )

    assert arrival_times["Destination"].isoformat() == (
        "2026-09-07T08:00:10+05:30"
    )

    assert arrival_times["Road near"] > (
        arrival_times["Start"]
    )

    assert arrival_times["Geographic near"] > (
        arrival_times["Road near"]
    )

    assert arrival_times["Destination"] > (
        arrival_times["Geographic near"]
    )


def test_timezone_less_departure_time_is_rejected():
    with pytest.raises(
        ValueError,
        match="timezone",
    ):
        OptimizerAgent(
            routing_service=WeatherRoutingStub,
            weather_service=TimeAwareWeatherService,
            weather_risk_engine=FakeWeatherRiskEngine,
        ).optimize(
            route_plan(),
            objective="weather_aware",
            weather_sensitive=True,
            weather_weight=0.3,
            departure_time="2026-09-07T08:00:00",
        )