from typing import List, Optional

from pydantic import BaseModel

from app.models.route_request import RouteRequest
from app.models.location import Location
from app.models.route_plan import RoutePlan
from app.models.optimization_result import OptimizationResult
from app.models.weather_analysis import WeatherAnalysis
from app.models.reflection_result import ReflectionResult
from app.models.route_planning_result import RoutePlanningResult


class RoutePlannerState(BaseModel):

    # Original user query
    query: str

    # Parser output
    request: Optional[RouteRequest] = None

    # Retriever outputs
    start_location: Optional[Location] = None

    destination_location: Optional[Location] = None

    waypoint_locations: List[Location] = []

    # Builder output
    route_plan: Optional[RoutePlan] = None

    # Optimizer output
    optimization: Optional[OptimizationResult] = None

    # Weather output
    weather: Optional[WeatherAnalysis] = None

    # Reflection output
    reflection: Optional[ReflectionResult] = None

    # Final output
    result: Optional[RoutePlanningResult] = None