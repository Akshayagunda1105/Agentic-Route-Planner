from app.tools.retriever_tool import RetrieverTool
from app.models.retrieval_result import RetrievalResult

class RetrieverAgent:

    def __init__(self):

        self.tool = RetrieverTool()
    def resolve_location(
    self,
    query: str
):

        location = self.tool.search_district(query)

        if location:

            return RetrievalResult(

                resolved=True,

                location=location,

                message="District matched."

            )

        location = self.tool.search_subdistrict(query)

        if location:

            return RetrievalResult(

                resolved=True,

                location=location,

                message="Subdistrict matched."

            )

        location = self.tool.search_village(query)

        if location:

            return RetrievalResult(

                resolved=True,

                location=location,

                message="Village matched."

            )

        candidates = self.tool.get_candidate_matches(
            query,
            "village"
        )

        if len(candidates) == 0:

            return RetrievalResult(

                resolved=False,

                message="No matching location found."

            )

        if len(candidates) == 1:

            return RetrievalResult(

                resolved=True,

                location=candidates[0],

                message="Resolved using RapidFuzz."

            )

        return RetrievalResult(

            resolved=False,

            needs_user_selection=True,

            candidates=candidates,

            message="Multiple matching locations found."

        )