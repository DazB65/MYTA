#!/usr/bin/env python3
"""
Production Environment Setup Script

This script helps set up environment variables for production deployment.
It generates secure credentials and provides deployment instructions.
"""

import hashlib
import secrets
import getpass
import sys
import os
from pathlib import Path

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_secure_key() -> str:
    """Generate a secure random key"""
    return secrets.token_urlsafe(32)

def setup_dashboard_auth():
    """Set up dashboard authentication credentials"""
    print("\n🔐 Dashboard Authentication Setup")
    print("-" * 40)
    
    while True:
        password = getpass.getpass("Enter secure dashboard password: ")
        if len(password) < 12:
            print("❌ Password must be at least 12 characters long for production")
            continue
        
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("❌ Passwords don't match")
            continue
        
        break
    
    password_hash = hash_password(password)
    jwt_secret = generate_secure_key()
    
    return {
        'DASHBOARD_PASSWORD_HASH': password_hash,
        'DASHBOARD_JWT_SECRET': jwt_secret
    }

def setup_security_keys():
    """Set up security keys"""
    print("\n🔑 Security Keys Setup")
    print("-" * 40)
    
    return {
        'BOSS_AGENT_SECRET_KEY': generate_secure_key(),
        'SESSION_SECRET_KEY': generate_secure_key()
    }

def get_api_keys():
    """Get API keys from user"""
    print("\n🔌 API Keys Setup")
    print("-" * 40)
    print("Enter your API keys (press Enter to skip):")
    
    api_keys = {}
    
    # OpenAI
    openai_key = getpass.getpass("OpenAI API Key: ").strip()
    if openai_key:
        api_keys['OPENAI_API_KEY'] = openai_key
    
    # Google/YouTube
    google_key = getpass.getpass("Google API Key: ").strip()
    if google_key:
        api_keys['GOOGLE_API_KEY'] = google_key
        api_keys['YOUTUBE_API_KEY'] = google_key
    
    # OAuth
    google_client_id = input("Google OAuth Client ID: ").strip()
    if google_client_id:
        api_keys['GOOGLE_CLIENT_ID'] = google_client_id
    
    google_client_secret = getpass.getpass("Google OAuth Client Secret: ").strip()
    if google_client_secret:
        api_keys['GOOGLE_CLIENT_SECRET'] = google_client_secret
    
    return api_keys

def generate_env_file(env_vars: dict, filename: str = ".env.production"):
    """Generate environment file"""
    env_path = Path(filename)
    
    content = f"""# MYTA Production Environment Variables
# Generated on {os.popen('date').read().strip()}
# 
# ⚠️  CRITICAL: Keep this file secure and never commit to version control!

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

# Security Keys
"""
    
    for key, value in env_vars.items():
        content += f"{key}={value}\n"
    
    content += """
# Database (update with your production database URL)
DATABASE_URL=sqlite:///./Vidalytics.db

# CORS (update with your production domains)
CORS_ORIGINS=["https://yourdomain.com"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=500
"""
    
    with open(env_path, 'w') as f:
        f.write(content)
    
    return env_path

def print_deployment_instructions(env_vars: dict):
    """Print deployment instructions"""
    print("\n🚀 Deployment Instructions")
    print("=" * 50)
    
    print("\n📋 For Vercel deployment:")
    print("-" * 30)
    for key, value in env_vars.items():
        print(f"vercel env add {key}")
        print(f"# Enter: {value}")
    
    print("\n📋 For Docker deployment:")
    print("-" * 30)
    for key, value in env_vars.items():
        print(f"export {key}='{value}'")
    
    print("\n📋 For Kubernetes deployment:")
    print("-" * 30)
    print("kubectl create secret generic myta-secrets \\")
    for key, value in env_vars.items():
        print(f"  --from-literal={key}='{value}' \\")
    print("  --dry-run=client -o yaml > myta-secrets.yaml")

def main():
    """Main setup function"""
    print("🎯 MYTA Production Environment Setup")
    print("=" * 50)
    print("This script will help you set up secure environment variables for production.")
    print("⚠️  All generated credentials will be displayed only once - save them securely!")
    
    # Collect all environment variables
    env_vars = {}
    
    # Dashboard authentication
    dashboard_vars = setup_dashboard_auth()
    env_vars.update(dashboard_vars)
    
    # Security keys
    security_vars = setup_security_keys()
    env_vars.update(security_vars)
    
    # API keys
    api_vars = get_api_keys()
    env_vars.update(api_vars)
    
    # Generate .env file
    print("\n📄 Generating environment file...")
    env_file = generate_env_file(env_vars)
    print(f"✅ Created {env_file}")
    
    # Show deployment instructions
    print_deployment_instructions(env_vars)
    
    print(f"\n✅ Production environment setup complete!")
    print(f"📁 Environment file saved to: {env_file}")
    print(f"🔒 Keep these credentials secure and never commit them to version control!")
    print(f"🗑️  Delete {env_file} after deploying to production!")

if __name__ == "__main__":
    main()
