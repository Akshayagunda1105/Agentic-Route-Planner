import time

from app.models.route_plan import RoutePlan
from app.models.optimization_result import OptimizationResult

from app.strategies.optimization_strategy import (
    OptimizationStrategy
)

from app.services.distance_service import (
    DistanceService
)


class NearestNeighborStrategy(
    OptimizationStrategy
):

    def optimize(
        self,
        route_plan: RoutePlan
    ) -> OptimizationResult:

        start_time = time.perf_counter()

        # Initial state
        current_location = route_plan.start

        remaining_locations = route_plan.destinations.copy()

        optimized_route = [current_location]

        total_distance = 0

        # Continue until every destination is visited
        while remaining_locations:

            nearest_location = None

            shortest_distance = float("inf")

            # Find the nearest location
            for location in remaining_locations:

                distance = DistanceService.calculate(
                    current_location,
                    location
                )

                if distance < shortest_distance:

                    shortest_distance = distance

                    nearest_location = location

            # Add the nearest location to the optimized route
            optimized_route.append(
                nearest_location
            )

            # Update total distance
            total_distance += shortest_distance

            # Remove the visited location
            remaining_locations.remove(
                nearest_location
            )

            # Move to the selected location
            current_location = nearest_location

        end_time = time.perf_counter()

        return OptimizationResult(

            route=optimized_route,

            total_distance=total_distance,

            strategy="Nearest Neighbor",

            execution_time=end_time - start_time

        )