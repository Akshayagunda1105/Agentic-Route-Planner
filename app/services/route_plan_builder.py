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

        return RoutePlan(

            start=start,

            waypoints=waypoints.copy(),

            destination=destination

        )
