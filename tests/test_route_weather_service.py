from datetime import datetime
from app.models.weather_risk import WeatherRisk
from app.models.location import Location
from app.models.weather_info import WeatherInfo
from app.services.route_weather_service import RouteWeatherService


def location(name: str) -> Location:
    return Location(
        name=name,
        district="District",
        subdistrict="Subdistrict",
        latitude=17.0,
        longitude=78.0,
    )


class FakeWeatherService:
    calls = []

    @classmethod
    def get_weather_at_coordinates(
        cls,
        latitude,
        longitude,
        target_time=None,
        name="Road sample",
    ):
        cls.calls.append(
            {
                "latitude": latitude,
                "longitude": longitude,
                "target_time": target_time,
                "name": name,
            }
        )

        return WeatherInfo(
            location=Location(
                name=name,
                district="",
                subdistrict="",
                latitude=latitude,
                longitude=longitude,
                source="road_sample",
            ),
            temperature=25.0,
            condition="Clear",
            humidity=50,
            wind_speed=2.0,
            forecast_time=target_time,
        )


class FakeRiskEngine:
    @classmethod
    def calculate_risk(cls, weather):
        return WeatherRisk(
            score=20.0,
            level="Low",
            recommendation="Safe to travel.",
        )
    

def test_geometry_is_sampled_at_configured_distance():
    FakeWeatherService.calls = []

    service = RouteWeatherService(
        weather_service=FakeWeatherService,
        weather_risk_engine=FakeRiskEngine,
        sample_distance_km=10.0,
    )

    # Approximately 22 km of road.
    geometry = [
        [78.0000, 17.0000],
        [78.1000, 17.0000],
        [78.2000, 17.0000],
    ]

    segments = service.evaluate_route(
        geometry=geometry,
        origin=location("Start"),
        destination=location("Destination"),
    )

    # First and last geometry points must always be included.
    assert len(segments) >= 3

    assert segments[0].latitude == 17.0
    assert segments[0].longitude == 78.0

    assert segments[-1].latitude == 17.0
    assert segments[-1].longitude == 78.2

    # Every generated weather sample must have a road_sample source.
    for segment in segments:
        assert segment.weather is not None
        assert segment.weather.location.source == "road_sample"


def test_weather_is_requested_at_arrival_time():
    FakeWeatherService.calls = []

    service = RouteWeatherService(
        weather_service=FakeWeatherService,
        weather_risk_engine=FakeRiskEngine,
        sample_distance_km=10.0,
    )

    geometry = [
        [78.0000, 17.0000],
        [78.1000, 17.0000],
        [78.2000, 17.0000],
    ]

    departure_time = datetime.fromisoformat(
        "2026-09-07T08:00:00+05:30"
    )

    segments = service.evaluate_route(
        geometry=geometry,
        origin=location("Start"),
        destination=location("Destination"),
        departure_time=departure_time,
        duration_minutes=60.0,
    )

    assert len(segments) >= 3

    assert FakeWeatherService.calls[0]["target_time"] == (
        departure_time
    )

    # Samples farther along the route must have later estimated
    # arrival times.
    times = [
        call["target_time"]
        for call in FakeWeatherService.calls
    ]

    for previous, current in zip(times, times[1:]):
        assert current > previous


def test_route_weather_without_departure_time_uses_current_weather():
    FakeWeatherService.calls = []

    service = RouteWeatherService(
        weather_service=FakeWeatherService,
        weather_risk_engine=FakeRiskEngine,
        sample_distance_km=10.0,
    )

    geometry = [
        [78.0000, 17.0000],
        [78.1000, 17.0000],
    ]

    segments = service.evaluate_route(
        geometry=geometry,
        origin=location("Start"),
        destination=location("Destination"),
    )

    assert len(segments) >= 2

    for call in FakeWeatherService.calls:
        assert call["target_time"] is None


def test_invalid_sample_distance_is_rejected():
    try:
        RouteWeatherService(
            weather_service=FakeWeatherService,
            weather_risk_engine=FakeRiskEngine,
            sample_distance_km=0,
        )
        assert False, "Expected ValueError"
    except ValueError as error:
        assert "sample_distance_km" in str(error)


def test_empty_geometry_returns_no_weather_segments():
    FakeWeatherService.calls = []

    service = RouteWeatherService(
        weather_service=FakeWeatherService,
        weather_risk_engine=FakeRiskEngine,
        sample_distance_km=10.0,
    )

    segments = service.evaluate_route(
        geometry=[],
        origin=location("Start"),
        destination=location("Destination"),
    )

    assert segments == []
    assert FakeWeatherService.calls == []