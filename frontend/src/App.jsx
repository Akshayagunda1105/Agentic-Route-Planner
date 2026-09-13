import { useState } from "react";

import Header from "./components/Header";
import QueryInput from "./components/QueryInput";
import RouteCard from "./components/RouteCard";
import DistanceCard from "./components/DistanceCard";
import api from "./services/api";
import WeatherCard from "./components/WeatherCard";
import RecommendationCard from "./components/RecommendationCard";
import LoadingSpinner from "./components/LoadingSpinner";
import RouteMap from "./components/RouteMap";

function App() {

  const [query, setQuery] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [selections, setSelections] = useState({});

  const [selectedOptionId, setSelectedOptionId] = useState(null);


  const handleSubmit = async () => {

    if (!query.trim()) return;

    setLoading(true);

    try {

      const response = await api.post(
        "/plan-route",
        {
          query,
          selections
        }
      );

      console.log(response.data);

      setResult(response.data);

      if (response.data.selected_option_id) {

        setSelectedOptionId(
          response.data.selected_option_id
        );

      }
      else if (
        response.data.options?.length === 1
      ) {

        setSelectedOptionId(
          response.data.options[0].option_id
        );

      }
      else {

        setSelectedOptionId(null);

      }

    }

    catch (error) {

      console.error(error);

      alert(
        error.response?.data?.detail ||
        "Failed to fetch route."
      );

    }

    finally {

      setLoading(false);

    }

  };


  const chooseLocation = (
    pendingQuery,
    location
  ) => {

    setSelections((current) => ({
      ...current,
      [pendingQuery]: location
    }));

  };


  const selectRouteOption = (optionId) => {

    setSelectedOptionId(optionId);

  };


  const selectedOption =
    result?.options?.find(
      (option) =>
        option.option_id === selectedOptionId
    );


  const displayedOptimization =
    selectedOption?.optimization ||
    result?.optimization;


  const displayedWeather =
    selectedOption?.weather ||
    result?.weather;


  return (

    <div className="min-h-screen bg-slate-100">

      <div className="max-w-6xl mx-auto p-10">

        <Header />

        <QueryInput
          query={query}
          setQuery={setQuery}
          onSubmit={handleSubmit}
        />


        {loading && <LoadingSpinner />}


        {result?.pending_locations?.map((pending) => (

          <div
            key={pending.query}
            className="bg-amber-50 border border-amber-300 rounded-2xl p-6 mt-8"
          >

            <h2 className="text-xl font-bold">
              Choose a location
            </h2>

            <p className="mt-2">
              {pending.message}
            </p>

            <div className="grid gap-3 mt-4">

              {pending.candidates.map((location) => (

                <button
                  key={`${location.name}-${location.latitude}-${location.longitude}`}
                  onClick={() =>
                    chooseLocation(
                      pending.query,
                      location
                    )
                  }
                  className="text-left rounded-xl bg-white border p-4 hover:border-blue-600"
                >

                  <strong>
                    {location.name}
                  </strong>

                  {" — "}

                  {location.subdistrict},{" "}
                  {location.district}

                </button>

              ))}

            </div>


            {pending.candidates.length > 0 && (

              <button
                onClick={handleSubmit}
                className="mt-4 bg-blue-600 text-white rounded-xl px-5 py-3"
              >
                Continue with selection
              </button>

            )}

          </div>

        ))}


        {result && !result.pending_locations?.length && (

          <>

            {result.selection_required &&
              result.options?.length > 0 && (

                <div className="bg-amber-50 border border-amber-300 rounded-2xl p-6 mt-8">

                  <h2 className="text-2xl font-bold">
                    Weather Risk Detected
                  </h2>

                  <p className="mt-2 text-slate-700">
                    The requested route has significant
                    weather risk. Choose which route
                    you want to take.
                  </p>


                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5">

                    {result.options.map((option) => (

                      <button
                        key={option.option_id}
                        onClick={() =>
                          selectRouteOption(
                            option.option_id
                          )
                        }
                        className={`text-left rounded-2xl border-2 p-5 bg-white transition ${
                          selectedOptionId === option.option_id
                            ? "border-blue-600 ring-2 ring-blue-200"
                            : "border-slate-200 hover:border-blue-400"
                        }`}
                      >

                        <div className="flex items-center justify-between">

                          <h3 className="text-lg font-bold">
                            {option.label}
                          </h3>

                          {selectedOptionId === option.option_id && (

                            <span className="text-sm font-semibold text-blue-600">
                              Selected
                            </span>

                          )}

                        </div>


                        <p className="mt-2 text-slate-600">
                          {option.description}
                        </p>


                        {option.weather_risk_score !== null &&
                          option.weather_risk_score !== undefined && (

                            <p className="mt-4 font-semibold">
                              Weather risk score:{" "}
                              {option.weather_risk_score}
                            </p>

                          )}

                      </button>

                    ))}

                  </div>

                </div>

              )}


            {displayedOptimization && (

              <>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">

                  <DistanceCard
                    optimization={displayedOptimization}
                  />

                  <WeatherCard
                    weather={displayedWeather}
                  />

                </div>


                <RouteCard
                  optimization={displayedOptimization}
                />


                <RouteMap
                  optimization={displayedOptimization}
                />


                <RecommendationCard
                  weather={displayedWeather}
                />

              </>

            )}

          </>

        )}

      </div>

    </div>

  );

}

export default App;