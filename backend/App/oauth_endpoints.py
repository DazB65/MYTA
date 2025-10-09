"""
OAuth 2.0 Authorization Flow Endpoints for Vidalytics
Handles OAuth authorization, callback, and token management endpoints
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic.v1 import BaseModel, Field

from .oauth_manager import get_oauth_manager, OAuthToken

# Configure logging
logger = logging.getLogger(__name__)

# Create router
oauth_router = APIRouter(prefix="/auth", tags=["OAuth"])

class OAuthInitRequest(BaseModel):
    """Request to initiate OAuth flow"""
    user_id: str = Field(..., description="User ID to associate with OAuth token")
    return_url: Optional[str] = Field(None, description="URL to redirect after successful authentication")

class OAuthStatusResponse(BaseModel):
    """OAuth status response"""
    authenticated: bool
    user_id: str
    expires_at: Optional[str] = None
    expires_in_seconds: Optional[float] = None
    scopes: Optional[list] = None
    needs_refresh: Optional[bool] = None
    message: Optional[str] = None

class OAuthTokenResponse(BaseModel):
    """OAuth token response"""
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    created_at: str

@oauth_router.get("/status/{user_id}")
async def get_oauth_status(user_id: str) -> OAuthStatusResponse:
    """Get OAuth authentication status for a user"""
    try:
        oauth_manager = get_oauth_manager()
        status = oauth_manager.get_oauth_status(user_id)
        
        response_data = {
            "authenticated": status["authenticated"],
            "user_id": user_id
        }
        
        if status["authenticated"]:
            response_data.update({
                "expires_at": status.get("expires_at"),
                "expires_in_seconds": status.get("expires_in_seconds"),
                "scopes": status.get("scopes"),
                "needs_refresh": status.get("needs_refresh")
            })
        else:
            response_data["message"] = status.get("message", "Not authenticated")
        
        return OAuthStatusResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Failed to get OAuth status for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get OAuth status")

@oauth_router.post("/initiate")
async def initiate_oauth(request: OAuthInitRequest) -> Dict[str, Any]:
    """Initiate OAuth flow for YouTube access"""
    try:
        oauth_manager = get_oauth_manager()
        
        # Check if OAuth is properly configured
        if not all([oauth_manager.client_id, oauth_manager.client_secret, oauth_manager.redirect_uri]):
            raise HTTPException(
                status_code=500, 
                detail="OAuth not configured. Please check Google OAuth credentials in .env file."
            )
        
        # Generate authorization URL
        auth_url, state = oauth_manager.generate_authorization_url(request.user_id)
        
        logger.info(f"Generated OAuth authorization URL for user {request.user_id}")
        
        return {
            "authorization_url": auth_url,
            "state": state,
            "user_id": request.user_id,
            "return_url": request.return_url,
            "message": "Redirect user to authorization_url to complete OAuth flow"
        }
        
    except Exception as e:
        logger.error(f"Failed to initiate OAuth for user {request.user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate OAuth: {str(e)}")

@oauth_router.get("/callback")
async def oauth_callback(request: Request) -> RedirectResponse:
    """Handle OAuth callback from Google"""
    try:
        # Extract parameters from callback
        code = request.query_params.get("code")
        state = request.query_params.get("state")
        error = request.query_params.get("error")
        
        logger.info(f"🔄 OAuth callback received - code: {'present' if code else 'missing'}, state: {'present' if state else 'missing'}, error: {error}")
        
        # Check for errors
        if error:
            logger.error(f"❌ OAuth callback error from Google: {error}")
            return RedirectResponse(
                url=f"/?oauth_error={error}",
                status_code=302
            )
        
        if not code or not state:
            logger.error(f"❌ OAuth callback missing parameters - code: {'present' if code else 'missing'}, state: {'present' if state else 'missing'}")
            return RedirectResponse(
                url="/?oauth_error=missing_parameters",
                status_code=302
            )
        
        # Process OAuth callback
        logger.info(f"🔄 Processing OAuth callback with state: {state[:10]}...")
        oauth_manager = get_oauth_manager()
        token = await oauth_manager.handle_callback(code, state)
        
        if not token:
            logger.error("❌ Failed to process OAuth callback - token exchange failed")
            return RedirectResponse(
                url="/?oauth_error=callback_failed",
                status_code=302
            )
        
        # Success - redirect to main app
        logger.info(f"✅ OAuth callback successful for user {token.user_id}")
        return RedirectResponse(
            url=f"/?oauth_success=true&user_id={token.user_id}",
            status_code=302
        )
        
    except Exception as e:
        logger.error(f"OAuth callback exception: {e}")
        return RedirectResponse(
            url=f"/?oauth_error=server_error",
            status_code=302
        )

@oauth_router.post("/refresh/{user_id}")
async def refresh_oauth_token(user_id: str) -> Dict[str, Any]:
    """Refresh OAuth token for a user"""
    try:
        oauth_manager = get_oauth_manager()
        token = await oauth_manager.refresh_token(user_id)
        
        if not token:
            raise HTTPException(
                status_code=404, 
                detail="No token found for user or refresh failed"
            )
        
        logger.info(f"Token refreshed for user {user_id}")
        
        return {
            "success": True,
            "user_id": user_id,
            "expires_at": token.expires_at.isoformat(),
            "expires_in_seconds": (token.expires_at - datetime.now()).total_seconds(),
            "message": "Token refreshed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to refresh token for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh token")

@oauth_router.delete("/revoke/{user_id}")
async def revoke_oauth_token(user_id: str) -> Dict[str, Any]:
    """Revoke OAuth token for a user"""
    try:
        oauth_manager = get_oauth_manager()
        success = await oauth_manager.revoke_token(user_id)
        
        if not success:
            raise HTTPException(
                status_code=404, 
                detail="No token found for user or revoke failed"
            )
        
        logger.info(f"Token revoked for user {user_id}")
        
        return {
            "success": True,
            "user_id": user_id,
            "message": "Token revoked successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to revoke token for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to revoke token")

@oauth_router.get("/token/{user_id}")
async def get_oauth_token(user_id: str) -> OAuthTokenResponse:
    """Get OAuth token information for a user (for debugging/admin)"""
    try:
        oauth_manager = get_oauth_manager()
        token = await oauth_manager.get_valid_token(user_id)
        
        if not token:
            raise HTTPException(
                status_code=404, 
                detail="No valid token found for user"
            )
        
        # Return token info (excluding sensitive data)
        return OAuthTokenResponse(
            access_token=token.access_token[:20] + "...",  # Truncated for security
            token_type=token.token_type,
            expires_in=int((token.expires_at - datetime.now()).total_seconds()),
            scope=token.scope,
            created_at=token.created_at.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get token for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get token")

@oauth_router.get("/health")
async def oauth_health_check() -> Dict[str, Any]:
    """Check OAuth system health"""
    try:
        oauth_manager = get_oauth_manager()
        
        # Check configuration
        config_ok = all([
            oauth_manager.client_id,
            oauth_manager.client_secret,
            oauth_manager.redirect_uri
        ])
        
        # Check database connectivity
        db_ok = True
        try:
            oauth_manager._init_database()
        except:
            db_ok = False
        
        status = "healthy" if (config_ok and db_ok) else "unhealthy"
        
        return {
            "status": status,
            "configuration": {
                "client_id_configured": bool(oauth_manager.client_id),
                "client_secret_configured": bool(oauth_manager.client_secret),
                "redirect_uri_configured": bool(oauth_manager.redirect_uri),
                "redirect_uri": oauth_manager.redirect_uri
            },
            "database": {
                "connected": db_ok
            },
            "scopes": oauth_manager.scopes,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"OAuth health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Utility functions for use in other parts of the application
async def get_user_youtube_service(user_id: str, service_name: str = "youtube", version: str = "v3"):
    """Get authenticated YouTube service for a user"""
    try:
        oauth_manager = get_oauth_manager()
        service = await oauth_manager.get_youtube_service(user_id, service_name, version)
        return service
    except Exception as e:
        logger.error(f"Failed to get YouTube service for user {user_id}: {e}")
        return None

async def check_user_authentication(user_id: str) -> bool:
    """Check if user is authenticated for YouTube access"""
    try:
        oauth_manager = get_oauth_manager()
        token = await oauth_manager.get_valid_token(user_id)
        return token is not None
    except Exception as e:
        logger.error(f"Failed to check authentication for user {user_id}: {e}")
        return False

# Dependency for routes that require OAuth authentication
async def require_oauth_authentication(user_id: str = None) -> str:
    """Dependency that requires OAuth authentication"""
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID required")
    
    if not await check_user_authentication(user_id):
        raise HTTPException(
            status_code=401, 
            detail="YouTube authentication required. Please complete OAuth flow."
        )
    
    return user_id