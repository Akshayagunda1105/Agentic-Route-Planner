from pydantic import BaseModel, Field
from typing import List


class RouteRequest(BaseModel):
    start: str
    destination: str
    # Each stop triggers an external weather request; bound work per request.
    waypoints: List[str] = Field(default_factory=list, max_length=8)
