function WeatherCard({ weather }) {

  if (!weather) return null;

  const overallRisk = weather.overall_risk;

  const riskLevel = overallRisk?.level || "Unknown";
  const riskScore = overallRisk?.score;
  const recommendation =
    overallRisk?.recommendation ||
    weather.recommendation ||
    "No recommendation available.";

  const getRiskClass = (level) => {

    switch (level?.toLowerCase()) {

      case "low":
        return "bg-green-500";

      case "medium":
        return "bg-yellow-500";

      case "high":
        return "bg-orange-500";

      case "critical":
        return "bg-red-600";

      default:
        return "bg-gray-500";
    }
  };


  return (

    <div className="bg-white rounded-2xl shadow-lg p-8">

      <h2 className="text-2xl font-bold mb-6">
        🌤 Weather
      </h2>


      <div className="space-y-5">

        {weather.reports?.map((report, index) => (

          <div
            key={index}
            className="border rounded-xl p-4"
          >

            <h3 className="text-lg font-semibold">
              📍 {report.weather.location.name}
            </h3>


            <div className="mt-3 space-y-1 text-gray-700">

              <p>
                Condition: {report.weather.condition}
              </p>

              <p>
                Temperature: {report.weather.temperature}°C
              </p>

              <p>
                Humidity: {report.weather.humidity}%
              </p>

              <p>
                Wind Speed: {report.weather.wind_speed} m/s
              </p>

            </div>

          </div>

        ))}

      </div>


      <div className="mt-6">

        <h3 className="font-semibold text-lg">
          Overall Risk
        </h3>


        <div className="mt-3 flex items-center gap-3 flex-wrap">

          <span
            className={`
              inline-block
              px-4
              py-2
              rounded-full
              text-white
              font-semibold
              ${getRiskClass(riskLevel)}
            `}
          >
            {riskLevel}
          </span>


          {riskScore !== null &&
            riskScore !== undefined && (

              <span className="font-semibold text-gray-700">
                Score: {riskScore}/100
              </span>

            )}

        </div>


        <p className="mt-3 text-gray-700">
          {recommendation}
        </p>

      </div>

    </div>

  );

}

export default WeatherCard;