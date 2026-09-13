from typing import List, Optional

from pydantic import BaseModel, Field


class ReflectionResult(BaseModel):

    approved: bool

    should_retry: bool = False

    message: str

    failed_checks: List[str] = Field(
        default_factory=list
    )

    weather_risk_score: Optional[float] = None

    weather_risk_threshold: Optional[float] = None

    replan_reason: Optional[str] = None