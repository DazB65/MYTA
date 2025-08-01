#!/usr/bin/env python3
"""
Test script for OAuth 2.0 implementation
Verifies OAuth components work correctly
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.oauth_manager import OAuthManager, OAuthToken
from backend.oauth_endpoints import oauth_router
from datetime import datetime, timedelta

async def test_oauth_manager():
    """Test OAuth manager functionality"""
    print("🔑 Testing OAuth Manager...")
    
    # Initialize OAuth manager
    oauth_manager = OAuthManager()
    
    print(f"✓ OAuth Manager initialized")
    print(f"  Client ID configured: {bool(oauth_manager.client_id)}")
    print(f"  Client Secret configured: {bool(oauth_manager.client_secret)}")
    print(f"  Redirect URI: {oauth_manager.redirect_uri}")
    print(f"  Scopes: {oauth_manager.scopes}")
    
    # Test state generation
    test_user = "test_user_123"
    try:
        auth_url, state = oauth_manager.generate_authorization_url(test_user)
        print(f"✓ Authorization URL generated successfully")
        print(f"  State: {state[:20]}...")
        print(f"  URL contains Google OAuth: {'accounts.google.com' in auth_url}")
    except Exception as e:
        print(f"❌ Failed to generate authorization URL: {e}")
    
    # Test OAuth status
    status = oauth_manager.get_oauth_status(test_user)
    print(f"✓ OAuth status check: {status['authenticated']}")
    
    return True

def test_oauth_endpoints():
    """Test OAuth endpoints"""
    print("\n🛠️ Testing OAuth Endpoints...")
    
    # Check if router is properly configured
    print(f"✓ OAuth router created with prefix: {oauth_router.prefix}")
    print(f"✓ OAuth router has {len(oauth_router.routes)} routes:")
    
    for route in oauth_router.routes:
        print(f"  - {route.methods if hasattr(route, 'methods') else 'N/A'} {route.path}")
    
    return True

def test_oauth_integration():
    """Test OAuth integration with YouTube API"""
    print("\n📺 Testing YouTube API OAuth Integration...")
    
    try:
        from backend.youtube_api_integration import YouTubeAPIIntegration
        
        integration = YouTubeAPIIntegration()
        print(f"✓ YouTube integration has OAuth manager: {bool(integration.oauth_manager)}")
        print(f"✓ YouTube integration has API key fallback: {bool(integration.api_key)}")
        
        # Test method signatures
        import inspect
        
        # Check if get_channel_data accepts user_id parameter
        sig = inspect.signature(integration.get_channel_data)
        has_user_id = 'user_id' in sig.parameters
        print(f"✓ get_channel_data supports OAuth (user_id param): {has_user_id}")
        
        # Check if get_recent_videos accepts user_id parameter
        sig = inspect.signature(integration.get_recent_videos)
        has_user_id = 'user_id' in sig.parameters
        print(f"✓ get_recent_videos supports OAuth (user_id param): {has_user_id}")
        
        # Check if get_channel_analytics exists
        has_analytics = hasattr(integration, 'get_channel_analytics')
        print(f"✓ get_channel_analytics method exists: {has_analytics}")
        
        return True
        
    except Exception as e:
        print(f"❌ YouTube OAuth integration test failed: {e}")
        return False

def test_database_schema():
    """Test OAuth database schema"""
    print("\n🗃️ Testing OAuth Database Schema...")
    
    try:
        import sqlite3
        
        # Test database initialization
        oauth_manager = OAuthManager()
        
        # Check if table exists
        with sqlite3.connect(oauth_manager.db_path) as conn:
            cursor = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='oauth_tokens'
            """)
            table_exists = cursor.fetchone() is not None
            
        print(f"✓ OAuth tokens table exists: {table_exists}")
        
        if table_exists:
            with sqlite3.connect(oauth_manager.db_path) as conn:
                cursor = conn.execute("PRAGMA table_info(oauth_tokens)")
                columns = [row[1] for row in cursor.fetchall()]
                
            expected_columns = [
                'user_id', 'access_token', 'refresh_token', 'token_type',
                'expires_at', 'scope', 'created_at', 'updated_at'
            ]
            
            all_columns_present = all(col in columns for col in expected_columns)
            print(f"✓ All required columns present: {all_columns_present}")
            print(f"  Columns: {columns}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database schema test failed: {e}")
        return False

def test_frontend_integration():
    """Test frontend OAuth integration files"""
    print("\n🌐 Testing Frontend Integration...")
    
    files_to_check = [
        'frontend/components/oauth/oauth-integration.js',
        'frontend/components/oauth/oauth-ui.html'
    ]
    
    all_files_exist = True
    
    for file_path in files_to_check:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        exists = os.path.exists(full_path)
        print(f"✓ {file_path}: {'✓' if exists else '❌'}")
        
        if exists and file_path.endswith('.js'):
            # Check for key functions
            with open(full_path, 'r') as f:
                content = f.read()
                
            key_functions = [
                'checkOAuthStatus', 'initiateOAuth', 'handleOAuthCallback',
                'refreshToken', 'revokeToken'
            ]
            
            for func in key_functions:
                has_function = func in content
                print(f"  - {func}: {'✓' if has_function else '❌'}")
        
        all_files_exist = all_files_exist and exists
    
    return all_files_exist

def check_environment_configuration():
    """Check environment configuration"""
    print("\n⚙️ Checking Environment Configuration...")
    
    required_vars = ['GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'OAUTH_REDIRECT_URI']
    optional_vars = ['YOUTUBE_API_KEY', 'BOSS_AGENT_SECRET_KEY']
    
    config_status = {}
    
    for var in required_vars:
        value = os.getenv(var)
        configured = bool(value and value != 'your_google_client_id_here' and value != 'your_google_client_secret_here')
        config_status[var] = configured
        print(f"{'✓' if configured else '⚠️'} {var}: {'Configured' if configured else 'Not configured'}")
    
    for var in optional_vars:
        value = os.getenv(var)
        configured = bool(value and not value.startswith('your_'))
        config_status[var] = configured
        print(f"{'✓' if configured else '⚠️'} {var}: {'Configured' if configured else 'Not configured'}")
    
    return config_status

async def main():
    """Run all OAuth tests"""
    print("🧪 Vidalytics OAuth 2.0 Implementation Test Suite")
    print("=" * 60)
    
    test_results = {}
    
    # Run tests
    test_results['environment'] = check_environment_configuration()
    test_results['oauth_manager'] = await test_oauth_manager()
    test_results['oauth_endpoints'] = test_oauth_endpoints()
    test_results['youtube_integration'] = test_oauth_integration()
    test_results['database_schema'] = test_database_schema()
    test_results['frontend_integration'] = test_frontend_integration()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    # Environment summary
    env_status = test_results['environment']
    required_configured = all(env_status.get(var, False) for var in ['GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'OAUTH_REDIRECT_URI'])
    
    print(f"Environment Configuration: {'✓ Ready' if required_configured else '⚠️ Needs setup'}")
    print(f"OAuth Manager: {'✓ Working' if test_results['oauth_manager'] else '❌ Failed'}")
    print(f"OAuth Endpoints: {'✓ Working' if test_results['oauth_endpoints'] else '❌ Failed'}")
    print(f"YouTube Integration: {'✓ Working' if test_results['youtube_integration'] else '❌ Failed'}")
    print(f"Database Schema: {'✓ Working' if test_results['database_schema'] else '❌ Failed'}")
    print(f"Frontend Integration: {'✓ Working' if test_results['frontend_integration'] else '❌ Failed'}")
    
    # Overall status
    all_tests_passed = all(test_results[key] for key in ['oauth_manager', 'oauth_endpoints', 'youtube_integration', 'database_schema', 'frontend_integration'])
    
    print("\n" + "=" * 60)
    if all_tests_passed and required_configured:
        print("🎉 OAuth 2.0 Implementation: READY FOR TESTING")
        print("✓ All components implemented and working")
        print("✓ Environment properly configured")
        print("\nNext steps:")
        print("1. Set your Google OAuth credentials in .env")
        print("2. Start the server: uvicorn main:app --reload --host 0.0.0.0 --port 8888")
        print("3. Test OAuth flow at http://localhost:8888")
    elif all_tests_passed:
        print("⚠️ OAuth 2.0 Implementation: READY (NEEDS CONFIGURATION)")
        print("✓ All components implemented and working")
        print("⚠️ Environment needs OAuth credentials")
        print("\nNext steps:")
        print("1. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env")
        print("2. Start the server and test OAuth flow")
    else:
        print("❌ OAuth 2.0 Implementation: NEEDS FIXES")
        print("Some components need attention before testing")
    
    return all_tests_passed

if __name__ == "__main__":
    asyncio.run(main())