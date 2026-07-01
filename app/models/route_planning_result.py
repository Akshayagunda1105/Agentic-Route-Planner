from typing import List, Optional

from pydantic import BaseModel

from app.models.optimization_result import (
    OptimizationResult
)

from app.models.retrieval_result import (
    RetrievalResult
)

from app.models.reflection_result import (
    ReflectionResult
)


class RoutePlanningResult(BaseModel):

    success: bool

    optimization: Optional[
        OptimizationResult
    ] = None

    reflection: Optional[
        ReflectionResult
    ] = None

    pending_locations: List[
        RetrievalResult
    ] = []

    errors: List[str] = []