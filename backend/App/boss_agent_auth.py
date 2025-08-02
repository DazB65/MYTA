"""
Boss Agent Authentication System for Vidalytics
Implements JWT-based authentication for hierarchical agent communication
"""

import jwt
import secrets
import time
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import logging

from security_config import get_boss_agent_secret

logger = logging.getLogger(__name__)

@dataclass
class BossAgentCredentials:
    """Boss agent authentication credentials"""
    agent_id: str = "boss_agent"
    secret_key: str = None
    algorithm: str = "HS256"
    token_expiry_hours: int = 1
    
    def __post_init__(self):
        if self.secret_key is None:
            # Generate a secure random secret key
            self.secret_key = secrets.token_urlsafe(64)

@dataclass
class AuthenticationResult:
    """Result of authentication validation"""
    is_valid: bool
    agent_id: Optional[str] = None
    request_id: Optional[str] = None
    error_message: Optional[str] = None
    permissions: List[str] = None

class BossAgentAuthenticator:
    """Handles boss agent authentication and token management"""
    
    def __init__(self, credentials: Optional[BossAgentCredentials] = None):
        self.credentials = credentials or BossAgentCredentials()
        
        # Use secure configuration
        self.credentials.secret_key = get_boss_agent_secret()
        logger.info("Loaded boss agent secret from secure configuration")
    
    def generate_boss_agent_token(self, request_id: str, additional_claims: Dict[str, Any] = None) -> str:
        """Generate a JWT token for boss agent requests"""
        
        now_timestamp = int(time.time())
        expiry_timestamp = now_timestamp + (self.credentials.token_expiry_hours * 3600)
        
        payload = {
            # Standard JWT claims
            'iss': 'Vidalytics_Boss_Agent',  # Issuer
            'sub': self.credentials.agent_id,  # Subject
            'aud': 'specialized_agents',  # Audience
            'iat': now_timestamp,  # Issued at
            'exp': expiry_timestamp,  # Expiry
            'nbf': now_timestamp,  # Not before
            'jti': request_id,  # JWT ID (request ID)
            
            # Custom claims
            'agent_role': 'boss_agent',
            'permissions': [
                'delegate_to_specialized_agents',
                'receive_specialized_responses',
                'orchestrate_multi_agent_requests'
            ],
            'hierarchy_level': 'boss',
            'request_id': request_id,
            'timestamp': datetime.utcfromtimestamp(now_timestamp).isoformat()
        }
        
        # Add any additional claims
        if additional_claims:
            payload.update(additional_claims)
        
        try:
            token = jwt.encode(
                payload, 
                self.credentials.secret_key, 
                algorithm=self.credentials.algorithm
            )
            
            logger.debug(f"Generated boss agent token for request {request_id}")
            return token
            
        except Exception as e:
            logger.error(f"Failed to generate boss agent token: {e}")
            raise ValueError(f"Token generation failed: {e}")
    
    def validate_boss_agent_token(self, token: str, expected_request_id: Optional[str] = None) -> AuthenticationResult:
        """Validate a boss agent JWT token"""
        
        if not token:
            return AuthenticationResult(
                is_valid=False,
                error_message="No authentication token provided"
            )
        
        try:
            # Decode and verify the token
            payload = jwt.decode(
                token,
                self.credentials.secret_key,
                algorithms=[self.credentials.algorithm],
                audience='specialized_agents'
            )
            
            # Extract claims
            agent_id = payload.get('sub')
            request_id = payload.get('request_id') or payload.get('jti')
            agent_role = payload.get('agent_role')
            permissions = payload.get('permissions', [])
            hierarchy_level = payload.get('hierarchy_level')
            
            # Validate boss agent identity
            if agent_role != 'boss_agent':
                return AuthenticationResult(
                    is_valid=False,
                    error_message=f"Invalid agent role: {agent_role}"
                )
            
            if hierarchy_level != 'boss':
                return AuthenticationResult(
                    is_valid=False,
                    error_message=f"Invalid hierarchy level: {hierarchy_level}"
                )
            
            # Validate request ID if provided
            if expected_request_id and request_id != expected_request_id:
                return AuthenticationResult(
                    is_valid=False,
                    error_message="Request ID mismatch"
                )
            
            # Check required permissions
            required_permissions = ['delegate_to_specialized_agents']
            if not all(perm in permissions for perm in required_permissions):
                return AuthenticationResult(
                    is_valid=False,
                    error_message="Insufficient permissions"
                )
            
            logger.debug(f"Successfully validated boss agent token for request {request_id}")
            
            return AuthenticationResult(
                is_valid=True,
                agent_id=agent_id,
                request_id=request_id,
                permissions=permissions
            )
            
        except jwt.ExpiredSignatureError:
            return AuthenticationResult(
                is_valid=False,
                error_message="Authentication token has expired"
            )
        except jwt.InvalidTokenError as e:
            return AuthenticationResult(
                is_valid=False,
                error_message=f"Invalid authentication token: {e}"
            )
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return AuthenticationResult(
                is_valid=False,
                error_message=f"Token validation failed: {e}"
            )
    
    def create_authenticated_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add authentication to a boss agent request"""
        
        request_id = request_data.get('request_id')
        if not request_id:
            raise ValueError("Request ID is required for authentication")
        
        # Generate authentication token
        token = self.generate_boss_agent_token(request_id)
        
        # Add authentication headers to request
        authenticated_request = request_data.copy()
        authenticated_request.update({
            'boss_agent_token': token,
            'authentication': {
                'agent_id': self.credentials.agent_id,
                'timestamp': datetime.utcnow().isoformat(),
                'auth_method': 'jwt'
            }
        })
        
        return authenticated_request
    
    def extract_request_authentication(self, request_data: Dict[str, Any]) -> AuthenticationResult:
        """Extract and validate authentication from a request"""
        
        # Extract token from request
        token = request_data.get('boss_agent_token')
        if not token:
            # Check alternative token locations
            auth_header = request_data.get('authentication', {})
            token = auth_header.get('token') or auth_header.get('bearer_token')
        
        if not token:
            return AuthenticationResult(
                is_valid=False,
                error_message="No authentication token found in request"
            )
        
        # Validate the token
        expected_request_id = request_data.get('request_id')
        return self.validate_boss_agent_token(token, expected_request_id)

class SpecializedAgentAuthMixin:
    """Mixin class for specialized agents to handle boss agent authentication"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authenticator = BossAgentAuthenticator()
    
    def _validate_boss_agent_request(self, request_data: Dict[str, Any]) -> bool:
        """Validate that the request comes from an authenticated boss agent"""
        
        auth_result = self.authenticator.extract_request_authentication(request_data)
        
        if not auth_result.is_valid:
            logger.warning(f"Boss agent authentication failed: {auth_result.error_message}")
            return False
        
        logger.debug(f"Boss agent authentication successful for request {auth_result.request_id}")
        return True
    
    def _create_unauthorized_response(self, request_id: str) -> Dict[str, Any]:
        """Create a standardized unauthorized response"""
        
        return {
            'agent_type': getattr(self, 'agent_type', 'unknown'),
            'response_id': f"unauth_{request_id}",
            'request_id': request_id,
            'timestamp': datetime.utcnow().isoformat(),
            'domain_match': False,
            'analysis': {
                'summary': 'Unauthorized request: Boss agent authentication required',
                'error_type': 'authentication_error',
                'error_message': 'This agent only accepts requests from authorized boss agents',
                'required_auth': 'boss_agent_jwt_token'
            },
            'confidence_score': 0.0,
            'processing_time': 0.0,
            'for_boss_agent_only': True,
            'authentication_required': True
        }

# Global authenticator instance
_global_authenticator = None

def get_boss_agent_authenticator() -> BossAgentAuthenticator:
    """Get or create global boss agent authenticator"""
    global _global_authenticator
    if _global_authenticator is None:
        _global_authenticator = BossAgentAuthenticator()
    return _global_authenticator

def create_boss_agent_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to create an authenticated boss agent request"""
    authenticator = get_boss_agent_authenticator()
    return authenticator.create_authenticated_request(request_data)

def validate_specialized_agent_request(request_data: Dict[str, Any]) -> AuthenticationResult:
    """Convenience function to validate a request to a specialized agent"""
    authenticator = get_boss_agent_authenticator()
    return authenticator.extract_request_authentication(request_data)

# Environment setup helper
def setup_boss_agent_authentication():
    """Setup boss agent authentication with environment variables"""
    
    # Check if secret key is provided
    secret_key = os.getenv('BOSS_AGENT_SECRET_KEY')
    if not secret_key:
        # Generate and suggest a secret key
        suggested_secret = secrets.token_urlsafe(64)
        logger.warning(
            f"No BOSS_AGENT_SECRET_KEY environment variable found. "
            f"Consider setting: export BOSS_AGENT_SECRET_KEY='{suggested_secret}'"
        )
    
    # Initialize global authenticator
    global _global_authenticator
    credentials = BossAgentCredentials(secret_key=secret_key) if secret_key else None
    _global_authenticator = BossAgentAuthenticator(credentials)
    
    logger.info("Boss agent authentication system initialized")
    return _global_authenticator

# Auto-setup on import
setup_boss_agent_authentication()