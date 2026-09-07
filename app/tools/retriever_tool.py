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

        # -------------------------------
        # Prefer the headquarters/town
        # with the same name as district
        # -------------------------------

        if source == "district":

            name = representative["district"]

            headquarters = rows[
                rows["village"].str.lower()
                == name.lower()
            ]

            if not headquarters.empty:

                row = headquarters.iloc[0]

                return self._row_to_location(
                    row,
                    source="district_hq",
                    score=98.0
                )

        # -------------------------------
        # Prefer town matching subdistrict
        # -------------------------------

        elif source == "subdistrict":

            name = representative["subdistric"]

            headquarters = rows[
                rows["village"].str.lower()
                == name.lower()
            ]

            if not headquarters.empty:

                row = headquarters.iloc[0]

                return self._row_to_location(
                    row,
                    source="subdistrict_hq",
                    score=96.0
                )

        else:
            name = representative["village"]

        # -------------------------------
        # Fallback to centroid only when
        # no headquarters exists
        # -------------------------------

        return Location(

            name=name,

            district=representative["district"],

            subdistrict=representative["subdistric"],

            latitude=rows["latitude"].mean(),

            longitude=rows["longitude"].mean(),

            confidence=90.0,

            score=90.0,

            source=f"{source}_centroid"

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
    # Best RapidFuzz Match
    # ==========================================

    def get_best_fuzzy_match(
        self,
        query: str,
        column: str
    ):

        values = (

            self.df[column]

            .dropna()

            .unique()

            .tolist()

        )

        match = process.extractOne(

            query,

            values,

            scorer=fuzz.WRatio

        )

        if match is None:
            return None

        value, score, _ = match

        rows = self.df[
            self.df[column] == value
        ]

        if rows.empty:
            return None

        row = rows.iloc[0]

        return self._row_to_location(

            row,

            source="rapidfuzz",

            score=score

        )

    def get_village_candidates(
        self,
        village_name: str,
        source: str = "village",
        score: float = 100.0,
        limit: int = 10
    ):
        """Return distinct places for a name instead of silently choosing row 0."""
        rows = self.dataset.get_rows_by_village(village_name)
        candidates = []
        seen = set()

        for _, row in rows.iterrows():
            identity = (
                row["village"], row["district"], row["subdistric"],
                row["latitude"], row["longitude"]
            )
            if identity in seen:
                continue
            seen.add(identity)
            candidates.append(self._row_to_location(row, source=source, score=score))
            if len(candidates) == limit:
                break

        return candidates
