#!/usr/bin/env python3
"""
API Key Rotation Script for MYTA Application
Automates the process of rotating API keys for security compliance
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import subprocess
import shutil
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('key_rotation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class APIKeyRotator:
    """Handles API key rotation for various services"""
    
    def __init__(self, env_file: str = ".env", backup_dir: str = "backups/keys"):
        self.env_file = env_file
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Services that support automated key rotation
        self.rotatable_services = {
            'openai': {
                'env_var': 'OPENAI_API_KEY',
                'rotation_method': self._rotate_openai_key,
                'validation_method': self._validate_openai_key
            },
            'anthropic': {
                'env_var': 'ANTHROPIC_API_KEY',
                'rotation_method': self._rotate_anthropic_key,
                'validation_method': self._validate_anthropic_key
            },
            'google': {
                'env_var': 'GOOGLE_API_KEY',
                'rotation_method': self._rotate_google_key,
                'validation_method': self._validate_google_key
            },
            'youtube': {
                'env_var': 'YOUTUBE_API_KEY',
                'rotation_method': self._rotate_youtube_key,
                'validation_method': self._validate_youtube_key
            }
        }
        
        # Internal keys that can be regenerated
        self.regeneratable_keys = {
            'boss_agent_secret': 'BOSS_AGENT_SECRET_KEY',
            'session_secret': 'SESSION_SECRET_KEY'
        }
    
    def backup_current_keys(self) -> str:
        """Create a backup of current environment file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"env_backup_{timestamp}.env"
        
        if os.path.exists(self.env_file):
            shutil.copy2(self.env_file, backup_file)
            logger.info(f"Created backup: {backup_file}")
            return str(backup_file)
        else:
            logger.warning(f"Environment file {self.env_file} not found")
            return ""
    
    def load_env_vars(self) -> Dict[str, str]:
        """Load environment variables from .env file"""
        env_vars = {}
        
        if not os.path.exists(self.env_file):
            logger.error(f"Environment file {self.env_file} not found")
            return env_vars
        
        with open(self.env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        
        return env_vars
    
    def save_env_vars(self, env_vars: Dict[str, str]) -> bool:
        """Save environment variables back to .env file"""
        try:
            # Read the original file to preserve comments and structure
            lines = []
            if os.path.exists(self.env_file):
                with open(self.env_file, 'r') as f:
                    lines = f.readlines()
            
            # Update existing variables and preserve structure
            updated_lines = []
            updated_vars = set()
            
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and '=' in stripped:
                    key = stripped.split('=', 1)[0].strip()
                    if key in env_vars:
                        updated_lines.append(f"{key}={env_vars[key]}\n")
                        updated_vars.add(key)
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            
            # Add any new variables
            for key, value in env_vars.items():
                if key not in updated_vars:
                    updated_lines.append(f"{key}={value}\n")
            
            # Write back to file
            with open(self.env_file, 'w') as f:
                f.writelines(updated_lines)
            
            logger.info(f"Updated environment file: {self.env_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save environment variables: {e}")
            return False
    
    def generate_secure_key(self, length: int = 64) -> str:
        """Generate a secure random key"""
        import secrets
        return secrets.token_urlsafe(length)
    
    def rotate_internal_keys(self) -> Dict[str, str]:
        """Rotate internal application keys"""
        logger.info("Rotating internal keys...")
        
        env_vars = self.load_env_vars()
        rotated_keys = {}
        
        for key_name, env_var in self.regeneratable_keys.items():
            old_key = env_vars.get(env_var, '')
            new_key = self.generate_secure_key()
            
            env_vars[env_var] = new_key
            rotated_keys[env_var] = {
                'old': old_key[:10] + '...' if old_key else 'None',
                'new': new_key[:10] + '...',
                'rotated_at': datetime.now().isoformat()
            }
            
            logger.info(f"Rotated {env_var}")
        
        if self.save_env_vars(env_vars):
            return rotated_keys
        else:
            logger.error("Failed to save rotated internal keys")
            return {}
    
    def _rotate_openai_key(self, current_key: str) -> Optional[str]:
        """Rotate OpenAI API key (manual process - returns instructions)"""
        logger.warning("OpenAI key rotation requires manual intervention")
        logger.info("Steps to rotate OpenAI key:")
        logger.info("1. Go to https://platform.openai.com/api-keys")
        logger.info("2. Create a new API key")
        logger.info("3. Update the OPENAI_API_KEY in your environment")
        logger.info("4. Delete the old key from OpenAI dashboard")
        return None
    
    def _validate_openai_key(self, api_key: str) -> bool:
        """Validate OpenAI API key"""
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            # Test with a simple API call
            response = client.models.list()
            return True
        except Exception as e:
            logger.error(f"OpenAI key validation failed: {e}")
            return False
    
    def _rotate_anthropic_key(self, current_key: str) -> Optional[str]:
        """Rotate Anthropic API key (manual process)"""
        logger.warning("Anthropic key rotation requires manual intervention")
        logger.info("Steps to rotate Anthropic key:")
        logger.info("1. Go to https://console.anthropic.com/")
        logger.info("2. Create a new API key")
        logger.info("3. Update the ANTHROPIC_API_KEY in your environment")
        logger.info("4. Delete the old key from Anthropic console")
        return None
    
    def _validate_anthropic_key(self, api_key: str) -> bool:
        """Validate Anthropic API key"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            # Test with a simple API call (this might fail but will validate the key format)
            return api_key.startswith('sk-ant-api03-')
        except Exception as e:
            logger.error(f"Anthropic key validation failed: {e}")
            return False
    
    def _rotate_google_key(self, current_key: str) -> Optional[str]:
        """Rotate Google API key (manual process)"""
        logger.warning("Google API key rotation requires manual intervention")
        logger.info("Steps to rotate Google API key:")
        logger.info("1. Go to https://console.cloud.google.com/apis/credentials")
        logger.info("2. Create a new API key")
        logger.info("3. Update the GOOGLE_API_KEY in your environment")
        logger.info("4. Delete the old key from Google Cloud Console")
        return None
    
    def _validate_google_key(self, api_key: str) -> bool:
        """Validate Google API key"""
        # Basic format validation
        return len(api_key) > 30 and api_key.startswith('AIza')
    
    def _rotate_youtube_key(self, current_key: str) -> Optional[str]:
        """Rotate YouTube API key (usually same as Google API key)"""
        return self._rotate_google_key(current_key)
    
    def _validate_youtube_key(self, api_key: str) -> bool:
        """Validate YouTube API key"""
        return self._validate_google_key(api_key)
    
    def create_rotation_report(self, rotated_keys: Dict[str, any]) -> str:
        """Create a rotation report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.backup_dir / f"rotation_report_{timestamp}.json"
        
        report = {
            'rotation_timestamp': datetime.now().isoformat(),
            'rotated_keys': rotated_keys,
            'next_rotation_due': (datetime.now() + timedelta(days=90)).isoformat(),
            'backup_location': str(self.backup_dir)
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Rotation report saved: {report_file}")
        return str(report_file)
    
    def rotate_keys(self, services: List[str] = None, force: bool = False) -> Dict[str, any]:
        """Main method to rotate API keys"""
        logger.info("Starting API key rotation process...")
        
        # Create backup
        backup_file = self.backup_current_keys()
        
        results = {
            'backup_file': backup_file,
            'rotated_keys': {},
            'manual_rotation_required': [],
            'errors': []
        }
        
        try:
            # Always rotate internal keys
            internal_keys = self.rotate_internal_keys()
            results['rotated_keys'].update(internal_keys)
            
            # Handle external service keys
            if services is None:
                services = list(self.rotatable_services.keys())
            
            for service in services:
                if service in self.rotatable_services:
                    service_config = self.rotatable_services[service]
                    env_var = service_config['env_var']
                    
                    env_vars = self.load_env_vars()
                    current_key = env_vars.get(env_var, '')
                    
                    if current_key:
                        # For now, all external services require manual rotation
                        results['manual_rotation_required'].append({
                            'service': service,
                            'env_var': env_var,
                            'current_key_preview': current_key[:10] + '...' if current_key else 'None'
                        })
                        
                        # Call rotation method (which provides instructions)
                        service_config['rotation_method'](current_key)
                    else:
                        logger.warning(f"No key found for {service} ({env_var})")
            
            # Create rotation report
            report_file = self.create_rotation_report(results)
            results['report_file'] = report_file
            
            logger.info("Key rotation process completed")
            return results
            
        except Exception as e:
            logger.error(f"Key rotation failed: {e}")
            results['errors'].append(str(e))
            return results


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Rotate API keys for MYTA application")
    parser.add_argument('--services', nargs='+', help='Services to rotate keys for')
    parser.add_argument('--internal-only', action='store_true', help='Only rotate internal keys')
    parser.add_argument('--force', action='store_true', help='Force rotation even if not due')
    parser.add_argument('--env-file', default='.env', help='Environment file path')
    parser.add_argument('--backup-dir', default='backups/keys', help='Backup directory')
    
    args = parser.parse_args()
    
    rotator = APIKeyRotator(args.env_file, args.backup_dir)
    
    if args.internal_only:
        logger.info("Rotating internal keys only...")
        results = rotator.rotate_internal_keys()
        print(f"Rotated {len(results)} internal keys")
    else:
        services = args.services if args.services else None
        results = rotator.rotate_keys(services, args.force)
        
        print("\n=== Key Rotation Summary ===")
        print(f"Backup created: {results.get('backup_file', 'None')}")
        print(f"Internal keys rotated: {len(results.get('rotated_keys', {}))}")
        print(f"Manual rotation required: {len(results.get('manual_rotation_required', []))}")
        
        if results.get('manual_rotation_required'):
            print("\nServices requiring manual rotation:")
            for item in results['manual_rotation_required']:
                print(f"  - {item['service']}: {item['env_var']}")
        
        if results.get('errors'):
            print(f"\nErrors: {len(results['errors'])}")
            for error in results['errors']:
                print(f"  - {error}")
        
        print(f"\nReport saved: {results.get('report_file', 'None')}")


if __name__ == "__main__":
    main()
