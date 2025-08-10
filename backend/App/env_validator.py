"""
Environment Variable Validator for Vidalytics
Ensures all required environment variables are set and valid
"""

import os
import sys
import re
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging
import secrets

logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Validation severity levels"""
    CRITICAL = "critical"  # App cannot start without these
    WARNING = "warning"    # App can start but functionality limited
    INFO = "info"          # Optional but recommended


class EnvValidator:
    """Validates environment variables at application startup"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        
        # Define required variables and their validation rules
        self.validations = {
            # Critical security keys
            "BOSS_AGENT_SECRET_KEY": {
                "level": ValidationLevel.CRITICAL,
                "validator": self._validate_secret_key,
                "description": "Boss agent secret key for JWT signing"
            },
            "SESSION_SECRET_KEY": {
                "level": ValidationLevel.CRITICAL,
                "validator": self._validate_secret_key,
                "description": "Session secret key for session encryption"
            },
            
            # API Keys (Warning level - app can start but features limited)
            "OPENAI_API_KEY": {
                "level": ValidationLevel.WARNING,
                "validator": self._validate_api_key,
                "description": "OpenAI API key for AI services"
            },
            "ANTHROPIC_API_KEY": {
                "level": ValidationLevel.WARNING,
                "validator": self._validate_api_key,
                "description": "Anthropic API key for Claude AI services"
            },
            "GOOGLE_API_KEY": {
                "level": ValidationLevel.WARNING,
                "validator": self._validate_api_key,
                "description": "Google API key for various Google services"
            },
            "YOUTUBE_API_KEY": {
                "level": ValidationLevel.WARNING,
                "validator": self._validate_api_key,
                "description": "YouTube Data API v3 key"
            },
            
            # OAuth Configuration
            "GOOGLE_CLIENT_ID": {
                "level": ValidationLevel.WARNING,
                "validator": self._validate_oauth_client_id,
                "description": "Google OAuth client ID"
            },
            "GOOGLE_CLIENT_SECRET": {
                "level": ValidationLevel.WARNING,
                "validator": self._validate_oauth_secret,
                "description": "Google OAuth client secret"
            },
            
            # Server Configuration
            "HOST": {
                "level": ValidationLevel.INFO,
                "validator": self._validate_host,
                "description": "Server host (use 127.0.0.1 for security)"
            },
            "PORT": {
                "level": ValidationLevel.INFO,
                "validator": self._validate_port,
                "description": "Server port"
            },
            
            # Database
            "DATABASE_URL": {
                "level": ValidationLevel.CRITICAL,
                "validator": self._validate_database_url,
                "description": "Database connection URL"
            },
            
            # Environment
            "ENVIRONMENT": {
                "level": ValidationLevel.INFO,
                "validator": self._validate_environment,
                "description": "Application environment (development/staging/production)"
            }
        }
    
    def validate(self) -> Tuple[bool, Dict[str, List[str]]]:
        """
        Validate all environment variables
        Returns: (is_valid, issues_dict)
        """
        
        for var_name, config in self.validations.items():
            value = os.getenv(var_name)
            level = config["level"]
            validator = config["validator"]
            description = config["description"]
            
            # Check if variable exists
            if not value:
                if level == ValidationLevel.CRITICAL:
                    self.errors.append(f"Missing critical variable: {var_name} - {description}")
                elif level == ValidationLevel.WARNING:
                    self.warnings.append(f"Missing variable: {var_name} - {description}")
                else:
                    self.info.append(f"Optional variable not set: {var_name} - {description}")
                continue
            
            # Validate the value
            is_valid, message = validator(value, var_name)
            if not is_valid:
                if level == ValidationLevel.CRITICAL:
                    self.errors.append(f"{var_name}: {message}")
                elif level == ValidationLevel.WARNING:
                    self.warnings.append(f"{var_name}: {message}")
                else:
                    self.info.append(f"{var_name}: {message}")
        
        # Check for insecure values
        self._check_security_issues()
        
        # Determine if app can start
        can_start = len(self.errors) == 0
        
        return can_start, {
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info
        }
    
    def _validate_secret_key(self, value: str, var_name: str) -> Tuple[bool, str]:
        """Validate secret keys are secure"""
        
        # Check minimum length (32 characters)
        if len(value) < 32:
            return False, "Secret key too short (minimum 32 characters)"
        
        # Check for placeholder values
        placeholders = [
            "your_", "change_", "replace_", "example", "default",
            "secret", "key", "123", "abc", "xxx", "placeholder"
        ]
        value_lower = value.lower()
        for placeholder in placeholders:
            if placeholder in value_lower:
                return False, f"Secret key contains placeholder text '{placeholder}'"
        
        # Check for sufficient entropy (basic check)
        if len(set(value)) < 10:
            return False, "Secret key has insufficient entropy (too few unique characters)"
        
        return True, "Valid secret key"
    
    def _validate_api_key(self, value: str, var_name: str) -> Tuple[bool, str]:
        """Validate API keys"""
        
        # Check for placeholder values
        if value.startswith("your_") or value.startswith("sk-"):
            if "xxx" in value.lower() or "your_" in value.lower():
                return False, "API key appears to be a placeholder"
        
        # Basic format validation
        if len(value) < 20:
            return False, "API key seems too short"
        
        return True, "Valid API key format"
    
    def _validate_oauth_client_id(self, value: str, var_name: str) -> Tuple[bool, str]:
        """Validate OAuth client ID"""
        
        if value.startswith("your_") or value == "your_google_client_id_here":
            return False, "OAuth client ID is a placeholder"
        
        # Google OAuth client IDs typically end with .apps.googleusercontent.com
        if "GOOGLE" in var_name and not value.endswith(".apps.googleusercontent.com"):
            return False, "Invalid Google OAuth client ID format"
        
        return True, "Valid OAuth client ID"
    
    def _validate_oauth_secret(self, value: str, var_name: str) -> Tuple[bool, str]:
        """Validate OAuth client secret"""
        
        if value.startswith("your_") or value == "your_google_client_secret_here":
            return False, "OAuth client secret is a placeholder"
        
        if len(value) < 20:
            return False, "OAuth client secret seems too short"
        
        return True, "Valid OAuth client secret"
    
    def _validate_host(self, value: str, var_name: str) -> Tuple[bool, str]:
        """Validate host configuration"""
        
        # Security warning for 0.0.0.0
        if value == "0.0.0.0":
            return False, "Host set to 0.0.0.0 (binds to all interfaces) - use 127.0.0.1 for security"
        
        # Validate IP format or hostname
        ip_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        if ip_pattern.match(value):
            parts = value.split(".")
            if all(0 <= int(part) <= 255 for part in parts):
                return True, "Valid IP address"
            return False, "Invalid IP address"
        
        # Basic hostname validation
        if re.match(r"^[a-zA-Z0-9.-]+$", value):
            return True, "Valid hostname"
        
        return False, "Invalid host format"
    
    def _validate_port(self, value: str, var_name: str) -> Tuple[bool, str]:
        """Validate port number"""
        
        try:
            port = int(value)
            if 1 <= port <= 65535:
                if port < 1024:
                    return True, "Using privileged port (< 1024)"
                return True, "Valid port number"
            return False, "Port must be between 1 and 65535"
        except ValueError:
            return False, "Port must be a number"
    
    def _validate_database_url(self, value: str, var_name: str) -> Tuple[bool, str]:
        """Validate database URL"""
        
        # Check for supported database schemes
        valid_schemes = ["sqlite", "postgresql", "mysql", "mariadb"]
        
        if not any(value.startswith(f"{scheme}://") for scheme in valid_schemes):
            return False, "Invalid database URL scheme"
        
        # Warning for SQLite in production
        if value.startswith("sqlite://") and os.getenv("ENVIRONMENT") == "production":
            return True, "Warning: Using SQLite in production is not recommended"
        
        return True, "Valid database URL"
    
    def _validate_environment(self, value: str, var_name: str) -> Tuple[bool, str]:
        """Validate environment setting"""
        
        valid_environments = ["development", "staging", "production", "test"]
        
        if value.lower() not in valid_environments:
            return False, f"Invalid environment. Must be one of: {', '.join(valid_environments)}"
        
        return True, f"Environment: {value}"
    
    def _check_security_issues(self):
        """Check for common security issues"""
        
        # Check if debug is enabled in production
        if os.getenv("ENVIRONMENT") == "production" and os.getenv("DEBUG", "").lower() == "true":
            self.errors.append("DEBUG mode is enabled in production!")
        
        # Check if using default secret keys
        boss_key = os.getenv("BOSS_AGENT_SECRET_KEY", "")
        session_key = os.getenv("SESSION_SECRET_KEY", "")
        
        if boss_key == session_key and boss_key:
            self.warnings.append("BOSS_AGENT_SECRET_KEY and SESSION_SECRET_KEY are identical - use different keys")
        
        # Check CORS origins in production
        if os.getenv("ENVIRONMENT") == "production":
            cors_origins = os.getenv("CORS_ORIGINS", "")
            if "localhost" in cors_origins or "127.0.0.1" in cors_origins:
                self.warnings.append("CORS_ORIGINS contains localhost in production")
    
    def print_validation_report(self, issues: Dict[str, List[str]]):
        """Print a formatted validation report"""
        
        print("\n" + "="*60)
        print("ENVIRONMENT VARIABLE VALIDATION REPORT")
        print("="*60)
        
        if issues["errors"]:
            print("\n❌ CRITICAL ERRORS (Application cannot start):")
            for error in issues["errors"]:
                print(f"  • {error}")
        
        if issues["warnings"]:
            print("\n⚠️  WARNINGS (Limited functionality):")
            for warning in issues["warnings"]:
                print(f"  • {warning}")
        
        if issues["info"]:
            print("\nℹ️  INFO (Optional configurations):")
            for info in issues["info"]:
                print(f"  • {info}")
        
        if not any(issues.values()):
            print("\n✅ All environment variables are properly configured!")
        
        print("\n" + "="*60)
    
    def generate_secure_key(self) -> str:
        """Generate a secure random key"""
        return secrets.token_urlsafe(64)
    
    def suggest_fixes(self):
        """Suggest fixes for common issues"""
        
        print("\n📝 SUGGESTED FIXES:")
        print("-" * 40)
        
        # Check for missing secret keys
        if not os.getenv("BOSS_AGENT_SECRET_KEY") or not os.getenv("SESSION_SECRET_KEY"):
            print("\nGenerate secure secret keys:")
            print("  python -c \"import secrets; print('BOSS_AGENT_SECRET_KEY=' + secrets.token_urlsafe(64))\"")
            print("  python -c \"import secrets; print('SESSION_SECRET_KEY=' + secrets.token_urlsafe(64))\"")
        
        # Check for missing .env file
        if not os.path.exists(".env"):
            print("\nCreate .env file from template:")
            print("  cp .env.example .env")
            print("  # Then edit .env with your actual values")
        
        print("\n" + "="*60)


def validate_environment():
    """Main validation function to be called at startup"""
    
    validator = EnvValidator()
    can_start, issues = validator.validate()
    
    # Print validation report
    validator.print_validation_report(issues)
    
    # Suggest fixes if there are issues
    if issues["errors"] or issues["warnings"]:
        validator.suggest_fixes()
    
    # Exit if critical errors
    if not can_start:
        logger.critical("Environment validation failed. Please fix the errors above.")
        sys.exit(1)
    
    # Log warnings
    if issues["warnings"]:
        logger.warning(f"Environment validation warnings: {len(issues['warnings'])} issues found")
    
    logger.info("Environment validation completed successfully")
    return True


if __name__ == "__main__":
    # Run validation when script is executed directly
    validate_environment()