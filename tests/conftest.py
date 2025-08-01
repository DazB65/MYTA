"""
Global pytest configuration and fixtures for Vidalytics testing
"""
import asyncio
import os
import sys
import tempfile
import pytest
import secrets
from pathlib import Path
from typing import AsyncGenerator, Generator
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from config import Settings, Environment
from main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Test configuration settings"""
    return Settings(
        environment=Environment.TESTING,
        debug=True,
        database_url="sqlite:///:memory:",
        openai_api_key="test-openai-key",
        google_api_key="test-google-key", 
        youtube_api_key="test-youtube-key",
        boss_agent_secret_key=secrets.token_urlsafe(32),
        session_secret_key=secrets.token_urlsafe(16),
        cors_origins=["http://localhost:3000"],
        enable_analytics=False,
        enable_oauth=False,
    )


@pytest.fixture(scope="function")
def temp_db():
    """Create a temporary database for testing"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_file.close()
    yield temp_file.name
    os.unlink(temp_file.name)


@pytest.fixture(scope="function")
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        "ENVIRONMENT": "testing",
        "OPENAI_API_KEY": "test-openai-key",
        "GOOGLE_API_KEY": "test-google-key",
        "YOUTUBE_API_KEY": "test-youtube-key",
        "BOSS_AGENT_SECRET_KEY": secrets.token_urlsafe(32),
        "SESSION_SECRET_KEY": secrets.token_urlsafe(16),
    }):
        yield


@pytest.fixture(scope="function")
def test_client(test_settings: Settings, mock_env_vars) -> Generator[TestClient, None, None]:
    """FastAPI test client"""
    with patch("config.get_settings", return_value=test_settings):
        with TestClient(app) as client:
            yield client


@pytest.fixture(scope="function")
async def async_client(test_settings: Settings, mock_env_vars) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for testing"""
    with patch("config.get_settings", return_value=test_settings):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client


@pytest.fixture(scope="function")
def mock_openai():
    """Mock OpenAI API responses"""
    with patch("openai.OpenAI") as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        
        # Mock completion response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test AI response"))]
        mock_response.usage = Mock(
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150
        )
        mock_client.chat.completions.create.return_value = mock_response
        
        yield mock_client


@pytest.fixture(scope="function")
def mock_google_ai():
    """Mock Google Generative AI responses"""
    with patch("google.generativeai.configure") as mock_configure, \
         patch("google.generativeai.GenerativeModel") as mock_model:
        
        mock_instance = Mock()
        mock_response = Mock()
        mock_response.text = "Test Google AI response"
        mock_response.usage_metadata = Mock(
            prompt_token_count=80,
            candidates_token_count=40,
            total_token_count=120
        )
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance
        
        yield mock_instance


@pytest.fixture(scope="function")
def mock_youtube_api():
    """Mock YouTube Data API responses"""
    with patch("googleapiclient.discovery.build") as mock_build:
        mock_youtube = Mock()
        
        # Mock channel data
        mock_youtube.channels().list().execute.return_value = {
            "items": [{
                "id": "test-channel-id",
                "snippet": {
                    "title": "Test Channel",
                    "description": "Test Description"
                },
                "statistics": {
                    "subscriberCount": "1000",
                    "viewCount": "50000",
                    "videoCount": "100"
                }
            }]
        }
        
        # Mock video data
        mock_youtube.videos().list().execute.return_value = {
            "items": [{
                "id": "test-video-id",
                "snippet": {
                    "title": "Test Video",
                    "description": "Test Video Description",
                    "publishedAt": "2024-01-01T00:00:00Z"
                },
                "statistics": {
                    "viewCount": "1000",
                    "likeCount": "100",
                    "commentCount": "10"
                }
            }]
        }
        
        mock_build.return_value = mock_youtube
        yield mock_youtube


@pytest.fixture(scope="function")
def mock_database():
    """Mock database operations"""
    with patch("sqlalchemy.create_engine") as mock_engine, \
         patch("sqlalchemy.orm.sessionmaker") as mock_sessionmaker:
        
        mock_session = Mock()
        mock_sessionmaker.return_value.return_value = mock_session
        
        # Mock common database operations
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.close.return_value = None
        
        yield mock_session


@pytest.fixture(scope="function")
def sample_user_data():
    """Sample user data for testing"""
    return {
        "user_id": "test-user-123",
        "channel_name": "Test Channel",
        "channel_id": "test-channel-id",
        "subscriber_count": 1000,
        "total_views": 50000,
        "video_count": 100,
        "niche": "Technology",
        "goals": ["Growth", "Monetization"],
        "content_type": "Educational"
    }


@pytest.fixture(scope="function")
def sample_video_data():
    """Sample video data for testing"""
    return {
        "video_id": "test-video-123",
        "title": "Test Video Title",
        "description": "Test video description",
        "view_count": 1000,
        "like_count": 100,
        "comment_count": 10,
        "published_at": "2024-01-01T00:00:00Z",
        "duration": "PT10M30S",
        "tags": ["test", "video", "example"]
    }


@pytest.fixture(scope="function") 
def mock_boss_agent_token():
    """Generate a mock boss agent JWT token"""
    return secrets.token_urlsafe(32)


@pytest.fixture(scope="function")
def agent_test_context():
    """Shared context for agent testing"""
    return {
        "request_id": str(secrets.token_hex(16)),
        "channel_id": "test-channel-id", 
        "time_period": "last_30d",
        "analysis_depth": "standard",
        "token_budget": {
            "input_tokens": 3000,
            "output_tokens": 1500
        }
    }


# Test markers for organized test execution
pytest_plugins = ["pytest_asyncio"]


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual components"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests between components"
    )
    config.addinivalue_line(
        "markers", "e2e: End-to-end tests of complete workflows"
    )
    config.addinivalue_line(
        "markers", "security: Security-focused tests"
    )
    config.addinivalue_line(
        "markers", "performance: Performance and load tests"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to run"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Auto-mark tests based on file path
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "security" in str(item.fspath):
            item.add_marker(pytest.mark.security)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)