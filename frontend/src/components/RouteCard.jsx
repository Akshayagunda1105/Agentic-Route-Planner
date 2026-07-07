function RouteCard({ optimization }) {

  if (!optimization) return null;

  return (

    <div className="bg-white rounded-2xl shadow-lg p-8 mt-8">

      <h2 className="text-2xl font-bold mb-6">

        📍 Optimized Route

      </h2>

      <div className="space-y-3">

        {optimization.route.map((location, index) => (

          <div
            key={index}
            className="flex flex-col items-center"
          >

            <div
              className="
              bg-blue-100
              text-blue-700
              px-6
              py-3
              rounded-full
              font-semibold
              "
            >

              {location.name}

            </div>

            {index !== optimization.route.length - 1 && (

              <div className="text-3xl text-blue-500">

                ↓

              </div>

            )}

          </div>

        ))}

      </div>

    </div>

  );

}

export default RouteCard;