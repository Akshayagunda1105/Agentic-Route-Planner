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

        overall_risk = None

        recommendation = "No weather data available."

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

            if (
                overall_risk is None
                or risk.score > overall_risk.score
            ):

                overall_risk = risk

                recommendation = (
                    risk.recommendation
                )

        return WeatherAnalysis(

            reports=reports,

            overall_risk=overall_risk,

            recommendation=recommendation

        )