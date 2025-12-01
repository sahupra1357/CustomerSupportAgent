"""
Global configuration for the Customer Support Agent application.
This module should be imported before any other application modules.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash-lite")

# Database Configuration
DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///./db/adk_sessions.db")

# App Configuration
APP_NAME = "customer_support_app"

from google.genai import types
retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

DB_PATH = os.getenv("DB_PATH", "./db/customer_support.db")