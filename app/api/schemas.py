from pydantic import BaseModel


class RouteRequest(BaseModel):

    query: str