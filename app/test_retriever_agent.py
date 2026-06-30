from app.agents.retriever_agent import RetrieverAgent

agent = RetrieverAgent()

queries = [
    "Hyderabad",
    "Kodad",
    "Hyderbad",
    "Pochampalle",
    "xyzabc"
]

for query in queries:

    print("\n" + "=" * 60)
    print(f"Query: {query}")
    print("=" * 60)

    result = agent.resolve_location(query)

    print(result)