function QueryInput({
  query,
  setQuery,
  onSubmit
}) {
  return (
    <div>

      <input
        type="text"
        placeholder="Enter your travel query..."
        value={query}
        onChange={(e) =>
          setQuery(e.target.value)
        }
      />

      <button onClick={onSubmit}>
        🚀 Plan Route
      </button>

    </div>
  );
}

export default QueryInput;