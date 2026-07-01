from app.agents.reflection_agent import ReflectionAgent

from app.models.location import Location
from app.models.optimization_result import OptimizationResult


agent = ReflectionAgent()

route = [

    Location(
        name="Hyderabad",
        district="Hyderabad",
        subdistrict="Shaikpet",
        latitude=17.42,
        longitude=78.47
    ),

    Location(
        name="Kodad",
        district="Suryapet",
        subdistrict="Kodad",
        latitude=17.00,
        longitude=79.97
    )

]

optimization = OptimizationResult(

    route=route,

    total_distance=140,

    strategy="Nearest Neighbor",

    execution_time=0.001

)

result = agent.evaluate(
    optimization
)

print(result)