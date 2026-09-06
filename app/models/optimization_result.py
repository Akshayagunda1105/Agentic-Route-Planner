from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.location import Location


class OptimizationResult(BaseModel):

    route: List[Location]

    total_distance: float

    strategy: str

    execution_time: float

    # Populated by the road-routing provider.
    total_duration: Optional[float] = None

    geometry: Optional[List[List[float]]] = None

    legs: List[dict] = Field(default_factory=list)
