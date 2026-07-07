function WeatherCard({ weather }) {

  if (!weather) return null;

  return (

    <div className="bg-white rounded-2xl shadow-lg p-8">

      <h2 className="text-2xl font-bold mb-6">

        🌤 Weather

      </h2>

      <div className="space-y-5">

        {weather.reports.map((report, index) => (

          <div
            key={index}
            className="border rounded-xl p-4"
          >

            <h3 className="text-lg font-semibold">

              📍 {report.weather.location.name}

            </h3>

            <div className="mt-3 space-y-1 text-gray-700">

              <p>Condition: {report.weather.condition}</p>

              <p>Temperature: {report.weather.temperature}°C</p>

              <p>Humidity: {report.weather.humidity}%</p>

              <p>Wind Speed: {report.weather.wind_speed} km/h</p>

            </div>

          </div>

        ))}

      </div>

      <div className="mt-6">

        <h3 className="font-semibold text-lg">

          Overall Risk

        </h3>

        <span
          className={`
            inline-block
            mt-2
            px-4
            py-2
            rounded-full
            text-white
            ${
              weather.overall_risk === "Low"
                ? "bg-green-500"
                : weather.overall_risk === "Medium"
                ? "bg-yellow-500"
                : "bg-red-500"
            }
          `}
        >
          {weather.overall_risk}
        </span>

      </div>

    </div>

  );

}

export default WeatherCard;