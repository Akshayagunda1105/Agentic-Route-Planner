from typing import List

from pydantic import BaseModel

from app.models.location import Location


class RoutePlan(BaseModel):

    start: Location

    waypoints: List[Location]

    destination: Location
