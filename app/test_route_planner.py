from app.orchestrators.route_planner import RoutePlanner

planner = RoutePlanner()

result = planner.plan(
    "I am in Hyderabad and want to visit Kodad before Suryapet"
)

print(result)

print("\nOptimized Route:\n")
print(result.optimization)

print("\nWeather Analysis:\n")
print(result.weather)

print("\nReflection:\n")
print(result.reflection)