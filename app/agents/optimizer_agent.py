from datetime import datetime, timedelta

from app.models.route_plan import RoutePlan
from app.models.optimization_result import OptimizationResult
from app.models.road_cost_matrix import RoadCostMatrix

from app.strategies.optimization_strategy import OptimizationStrategy
from app.strategies.nearest_neighbor import NearestNeighborStrategy

from app.services.routing_service import (
    RoutingProviderUnavailableError,
    RoutingService,
)
from app.services.weather_service import WeatherService
from app.services.weather_risk_engine import WeatherRiskEngine


class OptimizerAgent:

    def __init__(
        self,
        strategy: OptimizationStrategy = None,
        routing_service=RoutingService,
        road_cost_metric: str = "duration",
        weather_service=WeatherService,
        weather_risk_engine=WeatherRiskEngine,
    ):
        if strategy is None:
            strategy = NearestNeighborStrategy()

        self.strategy = strategy
        self.routing_service = routing_service
        self.road_cost_metric = road_cost_metric
        self.weather_service = weather_service
        self.weather_risk_engine = weather_risk_engine

    def optimize(
        self,
        route_plan: RoutePlan,
        objective: str = "duration",
        weather_sensitive: bool = False,
        weather_weight: float = 0.3,
        departure_time: str | None = None,
    ) -> OptimizationResult:

        if objective not in {
            "distance",
            "duration",
            "weather_aware",
        }:
            raise ValueError(
                "Objective must be 'distance', 'duration', or "
                "'weather_aware'."
            )

        if not 0.0 <= weather_weight <= 1.0:
            raise ValueError(
                "weather_weight must be between 0.0 and 1.0."
            )

        if objective == "weather_aware":
            weather_sensitive = True

        parsed_departure_time = self._parse_departure_time(
            departure_time
        )

        locations = [
            route_plan.start,
            *route_plan.waypoints,
            route_plan.destination,
        ]

        try:
            road_cost_matrix = (
                self.routing_service.get_road_cost_matrix(
                    locations
                )
            )
        except RoutingProviderUnavailableError as error:
            fallback = self.strategy.optimize(route_plan)

            return fallback.model_copy(
                update={
                    "strategy": (
                        "Nearest Neighbor "
                        "(Haversine fallback)"
                    ),
                    "fallback_reason": str(error),
                }
            )

        ordering_metric = self._get_ordering_metric(
            objective
        )

        optimization_matrix = road_cost_matrix

        if weather_sensitive:
            # First create a road-only route. We need this provisional
            # ordering to estimate when the vehicle reaches each location.
            provisional_estimate = self.strategy.optimize(
                route_plan,
                road_cost_matrix=road_cost_matrix,
                cost_metric=ordering_metric,
            )

            arrival_times = self._calculate_arrival_times(
                provisional_estimate.route,
                road_cost_matrix,
                locations,
                parsed_departure_time,
            )

            optimization_matrix = (
                self._build_weather_aware_matrix(
                    locations=locations,
                    road_cost_matrix=road_cost_matrix,
                    weather_weight=weather_weight,
                    arrival_times=arrival_times,
                )
            )

        estimate = self.strategy.optimize(
            route_plan,
            road_cost_matrix=optimization_matrix,
            cost_metric=ordering_metric,
        )

        road_route = self.routing_service.get_route(
            estimate.route
        )

        strategy_name = (
            "Nearest Neighbor + 2-opt "
            "(weather-aware road costs)"
            if weather_sensitive
            else (
                "Nearest Neighbor + 2-opt "
                "(OpenRouteService road costs)"
            )
        )

        return OptimizationResult(
            route=estimate.route,
            total_distance=road_route["distance_km"],
            total_duration=road_route["duration_minutes"],
            geometry=road_route["geometry"],
            legs=road_route["legs"],
            geographic_distance=estimate.geographic_distance,
            road_distance=road_route["distance_km"],
            road_duration=road_route["duration_minutes"],
            ordering_cost_source=(
                "weather_adjusted_road_network"
                if weather_sensitive
                else estimate.ordering_cost_source
            ),
            ordering_cost_metric=(
                "weather_adjusted_duration"
                if weather_sensitive
                else estimate.ordering_cost_metric
            ),
            is_road_optimized=True,
            strategy=strategy_name,
            execution_time=estimate.execution_time,
        )

    @staticmethod
    def _parse_departure_time(
        departure_time: str | None,
    ) -> datetime | None:

        if departure_time is None:
            return None

        try:
            parsed = datetime.fromisoformat(
                departure_time
            )
        except ValueError as error:
            raise ValueError(
                "departure_time must be a valid ISO-8601 datetime."
            ) from error

        if parsed.tzinfo is None:
            raise ValueError(
                "departure_time must include timezone information."
            )

        return parsed

    @staticmethod
    def _get_ordering_metric(
        objective: str,
    ) -> str:

        if objective == "distance":
            return "distance"

        # Duration is also the base metric for weather-aware
        # optimization because weather risk is applied as a
        # multiplier to road travel time.
        return "duration"

    @staticmethod
    def _calculate_arrival_times(
        route,
        road_cost_matrix: RoadCostMatrix,
        locations,
        departure_time: datetime | None,
    ) -> dict[str, datetime | None]:

        if departure_time is None:
            return {
                location.name: None
                for location in route
            }

        location_to_index = {
            id(location): index
            for index, location in enumerate(locations)
        }

        current_time = departure_time

        arrival_times = {
            route[0].name: current_time
        }

        for origin, destination in zip(
            route,
            route[1:],
        ):
            origin_index = location_to_index[id(origin)]
            destination_index = location_to_index[id(destination)]

            duration_seconds = (
                road_cost_matrix.duration_seconds[
                    origin_index
                ][destination_index]
            )

            if duration_seconds is None:
                arrival_times[destination.name] = None
                continue

            current_time = current_time + timedelta(
                seconds=float(duration_seconds)
            )

            arrival_times[destination.name] = current_time

        return arrival_times

    def _build_weather_aware_matrix(
        self,
        locations,
        road_cost_matrix: RoadCostMatrix,
        weather_weight: float,
        arrival_times: dict[str, datetime | None],
    ) -> RoadCostMatrix:

        weather_risks = []

        for location in locations:

            target_time = arrival_times.get(
                location.name
            )

            if target_time is not None:
                weather = self.weather_service.get_weather_at(
                    location,
                    target_time,
                )
            else:
                # Preserve the existing behavior when the user
                # does not provide a departure time.
                weather = self.weather_service.get_weather(
                    location
                )

            risk = self.weather_risk_engine.calculate_risk(
                weather
            )

            weather_risks.append(
                min(
                    max(float(risk.score), 0.0),
                    100.0,
                )
            )

        adjusted_durations = []

        for origin_index, origin_row in enumerate(
            road_cost_matrix.duration_seconds
        ):
            adjusted_row = []

            for destination_index, duration in enumerate(
                origin_row
            ):

                if duration is None:
                    adjusted_row.append(None)
                    continue

                if origin_index == destination_index:
                    adjusted_row.append(duration)
                    continue

                origin_risk = weather_risks[
                    origin_index
                ]

                destination_risk = weather_risks[
                    destination_index
                ]

                average_risk = (
                    origin_risk + destination_risk
                ) / 2.0

                weather_multiplier = (
                    1.0
                    + weather_weight
                    * (average_risk / 100.0)
                )

                adjusted_row.append(
                    duration * weather_multiplier
                )

            adjusted_durations.append(adjusted_row)

        return RoadCostMatrix(
            distance_meters=(
                road_cost_matrix.distance_meters
            ),
            duration_seconds=adjusted_durations,
        )