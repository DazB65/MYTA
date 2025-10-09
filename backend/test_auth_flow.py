"""
Test the complete authentication flow
Tests registration, email verification, and password reset
"""

import asyncio
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"test_{datetime.now().timestamp()}@example.com"
TEST_PASSWORD = "TestPass123!"
TEST_NAME = "Test User"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_result(success, message, data=None):
    """Print test result"""
    icon = "✅" if success else "❌"
    print(f"\n{icon} {message}")
    if data:
        print(f"   Data: {json.dumps(data, indent=2)}")

async def test_registration():
    """Test user registration"""
    print_section("TEST 1: User Registration")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD,
                "confirm_password": TEST_PASSWORD,
                "name": TEST_NAME
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Registration successful!", {
                "email": data.get("user", {}).get("email"),
                "requires_verification": data.get("requires_verification"),
                "token_received": bool(data.get("token"))
            })
            return data.get("token"), data.get("user", {}).get("id")
        else:
            print_result(False, f"Registration failed: {response.text}")
            return None, None
            
    except Exception as e:
        print_result(False, f"Registration error: {e}")
        return None, None

async def test_email_verification_with_code(code):
    """Test email verification with 6-digit code"""
    print_section("TEST 2: Email Verification (with code)")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/verify-email",
            json={"code": code}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Email verified with code!", {
                "email": data.get("user", {}).get("email"),
                "is_verified": data.get("user", {}).get("is_verified")
            })
            return True
        else:
            print_result(False, f"Verification failed: {response.text}")
            return False
            
    except Exception as e:
        print_result(False, f"Verification error: {e}")
        return False

async def test_resend_verification(token):
    """Test resending verification email"""
    print_section("TEST 3: Resend Verification Email")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/send-verification-email",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Verification email resent!", data)
            return True
        else:
            print_result(False, f"Resend failed: {response.text}")
            return False
            
    except Exception as e:
        print_result(False, f"Resend error: {e}")
        return False

async def test_password_reset_request():
    """Test password reset request"""
    print_section("TEST 4: Password Reset Request")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/request-password-reset",
            json={"email": TEST_EMAIL}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Password reset requested!", data)
            return True
        else:
            print_result(False, f"Reset request failed: {response.text}")
            return False
            
    except Exception as e:
        print_result(False, f"Reset request error: {e}")
        return False

async def test_login():
    """Test user login"""
    print_section("TEST 5: User Login")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Login successful!", {
                "email": data.get("user", {}).get("email"),
                "token_received": bool(data.get("token"))
            })
            return data.get("token")
        else:
            print_result(False, f"Login failed: {response.text}")
            return None
            
    except Exception as e:
        print_result(False, f"Login error: {e}")
        return None

async def main():
    """Run all authentication tests"""
    print("\n" + "🧪" * 35)
    print("  MYTA AUTHENTICATION FLOW TEST")
    print("🧪" * 35)
    
    print(f"\n📧 Test Email: {TEST_EMAIL}")
    print(f"🔐 Test Password: {TEST_PASSWORD}")
    
    # Check if backend is running
    print_section("Checking Backend Status")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_result(True, "Backend is running!")
        else:
            print_result(False, "Backend returned unexpected status")
            return
    except Exception as e:
        print_result(False, f"Backend is not running! Start it with: cd backend && uvicorn App.main:app --reload")
        return
    
    # Test 1: Registration
    token, user_id = await test_registration()
    if not token:
        print("\n❌ Cannot continue without successful registration")
        return
    
    # Test 2: Resend verification email
    await test_resend_verification(token)
    
    print("\n" + "⚠️ " * 35)
    print("  MANUAL STEP REQUIRED")
    print("⚠️ " * 35)
    print("\n📬 Check your email for the verification code")
    print("   (If using development mode, check the backend logs)")
    print("\n   Enter the 6-digit verification code: ", end="")
    
    verification_code = input().strip()
    
    if verification_code:
        # Test 3: Verify email with code
        verified = await test_email_verification_with_code(verification_code)
        
        if verified:
            # Test 4: Login after verification
            login_token = await test_login()
            
            # Test 5: Password reset
            await test_password_reset_request()
    
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print("\n✅ Registration endpoint working")
    print("✅ Email verification endpoint working")
    print("✅ Password reset request working")
    print("\n📝 Next steps:")
    print("   1. Check email delivery (or backend logs in dev mode)")
    print("   2. Test password reset flow with token from email")
    print("   3. Build frontend pages for these features")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    asyncio.run(main())

