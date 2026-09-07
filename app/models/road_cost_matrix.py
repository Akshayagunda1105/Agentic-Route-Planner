from typing import List, Optional

from pydantic import BaseModel


class RoadCostMatrix(BaseModel):
    """Pairwise road-network costs returned by the routing provider.

    Values are indexed in the same order as the locations supplied to the
    matrix endpoint. `None` means the provider found no road connection.
    """

    distance_meters: List[List[Optional[float]]]
    duration_seconds: List[List[Optional[float]]]
