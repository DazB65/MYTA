"""
Enhanced JWT Service for Vidalytics
Implements RS256 algorithm, token refresh, and advanced security features
"""

import os
import jwt
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import secrets
import hashlib

from .security_config import get_security_config
from .database_security import audit_logger

logger = logging.getLogger(__name__)

class EnhancedJWTService:
    """Enhanced JWT service with RS256 and refresh token support"""
    
    def __init__(self):
        self.security_config = get_security_config()
        self.algorithm = "RS256"  # Upgraded from HS256
        self.private_key = None
        self.public_key = None
        self._initialize_keys()
    
    def _initialize_keys(self):
        """Initialize RSA key pair for JWT signing"""
        try:
            # Try to load existing keys from environment
            private_key_pem = os.getenv('JWT_PRIVATE_KEY')
            public_key_pem = os.getenv('JWT_PUBLIC_KEY')
            
            if private_key_pem and public_key_pem:
                # Load existing keys
                self.private_key = serialization.load_pem_private_key(
                    private_key_pem.encode(),
                    password=None,
                    backend=default_backend()
                )
                self.public_key = serialization.load_pem_public_key(
                    public_key_pem.encode(),
                    backend=default_backend()
                )
                logger.info("Loaded JWT keys from environment")
            else:
                # Generate new key pair for development
                self._generate_key_pair()
                logger.warning("Generated new JWT key pair. Set JWT_PRIVATE_KEY and JWT_PUBLIC_KEY for production.")
                
        except Exception as e:
            logger.error(f"Failed to initialize JWT keys: {e}")
            # Fallback to HS256 with secret key
            self.algorithm = "HS256"
            logger.warning("Falling back to HS256 algorithm")
    
    def _generate_key_pair(self):
        """Generate a new RSA key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        self.private_key = private_key
        self.public_key = private_key.public_key()
        
        # Log the keys for development (remove in production)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        logger.info("Generated new RSA key pair for JWT")
        logger.debug(f"Private key: {private_pem.decode()}")
        logger.debug(f"Public key: {public_pem.decode()}")
    
    def create_access_token(self, user_id: str, permissions: list = None, 
                           session_id: str = None, additional_claims: Dict = None) -> str:
        """Create an access token with enhanced security"""
        now = datetime.utcnow()
        expires_at = now + timedelta(hours=self.security_config.get_session_config()['timeout_hours'])
        
        # Create token ID for tracking
        token_id = secrets.token_urlsafe(16)
        
        payload = {
            'sub': user_id,  # Subject (user ID)
            'iat': now,      # Issued at
            'exp': expires_at, # Expires at
            'nbf': now,      # Not before
            'jti': token_id, # JWT ID for tracking
            'type': 'access',
            'session_id': session_id,
            'permissions': permissions or [],
            'iss': 'vidalytics',  # Issuer
            'aud': 'vidalytics-api'  # Audience
        }
        
        # Add additional claims if provided
        if additional_claims:
            payload.update(additional_claims)
        
        try:
            if self.algorithm == "RS256":
                token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
            else:
                # Fallback to HS256
                token = jwt.encode(payload, self.security_config.get_jwt_secret(), algorithm=self.algorithm)
            
            # Log token creation
            audit_logger.log_action(
                action="access_token_created",
                user_id=user_id,
                additional_data={
                    'token_id': token_id,
                    'session_id': session_id,
                    'expires_at': expires_at.isoformat(),
                    'permissions': permissions
                },
                severity="INFO"
            )
            
            return token
            
        except Exception as e:
            logger.error(f"Failed to create access token: {e}")
            raise
    
    def create_refresh_token(self, user_id: str, session_id: str = None) -> str:
        """Create a refresh token"""
        now = datetime.utcnow()
        expires_at = now + timedelta(days=self.security_config.get_session_config().get('refresh_token_days', 30))
        
        token_id = secrets.token_urlsafe(16)
        
        payload = {
            'sub': user_id,
            'iat': now,
            'exp': expires_at,
            'jti': token_id,
            'type': 'refresh',
            'session_id': session_id,
            'iss': 'vidalytics',
            'aud': 'vidalytics-api'
        }
        
        try:
            if self.algorithm == "RS256":
                token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
            else:
                token = jwt.encode(payload, self.security_config.get_jwt_secret(), algorithm=self.algorithm)
            
            # Log refresh token creation
            audit_logger.log_action(
                action="refresh_token_created",
                user_id=user_id,
                additional_data={
                    'token_id': token_id,
                    'session_id': session_id,
                    'expires_at': expires_at.isoformat()
                },
                severity="INFO"
            )
            
            return token
            
        except Exception as e:
            logger.error(f"Failed to create refresh token: {e}")
            raise
    
    def verify_token(self, token: str, token_type: str = 'access') -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            if self.algorithm == "RS256":
                payload = jwt.decode(token, self.public_key, algorithms=[self.algorithm], 
                                   audience='vidalytics-api', issuer='vidalytics')
            else:
                payload = jwt.decode(token, self.security_config.get_jwt_secret(), 
                                   algorithms=[self.algorithm], audience='vidalytics-api', issuer='vidalytics')
            
            # Verify token type
            if payload.get('type') != token_type:
                logger.warning(f"Token type mismatch: expected {token_type}, got {payload.get('type')}")
                return None
            
            # Log token verification
            audit_logger.log_action(
                action=f"{token_type}_token_verified",
                user_id=payload.get('sub'),
                additional_data={
                    'token_id': payload.get('jti'),
                    'session_id': payload.get('session_id')
                },
                severity="DEBUG"
            )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        """Refresh an access token using a refresh token"""
        try:
            # Verify refresh token
            payload = self.verify_token(refresh_token, 'refresh')
            if not payload:
                return None
            
            user_id = payload.get('sub')
            session_id = payload.get('session_id')
            
            # Create new access token
            new_access_token = self.create_access_token(
                user_id=user_id,
                session_id=session_id,
                permissions=payload.get('permissions', [])
            )
            
            # Create new refresh token (rotate refresh tokens for security)
            new_refresh_token = self.create_refresh_token(
                user_id=user_id,
                session_id=session_id
            )
            
            # Log token refresh
            audit_logger.log_action(
                action="tokens_refreshed",
                user_id=user_id,
                additional_data={
                    'old_token_id': payload.get('jti'),
                    'session_id': session_id
                },
                severity="INFO"
            )
            
            return new_access_token, new_refresh_token
            
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return None
    
    def revoke_token(self, token: str, user_id: str = None):
        """Revoke a token (add to blacklist)"""
        try:
            payload = self.verify_token(token)
            if payload:
                token_id = payload.get('jti')
                user_id = user_id or payload.get('sub')
                
                # Log token revocation
                audit_logger.log_action(
                    action="token_revoked",
                    user_id=user_id,
                    additional_data={
                        'token_id': token_id,
                        'session_id': payload.get('session_id')
                    },
                    severity="INFO"
                )
                
                # Add to blacklist (implement blacklist storage as needed)
                # For now, just log the revocation
                logger.info(f"Token {token_id} revoked for user {user_id}")
                
        except Exception as e:
            logger.error(f"Token revocation error: {e}")
    
    def get_token_info(self, token: str) -> Optional[Dict[str, Any]]:
        """Get information about a token without full verification"""
        try:
            # Decode without verification to get basic info
            payload = jwt.decode(token, options={"verify_signature": False})
            return {
                'user_id': payload.get('sub'),
                'token_id': payload.get('jti'),
                'session_id': payload.get('session_id'),
                'type': payload.get('type'),
                'expires_at': payload.get('exp'),
                'issued_at': payload.get('iat')
            }
        except Exception as e:
            logger.error(f"Failed to get token info: {e}")
            return None

# Global JWT service instance
enhanced_jwt_service = EnhancedJWTService()
