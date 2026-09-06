import requests

from app.config.settings import OPENROUTESERVICE_API_KEY
from app.models.location import Location


class RoutingService:
    """Road routing through OpenRouteService's free API tier."""

    BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    # District/subdistrict representatives are geographic centroids and can
    # fall outside a road segment. Allow a practical nearest-road snap.
    SNAP_RADIUS_METERS = 5_000

    @classmethod
    def get_route(cls, locations: list[Location]) -> dict:
        if not OPENROUTESERVICE_API_KEY:
            raise RuntimeError(
                "OPENROUTESERVICE_API_KEY is not configured. "
                "Create a free key at openrouteservice.org and add it to .env."
            )

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
        response.raise_for_status()

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
