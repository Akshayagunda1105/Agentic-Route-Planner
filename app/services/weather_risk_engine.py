from app.models.weather_info import WeatherInfo
from app.models.weather_risk import WeatherRisk


class WeatherRiskEngine:

    @classmethod
    def calculate_risk(
        cls,
        weather: WeatherInfo
    ) -> WeatherRisk:

        score = 0

        # -------------------------
        # Condition Score
        # -------------------------

        condition_scores = {

            "Clear": 0,
            "Clouds": 5,
            "Mist": 10,
            "Haze": 10,
            "Fog": 20,
            "Drizzle": 20,
            "Rain": 35,
            "Thunderstorm": 70,
            "Snow": 60

        }

        score += condition_scores.get(
            weather.condition,
            10
        )

        # -------------------------
        # Wind Score
        # -------------------------

        if weather.wind_speed > 20:

            score += 30

        elif weather.wind_speed > 15:

            score += 20

        elif weather.wind_speed > 10:

            score += 10

        elif weather.wind_speed > 5:

            score += 5

        # -------------------------
        # Humidity Score
        # -------------------------

        if weather.humidity > 90:

            score += 10

        elif weather.humidity > 80:

            score += 5

        # -------------------------
        # Temperature Score
        # -------------------------

        if weather.temperature > 40:

            score += 20

        elif weather.temperature > 35:

            score += 10

        elif weather.temperature < 5:

            score += 20

        elif weather.temperature < 10:

            score += 10

        # -------------------------
        # Risk Level
        # -------------------------

        if score <= 20:

            level = "Low"

            recommendation = "Safe to travel."

        elif score <= 40:

            level = "Medium"

            recommendation = (
                "Travel with caution."
            )

        elif score <= 70:

            level = "High"

            recommendation = (
                "Delay travel if possible."
            )

        else:

            level = "Critical"

            recommendation = (
                "Avoid travelling."
            )

        return WeatherRisk(

            score=score,

            level=level,

            recommendation=recommendation

        )