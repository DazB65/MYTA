"""
Unit tests for Redis Session Manager
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch
import redis

from backend.redis_session_manager import (
    RedisSessionManager,
    SessionData,
    SessionStatus,
    RedisSessionConfig,
    get_session_manager
)


class TestSessionData:
    """Test SessionData dataclass"""
    
    def test_session_data_creation(self):
        """Test creating SessionData instance"""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=8)
        
        session = SessionData(
            session_id="test_session_123",
            user_id="test_user",
            created_at=now,
            last_accessed=now,
            expires_at=expires,
            status=SessionStatus.ACTIVE,
            ip_address="127.0.0.1",
            user_agent="test-agent",
            permissions=["user", "read"],
            metadata={"test": "data"}
        )
        
        assert session.session_id == "test_session_123"
        assert session.user_id == "test_user"
        assert session.status == SessionStatus.ACTIVE
        assert session.permissions == ["user", "read"]
        assert session.metadata == {"test": "data"}
    
    def test_session_data_defaults(self):
        """Test SessionData with default values"""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=8)
        
        session = SessionData(
            session_id="test_session_123",
            user_id="test_user",
            created_at=now,
            last_accessed=now,
            expires_at=expires,
            status=SessionStatus.ACTIVE
        )
        
        assert session.permissions == []
        assert session.metadata == {}
        assert session.ip_address is None
    
    def test_is_expired(self):
        """Test session expiry check"""
        now = datetime.now(timezone.utc)
        
        # Expired session
        expired_session = SessionData(
            session_id="expired",
            user_id="test_user",
            created_at=now - timedelta(hours=10),
            last_accessed=now - timedelta(hours=2),
            expires_at=now - timedelta(hours=1),
            status=SessionStatus.ACTIVE
        )
        
        assert expired_session.is_expired() is True
        
        # Active session
        active_session = SessionData(
            session_id="active",
            user_id="test_user",
            created_at=now,
            last_accessed=now,
            expires_at=now + timedelta(hours=8),
            status=SessionStatus.ACTIVE
        )
        
        assert active_session.is_expired() is False
    
    def test_is_valid(self):
        """Test session validity check"""
        now = datetime.now(timezone.utc)
        
        # Valid session
        valid_session = SessionData(
            session_id="valid",
            user_id="test_user",
            created_at=now,
            last_accessed=now,
            expires_at=now + timedelta(hours=8),
            status=SessionStatus.ACTIVE
        )
        
        assert valid_session.is_valid() is True
        
        # Revoked session
        revoked_session = SessionData(
            session_id="revoked",
            user_id="test_user",
            created_at=now,
            last_accessed=now,
            expires_at=now + timedelta(hours=8),
            status=SessionStatus.REVOKED
        )
        
        assert revoked_session.is_valid() is False
        
        # Expired session
        expired_session = SessionData(
            session_id="expired",
            user_id="test_user",
            created_at=now - timedelta(hours=10),
            last_accessed=now - timedelta(hours=2),
            expires_at=now - timedelta(hours=1),
            status=SessionStatus.ACTIVE
        )
        
        assert expired_session.is_valid() is False
    
    def test_to_dict(self):
        """Test converting SessionData to dictionary"""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=8)
        
        session = SessionData(
            session_id="test_session_123",
            user_id="test_user",
            created_at=now,
            last_accessed=now,
            expires_at=expires,
            status=SessionStatus.ACTIVE,
            ip_address="127.0.0.1",
            permissions=["user"],
            metadata={"test": "data"}
        )
        
        session_dict = session.to_dict()
        
        assert session_dict["session_id"] == "test_session_123"
        assert session_dict["user_id"] == "test_user"
        assert session_dict["status"] == "active"
        assert isinstance(session_dict["created_at"], str)
        assert session_dict["permissions"] == ["user"]
        assert session_dict["metadata"] == {"test": "data"}
    
    def test_from_dict(self):
        """Test creating SessionData from dictionary"""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=8)
        
        session_dict = {
            "session_id": "test_session_123",
            "user_id": "test_user",
            "created_at": now.isoformat(),
            "last_accessed": now.isoformat(),
            "expires_at": expires.isoformat(),
            "status": "active",
            "ip_address": "127.0.0.1",
            "user_agent": "test-agent",
            "permissions": ["user"],
            "metadata": {"test": "data"}
        }
        
        session = SessionData.from_dict(session_dict)
        
        assert session.session_id == "test_session_123"
        assert session.user_id == "test_user"
        assert session.status == SessionStatus.ACTIVE
        assert isinstance(session.created_at, datetime)
        assert session.permissions == ["user"]


class TestRedisSessionConfig:
    """Test Redis session configuration"""
    
    def test_config_creation(self):
        """Test creating session configuration"""
        config = RedisSessionConfig()
        
        assert config.session_timeout == timedelta(hours=8)
        assert config.refresh_threshold == timedelta(hours=1)
        assert config.max_sessions_per_user == 10
        assert config.key_prefix == "creatormate:session:"
        assert config.user_sessions_prefix == "creatormate:user_sessions:"
    
    def test_config_with_settings(self):
        """Test configuration with custom settings"""
        mock_settings = MagicMock()
        mock_settings.is_development.return_value = False
        
        config = RedisSessionConfig(mock_settings)
        
        assert config.secure_cookies is True
        assert config.httponly_cookies is True
        assert config.samesite_policy == "strict"


@pytest.fixture
def mock_redis():
    """Mock Redis client"""
    redis_mock = MagicMock(spec=redis.Redis)
    redis_mock.ping.return_value = True
    redis_mock.get.return_value = None
    redis_mock.set.return_value = True
    redis_mock.setex.return_value = True
    redis_mock.delete.return_value = 1
    redis_mock.sadd.return_value = 1
    redis_mock.srem.return_value = 1
    redis_mock.smembers.return_value = set()
    redis_mock.expire.return_value = True
    redis_mock.keys.return_value = []
    redis_mock.hgetall.return_value = {}
    redis_mock.hincrby.return_value = 1
    redis_mock.info.return_value = {
        'redis_version': '6.0.0',
        'connected_clients': 1,
        'used_memory_human': '1M',
        'uptime_in_seconds': 3600
    }
    redis_mock.connection_pool.connection_kwargs = {'host': 'localhost', 'port': 6379}
    
    return redis_mock


class TestRedisSessionManager:
    """Test Redis Session Manager"""
    
    @pytest.fixture
    def session_manager(self, mock_redis):
        """Create session manager with mocked Redis"""
        with patch('backend.redis_session_manager.get_settings') as mock_settings:
            mock_settings.return_value.is_development.return_value = True
            return RedisSessionManager(redis_client=mock_redis)
    
    def test_session_manager_initialization(self, mock_redis):
        """Test session manager initialization"""
        with patch('backend.redis_session_manager.get_settings') as mock_settings:
            mock_settings.return_value.is_development.return_value = True
            
            manager = RedisSessionManager(redis_client=mock_redis)
            
            assert manager.redis is mock_redis
            assert manager.config is not None
            mock_redis.ping.assert_called_once()
    
    def test_generate_session_id(self, session_manager):
        """Test session ID generation"""
        session_id = session_manager._generate_session_id()
        
        assert isinstance(session_id, str)
        assert len(session_id) == 64  # SHA256 hex string length
    
    def test_get_session_key(self, session_manager):
        """Test session key generation"""
        key = session_manager._get_session_key("test_session_123")
        assert key == "creatormate:session:test_session_123"
    
    def test_get_user_sessions_key(self, session_manager):
        """Test user sessions key generation"""
        key = session_manager._get_user_sessions_key("test_user")
        assert key == "creatormate:user_sessions:test_user"
    
    @pytest.mark.asyncio
    async def test_create_session(self, session_manager, mock_redis):
        """Test creating a new session"""
        # Mock Redis operations
        mock_redis.setex.return_value = True
        mock_redis.sadd.return_value = 1
        mock_redis.expire.return_value = True
        
        session_data = await session_manager.create_session(
            user_id="test_user",
            ip_address="127.0.0.1",
            user_agent="test-agent",
            permissions=["user", "read"],
            metadata={"test": "data"}
        )
        
        assert session_data.user_id == "test_user"
        assert session_data.ip_address == "127.0.0.1"
        assert session_data.user_agent == "test-agent"
        assert session_data.permissions == ["user", "read"]
        assert session_data.metadata == {"test": "data"}
        assert session_data.status == SessionStatus.ACTIVE
        
        # Verify Redis calls
        mock_redis.setex.assert_called_once()
        mock_redis.sadd.assert_called_once()
        mock_redis.expire.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_session_not_found(self, session_manager, mock_redis):
        """Test getting non-existent session"""
        mock_redis.get.return_value = None
        
        session_data = await session_manager.get_session("non_existent_session")
        
        assert session_data is None
        mock_redis.get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_session_found(self, session_manager, mock_redis):
        """Test getting existing session"""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=8)
        
        session_dict = {
            "session_id": "test_session_123",
            "user_id": "test_user",
            "created_at": now.isoformat(),
            "last_accessed": (now - timedelta(minutes=30)).isoformat(),
            "expires_at": expires.isoformat(),
            "status": "active",
            "ip_address": "127.0.0.1",
            "user_agent": "test-agent",
            "permissions": ["user"],
            "metadata": {"test": "data"}
        }
        
        mock_redis.get.return_value = json.dumps(session_dict)
        mock_redis.set.return_value = True
        
        session_data = await session_manager.get_session("test_session_123")
        
        assert session_data is not None
        assert session_data.session_id == "test_session_123"
        assert session_data.user_id == "test_user"
        assert session_data.status == SessionStatus.ACTIVE
        
        # Verify last_accessed was updated
        assert session_data.last_accessed > datetime.fromisoformat(session_dict["last_accessed"])
        
        mock_redis.get.assert_called_once()
        mock_redis.set.assert_called_once()  # Update last_accessed
    
    @pytest.mark.asyncio
    async def test_get_session_expired(self, session_manager, mock_redis):
        """Test getting expired session"""
        now = datetime.now(timezone.utc)
        expired_time = now - timedelta(hours=1)
        
        session_dict = {
            "session_id": "expired_session",
            "user_id": "test_user",
            "created_at": (now - timedelta(hours=10)).isoformat(),
            "last_accessed": (now - timedelta(hours=2)).isoformat(),
            "expires_at": expired_time.isoformat(),
            "status": "active",
            "ip_address": "127.0.0.1",
            "user_agent": "test-agent",
            "permissions": ["user"],
            "metadata": {}
        }
        
        mock_redis.get.return_value = json.dumps(session_dict)
        mock_redis.delete.return_value = 1
        mock_redis.srem.return_value = 1
        
        session_data = await session_manager.get_session("expired_session")
        
        assert session_data is None
        
        # Verify expired session was removed
        mock_redis.delete.assert_called_once()
        mock_redis.srem.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_session(self, session_manager, mock_redis):
        """Test updating session data"""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=8)
        
        session_dict = {
            "session_id": "test_session_123",
            "user_id": "test_user",
            "created_at": now.isoformat(),
            "last_accessed": now.isoformat(),
            "expires_at": expires.isoformat(),
            "status": "active",
            "ip_address": "127.0.0.1",
            "user_agent": "test-agent",
            "permissions": ["user"],
            "metadata": {"old": "data"}
        }
        
        mock_redis.get.return_value = json.dumps(session_dict)
        mock_redis.set.return_value = True
        
        success = await session_manager.update_session(
            "test_session_123",
            metadata={"new": "data", "updated": True},
            permissions=["user", "admin"]
        )
        
        assert success is True
        
        # Verify Redis was called to update session
        assert mock_redis.set.call_count == 2  # get_session + update_session
    
    @pytest.mark.asyncio
    async def test_revoke_session(self, session_manager, mock_redis):
        """Test revoking a session"""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=8)
        
        session_dict = {
            "session_id": "test_session_123",
            "user_id": "test_user",
            "created_at": now.isoformat(),
            "last_accessed": now.isoformat(),
            "expires_at": expires.isoformat(),
            "status": "active",
            "ip_address": "127.0.0.1",
            "user_agent": "test-agent",
            "permissions": ["user"],
            "metadata": {}
        }
        
        mock_redis.get.return_value = json.dumps(session_dict)
        mock_redis.set.return_value = True
        mock_redis.delete.return_value = 1
        mock_redis.srem.return_value = 1
        
        success = await session_manager.revoke_session("test_session_123")
        
        assert success is True
        
        # Verify session was removed from Redis
        mock_redis.delete.assert_called()
        mock_redis.srem.assert_called()
    
    @pytest.mark.asyncio
    async def test_revoke_all_user_sessions(self, session_manager, mock_redis):
        """Test revoking all sessions for a user"""
        # Mock user sessions
        mock_redis.smembers.return_value = {"session1", "session2", "session3"}
        
        # Mock get_session calls for each session
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=8)
        
        session_dict = {
            "session_id": "session1",
            "user_id": "test_user",
            "created_at": now.isoformat(),
            "last_accessed": now.isoformat(),
            "expires_at": expires.isoformat(),
            "status": "active",
            "ip_address": "127.0.0.1",
            "user_agent": "test-agent",
            "permissions": ["user"],
            "metadata": {}
        }
        
        mock_redis.get.return_value = json.dumps(session_dict)
        mock_redis.set.return_value = True
        mock_redis.delete.return_value = 1
        mock_redis.srem.return_value = 1
        
        revoked_count = await session_manager.revoke_all_user_sessions(
            "test_user",
            except_session_id="session2"
        )
        
        assert revoked_count == 2  # Should revoke session1 and session3, but not session2
        
        # Verify Redis operations
        mock_redis.smembers.assert_called_once()
        assert mock_redis.delete.call_count >= 2  # At least 2 sessions deleted
    
    @pytest.mark.asyncio
    async def test_get_user_sessions(self, session_manager, mock_redis):
        """Test getting all sessions for a user"""
        # Mock user sessions
        mock_redis.smembers.return_value = {"session1", "session2"}
        
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=8)
        
        session_dict = {
            "session_id": "session1",
            "user_id": "test_user",
            "created_at": now.isoformat(),
            "last_accessed": now.isoformat(),
            "expires_at": expires.isoformat(),
            "status": "active",
            "ip_address": "127.0.0.1",
            "user_agent": "test-agent",
            "permissions": ["user"],
            "metadata": {}
        }
        
        mock_redis.get.return_value = json.dumps(session_dict)
        mock_redis.set.return_value = True
        
        sessions = await session_manager.get_user_sessions("test_user")
        
        assert len(sessions) == 2
        assert all(isinstance(session, SessionData) for session in sessions)
        assert all(session.user_id == "test_user" for session in sessions)
    
    @pytest.mark.asyncio
    async def test_get_session_stats(self, session_manager, mock_redis):
        """Test getting session statistics"""
        # Mock Redis stats data
        mock_redis.hgetall.return_value = {
            "2024-01-01:created": "10",
            "2024-01-01:revoked": "2",
            "2024-01-02:created": "15",
            "2024-01-02:revoked": "3"
        }
        
        mock_redis.keys.return_value = ["session1", "session2", "session3"]
        
        stats = await session_manager.get_session_stats()
        
        assert "daily_stats" in stats
        assert "total_active_sessions" in stats
        assert "redis_info" in stats
        
        assert stats["total_active_sessions"] == 3
        assert "2024-01-01" in stats["daily_stats"]
        assert stats["daily_stats"]["2024-01-01"]["created"] == 10
    
    @pytest.mark.asyncio
    async def test_health_check(self, session_manager, mock_redis):
        """Test session system health check"""
        health_data = await session_manager.health_check()
        
        assert "status" in health_data
        assert "response_time_ms" in health_data
        assert "redis_version" in health_data
        assert "total_active_sessions" in health_data
        
        # Verify Redis operations were called
        mock_redis.set.assert_called()
        mock_redis.get.assert_called()
        mock_redis.delete.assert_called()
        mock_redis.info.assert_called()


class TestGlobalSessionManager:
    """Test global session manager function"""
    
    def test_get_session_manager_singleton(self):
        """Test that get_session_manager returns singleton"""
        with patch('backend.redis_session_manager.RedisSessionManager') as MockManager:
            mock_instance = MagicMock()
            MockManager.return_value = mock_instance
            
            # Clear any existing global instance
            import backend.redis_session_manager
            backend.redis_session_manager._session_manager = None
            
            manager1 = get_session_manager()
            manager2 = get_session_manager()
            
            assert manager1 is manager2
            MockManager.assert_called_once()


@pytest.mark.asyncio
async def test_cleanup_expired_sessions():
    """Test cleanup expired sessions function"""
    with patch('backend.redis_session_manager.get_session_manager') as mock_get_manager:
        mock_manager = AsyncMock()
        mock_manager.get_session_stats.return_value = {"total_active_sessions": 5}
        mock_manager.logger = MagicMock()
        mock_get_manager.return_value = mock_manager
        
        from backend.redis_session_manager import cleanup_expired_sessions
        await cleanup_expired_sessions()
        
        mock_manager.get_session_stats.assert_called_once()
        mock_manager.logger.info.assert_called_once()