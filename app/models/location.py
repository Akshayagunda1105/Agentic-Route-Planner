from pydantic import BaseModel


class Location(BaseModel):

    name: str

    district: str

    subdistrict: str

    latitude: float

    longitude: float

    confidence: float = 100.0

    score: float = 100.0

    source: str = "exact"