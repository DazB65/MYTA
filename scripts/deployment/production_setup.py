#!/usr/bin/env python3
"""
Production Setup Script for MYTA Application
Validates and configures production environment
"""

import os
import sys
import json
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import secrets
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ProductionSetup:
    """Handles production environment setup and validation"""
    
    def __init__(self, env_file: str = ".env.production"):
        self.env_file = env_file
        self.required_vars = {
            # Critical security variables
            'BOSS_AGENT_SECRET_KEY': {'type': 'secret', 'min_length': 32},
            'SESSION_SECRET_KEY': {'type': 'secret', 'min_length': 32},
            'ENCRYPTION_KEY': {'type': 'secret', 'min_length': 32},
            
            # Database
            'DATABASE_URL': {'type': 'url', 'required': True},
            'REDIS_URL': {'type': 'url', 'required': True},
            
            # API Keys
            'OPENAI_API_KEY': {'type': 'api_key', 'required': True},
            'ANTHROPIC_API_KEY': {'type': 'api_key', 'required': True},
            'GOOGLE_API_KEY': {'type': 'api_key', 'required': True},
            
            # OAuth
            'GOOGLE_CLIENT_ID': {'type': 'oauth', 'required': True},
            'GOOGLE_CLIENT_SECRET': {'type': 'oauth', 'required': True},
            
            # Supabase
            'VITE_SUPABASE_URL': {'type': 'url', 'required': True},
            'VITE_SUPABASE_ANON_KEY': {'type': 'api_key', 'required': True},
            
            # Security
            'CORS_ORIGINS': {'type': 'json_array', 'required': True},
            'OAUTH_REDIRECT_URI': {'type': 'url', 'required': True},
            
            # Environment
            'ENVIRONMENT': {'type': 'string', 'required': True, 'valid_values': ['production']},
            'DEBUG': {'type': 'boolean', 'required': True, 'valid_values': ['false']},
        }
        
        self.optional_vars = {
            # SSL/TLS
            'SSL_CERT_PATH': {'type': 'file_path'},
            'SSL_KEY_PATH': {'type': 'file_path'},
            
            # Monitoring
            'SENTRY_DSN': {'type': 'url'},
            'DATADOG_API_KEY': {'type': 'api_key'},
            
            # Alerting
            'SLACK_WEBHOOK_URL': {'type': 'url'},
            'ALERT_EMAIL_TO': {'type': 'email_list'},
        }
    
    def generate_secure_key(self, length: int = 32) -> str:
        """Generate a secure random key"""
        return secrets.token_urlsafe(length)
    
    def generate_encryption_key(self) -> str:
        """Generate a base64-encoded encryption key"""
        key = secrets.token_bytes(32)  # 256-bit key
        return base64.urlsafe_b64encode(key).decode()
    
    def validate_environment_variable(self, name: str, value: str, config: Dict) -> Tuple[bool, str]:
        """Validate a single environment variable"""
        var_type = config.get('type', 'string')
        
        # Check if required
        if config.get('required', False) and not value:
            return False, f"{name} is required but not set"
        
        if not value:
            return True, ""  # Optional variable not set
        
        # Type-specific validation
        if var_type == 'secret':
            min_length = config.get('min_length', 16)
            if len(value) < min_length:
                return False, f"{name} must be at least {min_length} characters long"
        
        elif var_type == 'url':
            if not (value.startswith('http://') or value.startswith('https://') or 
                   value.startswith('postgresql://') or value.startswith('redis://')):
                return False, f"{name} must be a valid URL"
        
        elif var_type == 'api_key':
            if len(value) < 10:
                return False, f"{name} appears to be too short for an API key"
        
        elif var_type == 'boolean':
            if value.lower() not in ['true', 'false']:
                return False, f"{name} must be 'true' or 'false'"
        
        elif var_type == 'json_array':
            try:
                parsed = json.loads(value)
                if not isinstance(parsed, list):
                    return False, f"{name} must be a JSON array"
            except json.JSONDecodeError:
                return False, f"{name} must be valid JSON"
        
        elif var_type == 'file_path':
            if not os.path.exists(value):
                return False, f"{name} file does not exist: {value}"
        
        elif var_type == 'email_list':
            emails = value.split(',')
            for email in emails:
                if '@' not in email.strip():
                    return False, f"{name} contains invalid email: {email.strip()}"
        
        # Check valid values
        valid_values = config.get('valid_values')
        if valid_values and value not in valid_values:
            return False, f"{name} must be one of: {', '.join(valid_values)}"
        
        return True, ""
    
    def load_environment_variables(self) -> Dict[str, str]:
        """Load environment variables from file"""
        env_vars = {}
        
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        
        # Also check actual environment variables
        for key in list(self.required_vars.keys()) + list(self.optional_vars.keys()):
            if key in os.environ:
                env_vars[key] = os.environ[key]
        
        return env_vars
    
    def validate_production_environment(self) -> Tuple[bool, List[str]]:
        """Validate production environment configuration"""
        logger.info("Validating production environment...")
        
        env_vars = self.load_environment_variables()
        errors = []
        warnings = []
        
        # Validate required variables
        for name, config in self.required_vars.items():
            value = env_vars.get(name, '')
            is_valid, error_msg = self.validate_environment_variable(name, value, config)
            
            if not is_valid:
                errors.append(error_msg)
        
        # Validate optional variables
        for name, config in self.optional_vars.items():
            value = env_vars.get(name, '')
            if value:  # Only validate if set
                is_valid, error_msg = self.validate_environment_variable(name, value, config)
                if not is_valid:
                    warnings.append(error_msg)
        
        # Additional production-specific checks
        
        # Check DEBUG is false
        if env_vars.get('DEBUG', '').lower() != 'false':
            errors.append("DEBUG must be set to 'false' in production")
        
        # Check ENVIRONMENT is production
        if env_vars.get('ENVIRONMENT', '') != 'production':
            errors.append("ENVIRONMENT must be set to 'production'")
        
        # Check CORS origins don't include localhost
        cors_origins = env_vars.get('CORS_ORIGINS', '[]')
        try:
            origins = json.loads(cors_origins)
            for origin in origins:
                if 'localhost' in origin or '127.0.0.1' in origin:
                    warnings.append(f"CORS origin contains localhost: {origin}")
        except json.JSONDecodeError:
            pass  # Already handled in validation
        
        # Check SSL configuration
        ssl_cert = env_vars.get('SSL_CERT_PATH', '')
        ssl_key = env_vars.get('SSL_KEY_PATH', '')
        if ssl_cert and not ssl_key:
            errors.append("SSL_KEY_PATH must be set if SSL_CERT_PATH is set")
        elif ssl_key and not ssl_cert:
            errors.append("SSL_CERT_PATH must be set if SSL_KEY_PATH is set")
        
        # Log results
        if errors:
            logger.error(f"Found {len(errors)} critical errors")
            for error in errors:
                logger.error(f"  - {error}")
        
        if warnings:
            logger.warning(f"Found {len(warnings)} warnings")
            for warning in warnings:
                logger.warning(f"  - {warning}")
        
        if not errors and not warnings:
            logger.info("✅ Production environment validation passed")
        
        return len(errors) == 0, errors + warnings
    
    def generate_production_secrets(self) -> Dict[str, str]:
        """Generate secure secrets for production"""
        logger.info("Generating production secrets...")
        
        secrets_generated = {
            'BOSS_AGENT_SECRET_KEY': self.generate_secure_key(32),
            'SESSION_SECRET_KEY': self.generate_secure_key(32),
            'ENCRYPTION_KEY': self.generate_encryption_key(),
            'ENCRYPTION_SALT': self.generate_secure_key(16),
        }
        
        logger.info(f"Generated {len(secrets_generated)} secure secrets")
        return secrets_generated
    
    def create_production_env_file(self, secrets: Dict[str, str] = None) -> str:
        """Create production environment file"""
        if secrets is None:
            secrets = self.generate_production_secrets()
        
        env_content = [
            "# MYTA Production Environment Configuration",
            "# Generated automatically - DO NOT COMMIT TO VERSION CONTROL",
            f"# Generated on: {os.popen('date').read().strip()}",
            "",
            "# Environment",
            "ENVIRONMENT=production",
            "DEBUG=false",
            "LOG_LEVEL=WARNING",
            "",
            "# Generated Secrets",
        ]
        
        for key, value in secrets.items():
            env_content.append(f"{key}={value}")
        
        env_content.extend([
            "",
            "# TODO: Configure the following variables for your production environment:",
            "# DATABASE_URL=postgresql://username:password@db-server:5432/myta_production",
            "# REDIS_URL=redis://username:password@redis-server:6379/0",
            "# OPENAI_API_KEY=your_openai_api_key",
            "# ANTHROPIC_API_KEY=your_anthropic_api_key",
            "# GOOGLE_API_KEY=your_google_api_key",
            "# GOOGLE_CLIENT_ID=your_google_client_id",
            "# GOOGLE_CLIENT_SECRET=your_google_client_secret",
            "# VITE_SUPABASE_URL=https://your-project.supabase.co",
            "# VITE_SUPABASE_ANON_KEY=your_supabase_anon_key",
            '# CORS_ORIGINS=["https://yourdomain.com"]',
            "# OAUTH_REDIRECT_URI=https://yourdomain.com/auth/callback",
            "",
        ])
        
        output_file = f"{self.env_file}.generated"
        with open(output_file, 'w') as f:
            f.write('\n'.join(env_content))
        
        logger.info(f"Created production environment template: {output_file}")
        return output_file
    
    def run_security_checks(self) -> bool:
        """Run additional security checks"""
        logger.info("Running security checks...")
        
        checks_passed = True
        
        # Check file permissions
        if os.path.exists(self.env_file):
            stat_info = os.stat(self.env_file)
            permissions = oct(stat_info.st_mode)[-3:]
            
            if permissions != '600':
                logger.warning(f"Environment file permissions are {permissions}, should be 600")
                logger.info(f"Run: chmod 600 {self.env_file}")
        
        # Check for common security issues
        env_vars = self.load_environment_variables()
        
        # Check for default/weak secrets
        weak_patterns = ['password', 'secret', 'key', 'default', 'admin', '123456']
        for name, value in env_vars.items():
            if any(pattern in value.lower() for pattern in weak_patterns):
                logger.warning(f"Variable {name} may contain weak/default value")
                checks_passed = False
        
        # Check for localhost in production URLs
        for name, value in env_vars.items():
            if 'localhost' in value or '127.0.0.1' in value:
                logger.warning(f"Variable {name} contains localhost: {value}")
        
        return checks_passed
    
    def setup_production_environment(self, generate_secrets: bool = False) -> bool:
        """Complete production environment setup"""
        logger.info("Setting up production environment...")
        
        success = True
        
        # Generate secrets if requested
        if generate_secrets:
            secrets = self.generate_production_secrets()
            env_file = self.create_production_env_file(secrets)
            logger.info(f"Generated production environment file: {env_file}")
            logger.warning("Remember to configure the remaining variables marked with TODO")
        
        # Validate environment
        is_valid, issues = self.validate_production_environment()
        if not is_valid:
            logger.error("Production environment validation failed")
            success = False
        
        # Run security checks
        security_ok = self.run_security_checks()
        if not security_ok:
            logger.warning("Some security checks failed")
        
        return success


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="MYTA Production Setup")
    parser.add_argument('--env-file', default='.env.production',
                       help='Production environment file path')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only validate existing environment')
    parser.add_argument('--generate-secrets', action='store_true',
                       help='Generate new production secrets')
    parser.add_argument('--security-check', action='store_true',
                       help='Run security checks only')
    
    args = parser.parse_args()
    
    setup = ProductionSetup(args.env_file)
    
    if args.security_check:
        success = setup.run_security_checks()
        exit(0 if success else 1)
    
    elif args.validate_only:
        is_valid, issues = setup.validate_production_environment()
        if issues:
            print("\nIssues found:")
            for issue in issues:
                print(f"  - {issue}")
        exit(0 if is_valid else 1)
    
    elif args.generate_secrets:
        secrets = setup.generate_production_secrets()
        env_file = setup.create_production_env_file(secrets)
        print(f"Generated production environment template: {env_file}")
        print("Remember to configure the remaining variables!")
    
    else:
        # Full setup
        success = setup.setup_production_environment(generate_secrets=True)
        exit(0 if success else 1)


if __name__ == "__main__":
    main()
