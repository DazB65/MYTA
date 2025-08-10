"""
Compatibility layer providing get_boss_agent_authenticator expected by routers/tests
"""
from typing import Any
from backend.App.security_config import get_boss_agent_secret

class _SimpleBossAgentAuthenticator:
    def generate_boss_agent_token(self) -> str:
        return get_boss_agent_secret()


def get_boss_agent_authenticator() -> Any:
    return _SimpleBossAgentAuthenticator()

