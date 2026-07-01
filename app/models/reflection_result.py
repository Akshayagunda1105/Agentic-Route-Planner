from pydantic import BaseModel


class ReflectionResult(BaseModel):

    approved: bool

    should_retry: bool = False

    message: str