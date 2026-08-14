"""
Central configuration for the Startup Validator platform.
Loads environment variables and provides app-wide settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Gemini API ──────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# ── Retry Settings ──────────────────────────────────────────
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY_SECONDS", "3"))

# ── Application Settings ────────────────────────────────────
APP_TITLE = "AI-Powered Startup Validation Platform"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "A multi-agent AI system that validates startup ideas by analyzing "
    "market potential, competition, risks, and investment attractiveness."
)
