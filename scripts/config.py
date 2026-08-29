import os

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# ==========================================
# Database
# ==========================================

DATABASE_PATH = "data/ecommerce.db"


# ==========================================
# Gemini
# ==========================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = "gemini-3.6-flash"


# ==========================================
# Application
# ==========================================

APP_NAME = "AI TEXT → SQL SYSTEM"