from typing import List

from pydantic import BaseModel

from app.models.location import Location


class OptimizationResult(BaseModel):

    route: List[Location]

    total_distance: float

    strategy: str

    execution_time: float