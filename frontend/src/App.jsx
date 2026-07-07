import { useState } from "react";

import Header from "./components/Header";
import QueryInput from "./components/QueryInput";
import RouteCard from "./components/RouteCard";
import DistanceCard from "./components/DistanceCard";
import api from "./services/api";
import WeatherCard from "./components/WeatherCard";
import RecommendationCard from "./components/RecommendationCard";
import LoadingSpinner from "./components/LoadingSpinner";

function App() {

  const [query, setQuery] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {

    if (!query.trim()) return;

    setLoading(true);

    try {

      const response = await api.post(

        "/plan-route",

        {
          query: query
        }

      );

      console.log(response.data);

      setResult(response.data);

    }

    catch (error) {

      console.error(error);

      alert("Failed to fetch route.");

    }

    finally {

      setLoading(false);

    }

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