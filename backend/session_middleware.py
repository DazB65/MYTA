"""
Session Middleware for Vidalytics
Integrates Redis session management with FastAPI requests
"""

import time
from typing import Optional, Dict, Any, Callable
from datetime import datetime, timezone

from fastapi import Request, Response, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from redis_session_manager import (
    get_session_manager, 
    SessionData, 
    SessionStatus,
    RedisSessionManager
)
from logging_config import get_logger, LogCategory, log_security_event
from config import get_settings


class SessionMiddleware(BaseHTTPMiddleware):
    """Middleware for handling Redis-based sessions"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.settings = get_settings()
        self.session_manager = get_session_manager()
        self.logger = get_logger(__name__, LogCategory.AUTHENTICATION)
        self.security = HTTPBearer(auto_error=False)
        
        # Session cookie settings
        self.cookie_name = "Vidalytics_session"
        self.cookie_secure = not self.settings.is_development()
        self.cookie_httponly = True
        self.cookie_samesite = "strict"
        self.cookie_path = "/"
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with session handling"""
        start_time = time.time()
        
        # Extract session information
        session_data = None
        session_id = None
        
        try:
            # Try to get session from cookie first
            session_id = request.cookies.get(self.cookie_name)
            
            # If no cookie, try Authorization header
            if not session_id:
                session_id = await self._extract_session_from_header(request)
            
            # Get session data if session ID exists
            if session_id:
                session_data = await self.session_manager.get_session(session_id)
                
                if session_data:
                    # Validate session security
                    if not await self._validate_session_security(request, session_data):
                        # Security violation - revoke session
                        await self.session_manager.revoke_session(session_id)
                        session_data = None
                        session_id = None
                        
                        log_security_event(
                            'session_security_violation',
                            'Session security validation failed',
                            severity='WARNING',
                            ip_address=self._get_client_ip(request),
                            additional_info={
                                'session_id': session_id[:8] + '...' if session_id else 'unknown',
                                'user_agent': request.headers.get('user-agent', 'unknown')
                            }
                        )
            
            # Attach session data to request state
            request.state.session_data = session_data
            request.state.session_id = session_id
            request.state.is_authenticated = session_data is not None
            request.state.user_id = session_data.user_id if session_data else None
            
            # Process request
            response = await call_next(request)
            
            # Handle session cookie in response
            if session_data:
                # Refresh session cookie if needed
                self._set_session_cookie(response, session_id)
            elif session_id:
                # Clear invalid session cookie
                self._clear_session_cookie(response)
            
            # Log session activity
            self._log_session_activity(request, session_data, time.time() - start_time)
            
            return response
            
        except Exception as e:
            # Log session middleware error
            self.logger.error(
                "Session middleware error",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e),
                        'session_id': session_id[:8] + '...' if session_id else 'none',
                        'path': request.url.path
                    }
                },
                exc_info=True
            )
            
            # Continue without session data
            request.state.session_data = None
            request.state.session_id = None
            request.state.is_authenticated = False
            request.state.user_id = None
            
            response = await call_next(request)
            return response
    
    async def _extract_session_from_header(self, request: Request) -> Optional[str]:
        """Extract session ID from Authorization header"""
        try:
            credentials: HTTPAuthorizationCredentials = await self.security(request)
            if credentials and credentials.scheme.lower() == "bearer":
                return credentials.credentials
        except:
            pass
        return None
    
    async def _validate_session_security(self, request: Request, session_data: SessionData) -> bool:
        """Validate session security constraints"""
        try:
            current_ip = self._get_client_ip(request)
            current_user_agent = request.headers.get('user-agent', '')
            
            # IP address validation (if stored in session)
            if session_data.ip_address and current_ip != session_data.ip_address:
                # Allow IP changes in development
                if not self.settings.is_development():
                    self.logger.warning(
                        "Session IP address mismatch",
                        extra={
                            'category': LogCategory.SECURITY.value,
                            'user_id': session_data.user_id,
                            'metadata': {
                                'session_ip': session_data.ip_address,
                                'request_ip': current_ip,
                                'session_id': session_data.session_id[:8] + '...'
                            }
                        }
                    )
                    return False
            
            # User agent validation (if stored in session)
            if session_data.user_agent and current_user_agent != session_data.user_agent:
                # Allow user agent changes (browsers update frequently)
                self.logger.info(
                    "Session user agent changed",
                    extra={
                        'category': LogCategory.AUTHENTICATION.value,
                        'user_id': session_data.user_id,
                        'metadata': {
                            'session_user_agent': session_data.user_agent[:50] + '...' if len(session_data.user_agent) > 50 else session_data.user_agent,
                            'request_user_agent': current_user_agent[:50] + '...' if len(current_user_agent) > 50 else current_user_agent,
                            'session_id': session_data.session_id[:8] + '...'
                        }
                    }
                )
            
            return True
            
        except Exception as e:
            self.logger.error(
                "Session security validation error",
                extra={
                    'category': LogCategory.ERROR.value,
                    'user_id': session_data.user_id if session_data else 'unknown',
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            return False
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get('x-forwarded-for')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        
        forwarded = request.headers.get('x-forwarded')
        if forwarded:
            return forwarded.split(',')[0].strip()
        
        real_ip = request.headers.get('x-real-ip')
        if real_ip:
            return real_ip
        
        # Fallback to direct client
        if hasattr(request, 'client') and request.client:
            return request.client.host
        
        return 'unknown'
    
    def _set_session_cookie(self, response: Response, session_id: str) -> None:
        """Set session cookie in response"""
        try:
            response.set_cookie(
                key=self.cookie_name,
                value=session_id,
                max_age=int(self.session_manager.config.session_timeout.total_seconds()),
                path=self.cookie_path,
                secure=self.cookie_secure,
                httponly=self.cookie_httponly,
                samesite=self.cookie_samesite
            )
        except Exception as e:
            self.logger.error(
                "Failed to set session cookie",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                }
            )
    
    def _clear_session_cookie(self, response: Response) -> None:
        """Clear session cookie from response"""
        try:
            response.delete_cookie(
                key=self.cookie_name,
                path=self.cookie_path
            )
        except Exception as e:
            self.logger.error(
                "Failed to clear session cookie",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                }
            )
    
    def _log_session_activity(self, request: Request, session_data: Optional[SessionData], duration_ms: float) -> None:
        """Log session activity"""
        try:
            if session_data:
                self.logger.debug(
                    "Session activity logged",
                    extra={
                        'category': LogCategory.AUTHENTICATION.value,
                        'user_id': session_data.user_id,
                        'metadata': {
                            'session_id': session_data.session_id[:8] + '...',
                            'path': request.url.path,
                            'method': request.method,
                            'duration_ms': duration_ms * 1000,
                            'ip_address': self._get_client_ip(request)
                        }
                    }
                )
        except Exception:
            # Don't fail request if logging fails
            pass


class SessionDependency:
    """Dependency for requiring authenticated sessions"""
    
    def __init__(self, require_permissions: Optional[list] = None):
        self.require_permissions = require_permissions or []
        self.logger = get_logger(__name__, LogCategory.AUTHENTICATION)
    
    async def __call__(self, request: Request) -> SessionData:
        """Validate and return session data"""
        # Get session data from request state (set by middleware)
        session_data: Optional[SessionData] = getattr(request.state, 'session_data', None)
        
        if not session_data:
            self.logger.warning(
                "Authentication required but no valid session found",
                extra={
                    'category': LogCategory.AUTHENTICATION.value,
                    'metadata': {
                        'path': request.url.path,
                        'method': request.method,
                        'ip_address': self._get_client_ip(request)
                    }
                }
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        # Check permissions if required
        if self.require_permissions:
            missing_permissions = []
            for permission in self.require_permissions:
                if permission not in session_data.permissions:
                    missing_permissions.append(permission)
            
            if missing_permissions:
                self.logger.warning(
                    f"Insufficient permissions for user",
                    extra={
                        'category': LogCategory.AUTHENTICATION.value,
                        'user_id': session_data.user_id,
                        'metadata': {
                            'required_permissions': self.require_permissions,
                            'missing_permissions': missing_permissions,
                            'user_permissions': session_data.permissions,
                            'path': request.url.path
                        }
                    }
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Missing: {', '.join(missing_permissions)}"
                )
        
        return session_data
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get('x-forwarded-for')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        
        if hasattr(request, 'client') and request.client:
            return request.client.host
        
        return 'unknown'


class OptionalSessionDependency:
    """Dependency for optional session authentication"""
    
    async def __call__(self, request: Request) -> Optional[SessionData]:
        """Return session data if available, None otherwise"""
        return getattr(request.state, 'session_data', None)


# Create dependency instances
require_auth = SessionDependency()
require_admin = SessionDependency(require_permissions=['admin'])
optional_auth = OptionalSessionDependency()


# Session management utilities
async def create_user_session(
    user_id: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    permissions: Optional[list] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> SessionData:
    """Create a new user session"""
    session_manager = get_session_manager()
    return await session_manager.create_session(
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        permissions=permissions or [],
        metadata=metadata or {}
    )


async def get_user_session(session_id: str) -> Optional[SessionData]:
    """Get session by ID"""
    session_manager = get_session_manager()
    return await session_manager.get_session(session_id)


async def revoke_user_session(session_id: str) -> bool:
    """Revoke a specific session"""
    session_manager = get_session_manager()
    return await session_manager.revoke_session(session_id)


async def revoke_all_user_sessions(user_id: str, except_session_id: Optional[str] = None) -> int:
    """Revoke all sessions for a user"""
    session_manager = get_session_manager()
    return await session_manager.revoke_all_user_sessions(user_id, except_session_id)


async def get_all_user_sessions(user_id: str) -> list:
    """Get all active sessions for a user"""
    session_manager = get_session_manager()
    return await session_manager.get_user_sessions(user_id)


async def update_user_session(
    session_id: str,
    metadata: Optional[Dict[str, Any]] = None,
    permissions: Optional[list] = None
) -> bool:
    """Update session data"""
    session_manager = get_session_manager()
    return await session_manager.update_session(session_id, metadata, permissions)