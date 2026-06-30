from app.utils.confidence import (
    AUTO_RESOLVE_THRESHOLD,
    SHOW_CANDIDATES_THRESHOLD,
    MINIMUM_ACCEPTABLE_SCORE,
    MIN_SCORE_DIFFERENCE
)


class DecisionMaker:

    @staticmethod
    def evaluate(candidates):

        if len(candidates) == 0:

            return "NO_MATCH"

        best = candidates[0]

        if best.score < MINIMUM_ACCEPTABLE_SCORE:

            return "NO_MATCH"

        if len(candidates) == 1:

            return "AUTO"

        second = candidates[1]

        difference = best.score - second.score

        if (

            best.score >= AUTO_RESOLVE_THRESHOLD

            and

            difference >= MIN_SCORE_DIFFERENCE

        ):

            return "AUTO"

        if best.score >= SHOW_CANDIDATES_THRESHOLD:

            return "SHOW"

        return "NO_MATCH"