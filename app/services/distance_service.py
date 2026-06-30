from math import radians, sin, cos, sqrt, atan2

from app.models.location import Location


class DistanceService:

    @staticmethod
    def calculate(

        loc1: Location,

        loc2: Location

    ) -> float:

        R = 6371

        lat1 = radians(loc1.latitude)
        lon1 = radians(loc1.longitude)

        lat2 = radians(loc2.latitude)
        lon2 = radians(loc2.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (

            sin(dlat / 2) ** 2

            +

            cos(lat1)

            *

            cos(lat2)

            *

            sin(dlon / 2) ** 2

        )

        c = 2 * atan2(

            sqrt(a),

            sqrt(1 - a)

        )

        return R * c