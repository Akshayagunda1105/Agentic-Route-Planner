from app.models.route_plan import RoutePlan
from app.models.route_request import RouteRequest

from app.agents.retriever_agent import RetrieverAgent


class RoutePlanBuilder:

    def __init__(self):

        self.retriever = RetrieverAgent()

    def build(
        self,
        request: RouteRequest
    ) -> RoutePlan:

        start = self.retriever.resolve_location(
            request.start
        )

        destination = self.retriever.resolve_location(
            request.destination
        )

        destinations = []

        for waypoint in request.waypoints:

            result = self.retriever.resolve_location(
                waypoint
            )

            destinations.append(
                result.location
            )

        destinations.append(
            destination.location
        )

        return RoutePlan(

            start=start.location,

            destinations=destinations

        )