"""
Startup Validator — FastAPI Application Entry Point.

AI-Powered Startup Validation Platform that uses multiple specialized
AI agents to analyze startup ideas and generate comprehensive reports.
"""

import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from config import APP_TITLE, APP_VERSION, APP_DESCRIPTION
from routes.validation import router as validation_router

# ── Logging setup ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
    datefmt="%H:%M:%S",
)

# ── FastAPI app ───────────────────────────────────────────
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
)

# ── CORS (allow frontend access during development) ──────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register API routers ──────────────────────────────────
app.include_router(validation_router)

# ── Serve static frontend ─────────────────────────────────
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

@app.get("/")
def serve_frontend():
    """Serve the main frontend UI."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# Mount remaining static assets (CSS, JS, images if any)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ── API info endpoint ─────────────────────────────────────
@app.get("/api")
def api_info():
    """API information and available endpoints."""
    return {
        "application": APP_TITLE,
        "version": APP_VERSION,
        "docs": "/docs",
        "endpoints": {
            "full_validation": "POST /api/v1/validate",
            "market_analysis": "POST /api/v1/analyze/market",
            "competitor_analysis": "POST /api/v1/analyze/competitor",
            "risk_analysis": "POST /api/v1/analyze/risk",
            "investor_analysis": "POST /api/v1/analyze/investor",
            "health": "GET /api/v1/health",
        },
    }


# ── Run with: uvicorn app:app --reload ───────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)