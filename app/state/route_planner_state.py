from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from app.models.route_request import RouteRequest
from app.models.location import Location
from app.models.route_plan import RoutePlan
from app.models.optimization_result import OptimizationResult
from app.models.weather_analysis import WeatherAnalysis
from app.models.reflection_result import ReflectionResult
from app.models.route_planning_result import RoutePlanningResult
from app.models.retrieval_result import RetrievalResult


class RoutePlannerState(BaseModel):

    # Original user query
    query: str

    # Parser output
    request: Optional[RouteRequest] = None

    # Retriever outputs
    start_location: Optional[Location] = None

    destination_location: Optional[Location] = None

    waypoint_locations: List[Location] = Field(
        default_factory=list
    )

    # Builder output
    route_plan: Optional[RoutePlan] = None

    # Primary optimizer output
    optimization: Optional[OptimizationResult] = None

    # Primary weather output
    weather: Optional[WeatherAnalysis] = None

    # Reflection output
    reflection: Optional[ReflectionResult] = None

    # Alternative route candidates generated when
    # critical weather risk requires user choice.
    options: List = Field(
        default_factory=list
    )

    # Indicates that the user must choose between
    # route candidates before planning is complete.
    selection_required: bool = False

    # ID of the route option selected by the user.
    selected_option_id: Optional[str] = None

    # Number of replanning cycles already requested.
    # Kept for compatibility with the existing graph.
    replan_attempt: int = 0

    # Retriever state
    pending_locations: List[RetrievalResult] = Field(
        default_factory=list
    )

    selections: Dict[str, Location] = Field(
        default_factory=dict
    )

    # Final output
    result: Optional[RoutePlanningResult] = None