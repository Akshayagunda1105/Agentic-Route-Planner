from app.models.optimization_result import OptimizationResult
from app.models.reflection_result import ReflectionResult
from app.models.weather_analysis import WeatherAnalysis


class ReflectionAgent:
    """
    Deterministic verification and guardrail agent.

    The Reflection Agent does not use an LLM.

    It evaluates the generated route and weather analysis using
    explicit, measurable rules.

    Critical weather is reported to the orchestration layer as a
    condition requiring user choice. The Reflection Agent does not
    automatically change route preferences or make the final route
    selection.
    """

    MAX_REPLAN_ATTEMPTS = 3

    # Weather scores above this value are considered critical.
    WEATHER_REPLAN_THRESHOLD = 70

    def evaluate(
        self,
        optimization: OptimizationResult,
        weather: WeatherAnalysis,
        replan_attempt: int = 0,
    ) -> ReflectionResult:

        failed_checks = []

        # =========================================================
        # Guardrail 1: Maximum replanning attempts
        # =========================================================

        if replan_attempt >= self.MAX_REPLAN_ATTEMPTS:

            return ReflectionResult(
                approved=False,
                should_retry=False,
                message=(
                    "Maximum replanning attempts reached. "
                    "The system could not complete route validation."
                ),
                failed_checks=["max_replan_attempts"],
                replan_reason="MAX_REPLAN_ATTEMPTS_REACHED",
            )

        # =========================================================
        # Guardrail 2: Route must exist
        # =========================================================

        route = optimization.route

        if not route:

            return ReflectionResult(
                approved=False,
                should_retry=True,
                message=(
                    "Optimizer returned an empty route. "
                    "A new route should be generated."
                ),
                failed_checks=["route_exists"],
                replan_reason="EMPTY_ROUTE",
            )

        # =========================================================
        # Guardrail 3: Distance must be valid
        # =========================================================

        if optimization.total_distance < 0:

            return ReflectionResult(
                approved=False,
                should_retry=True,
                message=(
                    "Invalid route detected: "
                    "route distance cannot be negative."
                ),
                failed_checks=["valid_distance"],
                replan_reason="INVALID_ROUTE_DISTANCE",
            )

        # =========================================================
        # Guardrail 4: Duration must be valid
        # =========================================================

        if (
            optimization.total_duration is not None
            and optimization.total_duration < 0
        ):

            return ReflectionResult(
                approved=False,
                should_retry=True,
                message=(
                    "Invalid route detected: "
                    "route duration cannot be negative."
                ),
                failed_checks=["valid_duration"],
                replan_reason="INVALID_ROUTE_DURATION",
            )

        # =========================================================
        # Guardrail 5: No duplicate locations
        # =========================================================

        location_names = [
            location.name.strip().lower()
            for location in route
        ]

        if len(location_names) != len(set(location_names)):

            return ReflectionResult(
                approved=False,
                should_retry=True,
                message=(
                    "Duplicate locations were found in "
                    "the optimized route."
                ),
                failed_checks=["duplicate_locations"],
                replan_reason="DUPLICATE_LOCATIONS",
            )

        # =========================================================
        # Guardrail 6: Weather analysis must exist
        # =========================================================

        if weather is None:

            return ReflectionResult(
                approved=False,
                should_retry=True,
                message=(
                    "Weather analysis is unavailable. "
                    "The route cannot be verified."
                ),
                failed_checks=["weather_available"],
                replan_reason="WEATHER_ANALYSIS_UNAVAILABLE",
            )

        # =========================================================
        # Guardrail 7: Weather reports must exist
        # =========================================================

        if not weather.reports:

            return ReflectionResult(
                approved=False,
                should_retry=True,
                message=(
                    "No weather reports were available for "
                    "the route."
                ),
                failed_checks=["weather_reports_available"],
                replan_reason="NO_WEATHER_REPORTS",
            )

        # =========================================================
        # Guardrail 8: Validate every weather risk score
        # =========================================================

        risk_scores = []

        for report in weather.reports:

            score = report.risk.score

            if not 0 <= score <= 100:

                return ReflectionResult(
                    approved=False,
                    should_retry=True,
                    message=(
                        "Invalid weather risk score detected. "
                        "Risk scores must be between 0 and 100."
                    ),
                    failed_checks=["weather_risk_score_range"],
                    weather_risk_score=float(score),
                    weather_risk_threshold=(
                        float(self.WEATHER_REPLAN_THRESHOLD)
                    ),
                    replan_reason="INVALID_WEATHER_RISK_SCORE",
                )

            risk_scores.append(score)

        # =========================================================
        # Guardrail 9: Calculate route weather risk
        # =========================================================

        maximum_weather_risk = max(risk_scores)

        average_weather_risk = (
            sum(risk_scores) / len(risk_scores)
        )

        # =========================================================
        # Guardrail 10: Critical weather
        #
        # Critical weather is NOT an automatic replan.
        #
        # The route remains a valid candidate, but the graph must
        # generate an alternative and ask the user to choose.
        # =========================================================

        if maximum_weather_risk > self.WEATHER_REPLAN_THRESHOLD:

            return ReflectionResult(
                approved=True,
                should_retry=False,
                message=(
                    "Critical weather risk detected on the "
                    "generated route. "
                    f"Maximum risk score is "
                    f"{maximum_weather_risk}/100 and average "
                    f"risk is {average_weather_risk:.1f}/100. "
                    "A lower-weather-risk alternative should "
                    "be presented to the user."
                ),
                failed_checks=[],
                weather_risk_score=float(maximum_weather_risk),
                weather_risk_threshold=(
                    float(self.WEATHER_REPLAN_THRESHOLD)
                ),
                replan_reason="CRITICAL_WEATHER_RISK",
            )

        # =========================================================
        # Guardrail 11: High weather risk
        # =========================================================

        if maximum_weather_risk >= 41:

            return ReflectionResult(
                approved=True,
                should_retry=False,
                message=(
                    "Route passed all deterministic guardrails, "
                    "but weather risk is elevated. "
                    f"Maximum weather risk is "
                    f"{maximum_weather_risk}/100 and average "
                    f"weather risk is "
                    f"{average_weather_risk:.1f}/100. "
                    "Travel with caution."
                ),
                failed_checks=[],
                weather_risk_score=float(maximum_weather_risk),
                weather_risk_threshold=(
                    float(self.WEATHER_REPLAN_THRESHOLD)
                ),
            )

        # =========================================================
        # All guardrails passed
        # =========================================================

        return ReflectionResult(
            approved=True,
            should_retry=False,
            message=(
                "Route passed all deterministic validation "
                "and weather guardrails."
            ),
            failed_checks=failed_checks,
            weather_risk_score=float(maximum_weather_risk),
            weather_risk_threshold=(
                float(self.WEATHER_REPLAN_THRESHOLD)
            ),
        )