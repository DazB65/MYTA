#!/usr/bin/env python3
"""
Environment Setup Script for Vidalytics
Helps set up the proper environment configuration
"""

import os
import sys
import secrets
import argparse
from pathlib import Path

def generate_secret_key(length: int = 64) -> str:
    """Generate a cryptographically secure secret key"""
    return secrets.token_urlsafe(length)

def create_env_local():
    """Create .env.local file with generated secrets"""
    env_local_path = Path(".env.local")
    
    if env_local_path.exists():
        response = input(".env.local already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping .env.local creation")
            return
    
    # Generate secure keys
    boss_agent_secret = generate_secret_key(64)
    session_secret = generate_secret_key(32)
    
    content = f"""# Local Environment Secrets (NEVER COMMIT THIS FILE)
# Generated automatically by setup-environment.py

# =================================================================
# CRITICAL: THIS FILE CONTAINS SECRETS - NEVER COMMIT TO GIT
# =================================================================

# AI Service API Keys (REPLACE WITH YOUR ACTUAL KEYS)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  
GOOGLE_API_KEY=your_google_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here

# OAuth Configuration (REPLACE WITH YOUR ACTUAL VALUES)
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Security Keys (GENERATED - DO NOT CHANGE UNLESS NECESSARY)
BOSS_AGENT_SECRET_KEY={boss_agent_secret}
SESSION_SECRET_KEY={session_secret}

# Database URL (Optional - uncomment to override)
# DATABASE_URL=postgresql://user:password@localhost:5432/Vidalytics
"""
    
    with open(env_local_path, "w") as f:
        f.write(content)
    
    print("✅ Created .env.local with generated secrets")
    print("⚠️  IMPORTANT: Replace API key placeholders with your actual keys")
    print("🔒 This file is automatically added to .gitignore")

def update_gitignore():
    """Ensure .env.local is in .gitignore"""
    gitignore_path = Path(".gitignore")
    
    # Read existing .gitignore
    gitignore_content = ""
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            gitignore_content = f.read()
    
    # Check if .env.local is already ignored
    env_patterns = [".env.local", "*.env.local", ".env.*.local"]
    
    needs_update = False
    for pattern in env_patterns:
        if pattern not in gitignore_content:
            gitignore_content += f"\n{pattern}"
            needs_update = True
    
    if needs_update:
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        print("✅ Updated .gitignore to exclude .env.local")
    else:
        print("✅ .gitignore already excludes .env.local")

def validate_environment(env_name: str):
    """Validate that environment files exist"""
    env_file = Path(f".env.{env_name}")
    
    if not env_file.exists():
        print(f"❌ Environment file .env.{env_name} not found")
        return False
    
    print(f"✅ Environment file .env.{env_name} exists")
    return True

def check_dependencies():
    """Check if required Python packages are installed"""
    required_imports = [
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'), 
        ('pydantic', 'pydantic'),
        ('python-dotenv', 'dotenv'),
        ('pydantic-settings', 'pydantic_settings')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_imports:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All required packages are installed")
    return True

def setup_environment(env_name: str):
    """Set up environment for specific stage"""
    print(f"🚀 Setting up {env_name} environment...")
    
    # Validate environment exists
    if not validate_environment(env_name):
        print(f"Please create .env.{env_name} first")
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Create .env.local for secrets
    create_env_local()
    
    # Update .gitignore
    update_gitignore()
    
    # Set environment variable
    os.environ['ENVIRONMENT'] = env_name
    
    print(f"✅ Environment setup complete for {env_name}")
    print(f"\nTo run the application:")
    print(f"export ENVIRONMENT={env_name}")
    print(f"cd backend && uvicorn main:app --reload")
    
    return True

def test_configuration():
    """Test configuration loading"""
    print("🧪 Testing configuration loading...")
    
    try:
        # Add backend to path
        sys.path.insert(0, str(Path(__file__).parent / "backend"))
        
        from config import load_environment_config
        
        settings = load_environment_config()
        
        print(f"✅ Configuration loaded successfully")
        print(f"   Environment: {settings.environment}")
        print(f"   Debug: {settings.debug}")
        print(f"   Database: {settings.database_url}")
        print(f"   CORS Origins: {settings.cors_origins}")
        
        # Check for missing API keys
        api_keys = {
            'OpenAI': settings.openai_api_key,
            'Google': settings.google_api_key,
            'YouTube': settings.youtube_api_key,
            'Boss Agent Secret': settings.boss_agent_secret_key
        }
        
        missing_keys = [name for name, key in api_keys.items() if not key or key.endswith('_here')]
        
        if missing_keys:
            print(f"⚠️  Missing API keys: {', '.join(missing_keys)}")
            print("   Update .env.local with your actual API keys")
        else:
            print("✅ All API keys configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description="Set up Vidalytics environment")
    parser.add_argument(
        'environment', 
        choices=['development', 'staging', 'production'],
        help='Environment to set up'
    )
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Test configuration after setup'
    )
    
    args = parser.parse_args()
    
    print("🎯 Vidalytics Environment Setup")
    print("=" * 40)
    
    # Setup environment
    success = setup_environment(args.environment)
    
    if success and args.test:
        print("\n" + "=" * 40)
        test_configuration()
    
    if success:
        print("\n🎉 Setup complete! Your environment is ready.")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()