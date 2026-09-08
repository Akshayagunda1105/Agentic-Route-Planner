from statistics import mean

from app.models.weather_segment import WeatherSegment


class RouteWeatherAggregator:
    """
    Aggregates weather risks from sampled points along a road segment.

    The goal is to avoid making a route decision based on weather at
    only the named waypoints. Instead, weather observations sampled
    along the actual road are combined into a segment-level risk.
    """

    @staticmethod
    def calculate_average_risk(
        weather_segments: list[WeatherSegment],
    ) -> float:
        """
        Calculate the average weather risk across all samples.

        Returns:
            A risk score between 0 and 100.

        If no valid risk samples are available, returns 0.
        """

        scores = [
            float(segment.risk.score)
            for segment in weather_segments
            if segment.risk is not None
        ]

        if not scores:
            return 0.0

        return min(
            max(mean(scores), 0.0),
            100.0,
        )

    @staticmethod
    def calculate_max_risk(
        weather_segments: list[WeatherSegment],
    ) -> float:
        """
        Return the highest weather risk encountered along the road.
        """

        scores = [
            float(segment.risk.score)
            for segment in weather_segments
            if segment.risk is not None
        ]

        if not scores:
            return 0.0

        return min(
            max(max(scores), 0.0),
            100.0,
        )

    @classmethod
    def calculate_route_risk(
        cls,
        weather_segments: list[WeatherSegment],
    ) -> float:
        """
        Calculate a conservative route-level weather risk.

        We use the maximum sampled risk rather than only the average,
        because a short but severe weather section should not disappear
        inside a long route with otherwise good weather.

        The result is normalized to 0-100.
        """

        return cls.calculate_max_risk(
            weather_segments
        )