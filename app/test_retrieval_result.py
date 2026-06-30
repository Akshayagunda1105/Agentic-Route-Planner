from app.models.location import Location
from app.models.retrieval_result import RetrievalResult

location = Location(
    name="Hyderabad",
    district="Hyderabad",
    subdistrict="Shaikpet",
    latitude=17.42,
    longitude=78.47
)

result = RetrievalResult(
    resolved=True,
    location=location,
    message="Location resolved successfully."
)

print(result)