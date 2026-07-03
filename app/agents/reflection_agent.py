from app.models.optimization_result import (
    OptimizationResult
)

from app.models.reflection_result import (
    ReflectionResult
)

from app.models.weather_analysis import (
    WeatherAnalysis
)

class ReflectionAgent:

    def evaluate(
    self,
    optimization: OptimizationResult,
    weather: WeatherAnalysis
) -> ReflectionResult:

        route = optimization.route

        # -----------------------------------
        # Rule 1
        # Route must not be empty
        # -----------------------------------

        if len(route) == 0:

            return ReflectionResult(

                approved=False,

                should_retry=True,

                message="Optimizer returned an empty route."

            )

        # -----------------------------------
        # Rule 2
        # Distance cannot be negative
        # -----------------------------------

        if optimization.total_distance < 0:

            return ReflectionResult(

                approved=False,

                should_retry=True,

                message="Negative route distance detected."

            )

        # -----------------------------------
        # Rule 3
        # Duplicate locations are not allowed
        # -----------------------------------

        names = [

            location.name

            for location in route

        ]

        if len(names) != len(set(names)):

            return ReflectionResult(

                approved=False,

                should_retry=True,

                message="Duplicate locations found."

            )

        # -----------------------------------
        # Rule 4
        # Critical weather
        # -----------------------------------

        if weather.overall_risk == "Critical":

            return ReflectionResult(

                approved=False,

                should_retry=True,

                message=(
                    "Critical weather conditions detected. "
                    "Travel is not recommended."
                )

            )

        # -----------------------------------
        # Rule 5
        # High weather risk
        # -----------------------------------

        if weather.overall_risk == "High":

            return ReflectionResult(

                approved=True,

                should_retry=False,

                message=(
                    "Route is optimized, but weather "
                    "conditions are risky. "
                    "Travel with caution."
                )

            )

        # -----------------------------------
        # Rule 6
        # Route looks valid
        # -----------------------------------

        return ReflectionResult(

            approved=True,

            should_retry=False,

            message="Route passed all validation checks."

        )