from app.models.weather_risk import WeatherRisk


risk = WeatherRisk(

    score=55,

    level="High",

    recommendation="Delay travel if possible."

)

print(risk)