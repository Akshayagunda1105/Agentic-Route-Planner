from app.models.location import Location
from app.services.route_plan_builder import RoutePlanBuilder
from app.strategies.nearest_neighbor import NearestNeighborStrategy


def location(name: str, latitude: float, longitude: float) -> Location:
    return Location(
        name=name,
        district="District",
        subdistrict="Subdistrict",
        latitude=latitude,
        longitude=longitude,
    )


def test_optimizer_keeps_requested_destination_last():
    start = location("Start", 0, 0)
    waypoint = location("Waypoint", 0, 1)
    destination = location("Destination", 0, 0.1)

    plan = RoutePlanBuilder().build(start, destination, [waypoint])
    result = NearestNeighborStrategy().optimize(plan)

    assert [place.name for place in result.route] == ["Start", "Waypoint", "Destination"]


def test_builder_does_not_mutate_the_waypoint_input():
    waypoints = [location("Waypoint", 0, 1)]
    RoutePlanBuilder().build(
        location("Start", 0, 0),
        location("End", 0, 2),
        waypoints
    )

    assert [place.name for place in waypoints] == ["Waypoint"]
