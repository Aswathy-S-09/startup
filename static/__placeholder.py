"""
Static file serving for the frontend UI.
Serves the index.html and any other static assets.
"""

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
