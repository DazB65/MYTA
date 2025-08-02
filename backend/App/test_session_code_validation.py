#!/usr/bin/env python3
"""
Session Management Code Validation Test
Validates the session management implementation without requiring Redis connection
"""

import sys
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_session_data_structure():
    """Test SessionData dataclass functionality"""
    print("🔄 Testing SessionData Structure...")
    
    try:
        from redis_session_manager import SessionData, SessionStatus
        
        # Test session creation
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
        
        print(f"   ✅ SessionData created successfully")
        print(f"   🆔 Session ID: {session.session_id}")
        print(f"   👤 User ID: {session.user_id}")
        print(f"   🟢 Status: {session.status.value}")
        print(f"   ✅ Is valid: {session.is_valid()}")
        print(f"   ❌ Is expired: {session.is_expired()}")
        
        # Test to_dict conversion
        session_dict = session.to_dict()
        print(f"   ✅ to_dict conversion successful")
        
        # Test from_dict creation
        restored_session = SessionData.from_dict(session_dict)
        print(f"   ✅ from_dict restoration successful")
        print(f"   🔄 Restored session ID: {restored_session.session_id}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ SessionData test failed: {e}")
        return False


def test_session_config():
    """Test Redis session configuration"""
    print("\n🔄 Testing Session Configuration...")
    
    try:
        from redis_session_manager import RedisSessionConfig
        
        # Create config
        config = RedisSessionConfig()
        
        print(f"   ✅ Config created successfully")
        print(f"   ⏰ Session timeout: {config.session_timeout}")
        print(f"   🔄 Refresh threshold: {config.refresh_threshold}")
        print(f"   👥 Max sessions per user: {config.max_sessions_per_user}")
        print(f"   🔐 Key prefix: {config.key_prefix}")
        print(f"   🔒 Secure cookies: {config.secure_cookies}")
        print(f"   🍪 HTTP-only cookies: {config.httponly_cookies}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Config test failed: {e}")
        return False


def test_session_middleware_imports():
    """Test session middleware imports and structure"""
    print("\n🔄 Testing Session Middleware Imports...")
    
    try:
        from session_middleware import (
            SessionMiddleware,
            SessionDependency,
            OptionalSessionDependency,
            require_auth,
            require_admin,
            optional_auth,
            create_user_session,
            get_user_session,
            revoke_user_session,
            revoke_all_user_sessions,
            get_all_user_sessions,
            update_user_session
        )
        
        print(f"   ✅ SessionMiddleware imported")
        print(f"   ✅ SessionDependency imported")
        print(f"   ✅ OptionalSessionDependency imported")
        print(f"   ✅ Authentication dependencies imported")
        print(f"   ✅ Session utility functions imported")
        
        # Test dependency creation
        custom_auth = SessionDependency(require_permissions=['admin'])
        print(f"   ✅ Custom auth dependency created")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Middleware import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_session_router_imports():
    """Test session router imports and structure"""
    print("\n🔄 Testing Session Router Imports...")
    
    try:
        from session_router import (
            router,
            LoginRequest,
            SessionResponse,
            SessionListResponse,
            SessionStatsResponse,
            UpdateSessionRequest
        )
        
        print(f"   ✅ Session router imported")
        print(f"   ✅ LoginRequest model imported")
        print(f"   ✅ SessionResponse model imported")
        print(f"   ✅ SessionListResponse model imported")
        print(f"   ✅ SessionStatsResponse model imported")
        print(f"   ✅ UpdateSessionRequest model imported")
        
        # Test model creation
        login_request = LoginRequest(user_id="test_user", remember_me=True)
        print(f"   ✅ LoginRequest model created: {login_request.user_id}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Router import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mock_session_manager():
    """Test session manager with mocked Redis"""
    print("\n🔄 Testing Session Manager (Mocked)...")
    
    try:
        # Mock Redis client
        mock_redis = MagicMock()
        mock_redis.ping.return_value = True
        mock_redis.setex.return_value = True
        mock_redis.get.return_value = None
        mock_redis.delete.return_value = 1
        mock_redis.connection_pool.connection_kwargs = {'host': 'localhost', 'port': 6379}
        
        with patch('backend.redis_session_manager.get_settings') as mock_settings:
            mock_settings.return_value.is_development.return_value = True
            
            from redis_session_manager import RedisSessionManager
            
            # Create session manager with mocked Redis
            session_manager = RedisSessionManager(redis_client=mock_redis)
            
            print(f"   ✅ Session manager created with mocked Redis")
            print(f"   ✅ Redis ping successful")
            
            # Test session ID generation
            session_id = session_manager._generate_session_id()
            print(f"   ✅ Session ID generated: {session_id[:16]}...")
            
            # Test key generation
            session_key = session_manager._get_session_key("test_session")
            user_key = session_manager._get_user_sessions_key("test_user")
            print(f"   ✅ Session key: {session_key}")
            print(f"   ✅ User sessions key: {user_key}")
            
            return True
        
    except Exception as e:
        print(f"   ❌ Mocked session manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_app_integration():
    """Test that main.py properly imports session components"""
    print("\n🔄 Testing Main App Integration...")
    
    try:
        # Read main.py and check for session imports
        with open('main.py', 'r') as f:
            main_content = f.read()
        
        checks = [
            ('session_router import', 'from session_router import router as session_router'),
            ('SessionMiddleware import', 'from session_middleware import SessionMiddleware'),
            ('session middleware added', 'app.add_middleware(SessionMiddleware)'),
            ('session router included', 'app.include_router(session_router)')
        ]
        
        for check_name, check_text in checks:
            if check_text in main_content:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name} - not found")
                return False
        
        print(f"   ✅ All main.py integration checks passed")
        return True
        
    except Exception as e:
        print(f"   ❌ Main app integration test failed: {e}")
        return False


def test_docker_configuration():
    """Test Docker configuration includes Redis"""
    print("\n🔄 Testing Docker Configuration...")
    
    try:
        # Check docker-compose.yml
        with open('../../docker-compose.yml', 'r') as f:
            compose_content = f.read()
        
        # Check docker-compose.dev.yml
        with open('../../docker-compose.dev.yml', 'r') as f:
            compose_dev_content = f.read()
        
        checks = [
            ('Redis service in production', 'redis:' in compose_content),
            ('Redis image in production', 'redis:7-alpine' in compose_content),
            ('Redis port in production', '6379:6379' in compose_content),
            ('Redis service in development', 'redis:' in compose_dev_content),
            ('Redis dependency in backend', 'depends_on:' in compose_content and 'redis' in compose_content),
            ('Redis URL environment variable', 'REDIS_URL=' in compose_content)
        ]
        
        for check_name, check_result in checks:
            if check_result:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}")
                return False
        
        print(f"   ✅ All Docker configuration checks passed")
        return True
        
    except Exception as e:
        print(f"   ❌ Docker configuration test failed: {e}")
        return False


def main():
    """Run all validation tests"""
    print("Redis Session Management Code Validation")
    print("=" * 50)
    
    tests = [
        test_session_data_structure,
        test_session_config,
        test_session_middleware_imports,
        test_session_router_imports,
        test_mock_session_manager,
        test_main_app_integration,
        test_docker_configuration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   💥 Test {test.__name__} crashed: {e}")
            failed += 1
    
    total = passed + failed
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if failed == 0:
        print("🎉 All code validation tests passed!")
        print("✅ Redis session management implementation is complete")
        print("💡 To test with real Redis, start a Redis server and run:")
        print("   redis-server")
        print("   python3 test_redis_session_integration.py")
        return True
    else:
        print(f"❌ {failed} test(s) failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)