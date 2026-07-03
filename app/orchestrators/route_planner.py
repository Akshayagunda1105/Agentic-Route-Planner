from app.agents.parser_agent import ParserAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.optimizer_agent import OptimizerAgent
from app.agents.weather_agent import WeatherAgent
from app.agents.reflection_agent import ReflectionAgent

from app.services.route_plan_builder import RoutePlanBuilder

from app.models.route_planning_result import (
    RoutePlanningResult
)


class RoutePlanner:

    def __init__(self):

        self.parser = ParserAgent()

        self.retriever = RetrieverAgent()

        self.builder = RoutePlanBuilder()

        self.optimizer = OptimizerAgent()

        self.weather = WeatherAgent()

        self.reflection = ReflectionAgent()

    def plan(
        self,
        query: str
    ):

        # Step 1 - Parse user query
        request = self.parser.parse(query)

        # Step 2 - Resolve start location
        start_result = self.retriever.resolve_location(
            request.start
        )

        if not start_result.resolved:

            return RoutePlanningResult(

                success=False,

                pending_locations=[start_result]
                if start_result.needs_user_selection
                else [],

                errors=[]
                if start_result.needs_user_selection
                else [start_result.message]

            )

        # Step 3 - Resolve destination
        destination_result = self.retriever.resolve_location(
            request.destination
        )

        if not destination_result.resolved:

            return RoutePlanningResult(

                success=False,

                pending_locations=[destination_result]
                if destination_result.needs_user_selection
                else [],

                errors=[]
                if destination_result.needs_user_selection
                else [destination_result.message]

            )

        # Step 4 - Resolve waypoints
        waypoint_locations = []

        for waypoint in request.waypoints:

            result = self.retriever.resolve_location(
                waypoint
            )

            if not result.resolved:

                return RoutePlanningResult(

                    success=False,

                    pending_locations=[result]
                    if result.needs_user_selection
                    else [],

                    errors=[]
                    if result.needs_user_selection
                    else [result.message]

                )

            waypoint_locations.append(
                result.location
            )

        # Step 5 - Build RoutePlan
        route_plan = self.builder.build(

            start_result.location,

            destination_result.location,

            waypoint_locations

        )

        # Step 6 - Optimize Route
        optimization = self.optimizer.optimize(
            route_plan
        )

        # Step 7 - Analyze Weather
        weather = self.weather.analyze(
            optimization
        )

        # Step 8 - Reflect on the Route
        reflection = self.reflection.evaluate(
            optimization,
            weather
        )

        # Step 9 - Return Final Result
        return RoutePlanningResult(

            success=reflection.approved,

            optimization=optimization,

            weather=weather,

            reflection=reflection

        )