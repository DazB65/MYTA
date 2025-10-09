# Shim module to maintain test import compatibility
# Re-exports the FastAPI app from App.main as `app`

from App.main import app  # noqa: F401

