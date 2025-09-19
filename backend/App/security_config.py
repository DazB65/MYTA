"""
Security Configuration Module for Vidalytics
Handles secure loading of environment variables and security settings
"""

import os
import secrets
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class SecurityConfig:
    """Centralized security configuration management"""
    
    def __init__(self):
        self._load_environment()
        self._validate_security_settings()
    
    def _load_environment(self):
        """Securely load environment variables"""
        environment = os.getenv("ENVIRONMENT", "development")
        
        # Only load .env file in development
        if environment == "development":
            # Check for .env file in current directory first, then parent directory
            if os.path.exists(".env"):
                load_dotenv(".env")
                logger.info("Loaded environment variables from .env file (development mode)")
            elif os.path.exists("../.env"):
                load_dotenv("../.env")
                logger.info("Loaded environment variables from ../.env file (development mode)")
            else:
                logger.warning("No .env file found in development mode")
        else:
            logger.info(f"Running in {environment} mode - using system environment variables")
    
    def _validate_security_settings(self):
        """Validate critical security settings"""
        critical_vars = [
            "OPENAI_API_KEY",
            "YOUTUBE_API_KEY",
            "GOOGLE_CLIENT_ID",
            "GOOGLE_CLIENT_SECRET"
        ]

        missing_vars = []
        for var in critical_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            logger.error(f"Missing critical environment variables: {missing_vars}")

        # Validate JWT secret
        if not self.get_jwt_secret():
            logger.warning("JWT secret not set - generating temporary secret for development")

    def get_jwt_secret(self) -> str:
        """Get or generate JWT secret key"""
        jwt_secret = os.getenv('JWT_SECRET_KEY')
        if not jwt_secret:
            # Generate a secure random secret for development
            jwt_secret = secrets.token_urlsafe(32)
            logger.warning("Using generated JWT secret. Set JWT_SECRET_KEY environment variable for production.")
        return jwt_secret

    def get_password_requirements(self) -> Dict[str, Any]:
        """Get password security requirements"""
        return {
            'min_length': int(os.getenv('PASSWORD_MIN_LENGTH', '8')),
            'require_uppercase': os.getenv('PASSWORD_REQUIRE_UPPERCASE', 'true').lower() == 'true',
            'require_lowercase': os.getenv('PASSWORD_REQUIRE_LOWERCASE', 'true').lower() == 'true',
            'require_numbers': os.getenv('PASSWORD_REQUIRE_NUMBERS', 'true').lower() == 'true',
            'require_special_chars': os.getenv('PASSWORD_REQUIRE_SPECIAL_CHARS', 'true').lower() == 'true',
            'hash_rounds': int(os.getenv('PASSWORD_HASH_ROUNDS', '12'))
        }

    def get_rate_limits(self) -> Dict[str, int]:
        """Get rate limiting configuration"""
        return {
            'per_minute': int(os.getenv('RATE_LIMIT_PER_MINUTE', '60')),
            'per_hour': int(os.getenv('RATE_LIMIT_PER_HOUR', '1000')),
            'per_day': int(os.getenv('RATE_LIMIT_PER_DAY', '10000')),
            'auth_per_minute': int(os.getenv('AUTH_RATE_LIMIT_PER_MINUTE', '5'))
        }

    def get_session_config(self) -> Dict[str, Any]:
        """Get session configuration"""
        return {
            'timeout_hours': int(os.getenv('SESSION_TIMEOUT_HOURS', '8')),
            'absolute_timeout_hours': int(os.getenv('SESSION_ABSOLUTE_TIMEOUT_HOURS', '24')),
            'max_concurrent': int(os.getenv('MAX_CONCURRENT_SESSIONS', '5'))
        }

    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers configuration"""
        environment = os.getenv('ENVIRONMENT', 'development')
        is_production = environment == 'production'

        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "X-Permitted-Cross-Domain-Policies": "none",
            "Cross-Origin-Embedder-Policy": "require-corp",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Resource-Policy": "same-origin"
        }

        # Add HSTS only in production
        if is_production:
            hsts_max_age = int(os.getenv('HSTS_MAX_AGE', '31536000'))
            headers["Strict-Transport-Security"] = f"max-age={hsts_max_age}; includeSubDomains; preload"

        # Add CSP if enabled
        if os.getenv('ENABLE_CSP', 'true').lower() == 'true':
            headers["Content-Security-Policy"] = self._get_csp_header()

        return headers

    def _get_csp_header(self) -> str:
        """Generate Content Security Policy header"""
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "connect-src 'self'",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'",
            "upgrade-insecure-requests"
        ]

        return "; ".join(csp_directives)
        
        # Validate OAuth redirect URI
        redirect_uri = os.getenv("OAUTH_REDIRECT_URI")
        if redirect_uri and not redirect_uri.startswith(("http://localhost", "https://")):
            logger.warning("OAuth redirect URI should use HTTPS in production")
        
        # Validate secret keys
        self._validate_secret_keys()
    
    def _validate_secret_keys(self):
        """Validate that secret keys are properly set"""
        boss_secret = os.getenv("BOSS_AGENT_SECRET_KEY")
        session_secret = os.getenv("SESSION_SECRET_KEY")
        
        if not boss_secret or boss_secret == "generate_secure_random_key_here":
            logger.warning("BOSS_AGENT_SECRET_KEY not set or using default - generating temporary key")
            # Generate a secure random secret
            new_secret = secrets.token_urlsafe(64)
            os.environ["BOSS_AGENT_SECRET_KEY"] = new_secret
            logger.warning("Generated temporary boss agent secret - set BOSS_AGENT_SECRET_KEY for persistence")
        
        if not session_secret or session_secret == "generate_secure_random_key_here":
            logger.warning("SESSION_SECRET_KEY not set or using default - generating temporary key")
            # Generate a secure random secret
            new_secret = secrets.token_urlsafe(64)
            os.environ["SESSION_SECRET_KEY"] = new_secret
            logger.warning("Generated temporary session secret - set SESSION_SECRET_KEY for persistence")
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Securely retrieve API keys"""
        key_mapping = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY", 
            "google": "GOOGLE_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "youtube": "YOUTUBE_API_KEY"
        }
        
        env_var = key_mapping.get(service.lower())
        if not env_var:
            logger.error(f"Unknown service: {service}")
            return None
        
        api_key = os.getenv(env_var)
        if not api_key:
            logger.error(f"API key not found for service: {service}")
            return None
        
        # Validate key format (basic check)
        if len(api_key) < 10:
            logger.error(f"Invalid API key format for service: {service}")
            return None
        
        return api_key
    
    def get_oauth_config(self) -> Dict[str, str]:
        """Get OAuth configuration"""
        return {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": os.getenv("OAUTH_REDIRECT_URI")
        }
    
    def get_boss_agent_secret(self) -> str:
        """Get or generate boss agent secret"""
        secret = os.getenv("BOSS_AGENT_SECRET_KEY")
        if not secret or secret == "generate_secure_random_key_here":
            # Generate a secure random secret
            secret = secrets.token_urlsafe(64)
            logger.warning("Generated temporary boss agent secret - set BOSS_AGENT_SECRET_KEY for persistence")
        return secret
    
    def get_session_secret(self) -> str:
        """Get or generate session secret"""
        secret = os.getenv("SESSION_SECRET_KEY")
        if not secret or secret == "generate_secure_random_key_here":
            # Generate a secure random secret
            secret = secrets.token_urlsafe(64)
            logger.warning("Generated temporary session secret - set SESSION_SECRET_KEY for persistence")
        return secret
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return os.getenv("ENVIRONMENT", "development").lower() == "production"
    
    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers for API responses"""
        
        # Build Content Security Policy
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline'",  # Allow inline scripts for React
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' https://yt3.googleusercontent.com https://*.googleusercontent.com https://i.ytimg.com data:",
            "media-src 'self' https://*.googlevideo.com",
            "connect-src 'self' https://api.openai.com https://generativelanguage.googleapis.com https://oauth2.googleapis.com https://www.googleapis.com",
            "frame-src 'none'",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "upgrade-insecure-requests" if self.is_production() else ""
        ]
        
        # Filter out empty directives
        csp = "; ".join(filter(None, csp_directives))
        
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Content-Security-Policy": csp,
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
            "Cross-Origin-Embedder-Policy": "require-corp",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Resource-Policy": "same-origin"
        }
        
        # Add HSTS only in production
        if self.is_production():
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        
        return headers

# Global security config instance
_security_config: Optional[SecurityConfig] = None

def get_security_config() -> SecurityConfig:
    """Get or create global security config instance"""
    global _security_config
    if _security_config is None:
        _security_config = SecurityConfig()
    return _security_config

def get_api_key(service: str) -> Optional[str]:
    """Convenience function to get API keys"""
    return get_security_config().get_api_key(service)

def get_oauth_config() -> Dict[str, str]:
    """Convenience function to get OAuth config"""
    return get_security_config().get_oauth_config()

def get_boss_agent_secret() -> str:
    """Convenience function to get boss agent secret"""
    return get_security_config().get_boss_agent_secret()

def get_session_secret() -> str:
    """Convenience function to get session secret"""
    return get_security_config().get_session_secret()