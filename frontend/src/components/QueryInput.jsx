import { FaRocket } from "react-icons/fa";

function QueryInput({
  query,
  setQuery,
  onSubmit
}) {
  return (

    <div className="bg-white rounded-2xl shadow-lg p-8">

      <h2 className="text-xl font-semibold mb-5">

        Where do you want to travel?

      </h2>

      <input

        className="
        w-full
        border
        border-gray-300
        rounded-xl
        p-4
        text-lg
        focus:outline-none
        focus:ring-2
        focus:ring-blue-500
        "

        type="text"

        placeholder="Example: I am in Hyderabad and want to visit Kodad"

        value={query}

        onChange={(e)=>setQuery(e.target.value)}

      />

      <button

  onClick={onSubmit}

  className="
  mt-6
  w-full
  bg-blue-600
  hover:bg-blue-700
  text-white
  rounded-xl
  py-4
  text-lg
  font-semibold
  transition
  flex
  justify-center
  items-center
  gap-3
  "

>

<FaRocket />

Plan Route

</button>
    </div>

  );
}

export default QueryInput;