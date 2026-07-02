from app.models.optimization_result import (
    OptimizationResult
)

from app.models.weather_analysis import (
    WeatherAnalysis
)

from app.models.weather_report import (
    WeatherReport
)

from app.services.weather_service import (
    WeatherService
)

from app.services.weather_risk_engine import (
    WeatherRiskEngine
)


class WeatherAgent:

    def analyze(
        self,
        optimization: OptimizationResult
    ) -> WeatherAnalysis:

        reports = []

        highest_score = 0

        overall_risk = "Low"

        recommendation = "Safe to travel."

        for location in optimization.route:

            weather = WeatherService.get_weather(
                location
            )

            risk = WeatherRiskEngine.calculate_risk(
                weather
            )

            report = WeatherReport(

                weather=weather,

                risk=risk

            )

            reports.append(
                report
            )

            if risk.score > highest_score:

                highest_score = risk.score

                overall_risk = risk.level

                recommendation = (
                    risk.recommendation
                )

        return WeatherAnalysis(

            reports=reports,

            overall_risk=overall_risk,

            recommendation=recommendation

        )