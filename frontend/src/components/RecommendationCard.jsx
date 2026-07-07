function RecommendationCard({ weather }) {

  if (!weather) return null;

  return (

    <div className="bg-white rounded-2xl shadow-lg p-8 mt-8">

      <h2 className="text-2xl font-bold mb-5">

        💡 AI Recommendation

      </h2>

      <div
        className="
        bg-blue-50
        border-l-4
        border-blue-600
        p-5
        rounded-xl
        "
      >

        <p className="text-lg">

          {weather.recommendation}

        </p>

      </div>

    </div>

  );

}

export default RecommendationCard;