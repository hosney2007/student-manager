import sys
import os

# make the project root importable (app.py, models/, routes/, etc. live there)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app  # noqa: E402

# Vercel's Python runtime looks for a WSGI-compatible "app" object
