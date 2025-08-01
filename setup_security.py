#!/usr/bin/env python3
"""
Security Setup Script for Vidalytics
Helps with secure environment configuration and key generation
"""

import os
import secrets
import sys
from pathlib import Path

def generate_secure_key(length: int = 64) -> str:
    """Generate a secure random key"""
    return secrets.token_urlsafe(length)

def check_env_file():
    """Check if .env file exists and has proper permissions"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Check file permissions (Unix-like systems)
    if hasattr(os, 'stat'):
        stat_info = env_file.stat()
        permissions = oct(stat_info.st_mode)[-3:]
        
        if permissions != '600':
            print(f"⚠️  .env file permissions are {permissions}, should be 600")
            print("Run: chmod 600 .env")
            return False
    
    print("✅ .env file exists with proper permissions")
    return True

def check_api_keys():
    """Check if API keys are configured"""
    required_keys = [
        "OPENAI_API_KEY",
        "YOUTUBE_API_KEY", 
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET"
    ]
    
    optional_keys = [
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
        "BOSS_AGENT_SECRET_KEY"
    ]
    
    missing_required = []
    missing_optional = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_required.append(key)
    
    for key in optional_keys:
        if not os.getenv(key):
            missing_optional.append(key)
    
    if missing_required:
        print(f"❌ Missing required API keys: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"⚠️  Missing optional API keys: {', '.join(missing_optional)}")
    
    print("✅ All required API keys are configured")
    return True

def generate_boss_agent_secret():
    """Generate a secure boss agent secret"""
    secret = generate_secure_key(64)
    print(f"Generated Boss Agent Secret Key:")
    print(f"BOSS_AGENT_SECRET_KEY={secret}")
    print("\nAdd this to your .env file")
    return secret

def check_database_permissions():
    """Check database file permissions"""
    db_file = Path("backend/Vidalytics.db")
    
    if not db_file.exists():
        print("ℹ️  Database file doesn't exist yet (will be created on first run)")
        return True
    
    if hasattr(os, 'stat'):
        stat_info = db_file.stat()
        permissions = oct(stat_info.st_mode)[-3:]
        
        if permissions != '600':
            print(f"⚠️  Database file permissions are {permissions}, should be 600")
            print("Run: chmod 600 backend/Vidalytics.db")
            return False
    
    print("✅ Database file has proper permissions")
    return True

def security_checklist():
    """Run complete security checklist"""
    print("🔒 Vidalytics Security Setup Checklist")
    print("=" * 50)
    
    checks = [
        ("Environment file", check_env_file),
        ("API keys configuration", check_api_keys),
        ("Database permissions", check_database_permissions)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n📋 Checking {check_name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("✅ All security checks passed!")
    else:
        print("❌ Some security checks failed. Please address the issues above.")
    
    return all_passed

def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "generate-secret":
            generate_boss_agent_secret()
        elif command == "check":
            security_checklist()
        elif command == "help":
            print("Vidalytics Security Setup Script")
            print("\nCommands:")
            print("  check           - Run security checklist")
            print("  generate-secret - Generate boss agent secret key")
            print("  help           - Show this help message")
        else:
            print(f"Unknown command: {command}")
            print("Run 'python setup_security.py help' for available commands")
    else:
        # Default: run security checklist
        security_checklist()

if __name__ == "__main__":
    main()