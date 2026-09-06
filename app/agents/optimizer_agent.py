from app.models.route_plan import RoutePlan
from app.models.optimization_result import (
    OptimizationResult
)

from app.strategies.optimization_strategy import (
    OptimizationStrategy
)

from app.strategies.nearest_neighbor import (
    NearestNeighborStrategy
)

from app.services.routing_service import RoutingService


class OptimizerAgent:

    def __init__(

        self,

        strategy: OptimizationStrategy = None

    ):

        if strategy is None:

            strategy = NearestNeighborStrategy()

        self.strategy = strategy

    def optimize(

        self,

        route_plan: RoutePlan

    ) -> OptimizationResult:

        estimate = self.strategy.optimize(route_plan)
        road_route = RoutingService.get_route(estimate.route)

        return OptimizationResult(
            route=estimate.route,
            total_distance=road_route["distance_km"],
            total_duration=road_route["duration_minutes"],
            geometry=road_route["geometry"],
            legs=road_route["legs"],
            strategy="Nearest Neighbor + OpenRouteService",
            execution_time=estimate.execution_time,
        )
