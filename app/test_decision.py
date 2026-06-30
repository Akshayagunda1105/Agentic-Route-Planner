from app.models.location import Location

from app.utils.decision import DecisionMaker


candidate1 = Location(
    name="Hyderabad",
    district="Hyderabad",
    subdistrict="Bandlaguda",
    latitude=17,
    longitude=78,
    score=55
)

candidate2 = Location(
    name="Hyderpur",
    district="Hyderabad",
    subdistrict="Bandlaguda",
    latitude=17,
    longitude=78,
    score=45
)

print(
    DecisionMaker.evaluate(
        [candidate1, candidate2]
    )
)