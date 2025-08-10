#!/usr/bin/env python3
"""
Generate secure keys for Vidalytics
Run this script to generate new secure keys for your .env file
"""

import secrets
import sys


def generate_secure_key(length=64):
    """Generate a secure random key"""
    return secrets.token_urlsafe(length)


def main():
    print("\n" + "="*60)
    print("🔐 SECURE KEY GENERATOR FOR VIDALYTICS")
    print("="*60)
    
    print("\n📝 Copy these keys to your .env file:\n")
    
    boss_key = generate_secure_key()
    session_key = generate_secure_key()
    
    print(f"BOSS_AGENT_SECRET_KEY={boss_key}")
    print(f"SESSION_SECRET_KEY={session_key}")
    
    print("\n⚠️  IMPORTANT:")
    print("  1. Never commit these keys to version control")
    print("  2. Use different keys for production")
    print("  3. Store production keys in a secure vault")
    print("  4. Rotate keys periodically")
    
    print("\n✅ Keys generated successfully!")
    print("="*60 + "\n")
    
    # Ask if user wants to update .env automatically
    response = input("Would you like to update your .env file automatically? (y/n): ")
    
    if response.lower() == 'y':
        try:
            import os
            env_path = os.path.join(os.path.dirname(__file__), '.env')
            
            # Read existing .env
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            # Update the keys
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('BOSS_AGENT_SECRET_KEY='):
                    lines[i] = f'BOSS_AGENT_SECRET_KEY={boss_key}\n'
                    updated = True
                elif line.startswith('SESSION_SECRET_KEY='):
                    lines[i] = f'SESSION_SECRET_KEY={session_key}\n'
                    updated = True
            
            # Write back
            if updated:
                with open(env_path, 'w') as f:
                    f.writelines(lines)
                print("✅ .env file updated successfully!")
            else:
                print("❌ Could not find keys in .env file. Please update manually.")
                
        except FileNotFoundError:
            print("❌ .env file not found. Please create it from .env.example first.")
        except Exception as e:
            print(f"❌ Error updating .env: {e}")
            print("Please update the file manually with the keys shown above.")
    else:
        print("\n👉 Please copy the keys above and update your .env file manually.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())