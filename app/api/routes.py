import logging

import requests
from fastapi import APIRouter, HTTPException

from app.api.schemas import RouteRequest

from app.state.route_planner_state import (
    RoutePlannerState
)

from app.graph.route_graph import (
    route_graph
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/plan-route")
def plan_route(request: RouteRequest):

    try:
        state = RoutePlannerState(
            query=request.query,
            selections=request.selections
        )
        result = route_graph.invoke(state)
        return result["result"]
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except (requests.RequestException, RuntimeError) as error:
        logger.exception("Route-planning provider failed")
        raise HTTPException(
            status_code=502,
            detail="A route-planning provider is unavailable. Please retry."
        ) from error
    except Exception as error:
        logger.exception("Unexpected route-planning failure")
        raise HTTPException(status_code=500, detail="Unable to plan the route.") from error
