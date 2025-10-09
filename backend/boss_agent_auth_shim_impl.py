# Provide legacy functions expected by agent_router and tests
from dataclasses import dataclass
from typing import Optional
from App.security_config import get_boss_agent_secret

@dataclass
class AuthResult:
    is_valid: bool
    error_message: Optional[str] = None


def validate_specialized_agent_request(request: dict) -> AuthResult:
    """Validate a simple token-based request from boss agent.
    Accepts either boss_agent_secret in body or bearer token under boss_agent_token.
    """
    secret = get_boss_agent_secret()
    token = request.get("boss_agent_secret") or request.get("boss_agent_token")
    if not token:
        return AuthResult(False, "Missing boss agent token")
    if token != secret:
        return AuthResult(False, "Invalid boss agent token")
    return AuthResult(True)

