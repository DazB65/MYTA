#!/usr/bin/env python3
"""
Simple script to update OAuth credentials in .env file
Usage: python3 update_oauth_credentials.py "YOUR_CLIENT_ID" "YOUR_CLIENT_SECRET"
"""

import sys
import re
from pathlib import Path

def update_oauth_credentials(client_id, client_secret):
    """Update OAuth credentials in .env file"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        return False
    
    # Read current content
    content = env_path.read_text()
    
    # Update GOOGLE_CLIENT_ID
    content = re.sub(
        r'^GOOGLE_CLIENT_ID=.*$', 
        f'GOOGLE_CLIENT_ID={client_id}', 
        content, 
        flags=re.MULTILINE
    )
    
    # Update GOOGLE_CLIENT_SECRET
    content = re.sub(
        r'^GOOGLE_CLIENT_SECRET=.*$', 
        f'GOOGLE_CLIENT_SECRET={client_secret}', 
        content, 
        flags=re.MULTILINE
    )
    
    # Write back
    env_path.write_text(content)
    
    print("✅ Updated OAuth credentials in .env file")
    print(f"   Client ID: {client_id[:20]}...")
    print(f"   Client Secret: {client_secret[:15]}...")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 update_oauth_credentials.py \"YOUR_CLIENT_ID\" \"YOUR_CLIENT_SECRET\"")
        print()
        print("Example:")
        print('python3 update_oauth_credentials.py "123456-abc.apps.googleusercontent.com" "GOCSPX-abc123"')
        sys.exit(1)
    
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    
    # Basic validation
    if not client_id.endswith('.apps.googleusercontent.com'):
        print("❌ Invalid Client ID format")
        sys.exit(1)
    
    if not client_secret.startswith('GOCSPX-'):
        print("❌ Invalid Client Secret format")
        sys.exit(1)
    
    if update_oauth_credentials(client_id, client_secret):
        print()
        print("🔄 Next steps:")
        print("1. Restart your Vidalytics server")
        print("2. Try connecting your YouTube account again")
        sys.exit(0)
    else:
        sys.exit(1)