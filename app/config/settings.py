import os
from pathlib import Path
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

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "telangana_villages.csv"

# ==============================
# Output
# ==============================

OUTPUT_FOLDER = PROJECT_ROOT / "output"

MAP_FILE = OUTPUT_FOLDER / "route_map.html"

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)
