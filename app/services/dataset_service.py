import pandas as pd

from app.config.settings import DATASET_PATH


class DatasetService:

    _instance = None
    _dataframe = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if self.__class__._dataframe is None:

            print("Loading dataset...")

            self.__class__._dataframe = pd.read_csv(
                DATASET_PATH
            )

    @property
    def dataframe(self):
        return self.__class__._dataframe

    def get_dataframe(self):
        return self.__class__._dataframe

    def get_unique_villages(self):
        return (
            self.__class__._dataframe["village"]
            .dropna()
            .unique()
            .tolist()
        )

    def get_unique_districts(self):
        return (
            self.__class__._dataframe["district"]
            .dropna()
            .unique()
            .tolist()
        )

    def get_unique_subdistricts(self):
        return (
            self.__class__._dataframe["subdistric"]
            .dropna()
            .unique()
            .tolist()
        )

    def get_rows_by_village(self, village_name: str):
        return self.__class__._dataframe[
            self.__class__._dataframe["village"].str.lower()
            == village_name.lower()
        ]

    def get_rows_by_district(self, district_name: str):
        return self.__class__._dataframe[
            self.__class__._dataframe["district"].str.lower()
            == district_name.lower()
        ]

    def get_rows_by_subdistrict(self, subdistrict_name: str):
        return self.__class__._dataframe[
            self.__class__._dataframe["subdistric"].str.lower()
            == subdistrict_name.lower()
        ]