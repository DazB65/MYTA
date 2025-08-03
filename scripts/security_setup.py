#!/usr/bin/env python3
"""
Security Setup Script for Vidalytics
Helps users properly configure their environment variables and security settings
"""

import os
import secrets
import sys
from pathlib import Path

def generate_secure_key(length: int = 64) -> str:
    """Generate a secure random key"""
    return secrets.token_urlsafe(length)

def check_env_file():
    """Check if .env file exists and has proper configuration"""
    env_path = Path("backend/.env")
    
    if not env_path.exists():
        print("❌ No .env file found in backend/ directory")
        print("Please create one from .env.example")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Check for placeholder values
    placeholder_indicators = [
        "your_api_key_here",
        "your_openai_api_key_here",
        "your_anthropic_api_key_here",
        "your_google_api_key_here",
        "your_youtube_api_key_here",
        "your_google_client_id_here",
        "your_google_client_secret_here",
        "generate_secure_random_key_here"
    ]
    
    issues = []
    for indicator in placeholder_indicators:
        if indicator in content:
            issues.append(f"Found placeholder: {indicator}")
    
    if issues:
        print("⚠️  .env file contains placeholder values:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    print("✅ .env file appears to be properly configured")
    return True

def create_secure_env_template():
    """Create a secure .env.example template"""
    template = """# Vidalytics Environment Configuration Template
# Copy this file to .env and fill in your actual API keys
# NEVER commit the .env file to version control

# Multi-Agent System API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
OAUTH_REDIRECT_URI=http://localhost:8888/auth/callback

# YouTube Data API v3
YOUTUBE_API_KEY=your_youtube_api_key_here
YT_API_KEY=your_youtube_api_key_here

# Security Keys (generate secure random keys)
BOSS_AGENT_SECRET_KEY=generate_secure_random_key_here
SESSION_SECRET_KEY=generate_secure_random_key_here

# Supabase Configuration
VITE_SUPABASE_URL=your_supabase_url_here
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Agent System Configuration
AGENT_CACHE_SIZE=5000
AGENT_CACHE_TTL=7200
MAX_CONCURRENT_AGENTS=10
API_RATE_LIMIT=100

# Environment Configuration
ENVIRONMENT=development
DEBUG=false
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=sqlite:///./Vidalytics.db
DATABASE_ECHO=false

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000"]

# Security Configuration
SECURITY_HEADERS_STRICT=true
CSRF_PROTECTION_STRICT=true

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_BURST=20

# Backup Configuration
BACKUP_FREQUENCY=daily
BACKUP_TIME=02:00
BACKUP_COMPRESSION=true
BACKUP_MAX_COUNT=7
BACKUP_CLEANUP_ENABLED=true
BACKUP_DIRECTORY=./backups
"""
    
    example_path = Path("backend/.env.example")
    with open(example_path, 'w') as f:
        f.write(template)
    
    print(f"✅ Created secure .env.example template at {example_path}")

def generate_secure_keys():
    """Generate secure keys for the user"""
    print("\n🔐 Generating secure keys...")
    
    boss_secret = generate_secure_key(64)
    session_secret = generate_secure_key(64)
    
    print("Generated secure keys:")
    print(f"BOSS_AGENT_SECRET_KEY={boss_secret}")
    print(f"SESSION_SECRET_KEY={session_secret}")
    print("\n⚠️  IMPORTANT: Copy these keys to your .env file and keep them secure!")

def check_git_status():
    """Check if .env file is being tracked by git"""
    import subprocess
    
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "backend/.env"],
            capture_output=True,
            text=True,
            cwd="."
        )
        
        if result.stdout.strip():
            print("❌ .env file is being tracked by git!")
            print("This is a security risk. Please remove it from tracking:")
            print("   git rm --cached backend/.env")
            print("   git commit -m 'Remove .env file from tracking'")
            return False
        else:
            print("✅ .env file is not tracked by git (good!)")
            return True
    except FileNotFoundError:
        print("⚠️  Git not found, cannot check .env tracking status")
        return True

def main():
    """Main security setup function"""
    print("🔒 Vidalytics Security Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("backend").exists():
        print("❌ Please run this script from the Vidalytics root directory")
        sys.exit(1)
    
    # Check git status
    git_ok = check_git_status()
    
    # Check .env file
    env_ok = check_env_file()
    
    # Create secure template
    create_secure_env_template()
    
    # Generate secure keys
    generate_secure_keys()
    
    print("\n" + "=" * 40)
    print("🔒 Security Setup Summary")
    print("=" * 40)
    
    if not git_ok:
        print("❌ CRITICAL: .env file is tracked by git - fix this immediately!")
    
    if not env_ok:
        print("⚠️  .env file needs configuration - update with real API keys")
    
    print("\n📋 Next Steps:")
    print("1. Update your .env file with real API keys")
    print("2. Replace placeholder secret keys with the generated ones")
    print("3. Set ENVIRONMENT=production for production deployments")
    print("4. Update CORS_ORIGINS with your actual domain")
    print("5. Consider using a secrets management service for production")
    
    print("\n🔗 API Key Sources:")
    print("- OpenAI: https://platform.openai.com/api-keys")
    print("- Anthropic: https://console.anthropic.com/")
    print("- Google: https://console.cloud.google.com/")
    print("- YouTube: https://console.cloud.google.com/apis/credentials")

if __name__ == "__main__":
    main() 