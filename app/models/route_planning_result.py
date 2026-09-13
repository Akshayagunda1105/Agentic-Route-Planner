from typing import List, Optional

from pydantic import BaseModel, Field

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


class RoutePlanningOption(BaseModel):

    option_id: str

    label: str

    description: str

    optimization: OptimizationResult

    weather: Optional[
        WeatherAnalysis
    ] = None

    weather_risk_score: Optional[float] = None


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

    options: List[
        RoutePlanningOption
    ] = Field(default_factory=list)

    selection_required: bool = False

    selected_option_id: Optional[str] = None

    pending_locations: List[
        RetrievalResult
    ] = Field(default_factory=list)

    errors: List[str] = Field(default_factory=list)