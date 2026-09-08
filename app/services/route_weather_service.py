from datetime import datetime, timedelta
from math import atan2, cos, radians, sin, sqrt

from app.models.location import Location
from app.models.weather_segment import WeatherSegment
from app.services.weather_service import WeatherService
from app.services.weather_risk_engine import WeatherRiskEngine


class RouteWeatherService:
    """
    Evaluates weather at sampled points along an already-routed road.

    The route geometry is expected in OpenRouteService format:
    [
        [longitude, latitude],
        [longitude, latitude],
        ...
    ]
    """

    DEFAULT_SAMPLE_DISTANCE_KM = 10.0

    def __init__(
        self,
        weather_service=WeatherService,
        weather_risk_engine=WeatherRiskEngine,
        sample_distance_km: float = DEFAULT_SAMPLE_DISTANCE_KM,
    ):
        if sample_distance_km <= 0:
            raise ValueError(
                "sample_distance_km must be greater than zero."
            )

        self.weather_service = weather_service
        self.weather_risk_engine = weather_risk_engine
        self.sample_distance_km = sample_distance_km

    def evaluate_route(
        self,
        geometry: list[list[float]],
        origin: Location,
        destination: Location,
        departure_time: datetime | None = None,
        duration_minutes: float | None = None,
    ) -> list[WeatherSegment]:
        """
        Sample the road geometry and evaluate weather at each sample.

        If departure_time and duration_minutes are supplied, weather is
        requested for the estimated arrival time at each sample.
        """

        if not geometry:
            return []

        if departure_time is not None and departure_time.tzinfo is None:
            raise ValueError(
                "departure_time must be timezone-aware."
            )

        samples = self._sample_geometry(geometry)

        if not samples:
            return []

        total_distance_km = self._geometry_distance_km(geometry)

        segments = []

        for distance_from_start_km, latitude, longitude in samples:
            sample_time = self._estimate_sample_time(
                departure_time=departure_time,
                duration_minutes=duration_minutes,
                distance_from_start_km=distance_from_start_km,
                total_distance_km=total_distance_km,
            )

            weather = self.weather_service.get_weather_at_coordinates(
                latitude=latitude,
                longitude=longitude,
                target_time=sample_time,
                name=f"Road sample ({latitude:.5f}, {longitude:.5f})",
            )

            risk = self.weather_risk_engine.calculate_risk(
                weather
            )

            segments.append(
                WeatherSegment(
                    origin=origin,
                    destination=destination,
                    latitude=latitude,
                    longitude=longitude,
                    weather=weather,
                    forecast_time=sample_time,
                    risk=risk,
                )
            )

        return segments

    def _sample_geometry(
        self,
        geometry: list[list[float]],
    ) -> list[tuple[float, float, float]]:
        """
        Return sampled points as:

            (distance_from_start_km, latitude, longitude)

        The first and last geometry points are always included.
        """

        if len(geometry) == 1:
            longitude, latitude = geometry[0]
            return [
                (0.0, latitude, longitude)
            ]

        samples = []

        accumulated_distance_km = 0.0
        next_sample_distance_km = 0.0

        first_longitude, first_latitude = geometry[0]

        samples.append(
            (
                0.0,
                first_latitude,
                first_longitude,
            )
        )

        next_sample_distance_km = self.sample_distance_km

        for index in range(1, len(geometry)):
            previous_longitude, previous_latitude = geometry[
                index - 1
            ]

            current_longitude, current_latitude = geometry[
                index
            ]

            segment_distance_km = self._haversine_distance_km(
                previous_latitude,
                previous_longitude,
                current_latitude,
                current_longitude,
            )

            if segment_distance_km <= 0:
                continue

            segment_start_distance_km = accumulated_distance_km
            segment_end_distance_km = (
                accumulated_distance_km
                + segment_distance_km
            )

            while next_sample_distance_km < segment_end_distance_km:
                fraction = (
                    next_sample_distance_km
                    - segment_start_distance_km
                ) / segment_distance_km

                latitude = (
                    previous_latitude
                    + fraction
                    * (
                        current_latitude
                        - previous_latitude
                    )
                )

                longitude = (
                    previous_longitude
                    + fraction
                    * (
                        current_longitude
                        - previous_longitude
                    )
                )

                samples.append(
                    (
                        next_sample_distance_km,
                        latitude,
                        longitude,
                    )
                )

                next_sample_distance_km += (
                    self.sample_distance_km
                )

            accumulated_distance_km = segment_end_distance_km

        last_longitude, last_latitude = geometry[-1]

        if not samples or (
            samples[-1][1] != last_latitude
            or samples[-1][2] != last_longitude
        ):
            samples.append(
                (
                    accumulated_distance_km,
                    last_latitude,
                    last_longitude,
                )
            )

        return samples

    @staticmethod
    def _estimate_sample_time(
        departure_time: datetime | None,
        duration_minutes: float | None,
        distance_from_start_km: float,
        total_distance_km: float,
    ) -> datetime | None:
        """
        Estimate arrival time at a sample using proportional travel
        progress along the final road route.

        This is intentionally simple at this stage. Later we can use
        per-geometry-point travel durations from ORS for more precise
        arrival times.
        """

        if (
            departure_time is None
            or duration_minutes is None
            or total_distance_km <= 0
        ):
            return departure_time

        progress = min(
            max(
                distance_from_start_km
                / total_distance_km,
                0.0,
            ),
            1.0,
        )

        elapsed_seconds = (
            duration_minutes
            * 60.0
            * progress
        )

        return departure_time + timedelta(
            seconds=elapsed_seconds
        )

    @classmethod
    def _geometry_distance_km(
        cls,
        geometry: list[list[float]],
    ) -> float:
        total = 0.0

        for index in range(1, len(geometry)):
            previous_longitude, previous_latitude = geometry[
                index - 1
            ]

            current_longitude, current_latitude = geometry[
                index
            ]

            total += cls._haversine_distance_km(
                previous_latitude,
                previous_longitude,
                current_latitude,
                current_longitude,
            )

        return total

    @staticmethod
    def _haversine_distance_km(
        latitude_1: float,
        longitude_1: float,
        latitude_2: float,
        longitude_2: float,
    ) -> float:
        earth_radius_km = 6371.0

        latitude_1_rad = radians(latitude_1)
        latitude_2_rad = radians(latitude_2)

        delta_latitude = radians(
            latitude_2 - latitude_1
        )

        delta_longitude = radians(
            longitude_2 - longitude_1
        )

        a = (
            sin(delta_latitude / 2) ** 2
            + cos(latitude_1_rad)
            * cos(latitude_2_rad)
            * sin(delta_longitude / 2) ** 2
        )

        return (
            2
            * earth_radius_km
            * atan2(
                sqrt(a),
                sqrt(1 - a),
            )
        )