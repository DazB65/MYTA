# Shim module to maintain test import compatibility
# Re-exports the FastAPI app from backend.App.main as `app`

from backend.App.main import app  # noqa: F401

