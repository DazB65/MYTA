#!/usr/bin/env python3
"""
Google OAuth 2.0 Setup Script for Vidalytics
This script helps configure Google OAuth credentials for YouTube Data API access.
"""

import os
import sys
import re
from pathlib import Path

def print_header():
    print("🔐 Vidalytics Google OAuth Setup")
    print("=" * 50)
    print()

def print_instructions():
    print("📋 Follow these steps to set up Google OAuth:")
    print()
    
    print("1. 🌐 Go to Google Cloud Console:")
    print("   https://console.cloud.google.com/")
    print()
    
    print("2. 📁 Create or select a project:")
    print("   - Click 'Select a project' → 'New Project'")
    print("   - Name: 'Vidalytics YouTube API'")
    print("   - Click 'Create'")
    print()
    
    print("3. 🔌 Enable YouTube Data API v3:")
    print("   - Go to 'APIs & Services' → 'Library'")
    print("   - Search for 'YouTube Data API v3'")
    print("   - Click on it and press 'Enable'")
    print()
    
    print("4. 🛡️ Configure OAuth consent screen:")
    print("   - Go to 'APIs & Services' → 'OAuth consent screen'")
    print("   - Choose 'External' user type")
    print("   - Fill in required fields:")
    print("     * App name: Vidalytics")
    print("     * User support email: your email")
    print("     * Developer contact: your email")
    print("   - Add scopes:")
    print("     * https://www.googleapis.com/auth/youtube.readonly")
    print("     * https://www.googleapis.com/auth/yt-analytics.readonly")
    print("     * https://www.googleapis.com/auth/yt-analytics-monetary.readonly")
    print("   - Add your email as a test user")
    print()
    
    print("5. 🔑 Create OAuth 2.0 credentials:")
    print("   - Go to 'APIs & Services' → 'Credentials'")
    print("   - Click '+ Create Credentials' → 'OAuth 2.0 Client IDs'")
    print("   - Application type: 'Web application'")
    print("   - Name: 'Vidalytics Local Development'")
    print("   - Authorized redirect URIs:")
    print("     * http://localhost:8888/auth/callback")
    print("   - Click 'Create'")
    print()
    
    print("6. 📋 Copy the credentials:")
    print("   - Copy the 'Client ID' and 'Client Secret'")
    print("   - You'll enter them below")
    print()

def validate_client_id(client_id):
    """Validate Google Client ID format"""
    pattern = r'^\d+-[a-zA-Z0-9]+\.apps\.googleusercontent\.com$'
    return re.match(pattern, client_id) is not None

def validate_client_secret(client_secret):
    """Validate Google Client Secret format"""
    pattern = r'^GOCSPX-[a-zA-Z0-9_-]+$'
    return re.match(pattern, client_secret) is not None

def get_credentials():
    """Get OAuth credentials from user input"""
    print("🔑 Enter your Google OAuth credentials:")
    print()
    
    while True:
        client_id = input("Google Client ID: ").strip()
        if not client_id:
            print("❌ Client ID cannot be empty")
            continue
        if not validate_client_id(client_id):
            print("❌ Invalid Client ID format. Should look like: 123456789-abc123.apps.googleusercontent.com")
            continue
        break
    
    while True:
        client_secret = input("Google Client Secret: ").strip()
        if not client_secret:
            print("❌ Client Secret cannot be empty")
            continue
        if not validate_client_secret(client_secret):
            print("❌ Invalid Client Secret format. Should look like: GOCSPX-abc123_def456")
            continue
        break
    
    return client_id, client_secret

def update_env_file(client_id, client_secret):
    """Update .env file with new OAuth credentials"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found. Creating new one...")
        env_content = ""
    else:
        env_content = env_path.read_text()
    
    # Update or add OAuth credentials
    oauth_lines = [
        "# Google OAuth 2.0 Configuration",
        f"GOOGLE_CLIENT_ID={client_id}",
        f"GOOGLE_CLIENT_SECRET={client_secret}",
        "OAUTH_REDIRECT_URI=http://localhost:8888/auth/callback"
    ]
    
    # Remove existing OAuth config
    lines = env_content.split('\n')
    new_lines = []
    in_oauth_section = False
    
    for line in lines:
        if line.strip() == "# Google OAuth 2.0 Configuration":
            in_oauth_section = True
            continue
        elif line.startswith("GOOGLE_CLIENT_ID=") or line.startswith("GOOGLE_CLIENT_SECRET=") or line.startswith("OAUTH_REDIRECT_URI="):
            continue
        elif in_oauth_section and line.strip() == "":
            in_oauth_section = False
            new_lines.append(line)
        else:
            new_lines.append(line)
    
    # Add new OAuth config
    if new_lines and new_lines[-1].strip():
        new_lines.append("")
    new_lines.extend(oauth_lines)
    new_lines.append("")
    
    # Write back to file
    env_path.write_text('\n'.join(new_lines))
    print(f"✅ Updated {env_path.absolute()}")

def test_credentials(client_id, client_secret):
    """Test the OAuth credentials"""
    print()
    print("🧪 Testing OAuth credentials...")
    
    try:
        import requests
        
        # Test if the client ID is valid by checking the discovery document
        response = requests.get(
            "https://oauth2.googleapis.com/token",
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "code": "invalid_code_for_testing",
                "redirect_uri": "http://localhost:8888/auth/callback"
            },
            timeout=10
        )
        
        if response.status_code == 400:
            error_data = response.json()
            if error_data.get("error") == "invalid_grant":
                print("✅ OAuth credentials format is valid")
                return True
            elif error_data.get("error") == "invalid_client":
                print("❌ Invalid client credentials")
                return False
        
        print("⚠️ Unexpected response from Google OAuth")
        return False
        
    except ImportError:
        print("⚠️ requests library not available - skipping credential test")
        return True
    except Exception as e:
        print(f"⚠️ Error testing credentials: {e}")
        return True

def main():
    """Main setup function"""
    print_header()
    
    print("Choose an option:")
    print("1. 📖 Show setup instructions")
    print("2. 🔑 Enter OAuth credentials")
    print("3. 🚀 Both (recommended)")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice in ["1", "3"]:
        print_instructions()
        if choice == "1":
            return
    
    if choice in ["2", "3"]:
        print("=" * 50)
        client_id, client_secret = get_credentials()
        
        print()
        print("🔄 Updating .env file...")
        update_env_file(client_id, client_secret)
        
        test_credentials(client_id, client_secret)
        
        print()
        print("✅ OAuth setup complete!")
        print()
        print("🔄 Next steps:")
        print("1. Restart your Vidalytics server")
        print("2. Try connecting your YouTube account again")
        print("3. Check the OAuth status in Settings")
        print()

if __name__ == "__main__":
    main()