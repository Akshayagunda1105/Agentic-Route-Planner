from abc import ABC, abstractmethod

from app.models.route_plan import RoutePlan
from app.models.optimization_result import OptimizationResult
from app.models.road_cost_matrix import RoadCostMatrix


class OptimizationStrategy(ABC):

    @abstractmethod
    def optimize(
        self,
        route_plan: RoutePlan,
        road_cost_matrix: RoadCostMatrix | None = None,
        cost_metric: str = "duration"
    ) -> OptimizationResult:
        pass
