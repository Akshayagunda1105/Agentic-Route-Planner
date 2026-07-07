from fastapi import APIRouter

from app.api.schemas import RouteRequest

from app.state.route_planner_state import (
    RoutePlannerState
)

from app.graph.route_graph import (
    route_graph
)

router = APIRouter()


@router.post("/plan-route")
def plan_route(request: RouteRequest):

    state = RoutePlannerState(

        query=request.query

    )

    result = route_graph.invoke(state)

    return result["result"]