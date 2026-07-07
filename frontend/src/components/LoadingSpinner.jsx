import { FaSpinner } from "react-icons/fa";

function LoadingSpinner() {

  return (

    <div className="flex justify-center mt-8">

      <div className="flex items-center gap-3">

        <FaSpinner
          className="animate-spin text-blue-600"
          size={30}
        />

        <span className="text-lg">

          Planning your journey...

        </span>

      </div>

    </div>

  );

}

export default LoadingSpinner;