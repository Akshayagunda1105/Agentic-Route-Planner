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

        return self.strategy.optimize(
            route_plan
        )