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

    }

    catch (error) {

      console.error(error);

      alert(error.response?.data?.detail || "Failed to fetch route.");

    }

    finally {

      setLoading(false);

    }

  };

  const chooseLocation = (pendingQuery, location) => {

    setSelections((current) => ({
      ...current,
      [pendingQuery]: location
    }));

  };

  return (

<div className="min-h-screen bg-slate-100">

<div className="max-w-6xl mx-auto p-10">

<Header/>

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

    <h2 className="text-xl font-bold">Choose a location</h2>

    <p className="mt-2">{pending.message}</p>

    <div className="grid gap-3 mt-4">

      {pending.candidates.map((location) => (

        <button
          key={`${location.name}-${location.latitude}-${location.longitude}`}
          onClick={() => chooseLocation(pending.query, location)}
          className="text-left rounded-xl bg-white border p-4 hover:border-blue-600"
        >
          <strong>{location.name}</strong> — {location.subdistrict}, {location.district}
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
{result && (

<>
  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">

    <DistanceCard
      optimization={result.optimization}
    />

    <WeatherCard
      weather={result.weather}
    />

  </div>

  <RouteCard
    optimization={result.optimization}
  />

  <RouteMap optimization={result.optimization} />

  <RecommendationCard
    weather={result.weather}
  />
</>
)}

</div>

</div>

);

}

export default App;
