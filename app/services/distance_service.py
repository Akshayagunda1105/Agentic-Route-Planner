from math import radians, sin, cos, sqrt, atan2

from app.models.location import Location


class DistanceService:

    @staticmethod
    def calculate(
        location1: Location,
        location2: Location
    ) -> float:

        earth_radius = 6371.0

        lat1 = radians(location1.latitude)
        lon1 = radians(location1.longitude)

        lat2 = radians(location2.latitude)
        lon2 = radians(location2.longitude)

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = (
            sin(delta_lat / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(delta_lon / 2) ** 2
        )

        c = 2 * atan2(
            sqrt(a),
            sqrt(1 - a)
        )

        return earth_radius * c