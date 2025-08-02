"""
Integration tests for Redis session management
"""

import pytest
import asyncio
import redis
from datetime import timedelta
from fastapi.testclient import TestClient
from fastapi import FastAPI

from backend import RedisSessionManager, SessionData, SessionStatus
from backend import SessionMiddleware
from backend import router as session_router


@pytest.fixture
def redis_client():
    """Create Redis client for testing"""
    try:
        # Try to connect to Redis
        client = redis.Redis(
            host='localhost',
            port=6379,
            db=15,  # Use different DB for testing
            decode_responses=True,
            socket_timeout=5,
            socket_connect_timeout=5
        )
        
        # Test connection
        client.ping()
        
        # Clear test database
        client.flushdb()
        
        yield client
        
        # Cleanup after tests
        client.flushdb()
        client.close()
        
    except (redis.ConnectionError, redis.TimeoutError):
        pytest.skip("Redis not available for integration tests")


@pytest.fixture
def session_manager(redis_client):
    """Create session manager with real Redis"""
    return RedisSessionManager(redis_client=redis_client)


@pytest.fixture
def test_app():
    """Create test FastAPI application"""
    app = FastAPI()
    
    # Add session middleware
    app.add_middleware(SessionMiddleware)
    
    # Include session router
    app.include_router(session_router)
    
    return app


@pytest.fixture
def client(test_app):
    """Create test client"""
    return TestClient(test_app)


class TestRedisSessionIntegration:
    """Integration tests for Redis session management"""
    
    @pytest.mark.asyncio
    async def test_create_and_retrieve_session(self, session_manager):
        """Test creating and retrieving a session"""
        # Create session
        session_data = await session_manager.create_session(
            user_id="test_user",
            ip_address="127.0.0.1",
            user_agent="test-agent",
            permissions=["user", "read"],
            metadata={"test": "integration"}
        )
        
        assert session_data.user_id == "test_user"
        assert session_data.permissions == ["user", "read"]
        assert session_data.metadata == {"test": "integration"}
        
        # Retrieve session
        retrieved_session = await session_manager.get_session(session_data.session_id)
        
        assert retrieved_session is not None
        assert retrieved_session.session_id == session_data.session_id
        assert retrieved_session.user_id == "test_user"
        assert retrieved_session.permissions == ["user", "read"]
        assert retrieved_session.metadata == {"test": "integration"}
    
    @pytest.mark.asyncio
    async def test_session_expiry_and_cleanup(self, session_manager):
        """Test session expiry and automatic cleanup"""
        # Create session with short expiry
        short_expiry = timedelta(seconds=1)
        session_data = await session_manager.create_session(
            user_id="test_user",
            custom_expiry=short_expiry
        )
        
        # Verify session exists
        retrieved_session = await session_manager.get_session(session_data.session_id)
        assert retrieved_session is not None
        
        # Wait for expiry
        await asyncio.sleep(2)
        
        # Verify session is removed
        expired_session = await session_manager.get_session(session_data.session_id)
        assert expired_session is None
    
    @pytest.mark.asyncio
    async def test_session_refresh(self, session_manager):
        """Test automatic session refresh"""
        # Create session with short timeout and refresh threshold
        session_manager.config.session_timeout = timedelta(seconds=10)
        session_manager.config.refresh_threshold = timedelta(seconds=8)
        
        session_data = await session_manager.create_session(
            user_id="test_user",
            ip_address="127.0.0.1"
        )
        
        original_expires_at = session_data.expires_at
        
        # Wait until refresh threshold is reached
        await asyncio.sleep(3)
        
        # Get session again - should trigger refresh
        refreshed_session = await session_manager.get_session(session_data.session_id)
        
        assert refreshed_session is not None
        assert refreshed_session.expires_at > original_expires_at
    
    @pytest.mark.asyncio
    async def test_multiple_sessions_per_user(self, session_manager):
        """Test multiple sessions for same user"""
        user_id = "multi_session_user"
        
        # Create multiple sessions
        session1 = await session_manager.create_session(
            user_id=user_id,
            ip_address="127.0.0.1",
            metadata={"device": "desktop"}
        )
        
        session2 = await session_manager.create_session(
            user_id=user_id,
            ip_address="192.168.1.100",
            metadata={"device": "mobile"}
        )
        
        session3 = await session_manager.create_session(
            user_id=user_id,
            ip_address="10.0.0.1",
            metadata={"device": "tablet"}
        )
        
        # Get all user sessions
        user_sessions = await session_manager.get_user_sessions(user_id)
        
        assert len(user_sessions) == 3
        
        session_ids = {s.session_id for s in user_sessions}
        assert session1.session_id in session_ids
        assert session2.session_id in session_ids
        assert session3.session_id in session_ids
        
        # Verify different metadata
        devices = {s.metadata.get("device") for s in user_sessions}
        assert devices == {"desktop", "mobile", "tablet"}
    
    @pytest.mark.asyncio
    async def test_session_limit_enforcement(self, session_manager):
        """Test session limit enforcement"""
        user_id = "limited_user"
        
        # Set low session limit for testing
        session_manager.config.max_sessions_per_user = 3
        
        # Create more sessions than limit
        sessions = []
        for i in range(5):
            session = await session_manager.create_session(
                user_id=user_id,
                metadata={"session_number": i}
            )
            sessions.append(session)
        
        # Should only have 3 sessions (oldest ones removed)
        user_sessions = await session_manager.get_user_sessions(user_id)
        assert len(user_sessions) == 3
        
        # Should be the most recent sessions
        session_numbers = {s.metadata.get("session_number") for s in user_sessions}
        assert session_numbers == {2, 3, 4}
    
    @pytest.mark.asyncio
    async def test_revoke_operations(self, session_manager):
        """Test session revocation operations"""
        user_id = "revoke_test_user"
        
        # Create multiple sessions
        session1 = await session_manager.create_session(user_id=user_id, metadata={"name": "session1"})
        session2 = await session_manager.create_session(user_id=user_id, metadata={"name": "session2"})
        session3 = await session_manager.create_session(user_id=user_id, metadata={"name": "session3"})
        
        # Verify all sessions exist
        user_sessions = await session_manager.get_user_sessions(user_id)
        assert len(user_sessions) == 3
        
        # Revoke specific session
        revoke_success = await session_manager.revoke_session(session2.session_id)
        assert revoke_success is True
        
        # Verify session2 is removed
        remaining_sessions = await session_manager.get_user_sessions(user_id)
        assert len(remaining_sessions) == 2
        
        remaining_ids = {s.session_id for s in remaining_sessions}
        assert session2.session_id not in remaining_ids
        assert session1.session_id in remaining_ids
        assert session3.session_id in remaining_ids
        
        # Revoke all sessions except session3
        revoked_count = await session_manager.revoke_all_user_sessions(
            user_id,
            except_session_id=session3.session_id
        )
        assert revoked_count == 1  # Only session1 should be revoked
        
        # Verify only session3 remains
        final_sessions = await session_manager.get_user_sessions(user_id)
        assert len(final_sessions) == 1
        assert final_sessions[0].session_id == session3.session_id
    
    @pytest.mark.asyncio
    async def test_session_update(self, session_manager):
        """Test updating session data"""
        # Create session
        session_data = await session_manager.create_session(
            user_id="update_test_user",
            permissions=["user"],
            metadata={"initial": "value"}
        )
        
        # Update session
        update_success = await session_manager.update_session(
            session_data.session_id,
            metadata={"updated": "value", "new_field": "data"},
            permissions=["user", "admin"]
        )
        assert update_success is True
        
        # Retrieve updated session
        updated_session = await session_manager.get_session(session_data.session_id)
        
        assert updated_session is not None
        assert updated_session.permissions == ["user", "admin"]
        assert updated_session.metadata == {"updated": "value", "new_field": "data"}
    
    @pytest.mark.asyncio
    async def test_session_statistics(self, session_manager):
        """Test session statistics collection"""
        # Create some sessions
        for i in range(3):
            await session_manager.create_session(f"stats_user_{i}")
        
        # Revoke one session
        sessions = await session_manager.get_user_sessions("stats_user_1")
        if sessions:
            await session_manager.revoke_session(sessions[0].session_id)
        
        # Get statistics
        stats = await session_manager.get_session_stats()
        
        assert "daily_stats" in stats
        assert "total_active_sessions" in stats
        assert "redis_info" in stats
        
        assert stats["total_active_sessions"] >= 2  # At least 2 active sessions
        assert stats["redis_info"]["connected"] is True
    
    @pytest.mark.asyncio
    async def test_health_check(self, session_manager):
        """Test health check functionality"""
        health_data = await session_manager.health_check()
        
        assert health_data["status"] == "healthy"
        assert "response_time_ms" in health_data
        assert "redis_version" in health_data
        assert "connected_clients" in health_data
        assert "used_memory_human" in health_data
        assert "total_active_sessions" in health_data
        assert health_data["uptime_seconds"] > 0
    
    @pytest.mark.asyncio
    async def test_concurrent_session_operations(self, session_manager):
        """Test concurrent session operations"""
        user_id = "concurrent_user"
        
        # Create multiple sessions concurrently
        tasks = []
        for i in range(10):
            task = session_manager.create_session(
                user_id=user_id,
                metadata={"session_index": i}
            )
            tasks.append(task)
        
        sessions = await asyncio.gather(*tasks)
        
        # Verify all sessions were created
        assert len(sessions) == 10
        assert all(s.user_id == user_id for s in sessions)
        
        # Verify unique session IDs
        session_ids = {s.session_id for s in sessions}
        assert len(session_ids) == 10
        
        # Concurrently revoke half the sessions
        revoke_tasks = []
        for i in range(0, 10, 2):  # Every other session
            task = session_manager.revoke_session(sessions[i].session_id)
            revoke_tasks.append(task)
        
        revoke_results = await asyncio.gather(*revoke_tasks)
        assert all(result is True for result in revoke_results)
        
        # Verify remaining sessions
        remaining_sessions = await session_manager.get_user_sessions(user_id)
        # Should have 5 sessions remaining (accounting for session limit)
        assert len(remaining_sessions) <= 5


class TestSessionAPIIntegration:
    """Integration tests for session API endpoints"""
    
    def test_login_endpoint(self, client):
        """Test login endpoint"""
        response = client.post("/api/session/login", json={
            "user_id": "test_user",
            "password": "test_password",
            "remember_me": False,
            "metadata": {"device": "test"}
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "session_id" in data["data"]
        assert data["data"]["user_id"] == "test_user"
        
        # Verify session cookie is set
        assert "Vidalytics_session" in response.cookies
    
    def test_login_and_get_current_session(self, client):
        """Test login and get current session"""
        # Login first
        login_response = client.post("/api/session/login", json={
            "user_id": "current_session_test",
            "metadata": {"test": "current"}
        })
        
        assert login_response.status_code == 200
        session_cookie = login_response.cookies["Vidalytics_session"]
        
        # Get current session
        response = client.get(
            "/api/session/current",
            cookies={"Vidalytics_session": session_cookie}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["user_id"] == "current_session_test"
        assert data["data"]["metadata"]["test"] == "current"
    
    def test_session_without_auth(self, client):
        """Test accessing protected endpoint without authentication"""
        response = client.get("/api/session/current")
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "Authentication required" in data["detail"]
    
    def test_logout_endpoint(self, client):
        """Test logout endpoint"""
        # Login first
        login_response = client.post("/api/session/login", json={
            "user_id": "logout_test"
        })
        
        session_cookie = login_response.cookies["Vidalytics_session"]
        
        # Logout
        response = client.post(
            "/api/session/logout",
            cookies={"Vidalytics_session": session_cookie}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Verify session is invalid after logout
        current_response = client.get(
            "/api/session/current",
            cookies={"Vidalytics_session": session_cookie}
        )
        
        assert current_response.status_code == 401
    
    def test_list_user_sessions(self, client):
        """Test listing user sessions"""
        user_id = "list_sessions_test"
        
        # Create multiple sessions by logging in from different "devices"
        sessions = []
        for device in ["desktop", "mobile", "tablet"]:
            response = client.post("/api/session/login", json={
                "user_id": user_id,
                "metadata": {"device": device}
            })
            assert response.status_code == 200
            sessions.append(response.cookies["Vidalytics_session"])
        
        # List sessions using the last session
        response = client.get(
            "/api/session/list",
            cookies={"Vidalytics_session": sessions[-1]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["total_count"] >= 3
        
        # Verify all sessions belong to the same user
        for session in data["data"]["sessions"]:
            assert session["user_id"] == user_id
    
    def test_revoke_specific_session(self, client):
        """Test revoking a specific session"""
        user_id = "revoke_specific_test"
        
        # Create two sessions
        session1_response = client.post("/api/session/login", json={
            "user_id": user_id,
            "metadata": {"name": "session1"}
        })
        session1_cookie = session1_response.cookies["Vidalytics_session"]
        session1_id = session1_response.json()["data"]["session_id"]
        
        session2_response = client.post("/api/session/login", json={
            "user_id": user_id,
            "metadata": {"name": "session2"}
        })
        session2_cookie = session2_response.cookies["Vidalytics_session"]
        
        # Revoke session1 using session2
        response = client.delete(
            f"/api/session/revoke/{session1_id}",
            cookies={"Vidalytics_session": session2_cookie}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Verify session1 is invalid
        invalid_response = client.get(
            "/api/session/current",
            cookies={"Vidalytics_session": session1_cookie}
        )
        assert invalid_response.status_code == 401
        
        # Verify session2 is still valid
        valid_response = client.get(
            "/api/session/current",
            cookies={"Vidalytics_session": session2_cookie}
        )
        assert valid_response.status_code == 200
    
    def test_logout_all_sessions(self, client):
        """Test logging out from all sessions"""
        user_id = "logout_all_test"
        
        # Create multiple sessions
        sessions = []
        for i in range(3):
            response = client.post("/api/session/login", json={
                "user_id": user_id,
                "metadata": {"session_number": i}
            })
            sessions.append(response.cookies["Vidalytics_session"])
        
        # Logout from all sessions using the last session
        response = client.post(
            "/api/session/logout-all",
            cookies={"Vidalytics_session": sessions[-1]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["revoked_sessions"] >= 2
        
        # Verify first two sessions are invalid
        for session_cookie in sessions[:-1]:
            invalid_response = client.get(
                "/api/session/current",
                cookies={"Vidalytics_session": session_cookie}
            )
            assert invalid_response.status_code == 401
        
        # Verify last session is still valid
        valid_response = client.get(
            "/api/session/current",
            cookies={"Vidalytics_session": sessions[-1]}
        )
        assert valid_response.status_code == 200
    
    def test_update_session(self, client):
        """Test updating session data"""
        # Login
        login_response = client.post("/api/session/login", json={
            "user_id": "update_session_test",
            "metadata": {"initial": "data"}
        })
        
        session_cookie = login_response.cookies["Vidalytics_session"]
        
        # Update session
        response = client.put(
            "/api/session/update",
            json={
                "metadata": {"updated": "data", "new_field": "value"},
                "permissions": ["user", "premium"]
            },
            cookies={"Vidalytics_session": session_cookie}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Verify session was updated
        current_response = client.get(
            "/api/session/current",
            cookies={"Vidalytics_session": session_cookie}
        )
        
        assert current_response.status_code == 200
        current_data = current_response.json()
        assert current_data["data"]["metadata"]["updated"] == "data"
        assert current_data["data"]["permissions"] == ["user", "premium"]
    
    def test_session_health_check(self, client):
        """Test session system health check"""
        response = client.get("/api/session/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "status" in data["data"]
        assert "response_time_ms" in data["data"]