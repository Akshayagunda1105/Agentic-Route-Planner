from app.tools.retriever_tool import RetrieverTool
from app.models.retrieval_result import RetrievalResult


AUTO_RESOLVE_THRESHOLD = 95
SUGGESTION_THRESHOLD = 90


class RetrieverAgent:

    def __init__(self):

        self.tool = RetrieverTool()

    def resolve_location(
        self,
        query: str
    ):

        # ------------------------------------------
        # Exact District Match
        # ------------------------------------------

        location = self.tool.search_district(query)

        if location:

            return RetrievalResult(

                resolved=True,

                location=location,

                message="District matched."

            )

        # ------------------------------------------
        # Exact Subdistrict Match
        # ------------------------------------------

        location = self.tool.search_subdistrict(query)

        if location:

            return RetrievalResult(

                resolved=True,

                location=location,

                message="Subdistrict matched."

            )

        # ------------------------------------------
        # Exact Village Match
        # ------------------------------------------

        candidates = self.tool.get_village_candidates(query)

        if len(candidates) == 1:

            return RetrievalResult(

                resolved=True,

                location=candidates[0],

                message="Village matched."

            )

        if len(candidates) > 1:

            return RetrievalResult(

                resolved=False,

                needs_user_selection=True,

                candidates=candidates,

                message="More than one village has this name. Choose its district or subdistrict.",

                query=query

            )

        # ------------------------------------------
        # Best Fuzzy Match
        # ------------------------------------------

        best_match = self.tool.get_best_fuzzy_match(

            query,

            "village"

        )

        if best_match:

            candidates = self.tool.get_village_candidates(

                best_match.name,

                source="rapidfuzz",

                score=best_match.score

            )

            if len(candidates) > 1 and best_match.score >= SUGGESTION_THRESHOLD:

                return RetrievalResult(

                    resolved=False,

                    needs_user_selection=True,

                    candidates=candidates,

                    message=f"'{best_match.name}' matches multiple villages. Choose one.",

                    query=query

                )

            # Auto resolve only when the matched village is unambiguous.
            if best_match.score >= AUTO_RESOLVE_THRESHOLD and candidates:

                return RetrievalResult(

                    resolved=True,

                    location=candidates[0],

                    message="Resolved using fuzzy match."

                )

            # Ask for confirmation if confidence is moderate
            elif best_match.score >= SUGGESTION_THRESHOLD:

                return RetrievalResult(

                    resolved=False,

                    needs_user_selection=True,

                    candidates=candidates or [best_match],

                    message=f"Did you mean '{best_match.name}'?",

                    query=query

                )

        # ------------------------------------------
        # No Suitable Match
        # ------------------------------------------

        return RetrievalResult(

            resolved=False,

            message="Location not found.",

            query=query

        )
