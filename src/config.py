import os
from pathlib import Path
from dotenv import load_dotenv

# Find project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Ingestion Database & CSV paths
DB_PATH_RAW = os.getenv("DATABASE_PATH", "data/database.db")
DB_PATH = PROJECT_ROOT / DB_PATH_RAW
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

CSV_PATH_RAW = os.getenv("CSV_PATH", "data/instamart_feedback_1000.csv")
CSV_PATH = PROJECT_ROOT / CSV_PATH_RAW
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

# Reddit credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "instamart-discovery-engine/0.1")

# Swiggy Instamart Product Categories
INSTAMART_CATEGORIES = [
    "Fruits & Vegetables",
    "Dairy, Bread & Eggs",
    "Snacks & Munchies",
    "Beverages",
    "Personal Care",
    "Cleaning & Household",
    "Baby Care",
    "Pet Care",
    "Meat & Fish",
    "Kitchen & Home Essentials",
    "Gourmet & Organic"
]

# Predefined user segments
USER_SEGMENTS = [
    "Routine Buyer",
    "Price-Sensitive Shopper",
    "Experiment Seeker",
    "Working Professional",
    "Student",
    "Family Planner",
    "Health-Conscious Buyer",
    "Pet Owner",
    "Baby Product Buyer"
]

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
IS_MOCK_LLM = not (GEMINI_API_KEY or OPENAI_API_KEY)

