"""
Configuration settings for FastAPI backend
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== SERVER CONFIG ====================
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("RELOAD", "True") == "True"

# ==================== FRONTEND CONFIG ====================
# CORS origins - allow frontend to call backend
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# ==================== FILE CONFIG ====================
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {".csv", ".xlsx"}

# Create upload directory if not exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==================== MODEL CONFIG ====================
MODEL_SAVE_DIR = "models"
os.makedirs(MODEL_SAVE_DIR, exist_ok=True)

# ==================== DATA PROCESSING CONFIG ====================
TEST_SIZE = 0.2
RANDOM_STATE = 42

# ==================== BUSINESS CONFIG ====================
MARGIN = 10  # Profit per conversion
COST_EMAIL = 1  # Cost per email

# ==================== LOGGING ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
