from pydantic import BaseModel
from typing import List


class RouteRequest(BaseModel):
    start: str
    destination: str
    waypoints: List[str]