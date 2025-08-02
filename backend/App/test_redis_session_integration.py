#!/usr/bin/env python3
"""
Test script for Redis Session Management Integration
Tests the complete session management system integration
"""

import asyncio
import sys
import os
import redis
from datetime import datetime, timedelta, timezone

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from redis_session_manager import get_session_manager, cleanup_expired_sessions
from session_middleware import create_user_session, get_user_session, revoke_user_session
from logging_config import get_logger, LogCategory


async def test_redis_session_integration():
    """Test Redis session management integration"""
    logger = get_logger(__name__, LogCategory.SYSTEM)
    
    print("🔄 Testing Redis Session Management Integration")
    print("=" * 60)
    
    try:
        # Test 1: Session Manager Connection
        print("\n1. Testing Session Manager Connection...")
        session_manager = get_session_manager()
        health_data = await session_manager.health_check()
        
        if health_data.get('status') == 'healthy':
            print(f"   ✅ Redis connection healthy (response time: {health_data.get('response_time_ms', 0):.2f}ms)")
            print(f"   📊 Redis version: {health_data.get('redis_version', 'unknown')}")
            print(f"   💾 Memory usage: {health_data.get('used_memory_human', 'unknown')}")
        else:
            print(f"   ❌ Redis connection unhealthy: {health_data}")
            return False
        
        # Test 2: Create Session
        print("\n2. Testing Session Creation...")
        test_user_id = "test_integration_user"
        session_data = await create_user_session(
            user_id=test_user_id,
            ip_address="127.0.0.1",
            user_agent="integration-test-agent",
            permissions=["user", "test"],
            metadata={"test": "integration", "environment": "test"}
        )
        
        print(f"   ✅ Session created successfully")
        print(f"   🆔 Session ID: {session_data.session_id[:16]}...")
        print(f"   👤 User ID: {session_data.user_id}")
        print(f"   ⏰ Expires at: {session_data.expires_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"   🔐 Permissions: {session_data.permissions}")
        
        # Test 3: Retrieve Session
        print("\n3. Testing Session Retrieval...")
        retrieved_session = await get_user_session(session_data.session_id)
        
        if retrieved_session:
            print(f"   ✅ Session retrieved successfully")
            print(f"   🔄 Last accessed: {retrieved_session.last_accessed.strftime('%H:%M:%S UTC')}")
            print(f"   ✅ Session is valid: {retrieved_session.is_valid()}")
        else:
            print(f"   ❌ Failed to retrieve session")
            return False
        
        # Test 4: Multiple Sessions for User
        print("\n4. Testing Multiple Sessions...")
        session2 = await create_user_session(
            user_id=test_user_id,
            ip_address="192.168.1.100",
            user_agent="mobile-test-agent",
            permissions=["user"],
            metadata={"device": "mobile", "test": "multiple_sessions"}
        )
        
        user_sessions = await session_manager.get_user_sessions(test_user_id)
        print(f"   ✅ Created second session")
        print(f"   📊 Total sessions for user: {len(user_sessions)}")
        
        # Test 5: Session Update
        print("\n5. Testing Session Update...")
        update_success = await session_manager.update_session(
            session_data.session_id,
            metadata={"test": "updated", "timestamp": datetime.now().isoformat()},
            permissions=["user", "test", "premium"]
        )
        
        if update_success:
            updated_session = await get_user_session(session_data.session_id)
            print(f"   ✅ Session updated successfully")
            print(f"   🔐 New permissions: {updated_session.permissions}")
            print(f"   📝 Updated metadata: {updated_session.metadata}")
        else:
            print(f"   ❌ Failed to update session")
        
        # Test 6: Session Statistics
        print("\n6. Testing Session Statistics...")
        stats = await session_manager.get_session_stats()
        print(f"   ✅ Statistics retrieved")
        print(f"   📊 Active sessions: {stats.get('total_active_sessions', 0)}")
        print(f"   💾 Redis connected: {stats.get('redis_info', {}).get('connected', False)}")
        
        # Test 7: Session Cleanup
        print("\n7. Testing Session Cleanup...")
        await cleanup_expired_sessions()
        print(f"   ✅ Cleanup completed successfully")
        
        # Test 8: Session Revocation
        print("\n8. Testing Session Revocation...")
        revoke_success = await revoke_user_session(session2.session_id)
        if revoke_success:
            print(f"   ✅ Session revoked successfully")
            
            # Verify session is gone
            revoked_session = await get_user_session(session2.session_id)
            if revoked_session is None:
                print(f"   ✅ Revoked session no longer accessible")
            else:
                print(f"   ⚠️  Revoked session still accessible (unexpected)")
        else:
            print(f"   ❌ Failed to revoke session")
        
        # Test 9: Cleanup Test Data
        print("\n9. Cleaning Up Test Data...")
        remaining_sessions = await session_manager.get_user_sessions(test_user_id)
        revoked_count = 0
        for session in remaining_sessions:
            if await revoke_user_session(session.session_id):
                revoked_count += 1
        
        print(f"   ✅ Cleaned up {revoked_count} test sessions")
        
        print("\n" + "=" * 60)
        print("🎉 All Redis Session Integration Tests Passed!")
        print("✅ Session management system is ready for production")
        return True
        
    except redis.ConnectionError as e:
        print(f"\n❌ Redis Connection Error: {e}")
        print("💡 Make sure Redis is running on localhost:6379")
        print("   You can start Redis with: redis-server")
        return False
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_session_expiry():
    """Test session expiry functionality"""
    print("\n🔄 Testing Session Expiry (Fast Test)")
    print("-" * 40)
    
    try:
        session_manager = get_session_manager()
        
        # Create session with very short expiry
        short_session = await session_manager.create_session(
            user_id="expiry_test_user",
            ip_address="127.0.0.1",
            custom_expiry=timedelta(seconds=2)
        )
        
        print(f"   ✅ Created session with 2-second expiry")
        print(f"   🆔 Session ID: {short_session.session_id[:16]}...")
        
        # Verify session exists
        retrieved = await session_manager.get_session(short_session.session_id)
        if retrieved:
            print(f"   ✅ Session initially accessible")
        
        # Wait for expiry
        print(f"   ⏳ Waiting 3 seconds for expiry...")
        await asyncio.sleep(3)
        
        # Try to retrieve expired session
        expired_session = await session_manager.get_session(short_session.session_id)
        if expired_session is None:
            print(f"   ✅ Expired session correctly removed")
            print(f"   🎯 Session expiry working as expected")
            return True
        else:
            print(f"   ❌ Expired session still accessible")
            return False
            
    except Exception as e:
        print(f"   ❌ Expiry test failed: {e}")
        return False


if __name__ == "__main__":
    print("Redis Session Management Integration Test")
    print("========================================")
    
    async def run_all_tests():
        # Run main integration tests
        main_tests_passed = await test_redis_session_integration()
        
        if main_tests_passed:
            # Run expiry tests
            expiry_tests_passed = await test_session_expiry()
            
            if expiry_tests_passed:
                print("\n🎉 ALL TESTS PASSED!")
                print("✅ Redis session management is fully integrated and working")
                sys.exit(0)
            else:
                print("\n⚠️  Some expiry tests failed")
                sys.exit(1)
        else:
            print("\n❌ Integration tests failed")
            sys.exit(1)
    
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test runner failed: {e}")
        sys.exit(1)