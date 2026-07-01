from rapidfuzz import process, fuzz

from app.services.dataset_service import DatasetService
from app.models.location import Location


class RetrieverTool:

    def __init__(self):

        self.dataset = DatasetService()
        self.df = self.dataset.get_dataframe()

    # ==========================================
    # Convert Single Row -> Location
    # ==========================================

    def _row_to_location(
        self,
        row,
        source="exact",
        score=100.0
    ):

        return Location(

            name=row["village"],

            district=row["district"],

            subdistrict=row["subdistric"],

            latitude=row["latitude"],

            longitude=row["longitude"],

            confidence=score,

            score=score,

            source=source
        )

    # ==========================================
    # Build Representative Location
    # ==========================================

    def _build_representative_location(
        self,
        rows,
        source: str
    ):

        if rows.empty:
            return None

        representative = rows.iloc[0]

        if source == "district":

            name = representative["district"]

        elif source == "subdistrict":

            name = representative["subdistric"]

        else:

            name = representative["village"]

        return Location(

            name=name,

            district=representative["district"],

            subdistrict=representative["subdistric"],

            latitude=rows["latitude"].mean(),

            longitude=rows["longitude"].mean(),

            confidence=95.0 if source == "district" else 93.0,

            score=95.0 if source == "district" else 93.0,

            source=source
        )

    # ==========================================
    # Exact District Search
    # ==========================================

    def search_district(
        self,
        district_name: str
    ):

        rows = self.dataset.get_rows_by_district(
            district_name
        )

        if rows.empty:
            return None

        return self._build_representative_location(
            rows,
            "district"
        )

    # ==========================================
    # Exact Subdistrict Search
    # ==========================================

    def search_subdistrict(
        self,
        subdistrict_name: str
    ):

        rows = self.dataset.get_rows_by_subdistrict(
            subdistrict_name
        )

        if rows.empty:
            return None

        return self._build_representative_location(
            rows,
            "subdistrict"
        )

    # ==========================================
    # Exact Village Search
    # ==========================================

    def search_village(
        self,
        village_name: str
    ):

        rows = self.dataset.get_rows_by_village(
            village_name
        )

        if rows.empty:
            return None

        row = rows.iloc[0]

        return self._row_to_location(
            row,
            source="village",
            score=100.0
        )

    # ==========================================
    # Generic RapidFuzz Search
    # ==========================================

    def fuzzy_search(
        self,
        query: str,
        column: str,
        limit: int = 5
    ):

        values = (

            self.df[column]

            .dropna()

            .unique()

            .tolist()

        )

        matches = process.extract(

            query,

            values,

            scorer=fuzz.WRatio,

            limit=limit

        )

        return matches

    # ==========================================
    # Convert RapidFuzz Matches -> Location Objects
    # ==========================================

    def get_candidate_matches(
        self,
        query: str,
        column: str,
        limit: int = 5
    ):

        matches = self.fuzzy_search(
            query,
            column,
            limit
        )

        candidates = []

        for value, score, _ in matches:

            rows = self.df[
                self.df[column] == value
            ]

            if rows.empty:
                continue

            row = rows.iloc[0]

            location = self._row_to_location(

                row,

                source="rapidfuzz",

                score=score

            )

            candidates.append(location)

        return candidates