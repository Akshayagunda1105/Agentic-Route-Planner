import pytest

from app.agents.optimizer_agent import OptimizerAgent
from app.models.location import Location
from app.models.road_cost_matrix import RoadCostMatrix
from app.models.route_plan import RoutePlan
from app.services.routing_service import RoutingProviderUnavailableError


def make_location(name: str, latitude: float, longitude: float) -> Location:
    return Location(
        name=name,
        district=name,
        subdistrict=name,
        latitude=latitude,
        longitude=longitude,
    )


def make_route_plan() -> RoutePlan:
    return RoutePlan(
        start=make_location("Start", 17.40, 78.40),
        waypoints=[
            make_location("Waypoint A", 17.50, 78.50),
            make_location("Waypoint B", 17.60, 78.60),
        ],
        destination=make_location("Destination", 17.70, 78.70),
    )


class FakeRoutingService:
    def __init__(self):
        self.matrix_calls = []
        self.route_calls = []

    def get_road_cost_matrix(self, locations):
        self.matrix_calls.append(locations)

        return RoadCostMatrix(
            distance_meters=[
                [0, 100, 200, 300],
                [100, 0, 100, 200],
                [200, 100, 0, 100],
                [300, 200, 100, 0],
            ],
            duration_seconds=[
                [0, 10, 20, 30],
                [10, 0, 10, 20],
                [20, 10, 0, 10],
                [30, 20, 10, 0],
            ],
        )

    def get_route(self, locations):
        self.route_calls.append(locations)

        return {
            "distance_km": 0.3,
            "duration_minutes": 0.5,
            "geometry": [
                [78.40, 17.40],
                [78.50, 17.50],
                [78.60, 17.60],
                [78.70, 17.70],
            ],
            "legs": [],
        }


class UnavailableRoutingService:
    def get_road_cost_matrix(self, locations):
        raise RoutingProviderUnavailableError(
            "Road-cost matrix service is unavailable."
        )

    def get_route(self, locations):
        raise AssertionError(
            "get_route should not be called when the road-cost matrix "
            "service is unavailable."
        )


def test_optimizer_uses_road_cost_matrix():
    routing_service = FakeRoutingService()

    agent = OptimizerAgent(
        routing_service=routing_service,
        road_cost_metric="duration",
    )

    result = agent.optimize(make_route_plan())

    assert len(routing_service.matrix_calls) == 1
    assert len(routing_service.route_calls) == 1

    assert result.is_road_optimized is True
    assert result.ordering_cost_source == "road_network"
    assert result.ordering_cost_metric == "duration"

    assert result.total_distance == 0.3
    assert result.total_duration == 0.5

    assert result.geometry is not None


def test_optimizer_uses_distance_as_road_cost_metric():
    routing_service = FakeRoutingService()

    agent = OptimizerAgent(
        routing_service=routing_service,
        road_cost_metric="distance",
    )

    result = agent.optimize(make_route_plan())

    assert result.is_road_optimized is True
    assert result.ordering_cost_source == "road_network"
    assert result.ordering_cost_metric == "distance"


def test_optimizer_falls_back_to_geographic_distance_when_matrix_unavailable():
    agent = OptimizerAgent(
        routing_service=UnavailableRoutingService()
    )

    result = agent.optimize(make_route_plan())

    assert result.is_road_optimized is False
    assert result.ordering_cost_source == "geographic"
    assert result.ordering_cost_metric == "distance"

    assert result.strategy == "Nearest Neighbor (Haversine fallback)"

    assert result.fallback_reason is not None
    assert "unavailable" in result.fallback_reason.lower()


def test_optimizer_preserves_start_and_destination():
    routing_service = FakeRoutingService()

    plan = make_route_plan()

    agent = OptimizerAgent(
        routing_service=routing_service
    )

    result = agent.optimize(plan)

    assert result.route[0] == plan.start
    assert result.route[-1] == plan.destination


def test_optimizer_passes_optimized_route_to_final_routing_service():
    routing_service = FakeRoutingService()

    plan = make_route_plan()

    agent = OptimizerAgent(
        routing_service=routing_service
    )

    agent.optimize(plan)

    routed_locations = routing_service.route_calls[0]

    assert routed_locations[0] == plan.start
    assert routed_locations[-1] == plan.destination
    assert len(routed_locations) == len(plan.waypoints) + 2