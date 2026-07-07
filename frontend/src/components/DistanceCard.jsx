function DistanceCard({ optimization }) {

  if (!optimization) return null;

  return (

    <div
      className="
      bg-white
      rounded-2xl
      shadow-lg
      p-8
      mt-8
      text-center
      "
    >

      <h2 className="text-2xl font-bold">

        📏 Total Distance

      </h2>

      <p
        className="
        text-5xl
        font-bold
        text-blue-600
        mt-5
        "
      >

        {optimization.total_distance.toFixed(2)} km

      </p>

    </div>

  );

}

export default DistanceCard;