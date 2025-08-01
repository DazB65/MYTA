#!/usr/bin/env python3
"""
Simple OAuth implementation test
"""

import os
import sys

def check_files():
    """Check if OAuth files exist"""
    print("🔍 Checking OAuth Implementation Files...")
    
    files = [
        'backend/oauth_manager.py',
        'backend/oauth_endpoints.py', 
        'frontend/components/oauth/oauth-integration.js',
        'frontend/components/oauth/oauth-ui.html'
    ]
    
    all_exist = True
    for file in files:
        exists = os.path.exists(file)
        print(f"{'✓' if exists else '❌'} {file}")
        all_exist = all_exist and exists
    
    return all_exist

def check_env_config():
    """Check environment configuration"""
    print("\n⚙️ Checking Environment Configuration...")
    
    # Load .env file
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
        
        checks = {
            'GOOGLE_CLIENT_ID': 'GOOGLE_CLIENT_ID=' in content,
            'GOOGLE_CLIENT_SECRET': 'GOOGLE_CLIENT_SECRET=' in content,
            'OAUTH_REDIRECT_URI': 'OAUTH_REDIRECT_URI=' in content
        }
        
        for key, exists in checks.items():
            configured = exists and 'your_' not in content.split(f'{key}=')[1].split('\n')[0] if exists else False
            print(f"{'✓' if configured else '⚠️'} {key}: {'Configured' if configured else 'Needs configuration'}")
        
        return all(checks.values())
    else:
        print("❌ .env file not found")
        return False

def check_dependencies():
    """Check if required dependencies can be imported"""
    print("\n📦 Checking Dependencies...")
    
    deps = [
        'google.oauth2.credentials',
        'google_auth_oauthlib.flow',
        'googleapiclient.discovery'
    ]
    
    all_available = True
    for dep in deps:
        try:
            __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            all_available = False
    
    return all_available

def check_main_app_integration():
    """Check if main.py includes OAuth router"""
    print("\n🔗 Checking Main App Integration...")
    
    try:
        with open('backend/main.py', 'r') as f:
            content = f.read()
        
        checks = {
            'OAuth import': 'oauth_endpoints' in content,
            'Router inclusion': 'include_router(oauth_router)' in content,
            'Authenticated endpoint': '/api/youtube/analytics/authenticated' in content
        }
        
        for check, passed in checks.items():
            print(f"{'✓' if passed else '❌'} {check}")
        
        return all(checks.values())
    except Exception as e:
        print(f"❌ Error checking main.py: {e}")
        return False

def main():
    """Run simple OAuth tests"""
    print("🧪 Vidalytics OAuth 2.0 Implementation Test")
    print("=" * 50)
    
    results = {
        'files': check_files(),
        'environment': check_env_config(),
        'dependencies': check_dependencies(),
        'integration': check_main_app_integration()
    }
    
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test.title()}: {status}")
    
    all_passed = all(results.values())
    
    print(f"\nOverall Status: {'✅ READY' if all_passed else '⚠️ NEEDS ATTENTION'}")
    
    if all_passed:
        print("\n🎉 OAuth implementation looks complete!")
        print("Next steps:")
        print("1. Configure Google OAuth credentials in .env")
        print("2. Start server: uvicorn main:app --reload --host 0.0.0.0 --port 8888")
        print("3. Test OAuth flow at http://localhost:8888")
    else:
        print("\n🔧 Issues found that need attention:")
        for test, passed in results.items():
            if not passed:
                if test == 'dependencies':
                    print(f"- Install OAuth dependencies: pip install google-auth-oauthlib")
                elif test == 'environment':
                    print(f"- Configure OAuth credentials in .env file")
                elif test == 'files':
                    print(f"- Some OAuth implementation files are missing")
                elif test == 'integration':
                    print(f"- OAuth not properly integrated into main app")

if __name__ == "__main__":
    main()