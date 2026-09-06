from app.services.dataset_service import DatasetService

dataset = DatasetService()

print()

print(f"Villages      : {len(dataset.get_unique_villages())}")
print(f"Districts     : {len(dataset.get_unique_districts())}")
print(f"Subdistricts  : {len(dataset.get_unique_subdistricts())}")

print()

print(dataset.get_rows_by_district("Hyderabad").head())

from app.services.dataset_service import DatasetService

dataset = DatasetService()

rows = dataset.get_rows_by_village("pochampalli")

print(rows)
print("Count:", len(rows))