# Make backend a package and export selected helpers used by modules/tests
from App.agent_cache import get_agent_cache  # noqa: F401
from model_integrations_shim import migrate_openai_call_to_integration  # noqa: F401
from App.agent_model_adapter import get_agent_model_adapter  # noqa: F401

