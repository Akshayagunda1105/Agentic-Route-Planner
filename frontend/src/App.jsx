import { useState } from "react";

import Header from "./components/Header";
import QueryInput from "./components/QueryInput";
import RouteCard from "./components/RouteCard";
import DistanceCard from "./components/DistanceCard";
import api from "./services/api";

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

    <div>

      <Header />

      <QueryInput

        query={query}

        setQuery={setQuery}

        onSubmit={handleSubmit}

      />

      {loading &&

        <p>Planning route...</p>

      }

      {result && (
  <>
    <RouteCard
      optimization={result.optimization}
    />

    <DistanceCard
      optimization={result.optimization}
    />
  </>
)}
    </div>

  );

}

export default App;