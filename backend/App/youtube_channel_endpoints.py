"""
YouTube Channel API Endpoints for MYTA
Handles fetching user's YouTube channel data including banner, avatar, and channel info
"""

import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.App.oauth_manager import get_oauth_manager
from backend.App.youtube_api_integration import get_youtube_integration

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/youtube", tags=["youtube"])

# Request/Response models
class AuthUrlRequest(BaseModel):
    userId: str

class AuthUrlResponse(BaseModel):
    authUrl: str
    state: str

class ChannelDataResponse(BaseModel):
    channelData: Dict[str, Any]
    connected: bool

class ConnectionStatusResponse(BaseModel):
    connected: bool
    channelData: Optional[Dict[str, Any]] = None

# Get OAuth manager and YouTube integration
oauth_manager = get_oauth_manager()
youtube_integration = get_youtube_integration()

@router.post("/auth-url", response_model=AuthUrlResponse)
async def get_auth_url(request: AuthUrlRequest):
    """Generate YouTube OAuth authorization URL"""
    try:
        auth_url, state = oauth_manager.generate_authorization_url(request.userId)
        
        return AuthUrlResponse(
            authUrl=auth_url,
            state=state
        )
    except Exception as e:
        logger.error(f"Failed to generate auth URL: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate authorization URL")

@router.get("/connection-status", response_model=ConnectionStatusResponse)
async def get_connection_status():
    """Check if user has connected their YouTube account"""
    try:
        # For now, use default user ID - in production, get from auth context
        user_id = "default_user"
        
        # Check if user has valid OAuth token
        token = await oauth_manager.get_valid_token(user_id)
        
        if token:
            # Try to fetch channel data to verify connection
            try:
                channel_data = await fetch_user_channel_data(user_id)
                return ConnectionStatusResponse(
                    connected=True,
                    channelData=channel_data
                )
            except Exception as e:
                logger.warning(f"Token exists but failed to fetch channel data: {e}")
                return ConnectionStatusResponse(connected=False)
        else:
            return ConnectionStatusResponse(connected=False)
            
    except Exception as e:
        logger.error(f"Failed to check connection status: {e}")
        return ConnectionStatusResponse(connected=False)

@router.get("/channel-data", response_model=ChannelDataResponse)
async def get_channel_data():
    """Fetch user's YouTube channel data"""
    try:
        # For now, use default user ID - in production, get from auth context
        user_id = "default_user"
        
        # Check if user has valid OAuth token
        token = await oauth_manager.get_valid_token(user_id)
        if not token:
            raise HTTPException(status_code=401, detail="YouTube account not connected")
        
        # Fetch channel data
        channel_data = await fetch_user_channel_data(user_id)
        
        return ChannelDataResponse(
            channelData=channel_data,
            connected=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch channel data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch channel data")

@router.post("/disconnect")
async def disconnect_youtube():
    """Disconnect user's YouTube account"""
    try:
        # For now, use default user ID - in production, get from auth context
        user_id = "default_user"
        
        # Revoke OAuth token
        success = await oauth_manager.revoke_token(user_id)
        
        if success:
            return {"message": "YouTube account disconnected successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to disconnect YouTube account")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to disconnect YouTube: {e}")
        raise HTTPException(status_code=500, detail="Failed to disconnect YouTube account")

async def fetch_user_channel_data(user_id: str) -> Dict[str, Any]:
    """Fetch comprehensive channel data for a user"""
    try:
        # Get authenticated YouTube service
        youtube_service = await oauth_manager.get_youtube_service(user_id)
        if not youtube_service:
            raise Exception("Failed to get authenticated YouTube service")
        
        # Fetch channel data using the service
        channels_response = youtube_service.channels().list(
            part='snippet,statistics,brandingSettings',
            mine=True
        ).execute()
        
        if not channels_response.get('items'):
            raise Exception("No channel found for authenticated user")
        
        channel = channels_response['items'][0]
        
        # Extract channel information
        snippet = channel.get('snippet', {})
        statistics = channel.get('statistics', {})
        branding = channel.get('brandingSettings', {})
        
        # Get banner URL from branding settings
        banner_url = None
        if branding.get('image', {}).get('bannerExternalUrl'):
            banner_url = branding['image']['bannerExternalUrl']
        
        # Format channel data
        channel_data = {
            'id': channel.get('id'),
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'customUrl': snippet.get('customUrl', ''),
            'publishedAt': snippet.get('publishedAt'),
            'thumbnails': snippet.get('thumbnails', {}),
            'bannerExternalUrl': banner_url,
            'subscriberCount': statistics.get('subscriberCount', '0'),
            'videoCount': statistics.get('videoCount', '0'),
            'viewCount': statistics.get('viewCount', '0'),
            'country': snippet.get('country'),
            'defaultLanguage': snippet.get('defaultLanguage')
        }
        
        logger.info(f"Successfully fetched channel data for user {user_id}: {channel_data['title']}")
        return channel_data
        
    except Exception as e:
        logger.error(f"Failed to fetch channel data for user {user_id}: {e}")
        raise

# OAuth callback handler (this would typically be in a separate auth module)
@router.get("/oauth/callback")
async def oauth_callback(code: str, state: str):
    """Handle OAuth callback from YouTube"""
    try:
        # Exchange code for tokens
        token_data = await oauth_manager.exchange_code_for_token(code, state)
        
        if token_data:
            return {"message": "YouTube account connected successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to connect YouTube account")
            
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        raise HTTPException(status_code=500, detail="OAuth callback failed")

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check for YouTube API integration"""
    try:
        api_status = youtube_integration.get_api_status()
        return {
            "status": "healthy" if api_status["api_available"] else "degraded",
            "api_available": api_status["api_available"],
            "quota_remaining": api_status.get("quota_remaining", "unknown")
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
