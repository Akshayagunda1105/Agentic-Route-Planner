from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class RouteRequest(BaseModel):

    start: str

    destination: str

    waypoints: List[str] = Field(
        default_factory=list,
        max_length=8,
    )

    # Route optimization objective.
    # "distance" minimizes road distance.
    # "duration" minimizes road travel time.
    # "weather_aware" considers both travel cost and weather risk.
    objective: Literal[
        "distance",
        "duration",
        "weather_aware",
    ] = "duration"

    # Whether weather conditions should influence route selection.
    weather_sensitive: bool = False

    # Weight given to weather risk when weather_sensitive is enabled.
    # 0.0 = ignore weather risk.
    # 1.0 = give weather risk maximum influence.
    weather_weight: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
    )

    # Optional travel mode for future routing-provider support.
    travel_mode: Literal[
        "driving",
        "cycling",
        "walking",
    ] = "driving"

    # Optional departure time in ISO-8601 format.
    # This will be used later for time-aware weather forecasting.
    departure_time: Optional[str] = None

    # Optional route constraints.
    avoid_highways: bool = False
    avoid_tolls: bool = False

    # Optional maximum route limits.
    max_duration_minutes: Optional[float] = Field(
        default=None,
        gt=0,
    )

    max_distance_km: Optional[float] = Field(
        default=None,
        gt=0,
    )