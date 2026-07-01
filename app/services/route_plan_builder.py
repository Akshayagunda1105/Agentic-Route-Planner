from typing import List

from app.models.location import Location
from app.models.route_plan import RoutePlan


class RoutePlanBuilder:

    def build(
        self,
        start: Location,
        destination: Location,
        waypoints: List[Location]
    ) -> RoutePlan:

        destinations = waypoints.copy()

        destinations.append(
            destination
        )

        return RoutePlan(

            start=start,

            destinations=destinations

        )