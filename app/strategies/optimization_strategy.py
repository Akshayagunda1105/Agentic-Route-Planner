from abc import ABC, abstractmethod

from app.models.route_plan import RoutePlan
from app.models.optimization_result import OptimizationResult


class OptimizationStrategy(ABC):

    @abstractmethod
    def optimize(
        self,
        route_plan: RoutePlan
    ) -> OptimizationResult:
        pass