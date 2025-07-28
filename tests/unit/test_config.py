"""
Unit tests for configuration management
"""
import os
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path

from config import Settings, Environment, load_environment_config, get_settings


class TestSettings:
    """Test Settings class functionality"""

    def test_default_settings(self):
        """Test default settings initialization"""
        settings = Settings()
        
        assert settings.app_name == "CreatorMate"
        assert settings.environment == Environment.DEVELOPMENT
        assert settings.debug is False
        assert settings.host == "0.0.0.0"
        assert settings.port == 8888
        assert settings.database_url == "sqlite:///./creatormate.db"

    def test_environment_methods(self):
        """Test environment checking methods"""
        dev_settings = Settings(environment=Environment.DEVELOPMENT)
        prod_settings = Settings(environment=Environment.PRODUCTION)
        staging_settings = Settings(environment=Environment.STAGING)
        
        assert dev_settings.is_development() is True
        assert dev_settings.is_production() is False
        assert dev_settings.is_staging() is False
        
        assert prod_settings.is_development() is False
        assert prod_settings.is_production() is True
        assert prod_settings.is_staging() is False
        
        assert staging_settings.is_development() is False
        assert staging_settings.is_production() is False
        assert staging_settings.is_staging() is True

    def test_cors_origins_parsing(self):
        """Test CORS origins parsing from different formats"""
        # Test list format
        settings = Settings(cors_origins=["http://localhost:3000", "https://example.com"])
        assert len(settings.cors_origins) == 2
        
        # Test JSON string format
        settings = Settings(cors_origins='["http://localhost:3000", "https://example.com"]')
        assert len(settings.cors_origins) == 2
        
        # Test comma-separated string format
        settings = Settings(cors_origins="http://localhost:3000,https://example.com")
        assert len(settings.cors_origins) == 2

    def test_database_config(self):
        """Test database configuration generation"""
        settings = Settings(
            database_url="postgresql://user:pass@localhost/db",
            database_echo=True
        )
        
        config = settings.get_database_config()
        assert config["url"] == "postgresql://user:pass@localhost/db"
        assert config["echo"] is True

    def test_cors_config(self):
        """Test CORS configuration generation"""
        settings = Settings(cors_origins=["http://localhost:3000"])
        
        config = settings.get_cors_config()
        assert config["allow_origins"] == ["http://localhost:3000"]
        assert config["allow_credentials"] is True
        assert "GET" in config["allow_methods"]
        assert "POST" in config["allow_methods"]

    def test_security_headers_development(self):
        """Test security headers for development environment"""
        settings = Settings(environment=Environment.DEVELOPMENT)
        headers = settings.get_security_headers()
        
        assert "Content-Security-Policy" in headers
        assert "X-Content-Type-Options" in headers
        assert "X-Frame-Options" in headers
        assert "'unsafe-inline'" in headers["Content-Security-Policy"]  # Allowed in dev
        assert "Strict-Transport-Security" not in headers  # Not in dev

    def test_security_headers_production(self):
        """Test security headers for production environment"""
        settings = Settings(environment=Environment.PRODUCTION)
        headers = settings.get_security_headers()
        
        assert "Content-Security-Policy" in headers
        assert "Strict-Transport-Security" in headers  # Required in production
        assert "'unsafe-inline'" not in headers["Content-Security-Policy"]  # Forbidden in prod
        assert "upgrade-insecure-requests" in headers["Content-Security-Policy"]

    def test_rate_limit_config(self):
        """Test rate limiting configuration"""
        settings = Settings(
            rate_limit_per_minute=120,
            rate_limit_burst=20
        )
        
        config = settings.get_rate_limit_config()
        assert config["per_minute"] == 120
        assert config["burst"] == 20


class TestLoadEnvironmentConfig:
    """Test environment configuration loading"""

    @patch("os.path.exists")
    @patch("config.load_dotenv")
    def test_load_development_config(self, mock_load_dotenv, mock_exists):
        """Test loading development configuration"""
        mock_exists.return_value = True
        
        with patch.dict(os.environ, {"ENVIRONMENT": "development"}):
            settings = load_environment_config()
        
        # Should load .env.development
        mock_load_dotenv.assert_any_call(".env.development")
        assert settings.environment == Environment.DEVELOPMENT

    @patch("os.path.exists")
    @patch("config.load_dotenv")  
    def test_load_production_config(self, mock_load_dotenv, mock_exists):
        """Test loading production configuration"""
        mock_exists.return_value = True
        
        with patch.dict(os.environ, {"ENVIRONMENT": "production"}):
            settings = load_environment_config()
        
        # Should load .env.production
        mock_load_dotenv.assert_any_call(".env.production")
        assert settings.environment == Environment.DEVELOPMENT  # Default fallback

    @patch("os.path.exists")
    @patch("config.load_dotenv")
    def test_load_secrets_file(self, mock_load_dotenv, mock_exists):
        """Test loading secrets from .env.local"""
        mock_exists.return_value = True
        
        load_environment_config()
        
        # Should load .env.local with override=True
        mock_load_dotenv.assert_any_call(".env.local", override=True)

    @patch("os.path.exists")
    @patch("config.load_dotenv")
    def test_fallback_env_file(self, mock_load_dotenv, mock_exists):
        """Test fallback to .env file"""
        mock_exists.return_value = True
        
        load_environment_config()
        
        # Should load .env as fallback with override=False
        mock_load_dotenv.assert_any_call(".env", override=False)

    def test_validate_required_settings_development(self):
        """Test validation passes for development environment"""
        settings = Settings(environment=Environment.DEVELOPMENT)
        
        # Should not raise exception for development
        from config import validate_required_settings
        validate_required_settings(settings)

    def test_validate_required_settings_production_missing(self):
        """Test validation fails for production with missing keys"""
        settings = Settings(
            environment=Environment.PRODUCTION,
            openai_api_key=None  # Missing required key
        )
        
        from config import validate_required_settings
        with pytest.raises(ValueError, match="Missing required production settings"):
            validate_required_settings(settings)

    def test_validate_required_settings_production_complete(self):
        """Test validation passes for production with all keys"""
        settings = Settings(
            environment=Environment.PRODUCTION,
            openai_api_key="test-key",
            google_api_key="test-key",
            youtube_api_key="test-key",
            boss_agent_secret_key="test-key"
        )
        
        from config import validate_required_settings
        validate_required_settings(settings)  # Should not raise


class TestGetSettings:
    """Test global settings instance management"""

    def test_singleton_behavior(self):
        """Test settings instance is singleton"""
        with patch("config.load_environment_config") as mock_load:
            mock_settings = Settings()
            mock_load.return_value = mock_settings
            
            # First call should load config
            settings1 = get_settings()
            mock_load.assert_called_once()
            
            # Second call should reuse instance
            settings2 = get_settings()
            mock_load.assert_called_once()  # Still only called once
            
            assert settings1 is settings2

    @patch("config._settings", None)  # Reset global instance
    def test_settings_loading(self):
        """Test settings are loaded correctly"""
        with patch("config.load_environment_config") as mock_load:
            mock_settings = Settings(app_name="TestApp")
            mock_load.return_value = mock_settings
            
            settings = get_settings()
            assert settings.app_name == "TestApp"
            mock_load.assert_called_once()


@pytest.mark.unit
class TestEnvironmentEnum:
    """Test Environment enum functionality"""

    def test_environment_values(self):
        """Test environment enum values"""
        assert Environment.DEVELOPMENT == "development"
        assert Environment.STAGING == "staging"
        assert Environment.PRODUCTION == "production"
        assert Environment.TESTING == "testing"

    def test_environment_case_insensitive(self):
        """Test environment validation is case insensitive"""
        settings = Settings(environment="DEVELOPMENT")
        assert settings.environment == "development"
        
        settings = Settings(environment="Production")
        assert settings.environment == "production"