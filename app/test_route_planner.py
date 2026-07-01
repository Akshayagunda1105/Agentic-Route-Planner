from app.orchestrators.route_planner import RoutePlanner

planner = RoutePlanner()

result = planner.plan(
    "I am in Hyderabad and want to visit Kodad and Nalgonda before reaching Suryapet."
)

print(result)

if result.success:
    print("\nOptimized Route:\n")
    print(result.optimization)
else:
    print("\nPlanning Failed")
    print(result.errors)
    print(result.pending_locations)