from app.tools.retriever_tool import RetrieverTool

tool = RetrieverTool()

print(tool.search_district("Hyderabad"))

print()

print(tool.search_subdistrict("Kodad"))

print()

print(tool.search_village("Hyderabad"))

print()

locations = tool.get_candidate_matches(
    "Hyderbad",
    "district"
)

print("RapidFuzz Candidates:\n")

for location in locations:

    print(location)