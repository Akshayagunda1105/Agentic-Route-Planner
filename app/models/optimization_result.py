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

    # Geographic distance is an estimate only; road values originate from ORS.
    geographic_distance: Optional[float] = None

    road_distance: Optional[float] = None

    road_duration: Optional[float] = None

    ordering_cost_source: str = "geographic"

    ordering_cost_metric: str = "distance"

    is_road_optimized: bool = False

    fallback_reason: Optional[str] = None

    geometry: Optional[List[List[float]]] = None

    legs: List[dict] = Field(default_factory=list)
