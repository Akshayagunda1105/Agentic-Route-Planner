function RouteCard({ optimization }) {

  if (!optimization) return null;

  return (

    <div>

      <h2>📍 Optimized Route</h2>

      {optimization.route.map((location, index) => (

        <div key={index}>

          <p>{location.name}</p>

          {index !== optimization.route.length - 1 && (
            <p>↓</p>
          )}

        </div>

      ))}

    </div>

  );

}

export default RouteCard;