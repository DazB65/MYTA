# Shim module to satisfy imports that expect `security_config` at backend level
# Re-export get_security_config and helpers from App.security_config

from App.security_config import (  # noqa: F401
    get_security_config,
    get_api_key,
    get_oauth_config,
    get_boss_agent_secret,
    get_session_secret,
    SecurityConfig,
)

