from app.models.location import Location
from app.models.road_cost_matrix import RoadCostMatrix
from app.models.route_plan import RoutePlan
from app.strategies.nearest_neighbor import NearestNeighborStrategy


def location(name: str) -> Location:
    return Location(
        name=name,
        district=name,
        subdistrict=name,
        latitude=17.0,
        longitude=78.0,
    )


def build_plan() -> RoutePlan:
    return RoutePlan(
        start=location("Start"),
        waypoints=[
            location("A"),
            location("B"),
            location("C"),
        ],
        destination=location("Destination"),
    )


def test_road_nearest_neighbor_uses_road_duration():
    plan = build_plan()

    matrix = RoadCostMatrix(
        distance_meters=[
            [0, 100, 500, 400, 600],
            [100, 0, 100, 500, 200],
            [500, 100, 0, 100, 300],
            [400, 500, 100, 0, 100],
            [600, 200, 300, 100, 0],
        ],
        duration_seconds=[
            [0, 10, 50, 40, 60],
            [10, 0, 10, 50, 20],
            [50, 10, 0, 10, 30],
            [40, 50, 10, 0, 10],
            [60, 20, 30, 10, 0],
        ],
    )

    strategy = NearestNeighborStrategy(
        max_2opt_iterations=0
    )

    result = strategy.optimize(
        plan,
        road_cost_matrix=matrix,
        cost_metric="duration",
    )

    assert result.is_road_optimized is True
    assert result.ordering_cost_source == "road_network"
    assert result.ordering_cost_metric == "duration"

    assert [place.name for place in result.route] == [
        "Start",
        "A",
        "B",
        "C",
        "Destination",
    ]


def test_2opt_improves_nearest_neighbor_route():
    plan = build_plan()

    # Index mapping:
    #
    # 0 = Start
    # 1 = A
    # 2 = B
    # 3 = C
    # 4 = Destination
    #
    # Nearest Neighbor produces:
    #
    # Start -> A -> C -> B -> Destination
    #
    # because:
    #
    # Start -> A = 10
    # Start -> C = 15
    # Start -> B = 20
    #
    # After reaching A:
    #
    # A -> C = 5
    # A -> B = 20
    #
    # Therefore C is selected before B.
    #
    # NN route cost:
    #
    # Start -> A -> C -> B -> Destination
    # 10 + 5 + 5 + 50 = 70
    #
    # 2-opt can reverse the C -> B segment:
    #
    # Start -> A -> B -> C -> Destination
    # 10 + 20 + 5 + 5 = 40
    #
    # Therefore 2-opt should produce a strictly better route.

    matrix = RoadCostMatrix(
        distance_meters=[
            [0, 10, 20, 15, 100],
            [10, 0, 20, 5, 100],
            [20, 20, 0, 5, 50],
            [15, 5, 5, 0, 5],
            [100, 100, 50, 5, 0],
        ],
        duration_seconds=[
            [0, 10, 20, 15, 100],
            [10, 0, 20, 5, 100],
            [20, 20, 0, 5, 50],
            [15, 5, 5, 0, 5],
            [100, 100, 50, 5, 0],
        ],
    )

    nn_strategy = NearestNeighborStrategy(
        max_2opt_iterations=0
    )

    improved_strategy = NearestNeighborStrategy(
        max_2opt_iterations=100
    )

    nn_result = nn_strategy.optimize(
        plan,
        road_cost_matrix=matrix,
        cost_metric="duration",
    )

    improved_result = improved_strategy.optimize(
        plan,
        road_cost_matrix=matrix,
        cost_metric="duration",
    )

    assert [
        place.name
        for place in nn_result.route
    ] == [
        "Start",
        "A",
        "C",
        "B",
        "Destination",
    ]

    assert improved_result.total_duration <= nn_result.total_duration

    assert improved_result.total_duration < nn_result.total_duration

    assert [
        place.name
        for place in improved_result.route
    ] == [
        "Start",
        "A",
        "B",
        "C",
        "Destination",
    ]


def test_2opt_never_moves_start_or_destination():
    plan = build_plan()

    matrix = RoadCostMatrix(
        distance_meters=[
            [0, 10, 20, 15, 100],
            [10, 0, 50, 5, 100],
            [20, 20, 0, 5, 5],
            [15, 50, 5, 0, 5],
            [100, 100, 5, 5, 0],
        ],
        duration_seconds=[
            [0, 10, 20, 15, 100],
            [10, 0, 50, 5, 100],
            [20, 20, 0, 5, 5],
            [15, 50, 5, 0, 5],
            [100, 100, 5, 5, 0],
        ],
    )

    strategy = NearestNeighborStrategy(
        max_2opt_iterations=100
    )

    result = strategy.optimize(
        plan,
        road_cost_matrix=matrix,
        cost_metric="duration",
    )

    assert result.route[0] == plan.start
    assert result.route[-1] == plan.destination


def test_2opt_does_not_worsen_initial_nearest_neighbor_solution():
    plan = build_plan()

    matrix = RoadCostMatrix(
        distance_meters=[
            [0, 10, 20, 30, 40],
            [10, 0, 10, 100, 20],
            [20, 10, 0, 10, 20],
            [30, 100, 10, 0, 10],
            [40, 20, 20, 10, 0],
        ],
        duration_seconds=[
            [0, 10, 20, 30, 40],
            [10, 0, 10, 100, 20],
            [20, 10, 0, 10, 20],
            [30, 100, 10, 0, 10],
            [40, 20, 20, 10, 0],
        ],
    )

    nn_only = NearestNeighborStrategy(
        max_2opt_iterations=0
    )

    with_2opt = NearestNeighborStrategy(
        max_2opt_iterations=100
    )

    nn_result = nn_only.optimize(
        plan,
        road_cost_matrix=matrix,
        cost_metric="duration",
    )

    improved_result = with_2opt.optimize(
        plan,
        road_cost_matrix=matrix,
        cost_metric="duration",
    )

    assert improved_result.total_duration <= nn_result.total_duration


def test_zero_2opt_iterations_returns_nearest_neighbor_solution():
    plan = build_plan()

    matrix = RoadCostMatrix(
        distance_meters=[
            [0, 10, 50, 20, 100],
            [10, 0, 10, 50, 100],
            [50, 10, 0, 10, 20],
            [20, 50, 10, 0, 10],
            [100, 100, 20, 10, 0],
        ],
        duration_seconds=[
            [0, 10, 50, 20, 100],
            [10, 0, 10, 50, 100],
            [50, 10, 0, 10, 20],
            [20, 50, 10, 0, 10],
            [100, 100, 20, 10, 0],
        ],
    )

    strategy = NearestNeighborStrategy(
        max_2opt_iterations=0
    )

    result = strategy.optimize(
        plan,
        road_cost_matrix=matrix,
        cost_metric="duration",
    )

    assert [
        place.name
        for place in result.route
    ] == [
        "Start",
        "A",
        "B",
        "C",
        "Destination",
    ]


def test_distance_metric_changes_optimization_metric():
    plan = build_plan()

    matrix = RoadCostMatrix(
        distance_meters=[
            [0, 10, 100, 50, 200],
            [10, 0, 10, 100, 100],
            [100, 10, 0, 10, 20],
            [50, 100, 10, 0, 10],
            [200, 100, 20, 10, 0],
        ],
        duration_seconds=[
            [0, 10, 20, 30, 40],
            [10, 0, 10, 20, 30],
            [20, 10, 0, 10, 20],
            [30, 20, 10, 0, 10],
            [40, 30, 20, 10, 0],
        ],
    )

    result = NearestNeighborStrategy(
        max_2opt_iterations=100
    ).optimize(
        plan,
        road_cost_matrix=matrix,
        cost_metric="distance",
    )

    assert result.is_road_optimized is True
    assert result.ordering_cost_metric == "distance"