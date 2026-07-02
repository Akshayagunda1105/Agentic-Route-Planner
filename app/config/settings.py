import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==============================
# Gemini Configuration
# ==============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

# ==============================
# Dataset
# ==============================

DATASET_PATH = "data/telangana_villages.csv"

# ==============================
# Output
# ==============================

OUTPUT_FOLDER = "output"

MAP_FILE = f"{OUTPUT_FOLDER}/route_map.html"

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)