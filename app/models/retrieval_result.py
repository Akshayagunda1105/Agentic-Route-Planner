from typing import List, Optional

from pydantic import BaseModel

from app.models.location import Location


class RetrievalResult(BaseModel):

    resolved: bool

    needs_user_selection: bool = False

    location: Optional[Location] = None

    candidates: List[Location] = []

    message: str = ""