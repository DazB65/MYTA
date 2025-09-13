"""
Compatibility layer providing get_boss_agent_authenticator expected by routers/tests
"""
from typing import Any, NamedTuple
from .security_config import get_boss_agent_secret

class ValidationResult(NamedTuple):
    is_valid: bool
    message: str = ""

class _SimpleBossAgentAuthenticator:
    def generate_boss_agent_token(self, request_id: str = "") -> str:
        return get_boss_agent_secret()

    def validate_boss_agent_token(self, token: str, request_id: str = "") -> ValidationResult:
        secret = get_boss_agent_secret()
        is_valid = token == secret
        return ValidationResult(is_valid=is_valid, message="Valid" if is_valid else "Invalid token")


def get_boss_agent_authenticator() -> Any:
    return _SimpleBossAgentAuthenticator()

