# Shim exposing get_agent_cache for legacy import path `backend.backups`
from backend.App.agent_cache import get_agent_cache  # noqa: F401

