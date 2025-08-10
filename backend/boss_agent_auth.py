# Shim providing expected functions for tests and re-exports
from backend.App.boss_agent_auth import *  # noqa: F401,F403
from backend.App.boss_agent_auth import SpecializedAgentAuthMixin  # noqa: F401
from backend.boss_agent_auth_shim_impl import validate_specialized_agent_request  # noqa: F401


def get_boss_agent_authenticator():  # noqa: D401
    """Return a simple authenticator instance compatible with current architecture."""
    return SpecializedAgentAuthMixin()
