"""
Session Management API Router for Vidalytics
Provides endpoints for session management and authentication
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request, Response, Depends, status
from pydantic.v1 import BaseModel, Field

from .session_middleware import (
    require_auth,
    create_user_session,
    get_user_session,
    revoke_user_session,
    revoke_all_user_sessions,
    get_all_user_sessions,
    update_user_session
)
from backend.App.redis_session_manager import get_session_manager, SessionData
from backend.App.api_models import StandardResponse, create_success_response, create_error_response
from backend.App.logging_config import get_logger, LogCategory, log_security_event
from backend.App.rate_limiter import limiter, get_rate_limit


# Pydantic models for request/response
class LoginRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    password: Optional[str] = Field(None, description="User password (for demo purposes)")
    remember_me: bool = Field(False, description="Extended session duration")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional session metadata")


class SessionResponse(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    user_id: str = Field(..., description="User identifier")
    created_at: datetime = Field(..., description="Session creation time")
    last_accessed: datetime = Field(..., description="Last access time")
    expires_at: datetime = Field(..., description="Session expiry time")
    ip_address: Optional[str] = Field(None, description="Client IP address")
    user_agent: Optional[str] = Field(None, description="Client user agent")
    permissions: List[str] = Field(default_factory=list, description="User permissions")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Session metadata")


class SessionListResponse(BaseModel):
    sessions: List[SessionResponse] = Field(..., description="List of user sessions")
    total_count: int = Field(..., description="Total number of sessions")


class SessionStatsResponse(BaseModel):
    daily_stats: Dict[str, Dict[str, int]] = Field(..., description="Daily session statistics")
    total_active_sessions: int = Field(..., description="Total active sessions")
    redis_info: Dict[str, Any] = Field(..., description="Redis connection info")


class UpdateSessionRequest(BaseModel):
    metadata: Optional[Dict[str, Any]] = Field(None, description="Session metadata to update")
    permissions: Optional[List[str]] = Field(None, description="User permissions to update")


# Create router
router = APIRouter(prefix="/api/session", tags=["session"])
logger = get_logger(__name__, LogCategory.AUTHENTICATION)


@router.post("/login", response_model=StandardResponse)
@limiter.limit(get_rate_limit("public", "auth"))
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest
):
    """
    Create a new user session (login)
    
    This is a simplified login endpoint for demonstration.
    In production, implement proper password validation.
    """
    try:
        # Get client information
        ip_address = _get_client_ip(request)
        user_agent = request.headers.get('user-agent', '')
        
        # For demo purposes, accept any user_id
        # In production, validate credentials against your user database
        user_id = login_data.user_id
        
        # Create session with appropriate permissions
        # In production, get permissions from user database
        permissions = ["user"]  # Default permissions
        if user_id == "admin":
            permissions.append("admin")
        
        # Create session
        session_data = await create_user_session(
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            permissions=permissions,
            metadata=login_data.metadata or {}
        )
        
        # Set session cookie
        response.set_cookie(
            key="Vidalytics_session",
            value=session_data.session_id,
            max_age=int(get_session_manager().config.session_timeout.total_seconds()),
            path="/",
            secure=not get_session_manager().settings.is_development(),
            httponly=True,
            samesite="strict"
        )
        
        logger.info(
            "User login successful",
            extra={
                'category': LogCategory.AUTHENTICATION.value,
                'user_id': user_id,
                'metadata': {
                    'session_id': session_data.session_id[:8] + '...',
                    'ip_address': ip_address,
                    'remember_me': login_data.remember_me
                }
            }
        )
        
        return create_success_response(
            "Login successful",
            {
                "session_id": session_data.session_id,
                "user_id": session_data.user_id,
                "expires_at": session_data.expires_at.isoformat(),
                "permissions": session_data.permissions
            }
        )
        
    except Exception as e:
        logger.error(
            "Login failed",
            extra={
                'category': LogCategory.ERROR.value,
                'metadata': {
                    'user_id': login_data.user_id,
                    'error_type': type(e).__name__,
                    'error_message': str(e),
                    'ip_address': _get_client_ip(request)
                }
            },
            exc_info=True
        )
        
        # Log security event for failed login
        log_security_event(
            'login_failed',
            f'Login attempt failed for user {login_data.user_id}',
            severity='WARNING',
            user_id=login_data.user_id,
            ip_address=_get_client_ip(request),
            additional_info={'error': str(e)}
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login failed"
        )


@router.post("/logout", response_model=StandardResponse)
@limiter.limit(get_rate_limit("authenticated", "default"))
async def logout(
    request: Request,
    response: Response,
    session_data: SessionData = Depends(require_auth)
):
    """Logout user (revoke current session)"""
    try:
        # Revoke current session
        success = await revoke_user_session(session_data.session_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to revoke session"
            )
        
        # Clear session cookie
        response.delete_cookie(
            key="Vidalytics_session",
            path="/"
        )
        
        logger.info(
            "User logout successful",
            extra={
                'category': LogCategory.AUTHENTICATION.value,
                'user_id': session_data.user_id,
                'metadata': {
                    'session_id': session_data.session_id[:8] + '...',
                    'ip_address': _get_client_ip(request)
                }
            }
        )
        
        return create_success_response("Logout successful")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Logout failed",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': session_data.user_id,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.post("/logout-all", response_model=StandardResponse)
@limiter.limit(get_rate_limit("authenticated", "default"))
async def logout_all_sessions(
    request: Request,
    response: Response,
    session_data: SessionData = Depends(require_auth)
):
    """Logout from all sessions except current"""
    try:
        # Revoke all other sessions for this user
        revoked_count = await revoke_all_user_sessions(
            session_data.user_id,
            except_session_id=session_data.session_id
        )
        
        logger.info(
            f"Revoked {revoked_count} sessions for user",
            extra={
                'category': LogCategory.AUTHENTICATION.value,
                'user_id': session_data.user_id,
                'metadata': {
                    'revoked_count': revoked_count,
                    'kept_session': session_data.session_id[:8] + '...',
                    'ip_address': _get_client_ip(request)
                }
            }
        )
        
        return create_success_response(
            f"Logged out from {revoked_count} other sessions",
            {"revoked_sessions": revoked_count}
        )
        
    except Exception as e:
        logger.error(
            "Logout all sessions failed",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': session_data.user_id,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to logout from all sessions"
        )


@router.get("/current", response_model=StandardResponse)
@limiter.limit(get_rate_limit("authenticated", "default"))
async def get_current_session(request: Request, session_data: SessionData = Depends(require_auth)):
    """Get current session information"""
    try:
        session_response = SessionResponse(
            session_id=session_data.session_id,
            user_id=session_data.user_id,
            created_at=session_data.created_at,
            last_accessed=session_data.last_accessed,
            expires_at=session_data.expires_at,
            ip_address=session_data.ip_address,
            user_agent=session_data.user_agent,
            permissions=session_data.permissions,
            metadata=session_data.metadata
        )
        
        return create_success_response(
            "Current session retrieved",
            session_response.dict()
        )
        
    except Exception as e:
        logger.error(
            "Failed to get current session",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': session_data.user_id,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get session information"
        )


@router.get("/list", response_model=StandardResponse)
@limiter.limit(get_rate_limit("authenticated", "default"))
async def list_user_sessions(request: Request, session_data: SessionData = Depends(require_auth)):
    """List all active sessions for current user"""
    try:
        sessions = await get_all_user_sessions(session_data.user_id)
        
        session_responses = []
        for session in sessions:
            session_responses.append(SessionResponse(
                session_id=session.session_id,
                user_id=session.user_id,
                created_at=session.created_at,
                last_accessed=session.last_accessed,
                expires_at=session.expires_at,
                ip_address=session.ip_address,
                user_agent=session.user_agent,
                permissions=session.permissions,
                metadata=session.metadata
            ))
        
        response_data = SessionListResponse(
            sessions=session_responses,
            total_count=len(session_responses)
        )
        
        return create_success_response(
            "User sessions retrieved",
            response_data.dict()
        )
        
    except Exception as e:
        logger.error(
            "Failed to list user sessions",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': session_data.user_id,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list sessions"
        )


@router.put("/update", response_model=StandardResponse)
@limiter.limit(get_rate_limit("authenticated", "default"))
async def update_current_session(
    request: Request,
    update_data: UpdateSessionRequest,
    session_data: SessionData = Depends(require_auth)
):
    """Update current session metadata and permissions"""
    try:
        success = await update_user_session(
            session_data.session_id,
            metadata=update_data.metadata,
            permissions=update_data.permissions
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update session"
            )
        
        logger.info(
            "Session updated successfully",
            extra={
                'category': LogCategory.AUTHENTICATION.value,
                'user_id': session_data.user_id,
                'metadata': {
                    'session_id': session_data.session_id[:8] + '...',
                    'updated_metadata': bool(update_data.metadata),
                    'updated_permissions': bool(update_data.permissions)
                }
            }
        )
        
        return create_success_response("Session updated successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to update session",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': session_data.user_id,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update session"
        )


@router.delete("/revoke/{session_id}", response_model=StandardResponse)
@limiter.limit(get_rate_limit("authenticated", "default"))
async def revoke_specific_session(
    request: Request,
    session_id: str,
    current_session: SessionData = Depends(require_auth)
):
    """Revoke a specific session (must be owned by current user)"""
    try:
        # Get the session to verify ownership
        target_session = await get_user_session(session_id)
        if not target_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Verify user owns this session
        if target_session.user_id != current_session.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot revoke other user's session"
            )
        
        # Revoke the session
        success = await revoke_user_session(session_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to revoke session"
            )
        
        logger.info(
            "Session revoked successfully",
            extra={
                'category': LogCategory.AUTHENTICATION.value,
                'user_id': current_session.user_id,
                'metadata': {
                    'revoked_session_id': session_id[:8] + '...',
                    'current_session_id': current_session.session_id[:8] + '...'
                }
            }
        )
        
        return create_success_response("Session revoked successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to revoke session",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': current_session.user_id,
                'metadata': {
                    'target_session_id': session_id[:8] + '...' if session_id else 'unknown',
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke session"
        )


@router.get("/stats", response_model=StandardResponse)
@limiter.limit(get_rate_limit("authenticated", "default"))
async def get_session_statistics(request: Request, session_data: SessionData = Depends(require_auth)):
    """Get session statistics (admin only for detailed stats)"""
    try:
        session_manager = get_session_manager()
        
        # Basic stats for all users
        basic_stats = {
            "user_sessions": len(await get_all_user_sessions(session_data.user_id)),
            "current_session_expires_at": session_data.expires_at.isoformat()
        }
        
        # Detailed stats for admin users
        if "admin" in session_data.permissions:
            detailed_stats = await session_manager.get_session_stats()
            basic_stats.update(detailed_stats)
        
        return create_success_response(
            "Session statistics retrieved",
            basic_stats
        )
        
    except Exception as e:
        logger.error(
            "Failed to get session statistics",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': session_data.user_id,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get session statistics"
        )


@router.get("/health", response_model=StandardResponse)
@limiter.limit(get_rate_limit("public", "health"))
async def session_health_check(request: Request):
    """Check session system health"""
    try:
        session_manager = get_session_manager()
        health_data = await session_manager.health_check()
        
        return create_success_response(
            "Session system health check completed",
            health_data
        )
        
    except Exception as e:
        logger.error(
            "Session health check failed",
            extra={
                'category': LogCategory.ERROR.value,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        
        return create_error_response(
            "Session system health check failed",
            {"error": str(e), "status": "unhealthy"}
        )


def _get_client_ip(request: Request) -> str:
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