function DistanceCard({ optimization }) {

  if (!optimization) return null;

  return (

    <div>

      <h2>📏 Total Distance</h2>

      <h3>

        {optimization.total_distance.toFixed(2)} km

      </h3>

    </div>

  );

}

export default DistanceCard;