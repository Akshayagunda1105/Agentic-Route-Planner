import requests

from app.config.settings import OPENROUTESERVICE_API_KEY
from app.models.location import Location
from app.models.road_cost_matrix import RoadCostMatrix


class RoutingProviderUnavailableError(RuntimeError):
    """The routing service cannot be reached or is temporarily unavailable."""


class RoutingProviderError(RuntimeError):
    """The routing service rejected a validly delivered request."""


class RoutingService:
    """Road routing through OpenRouteService's free API tier."""

    BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    MATRIX_URL = "https://api.openrouteservice.org/v2/matrix/driving-car"
    # District/subdistrict representatives are geographic centroids and can
    # fall outside a road segment. Allow a practical nearest-road snap.
    SNAP_RADIUS_METERS = 5_000

    @classmethod
    def get_road_cost_matrix(cls, locations: list[Location]) -> RoadCostMatrix:
        """Fetch all pairwise road distance and duration costs in one call."""
        cls._require_api_key()

        try:
            response = requests.post(
                cls.MATRIX_URL,
                headers={"Authorization": OPENROUTESERVICE_API_KEY},
                json={
                    "locations": [
                        [location.longitude, location.latitude]
                        for location in locations
                    ],
                    "metrics": ["distance", "duration"],
                    "units": "m",
                },
                timeout=20,
            )
        except requests.RequestException as error:
            raise RoutingProviderUnavailableError(
                "Road-cost matrix service is unavailable."
            ) from error

        cls._raise_for_provider_error(response, "road-cost matrix")
        payload = response.json()
        return RoadCostMatrix(
            distance_meters=payload["distances"],
            duration_seconds=payload["durations"],
        )

    @classmethod
    def get_route(cls, locations: list[Location]) -> dict:
        cls._require_api_key()

        try:
            response = requests.post(
                cls.BASE_URL,
                headers={"Authorization": OPENROUTESERVICE_API_KEY},
                json={
                    "coordinates": [
                        [location.longitude, location.latitude]
                        for location in locations
                    ],
                    "instructions": True,
                    "radiuses": [cls.SNAP_RADIUS_METERS] * len(locations),
                },
                timeout=20,
            )
        except requests.RequestException as error:
            raise RoutingProviderUnavailableError(
                "Road route service is unavailable."
            ) from error

        cls._raise_for_provider_error(response, "road route")

        features = response.json().get("features", [])
        if not features:
            raise RuntimeError("The routing provider returned no route.")

        feature = features[0]
        summary = feature["properties"]["summary"]
        segments = feature["properties"].get("segments", [])

        return {
            "distance_km": summary["distance"] / 1_000,
            "duration_minutes": summary["duration"] / 60,
            "geometry": feature["geometry"]["coordinates"],
            "legs": segments,
        }

    @staticmethod
    def _require_api_key() -> None:
        if not OPENROUTESERVICE_API_KEY:
            raise RoutingProviderUnavailableError(
                "OPENROUTESERVICE_API_KEY is not configured."
            )

    @staticmethod
    def _raise_for_provider_error(response, operation: str) -> None:
        if response.ok:
            return

        if response.status_code >= 500 or response.status_code == 429:
            raise RoutingProviderUnavailableError(
                f"OpenRouteService {operation} is temporarily unavailable."
            )

        try:
            message = response.json()["error"]["message"]
        except (KeyError, ValueError, TypeError):
            message = response.text
        raise RoutingProviderError(
            f"OpenRouteService {operation} failed: {message}"
        )
