import time

from app.models.route_plan import RoutePlan
from app.models.optimization_result import OptimizationResult
from app.models.road_cost_matrix import RoadCostMatrix

from app.strategies.optimization_strategy import OptimizationStrategy

from app.services.distance_service import DistanceService


class NearestNeighborStrategy(OptimizationStrategy):
    """
    Nearest Neighbor followed by optional 2-opt improvement.

    When a RoadCostMatrix is supplied, both the initial solution and the
    2-opt improvement use road-network costs.

    When no matrix is supplied, the strategy falls back to geographic
    Haversine distance. The result is explicitly marked as a fallback.
    """

    def __init__(
        self,
        max_2opt_iterations: int = 100,
    ):
        if max_2opt_iterations < 0:
            raise ValueError("max_2opt_iterations must be >= 0.")

        self.max_2opt_iterations = max_2opt_iterations

    def optimize(
        self,
        route_plan: RoutePlan,
        road_cost_matrix: RoadCostMatrix | None = None,
        cost_metric: str = "duration",
    ) -> OptimizationResult:

        if road_cost_matrix is not None:
            return self._optimize_with_road_cost(
                route_plan,
                road_cost_matrix,
                cost_metric,
            )

        return self._optimize_with_geographic_distance(route_plan)

    def _optimize_with_geographic_distance(
        self,
        route_plan: RoutePlan,
    ) -> OptimizationResult:

        start_time = time.perf_counter()

        current_location = route_plan.start
        remaining_locations = route_plan.waypoints.copy()

        optimized_route = [current_location]
        total_distance = 0.0

        while remaining_locations:
            nearest_location = None
            shortest_distance = float("inf")

            for location in remaining_locations:
                distance = DistanceService.calculate(
                    current_location,
                    location,
                )

                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_location = location

            optimized_route.append(nearest_location)
            total_distance += shortest_distance

            remaining_locations.remove(nearest_location)
            current_location = nearest_location

        total_distance += DistanceService.calculate(
            current_location,
            route_plan.destination,
        )

        optimized_route.append(route_plan.destination)

        end_time = time.perf_counter()

        return OptimizationResult(
            route=optimized_route,
            total_distance=total_distance,
            strategy="Nearest Neighbor",
            execution_time=end_time - start_time,
            geographic_distance=total_distance,
            ordering_cost_source="geographic",
            ordering_cost_metric="distance",
            is_road_optimized=False,
        )

    def _optimize_with_road_cost(
        self,
        route_plan: RoutePlan,
        road_cost_matrix: RoadCostMatrix,
        cost_metric: str,
    ) -> OptimizationResult:

        if cost_metric not in {"distance", "duration"}:
            raise ValueError(
                "Road cost metric must be 'distance' or 'duration'."
            )

        locations = [
            route_plan.start,
            *route_plan.waypoints,
            route_plan.destination,
        ]

        expected_size = len(locations)

        self._validate_matrix(
            road_cost_matrix,
            expected_size,
        )

        start_time = time.perf_counter()

        metric_matrix = (
            road_cost_matrix.duration_seconds
            if cost_metric == "duration"
            else road_cost_matrix.distance_meters
        )

        destination_index = expected_size - 1

        # The start is index 0.
        # Waypoints are 1 .. destination_index - 1.
        # The destination is always the final index.
        remaining_indices = set(
            range(1, destination_index)
        )

        current_index = 0
        nn_order = [current_index]

        # ---------------------------------------------------------
        # Phase 1: Nearest Neighbor initial solution
        # ---------------------------------------------------------

        while remaining_indices:

            reachable_candidates = [
                candidate
                for candidate in remaining_indices
                if self._matrix_cost(
                    metric_matrix,
                    current_index,
                    candidate,
                ) != float("inf")
            ]

            if not reachable_candidates:
                raise ValueError(
                    "No remaining waypoint is reachable on the road network."
                )

            next_index = min(
                reachable_candidates,
                key=lambda candidate: (
                    self._matrix_cost(
                        metric_matrix,
                        current_index,
                        candidate,
                    ),
                    candidate,
                ),
            )

            nn_order.append(next_index)
            remaining_indices.remove(next_index)
            current_index = next_index

        if (
            self._matrix_cost(
                metric_matrix,
                current_index,
                destination_index,
            )
            == float("inf")
        ):
            raise ValueError(
                "The destination is not reachable on the road network."
            )

        nn_order.append(destination_index)

        # Cost of the initial Nearest Neighbor solution.
        nn_cost = self._route_cost(
            metric_matrix,
            nn_order,
        )

        # ---------------------------------------------------------
        # Phase 2: 2-opt improvement
        # ---------------------------------------------------------

        improved_order = self._two_opt(
            nn_order,
            metric_matrix,
            max_iterations=self.max_2opt_iterations,
        )

        improved_cost = self._route_cost(
            metric_matrix,
            improved_order,
        )

        # Safety guarantee:
        # never return a solution worse than the original NN route.
        if improved_cost > nn_cost:
            improved_order = nn_order
            improved_cost = nn_cost

        route = [
            locations[index]
            for index in improved_order
        ]

        road_distance = (
            self._route_cost(
                road_cost_matrix.distance_meters,
                improved_order,
            )
            / 1_000
        )

        road_duration = (
            self._route_cost(
                road_cost_matrix.duration_seconds,
                improved_order,
            )
            / 60
        )

        return OptimizationResult(
            route=route,
            total_distance=road_distance,
            total_duration=road_duration,
            road_distance=road_distance,
            road_duration=road_duration,
            strategy="Nearest Neighbor + 2-opt (road network)",
            execution_time=time.perf_counter() - start_time,
            ordering_cost_source="road_network",
            ordering_cost_metric=cost_metric,
            is_road_optimized=True,
        )

    def _two_opt(
        self,
        route_order: list[int],
        metric_matrix: list[list[float | None]],
        max_iterations: int,
    ) -> list[int]:
        """
        Improve a route using 2-opt.

        Start and destination remain fixed.

        A candidate is accepted only when its total route cost is strictly
        lower than the current route cost.
        """

        best_order = route_order.copy()
        best_cost = self._route_cost(
            metric_matrix,
            best_order,
        )

        if len(best_order) <= 3 or max_iterations == 0:
            return best_order

        iteration = 0

        while iteration < max_iterations:
            improved = False

            # Keep index 0 (start) and the final index (destination) fixed.
            #
            # Reversing [i:j+1] changes the order of the waypoints between
            # two selected edges.
            for i in range(1, len(best_order) - 2):

                for j in range(i + 1, len(best_order) - 1):

                    candidate_order = (
                        best_order[:i]
                        + best_order[i:j + 1][::-1]
                        + best_order[j + 1:]
                    )

                    candidate_cost = self._route_cost(
                        metric_matrix,
                        candidate_order,
                    )

                    if candidate_cost < best_cost:
                        best_order = candidate_order
                        best_cost = candidate_cost
                        improved = True

                        # First-improvement strategy:
                        # restart the search from the beginning after
                        # accepting an improvement.
                        break

                if improved:
                    break

            if not improved:
                break

            iteration += 1

        return best_order

    @classmethod
    def _route_cost(
        cls,
        matrix: list[list[float | None]],
        route_order: list[int],
    ) -> float:
        total = 0.0

        for origin, destination in zip(
            route_order,
            route_order[1:],
        ):
            cost = cls._matrix_cost(
                matrix,
                origin,
                destination,
            )

            if cost == float("inf"):
                return float("inf")

            total += cost

        return total

    @staticmethod
    def _matrix_cost(
        matrix: list[list[float | None]],
        origin: int,
        destination: int,
    ) -> float:
        value = matrix[origin][destination]

        if value is None:
            return float("inf")

        return float(value)

    @staticmethod
    def _validate_matrix(
        road_cost_matrix: RoadCostMatrix,
        expected_size: int,
    ) -> None:

        if (
            len(road_cost_matrix.distance_meters) != expected_size
            or len(road_cost_matrix.duration_seconds) != expected_size
            or any(
                len(row) != expected_size
                for row in road_cost_matrix.distance_meters
            )
            or any(
                len(row) != expected_size
                for row in road_cost_matrix.duration_seconds
            )
        ):
            raise ValueError(
                "Road-cost matrix does not match the route locations."
            )

