"""
Authentication Middleware for Vidalytics API
Provides JWT-based authentication for API endpoints
"""

import jwt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable
from functools import wraps

from fastapi import Request, HTTPException, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic.v1 import BaseModel

from backend.App.security_config import get_security_config

logger = logging.getLogger(__name__)

# Import security monitoring (lazy import to avoid circular dependencies)
def get_security_monitor():
    try:
        from .security_monitoring import log_auth_failure, log_suspicious_request
        return log_auth_failure, log_suspicious_request
    except ImportError:
        # Fallback if security monitoring is not available
        return lambda *args, **kwargs: None, lambda *args, **kwargs: None

class AuthToken(BaseModel):
    """Authentication token data"""
    user_id: str
    session_id: str
    issued_at: datetime
    expires_at: datetime
    permissions: list[str] = []

class AuthenticationMiddleware:
    """Handles user authentication and session management"""

    def __init__(self):
        self.security_config = get_security_config()
        self.blacklisted_tokens = set()  # In production, use Redis
        self.security = HTTPBearer(auto_error=False)
        
    def generate_auth_token(self, user_id: str, session_id: str, 
                           permissions: list[str] = None) -> str:
        """Generate JWT authentication token for user"""
        try:
            now = datetime.utcnow()
            expires_at = now + timedelta(hours=8)  # 8 hour sessions
            
            payload = {
                'user_id': user_id,
                'session_id': session_id,
                'iat': now.timestamp(),
                'exp': expires_at.timestamp(),
                'permissions': permissions or ['read', 'write'],
                'iss': 'Vidalytics_API',
                'aud': 'Vidalytics_Users'
            }
            
            secret_key = self.security_config.get_boss_agent_secret()
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            
            logger.info(f"Generated auth token for user {user_id}")
            return token
            
        except Exception as e:
            logger.error(f"Failed to generate auth token: {e}")
            raise HTTPException(status_code=500, detail="Token generation failed")
    
    def verify_auth_token(self, token: str) -> AuthToken:
        """Verify and decode authentication token"""
        try:
            # Check if token is blacklisted
            if self.is_token_blacklisted(token):
                raise HTTPException(status_code=401, detail="Token has been revoked")

            secret_key = self.security_config.get_boss_agent_secret()
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=['HS256'],
                audience='Vidalytics_Users'
            )

            # Check expiration
            if datetime.utcnow().timestamp() > payload['exp']:
                raise HTTPException(status_code=401, detail="Token expired")

            return AuthToken(
                user_id=payload['user_id'],
                session_id=payload['session_id'],
                issued_at=datetime.fromtimestamp(payload['iat']),
                expires_at=datetime.fromtimestamp(payload['exp']),
                permissions=payload.get('permissions', [])
            )
            
        except jwt.ExpiredSignatureError:
            # Log expired token attempt
            log_auth_failure, _ = get_security_monitor()
            log_auth_failure("unknown", "unknown", "unknown", {"error": "expired_token"})
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError as e:
            # Log invalid token attempt
            log_auth_failure, _ = get_security_monitor()
            log_auth_failure("unknown", "unknown", "unknown", {"error": "invalid_token", "details": str(e)})
            logger.warning(f"Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            # Log general authentication failure
            log_auth_failure, _ = get_security_monitor()
            log_auth_failure("unknown", "unknown", "unknown", {"error": "auth_failure", "details": str(e)})
            logger.error(f"Token verification error: {e}")
            raise HTTPException(status_code=401, detail="Authentication failed")

    def set_secure_cookie(self, response: Response, token: str, max_age: int = 28800) -> None:
        """Set secure httpOnly cookie with JWT token"""
        response.set_cookie(
            key="auth_token",
            value=token,
            max_age=max_age,  # 8 hours default
            httponly=True,
            secure=True,  # HTTPS only in production
            samesite="strict",
            path="/"
        )

    def clear_auth_cookie(self, response: Response) -> None:
        """Clear authentication cookie"""
        response.delete_cookie(
            key="auth_token",
            path="/",
            httponly=True,
            secure=True,
            samesite="strict"
        )

    def get_token_from_cookie(self, request: Request) -> Optional[str]:
        """Extract token from httpOnly cookie"""
        return request.cookies.get("auth_token")

    def blacklist_token(self, token: str) -> None:
        """Add token to blacklist"""
        self.blacklisted_tokens.add(token)
        logger.info("Token blacklisted successfully")

    def is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted"""
        return token in self.blacklisted_tokens

# Global middleware instance
auth_middleware = AuthenticationMiddleware()

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> AuthToken:
    """Dependency to get current authenticated user from Bearer token or cookie"""
    token = None

    # Try Bearer token first
    if credentials:
        token = credentials.credentials
    else:
        # Try cookie as fallback
        token = auth_middleware.get_token_from_cookie(request)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return auth_middleware.verify_auth_token(token)

async def get_optional_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[AuthToken]:
    """Dependency to get current user if authenticated, None if not"""
    token = None

    # Try Bearer token first
    if credentials:
        token = credentials.credentials
    else:
        # Try cookie as fallback
        token = auth_middleware.get_token_from_cookie(request)

    if not token:
        return None

    try:
        return auth_middleware.verify_auth_token(token)
    except HTTPException:
        return None

def require_permissions(*required_permissions: str):
    """Decorator to require specific permissions"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Find the current_user parameter
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=401, detail="Authentication required")
            
            # Check permissions
            if not all(perm in current_user.permissions for perm in required_permissions):
                raise HTTPException(
                    status_code=403, 
                    detail=f"Insufficient permissions. Required: {required_permissions}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Legacy support for simple user_id authentication
async def get_user_id_from_request(request: Request) -> str:
    """
    DEPRECATED: Legacy function for backward compatibility
    Extract user_id from request headers or cookies
    This should be replaced with proper JWT authentication
    """
    logger.warning("Using deprecated user_id authentication - upgrade to JWT recommended")
    
    # Try to get from Authorization header first
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            auth_token = auth_middleware.verify_auth_token(token)
            return auth_token.user_id
        except:
            pass  # Fall back to legacy methods
    
    # Legacy fallback methods
    user_id = (
        request.headers.get("x-user-id") or
        request.cookies.get("user_id") or
        request.query_params.get("user_id")
    )
    
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found - authentication required")
    
    return user_id

def create_session_token(user_id: str, session_data: Dict[str, Any] = None) -> str:
    """Create a session token for authenticated user"""
    import uuid
    session_id = str(uuid.uuid4())

    # Store session data if needed (implement session storage)
    # For now, just create the token
    return auth_middleware.generate_auth_token(user_id, session_id)

def create_authenticated_response(response_data: Dict[str, Any], user_id: str, response: Response) -> Dict[str, Any]:
    """Create response with secure authentication cookie"""
    # Generate token
    token = create_session_token(user_id)

    # Set secure cookie
    auth_middleware.set_secure_cookie(response, token)

    # Return response data (without token in body for security)
    return {
        **response_data,
        "authenticated": True,
        "user_id": user_id
    }

# Utility functions for common authentication patterns
class AuthUtils:
    """Utility functions for authentication"""
    
    @staticmethod
    def extract_user_info(request: Request) -> Dict[str, str]:
        """Extract user information from request safely"""
        return {
            'ip_address': request.client.host if request.client else 'unknown',
            'user_agent': request.headers.get('user-agent', 'unknown')[:100],  # Truncate
            'origin': request.headers.get('origin', 'unknown')
        }
    
    @staticmethod
    def is_safe_redirect_url(url: str, allowed_hosts: list[str]) -> bool:
        """Check if redirect URL is safe"""
        from urllib.parse import urlparse
        
        if not url:
            return False
        
        parsed = urlparse(url)
        
        # Must be relative or from allowed hosts
        if not parsed.netloc:  # Relative URL
            return url.startswith('/')
        
        return parsed.netloc in allowed_hosts
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Generate CSRF token"""
        import secrets
        return secrets.token_urlsafe(32)

# Export commonly used functions
__all__ = [
    'AuthenticationMiddleware',
    'AuthToken',
    'get_current_user',
    'get_optional_user',
    'require_permissions',
    'get_user_id_from_request', 
    'create_session_token',
    'auth_middleware',
    'AuthUtils'
]