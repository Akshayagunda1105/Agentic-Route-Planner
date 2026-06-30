import time

from app.models.route_plan import RoutePlan
from app.models.optimization_result import OptimizationResult

from app.strategies.optimization_strategy import (
    OptimizationStrategy
)


class NearestNeighborStrategy(
    OptimizationStrategy
):

    def optimize(
        self,
        route_plan: RoutePlan
    ) -> OptimizationResult:

        start_time = time.perf_counter()

        # Algorithm will go here

        end_time = time.perf_counter()

        return OptimizationResult(

            route=[],

            total_distance=0,

            strategy="Nearest Neighbor",

            execution_time=end_time - start_time

        )