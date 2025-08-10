# Make backend a package and export selected helpers used by modules/tests
from backend.App.agent_cache import get_agent_cache  # noqa: F401
from backend.model_integrations_shim import migrate_openai_call_to_integration  # noqa: F401
from backend.App.agent_model_adapter import get_agent_model_adapter  # noqa: F401

