from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.location import Location


class RetrievalResult(BaseModel):

    resolved: bool

    needs_user_selection: bool = False

    location: Optional[Location] = None

    candidates: List[Location] = Field(default_factory=list)

    message: str = ""

    query: Optional[str] = None
