from app.agents.parser_agent import ParserAgent
from app.agents.optimizer_agent import OptimizerAgent

from app.services.route_plan_builder import (
    RoutePlanBuilder
)


class RoutePlanner:

    def __init__(self):

        self.parser = ParserAgent()

        self.builder = RoutePlanBuilder()

        self.optimizer = OptimizerAgent()

    def plan(
        self,
        query: str
    ):

        request = self.parser.parse(query)

        route_plan = self.builder.build(
            request
        )

        result = self.optimizer.optimize(
            route_plan
        )

        return result