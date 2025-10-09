"""
Test script for MYTA Email Service
Tests all authentication email types
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from backend/.env
backend_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(backend_dir, '.env'))

from App.email_service import (
    send_verification_email,
    send_password_reset_email,
    send_welcome_email,
    send_email_change_confirmation
)


async def test_all_emails():
    """Test all email types"""
    
    print("🧪 Testing MYTA Email Service\n")
    print("=" * 60)
    
    # Check environment
    print("\n📋 Environment Check:")
    print(f"USE_RESEND: {os.getenv('USE_RESEND', 'true')}")
    resend_key = os.getenv('RESEND_API_KEY', '')
    if resend_key:
        print(f"RESEND_API_KEY: {resend_key[:10]}... ✅")
    else:
        print("RESEND_API_KEY: Not set ❌")
    print(f"FROM_EMAIL: {os.getenv('FROM_EMAIL', 'noreply@myta.app')}")
    print(f"BASE_URL: {os.getenv('BASE_URL', 'http://localhost:3000')}")
    
    # Test email - use verified email for Resend testing
    # Change this to your email address
    test_email = input("\n📧 Enter your email address to receive test emails: ").strip()
    
    if not test_email:
        print("❌ No email provided. Exiting.")
        return
    
    print(f"\n✅ Will send test emails to: {test_email}")
    print("\n" + "=" * 60)
    
    # Test 1: Verification Email
    print("\n1️⃣ Testing Email Verification...")
    try:
        result = await send_verification_email(
            user_email=test_email,
            user_name="Test User",
            verification_token="test-token-abc123",
            verification_code="123456"
        )
        if result:
            print("   ✅ Verification email sent successfully!")
        else:
            print("   ❌ Failed to send verification email")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    await asyncio.sleep(2)  # Rate limiting
    
    # Test 2: Password Reset Email
    print("\n2️⃣ Testing Password Reset...")
    try:
        result = await send_password_reset_email(
            user_email=test_email,
            user_name="Test User",
            reset_token="reset-token-xyz789"
        )
        if result:
            print("   ✅ Password reset email sent successfully!")
        else:
            print("   ❌ Failed to send password reset email")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    await asyncio.sleep(2)  # Rate limiting
    
    # Test 3: Welcome Email
    print("\n3️⃣ Testing Welcome Email...")
    try:
        result = await send_welcome_email(
            user_email=test_email,
            user_name="Test User"
        )
        if result:
            print("   ✅ Welcome email sent successfully!")
        else:
            print("   ❌ Failed to send welcome email")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    await asyncio.sleep(2)  # Rate limiting
    
    # Test 4: Email Change Confirmation
    print("\n4️⃣ Testing Email Change Confirmation...")
    try:
        result = await send_email_change_confirmation(
            new_email=test_email,
            user_name="Test User",
            old_email="old-email@example.com",
            confirmation_token="change-token-def456"
        )
        if result:
            print("   ✅ Email change confirmation sent successfully!")
        else:
            print("   ❌ Failed to send email change confirmation")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("\n✅ Email service test complete!")
    print("\n📬 Check your inbox for 4 test emails:")
    print("   1. Email Verification")
    print("   2. Password Reset")
    print("   3. Welcome to MYTA")
    print("   4. Email Change Confirmation")
    print("\n💡 If you don't see them, check your spam folder.")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_all_emails())

