import { FaRoute } from "react-icons/fa";

function Header() {
  return (
    <header className="text-center mb-10">

      <div className="flex justify-center items-center gap-4">

        <FaRoute
          className="text-blue-600"
          size={50}
        />

        <h1 className="text-5xl font-bold text-blue-600">
          Agentic Route Planner
        </h1>

      </div>

      <p className="mt-4 text-gray-600 text-lg">
        AI-powered route optimization with
        real-time weather intelligence
      </p>

    </header>
  );
}

export default Header;