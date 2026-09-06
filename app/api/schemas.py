from typing import Dict

from pydantic import BaseModel, Field

from app.models.location import Location


class RouteRequest(BaseModel):

    query: str = Field(min_length=3, max_length=1_000)
    selections: Dict[str, Location] = Field(default_factory=dict)
