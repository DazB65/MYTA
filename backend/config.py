# Shim module to maintain test import compatibility
# Re-exports Settings and helpers from App.config and dotenv loaders for tests

from App.config import (
    Settings,
    Environment,
    get_settings,
    load_environment_config,
    validate_required_settings,
)
from dotenv import load_dotenv  # re-export for patching in tests

# expose independent _settings for patching in tests
_settings = None  # will be set by get_settings()