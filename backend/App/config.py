"""
Enhanced Configuration Management for Vidalytics
Handles environment-specific settings with validation and type safety
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class Environment(str, Enum):
    """Application environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class LogLevel(str, Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Settings(BaseSettings):
    """Application settings with environment-specific configuration"""
    
    # Core Application Settings
    app_name: str = Field(default="Vidalytics", description="Application name")
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Application environment")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8888, description="Server port")
    frontend_url: str = Field(default="http://localhost:3000", description="Frontend URL")
    backend_url: str = Field(default="http://localhost:8888", description="Backend URL")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///./Vidalytics.db", description="Database URL")
    database_echo: bool = Field(default=False, description="Echo SQL queries")
    
    # Security Configuration
    cors_origins: Union[str, List[str]] = Field(default_factory=lambda: [], description="CORS allowed origins")
    security_headers_strict: bool = Field(default=True, description="Strict security headers")
    csrf_protection_strict: bool = Field(default=True, description="Strict CSRF protection")

    @property
    def allowed_origins(self) -> List[str]:
        """Get environment-specific CORS origins"""
        if self.environment == "production":
            # Production origins - replace with your actual domain
            production_origins = os.getenv("CORS_ORIGINS", "").split(",")
            return [origin.strip() for origin in production_origins if origin.strip()]
        elif self.environment == "development":
            # Development origins
            return [
                "http://localhost:3000",
                "http://localhost:3001",  # Added for Nuxt dev server
                "http://localhost:5173",
                "http://localhost:8080",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",  # Added for Nuxt dev server
                "http://127.0.0.1:5173"
            ]
        else:
            # Testing or other environments
            return ["http://localhost:3000"]
    
    # API Keys (loaded from secrets)
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key") 
    google_api_key: Optional[str] = Field(default=None, description="Google API key")
    youtube_api_key: Optional[str] = Field(default=None, description="YouTube API key")
    
    # OAuth Configuration
    google_client_id: Optional[str] = Field(default=None, description="Google OAuth client ID")
    google_client_secret: Optional[str] = Field(default=None, description="Google OAuth client secret")
    oauth_redirect_uri: str = Field(default="http://localhost:8888/auth/google/callback", description="OAuth redirect URI")
    
    # Security Keys
    boss_agent_secret_key: Optional[str] = Field(default=None, description="Boss agent secret key")
    session_secret_key: Optional[str] = Field(default=None, description="Session secret key")

    # Dashboard Authentication
    dashboard_password_hash: Optional[str] = Field(default=None, description="Dashboard password hash (SHA-256)")
    dashboard_jwt_secret: Optional[str] = Field(default=None, description="Dashboard JWT secret key")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, description="Rate limit per minute")
    rate_limit_burst: int = Field(default=10, description="Rate limit burst")
    
    # Session Configuration
    session_timeout_hours: int = Field(default=8, description="Session timeout in hours")
    jwt_expiry_hours: int = Field(default=4, description="JWT expiry in hours")
    
    # Cache Configuration
    cache_ttl_hours: int = Field(default=2, description="Cache TTL in hours")
    enable_cache: bool = Field(default=True, description="Enable caching")
    
    # External Service URLs
    openai_api_base_url: str = Field(default="https://api.openai.com/v1", description="OpenAI API base URL")
    google_api_base_url: str = Field(default="https://generativelanguage.googleapis.com", description="Google API base URL")
    youtube_api_base_url: str = Field(default="https://www.googleapis.com/youtube/v3", description="YouTube API base URL")
    
    # Feature Flags
    enable_analytics: bool = Field(default=True, description="Enable analytics")
    enable_oauth: bool = Field(default=True, description="Enable OAuth")
    enable_multi_agent: bool = Field(default=True, description="Enable multi-agent system")
    enable_content_studio: bool = Field(default=True, description="Enable content studio")
    
    # Backup Configuration
    backup_enabled: bool = Field(default=True, description="Enable automatic backups")
    backup_frequency: str = Field(default="daily", description="Backup frequency (hourly, daily, weekly, monthly)")
    backup_time: str = Field(default="02:00", description="Backup time (HH:MM for daily/weekly/monthly, MM for hourly)")
    backup_compression: bool = Field(default=True, description="Enable backup compression")
    backup_max_count: int = Field(default=7, description="Maximum number of backups to retain")
    backup_cleanup_enabled: bool = Field(default=True, description="Enable automatic cleanup of old backups")
    backup_directory: str = Field(default="./backups", description="Directory for storing backups")
    
    # Backup Alert Configuration
    backup_email_alerts: bool = Field(default=False, description="Enable email alerts for backups")
    backup_email_recipients: str = Field(default="", description="Comma-separated list of email recipients")
    backup_webhook_url: Optional[str] = Field(default=None, description="Webhook URL for backup alerts")
    backup_alert_on_failure: bool = Field(default=True, description="Send alerts on backup failures")
    backup_alert_on_success: bool = Field(default=False, description="Send alerts on backup success")
    backup_alert_on_cleanup: bool = Field(default=False, description="Send alerts on backup cleanup")
    
    class Config:
        env_file_encoding = 'utf-8'
        case_sensitive = False
        validate_assignment = True
        use_enum_values = True
        
    @field_validator('cors_origins', mode='before')
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(',')]
        return v

    @field_validator('environment', mode='before')
    def validate_environment(cls, v):
        """Validate environment value"""
        if isinstance(v, str):
            return v.lower()
        return v
    
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment == Environment.DEVELOPMENT
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == Environment.PRODUCTION
    
    def is_staging(self) -> bool:
        """Check if running in staging"""
        return self.environment == Environment.STAGING
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            "url": self.database_url,
            "echo": self.database_echo,
        }
    
    def get_cors_config(self) -> Dict[str, Any]:
        """Get environment-specific CORS configuration"""
        origins = self.allowed_origins

        # More restrictive headers for production
        allowed_headers = [
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-CSRF-Token"
        ] if self.is_production() else ["*"]

        return {
            "allow_origins": origins,
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": allowed_headers,
            "expose_headers": ["X-Total-Count", "X-Rate-Limit-Remaining"],
            "max_age": 86400 if self.is_production() else 3600  # Cache preflight for 24h in prod, 1h in dev
        }
    
    def get_rate_limit_config(self) -> Dict[str, Any]:
        """Get rate limiting configuration"""
        return {
            "per_minute": self.rate_limit_per_minute,
            "burst": self.rate_limit_burst,
        }
    
    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers configuration"""
        csp_directives = [
            "default-src 'self'",
            "script-src 'self'" if self.is_production() else "script-src 'self' 'unsafe-inline'",
            ("style-src 'self' https://fonts.googleapis.com" if self.is_production() else "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com"),
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' https://yt3.googleusercontent.com https://*.googleusercontent.com https://i.ytimg.com data:",
            "media-src 'self' https://*.googlevideo.com",
            "connect-src 'self' https://api.openai.com https://generativelanguage.googleapis.com https://oauth2.googleapis.com https://www.googleapis.com",
            "frame-src 'none'",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]

        if self.is_production():
            csp_directives.append("upgrade-insecure-requests")

        csp = "; ".join(filter(None, csp_directives))

        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Content-Security-Policy": csp,
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
        }
        
        if self.security_headers_strict:
            headers.update({
                "Cross-Origin-Embedder-Policy": "require-corp",
                "Cross-Origin-Opener-Policy": "same-origin",
                "Cross-Origin-Resource-Policy": "same-origin"
            })
        
        if self.is_production():
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        
        return headers
    
    def get_backup_config(self) -> Dict[str, Any]:
        """Get backup configuration"""
        from backup_service import BackupFrequency, BackupSchedule, BackupAlert
        
        # Parse frequency
        frequency_map = {
            "hourly": BackupFrequency.HOURLY,
            "daily": BackupFrequency.DAILY,
            "weekly": BackupFrequency.WEEKLY,
            "monthly": BackupFrequency.MONTHLY
        }
        frequency = frequency_map.get(self.backup_frequency.lower(), BackupFrequency.DAILY)
        
        # Parse email recipients
        email_recipients = []
        if self.backup_email_recipients:
            email_recipients = [email.strip() for email in self.backup_email_recipients.split(',') if email.strip()]
        
        return {
            "schedule": BackupSchedule(
                frequency=frequency,
                time=self.backup_time,
                enabled=self.backup_enabled,
                compression=self.backup_compression,
                max_backups=self.backup_max_count,
                cleanup_enabled=self.backup_cleanup_enabled
            ),
            "alerts": BackupAlert(
                email_enabled=self.backup_email_alerts,
                email_recipients=email_recipients,
                webhook_url=self.backup_webhook_url,
                alert_on_failure=self.backup_alert_on_failure,
                alert_on_success=self.backup_alert_on_success,
                alert_on_cleanup=self.backup_alert_on_cleanup
            ),
            "directory": self.backup_directory
        }

def load_environment_config(env: str = None) -> Settings:
    """Load configuration for specific environment"""
    
    # Determine environment
    if not env:
        env = os.getenv("ENVIRONMENT", "development").lower()
    
    # Load base environment file
    env_file = f".env.{env}"
    if os.path.exists(env_file):
        load_dotenv(env_file)
        logger.info(f"Loaded environment config from {env_file}")

    # Load secrets from .env.local (never commit this)
    secrets_file = ".env.local"
    if os.path.exists(secrets_file):
        load_dotenv(secrets_file, override=True)
        logger.info("Loaded secrets from .env.local")

    # Load from .env as fallback
    if os.path.exists(".env"):
        load_dotenv(".env", override=False)
        logger.info("Loaded fallback config from .env")

    # Create settings instance
    settings = Settings()
    
    # Validate required settings
    validate_required_settings(settings)
    
    return settings

def validate_required_settings(settings: Settings):
    """Validate required settings are present"""
    required_for_production = [
        'openai_api_key',
        'google_api_key', 
        'youtube_api_key',
        'boss_agent_secret_key'
    ]
    
    if settings.is_production():
        missing = []
        for key in required_for_production:
            if not getattr(settings, key):
                missing.append(key.upper())
        
        if missing:
            raise ValueError(f"Missing required production settings: {', '.join(missing)}")
    
    logger.info(f"Configuration loaded for {settings.environment} environment")

def create_env_template():
    """Create .env.local template for secrets"""
    template_content = """# Local Environment Secrets (NEVER COMMIT THIS FILE)
# Copy from .env.example and fill in your actual values

# =================================================================
# CRITICAL: ADD THIS FILE TO .gitignore IMMEDIATELY
# =================================================================

# AI Service API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here

# OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Security Keys (generate with: python -c "import secrets; print(secrets.token_urlsafe(64))")
BOSS_AGENT_SECRET_KEY=your_boss_agent_secret_key_here
SESSION_SECRET_KEY=your_session_secret_key_here
"""
    
    if not os.path.exists(".env.local"):
        with open(".env.local", "w") as f:
            f.write(template_content)
        logger.info("Created .env.local template - please fill in your secrets")
    else:
        logger.info(".env.local already exists")

# Global settings instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get global settings instance by delegating to backend.config shim for test patchability"""
    try:
        # Importing here to allow tests to patch backend.config.load_environment_config and _settings
        from backend import config as config_shim  # type: ignore
        if getattr(config_shim, "_settings", None) is None:
            config_shim._settings = config_shim.load_environment_config()
        return config_shim._settings
    except Exception:
        pass
    # Fallback to module-level singleton
    global _settings
    if _settings is None:
        _settings = load_environment_config()
    return _settings

# Backward compatibility
def get_security_config():
    """Backward compatibility with existing security_config.py"""
    return get_settings()

if __name__ == "__main__":
    # Test configuration loading
    settings = load_environment_config()
    print(f"Environment: {settings.environment}")
    print(f"Debug: {settings.debug}")
    print(f"Database: {settings.database_url}")
    print(f"CORS Origins: {settings.cors_origins}")