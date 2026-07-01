from typing import List, Optional

from pydantic import BaseModel

from app.models.optimization_result import (
    OptimizationResult
)

from app.models.retrieval_result import (
    RetrievalResult
)


class RoutePlanningResult(BaseModel):

    success: bool

    optimization: Optional[
        OptimizationResult
    ] = None

    pending_locations: List[
        RetrievalResult
    ] = []

    errors: List[str] = []