from app.models.optimization_result import (
    OptimizationResult
)

from app.models.reflection_result import (
    ReflectionResult
)


class ReflectionAgent:

    def evaluate(
        self,
        optimization: OptimizationResult
    ) -> ReflectionResult:

        route = optimization.route

        # Rule 1
        # Route must not be empty
        if len(route) == 0:

            return ReflectionResult(

                approved=False,

                should_retry=True,

                message="Optimizer returned an empty route."

            )

        # Rule 2
        # Distance cannot be negative
        if optimization.total_distance < 0:

            return ReflectionResult(

                approved=False,

                should_retry=True,

                message="Negative route distance detected."

            )

        # Rule 3
        # Duplicate locations are not allowed
        names = [location.name for location in route]

        if len(names) != len(set(names)):

            return ReflectionResult(

                approved=False,

                should_retry=True,

                message="Duplicate locations found."

            )

        # Rule 4
        # Route looks valid

        return ReflectionResult(

            approved=True,

            should_retry=False,

            message="Route passed all validation checks."

        )