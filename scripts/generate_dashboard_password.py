#!/usr/bin/env python3
"""
Generate Dashboard Password Hash

This script helps generate a secure password hash for the dashboard authentication.
"""

import hashlib
import secrets
import getpass
import sys

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_jwt_secret() -> str:
    """Generate a secure JWT secret"""
    return secrets.token_urlsafe(32)

def main():
    print("🔐 MYTA Dashboard Password Setup")
    print("=" * 40)
    
    # Get password from user
    while True:
        password = getpass.getpass("Enter dashboard password: ")
        if len(password) < 8:
            print("❌ Password must be at least 8 characters long")
            continue
        
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("❌ Passwords don't match")
            continue
        
        break
    
    # Generate hash
    password_hash = hash_password(password)
    jwt_secret = generate_jwt_secret()
    
    print("\n✅ Generated secure credentials:")
    print("-" * 40)
    print(f"DASHBOARD_PASSWORD_HASH={password_hash}")
    print(f"DASHBOARD_JWT_SECRET={jwt_secret}")
    
    print("\n📋 Add these to your environment:")
    print("-" * 40)
    print("# For .env file:")
    print(f"DASHBOARD_PASSWORD_HASH={password_hash}")
    print(f"DASHBOARD_JWT_SECRET={jwt_secret}")
    
    print("\n# For shell export:")
    print(f"export DASHBOARD_PASSWORD_HASH='{password_hash}'")
    print(f"export DASHBOARD_JWT_SECRET='{jwt_secret}'")
    
    print("\n# For Vercel deployment:")
    print(f"vercel env add DASHBOARD_PASSWORD_HASH")
    print(f"vercel env add DASHBOARD_JWT_SECRET")
    
    print("\n🔒 Keep these credentials secure and never commit them to version control!")

if __name__ == "__main__":
    main()
