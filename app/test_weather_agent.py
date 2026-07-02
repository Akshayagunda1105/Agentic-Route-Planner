from app.models.location import Location

from app.models.optimization_result import (
    OptimizationResult
)

from app.agents.weather_agent import (
    WeatherAgent
)


route = [

    Location(

        name="Hyderabad",

        district="Hyderabad",

        subdistrict="Bandlaguda",

        latitude=17.40030329999287,

        longitude=78.47703451108815

    ),

    Location(

        name="Kodad",

        district="Suryapet",

        subdistrict="Kodad",

        latitude=16.97574826365493,

        longitude=79.99307992002012

    )

]

optimization = OptimizationResult(

    route=route,

    total_distance=180,

    strategy="Nearest Neighbor",

    execution_time=0.01

)

agent = WeatherAgent()

analysis = agent.analyze(
    optimization
)

print(analysis)