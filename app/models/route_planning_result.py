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

from app.models.weather_analysis import (
    WeatherAnalysis
)


class RoutePlanningResult(BaseModel):

    success: bool

    optimization: Optional[
        OptimizationResult
    ] = None

    weather: Optional[
        WeatherAnalysis
    ] = None

    reflection: Optional[
        ReflectionResult
    ] = None

    pending_locations: List[
        RetrievalResult
    ] = []

    errors: List[str] = []