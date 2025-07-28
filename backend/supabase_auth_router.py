"""
Supabase Authentication Router for CreatorMate
Handles token-based authentication with YouTube API using Supabase-managed OAuth
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import jwt
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Configure logging
logger = logging.getLogger(__name__)

# Create router
supabase_auth_router = APIRouter(prefix="/api/auth", tags=["Supabase Auth"])

# Bearer token security scheme
security = HTTPBearer()

class YouTubeTokensRequest(BaseModel):
    """Request containing YouTube OAuth tokens from Supabase"""
    access_token: str = Field(..., description="Google OAuth access token")
    refresh_token: Optional[str] = Field(None, description="Google OAuth refresh token")
    expires_at: Optional[str] = Field(None, description="Token expiration time")
    scopes: list[str] = Field(default=[], description="OAuth scopes")
    user_id: str = Field(..., description="Supabase user ID")

class TokenValidationResponse(BaseModel):
    """Response for token validation"""
    valid: bool
    user_id: str
    expires_at: Optional[str] = None
    scopes: list[str] = []
    message: str

class YouTubeServiceContext:
    """Context for storing YouTube service instances per request"""
    def __init__(self):
        self.services: Dict[str, Any] = {}
        self.tokens: Dict[str, YouTubeTokensRequest] = {}

# Global context for storing YouTube services per request
_youtube_context = YouTubeServiceContext()

@supabase_auth_router.post("/validate-youtube-tokens")
async def validate_youtube_tokens(tokens: YouTubeTokensRequest) -> TokenValidationResponse:
    """
    Validate YouTube OAuth tokens and create authenticated service
    This endpoint stores the tokens temporarily for use in subsequent API calls
    """
    try:
        logger.info(f"Validating YouTube tokens for user {tokens.user_id}")
        
        # Create Google credentials object
        credentials = Credentials(
            token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=tokens.scopes
        )
        
        # Test credentials by creating YouTube service
        youtube = build('youtube', 'v3', credentials=credentials)
        
        # Test with a simple API call to verify the token
        try:
            # Try to list channels (minimal API call to verify access)
            channels_response = youtube.channels().list(
                part='snippet',
                mine=True,
                maxResults=1
            ).execute()
            
            logger.info(f"✅ YouTube tokens validated for user {tokens.user_id}")
            
            # Store tokens and service in context for this request session
            request_key = f"user_{tokens.user_id}_{datetime.now().timestamp()}"
            _youtube_context.tokens[request_key] = tokens
            _youtube_context.services[request_key] = youtube
            
            return TokenValidationResponse(
                valid=True,
                user_id=tokens.user_id,
                expires_at=tokens.expires_at,
                scopes=tokens.scopes,
                message="Tokens validated successfully"
            )
            
        except Exception as api_error:
            logger.error(f"❌ YouTube API test failed: {api_error}")
            return TokenValidationResponse(
                valid=False,
                user_id=tokens.user_id,
                scopes=tokens.scopes,
                message=f"Invalid or expired tokens: {str(api_error)}"
            )
            
    except Exception as e:
        logger.error(f"❌ Token validation failed for user {tokens.user_id}: {e}")
        return TokenValidationResponse(
            valid=False,
            user_id=tokens.user_id,
            scopes=[],
            message=f"Token validation failed: {str(e)}"
        )

@supabase_auth_router.get("/youtube-service-status/{user_id}")
async def get_youtube_service_status(user_id: str) -> Dict[str, Any]:
    """
    Check if we have a valid YouTube service for the user
    """
    try:
        # Look for any services for this user
        user_services = {
            key: True for key in _youtube_context.services.keys() 
            if key.startswith(f"user_{user_id}_")
        }
        
        has_service = len(user_services) > 0
        
        return {
            "user_id": user_id,
            "has_youtube_service": has_service,
            "active_sessions": len(user_services),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to check YouTube service status for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to check service status")

# Dependency to get YouTube service for authenticated requests
async def get_youtube_service_for_user(user_id: str) -> Any:
    """
    Dependency to get YouTube service for a user
    Returns the most recent service instance for the user
    """
    try:
        # Find the most recent service for this user
        user_service_keys = [
            key for key in _youtube_context.services.keys()
            if key.startswith(f"user_{user_id}_")
        ]
        
        if not user_service_keys:
            raise HTTPException(
                status_code=401,
                detail="No YouTube authentication found. Please authenticate with YouTube first."
            )
        
        # Get the most recent service (highest timestamp)
        latest_key = max(user_service_keys, key=lambda k: float(k.split('_')[-1]))
        service = _youtube_context.services[latest_key]
        
        logger.info(f"Using YouTube service for user {user_id}")
        return service
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get YouTube service for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get YouTube service"
        )

# Dependency to get YouTube tokens for a user
async def get_youtube_tokens_for_user(user_id: str) -> YouTubeTokensRequest:
    """
    Dependency to get YouTube tokens for a user
    Returns the most recent tokens for the user
    """
    try:
        # Find the most recent tokens for this user
        user_token_keys = [
            key for key in _youtube_context.tokens.keys()
            if key.startswith(f"user_{user_id}_")
        ]
        
        if not user_token_keys:
            raise HTTPException(
                status_code=401,
                detail="No YouTube tokens found. Please authenticate with YouTube first."
            )
        
        # Get the most recent tokens (highest timestamp)
        latest_key = max(user_token_keys, key=lambda k: float(k.split('_')[-1]))
        tokens = _youtube_context.tokens[latest_key]
        
        logger.info(f"Using YouTube tokens for user {user_id}")
        return tokens
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get YouTube tokens for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get YouTube tokens"
        )

@supabase_auth_router.delete("/clear-session/{user_id}")
async def clear_user_session(user_id: str) -> Dict[str, Any]:
    """
    Clear stored YouTube services and tokens for a user
    """
    try:
        # Remove all services and tokens for this user
        services_removed = 0
        tokens_removed = 0
        
        # Remove services
        services_to_remove = [
            key for key in _youtube_context.services.keys()
            if key.startswith(f"user_{user_id}_")
        ]
        for key in services_to_remove:
            del _youtube_context.services[key]
            services_removed += 1
        
        # Remove tokens
        tokens_to_remove = [
            key for key in _youtube_context.tokens.keys()
            if key.startswith(f"user_{user_id}_")
        ]
        for key in tokens_to_remove:
            del _youtube_context.tokens[key]
            tokens_removed += 1
        
        logger.info(f"Cleared session for user {user_id}: {services_removed} services, {tokens_removed} tokens")
        
        return {
            "user_id": user_id,
            "services_removed": services_removed,
            "tokens_removed": tokens_removed,
            "message": "Session cleared successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to clear session for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear session")

@supabase_auth_router.get("/health")
async def supabase_auth_health() -> Dict[str, Any]:
    """
    Health check for Supabase authentication system
    """
    return {
        "status": "healthy",
        "active_services": len(_youtube_context.services),
        "active_tokens": len(_youtube_context.tokens),
        "timestamp": datetime.now().isoformat()
    }

# Cleanup function to remove old sessions (call periodically)
def cleanup_old_sessions(max_age_hours: int = 2):
    """
    Remove sessions older than max_age_hours
    """
    try:
        current_time = datetime.now().timestamp()
        cutoff_time = current_time - (max_age_hours * 3600)
        
        # Remove old services
        old_service_keys = [
            key for key in _youtube_context.services.keys()
            if float(key.split('_')[-1]) < cutoff_time
        ]
        for key in old_service_keys:
            del _youtube_context.services[key]
        
        # Remove old tokens
        old_token_keys = [
            key for key in _youtube_context.tokens.keys()
            if float(key.split('_')[-1]) < cutoff_time
        ]
        for key in old_token_keys:
            del _youtube_context.tokens[key]
        
        if old_service_keys or old_token_keys:
            logger.info(f"Cleaned up {len(old_service_keys)} old services and {len(old_token_keys)} old tokens")
            
    except Exception as e:
        logger.error(f"Failed to cleanup old sessions: {e}")