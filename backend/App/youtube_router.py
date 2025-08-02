"""
YouTube API Router for Vidalytics
Contains all YouTube-related API endpoints extracted from main.py
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import logging
import traceback

# Import models
from backend.App.api_models import (
    YouTubeAnalyticsRequest, StandardResponse, create_error_response, create_success_response
)

# Import services
from backend.App.youtube_api_integration import get_youtube_integration
from backend.App.enhanced_user_context import get_user_context


# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/youtube", tags=["youtube"])

# =============================================================================
# Helper Functions
# =============================================================================

async def _resolve_channel_id(provided_channel_id: str, user_id: str) -> str:
    """
    Resolve channel ID with multiple fallback strategies
    1. Use provided channel_id if valid
    2. Try to get from user context/database
    3. Try to get from OAuth token
    4. Try to auto-detect from user's YouTube account
    """
    logger.info(f"Resolving channel ID for user {user_id}, provided: {provided_channel_id}")
    
    # Strategy 1: Use provided channel_id if it's valid
    if provided_channel_id and provided_channel_id not in ["", "Unknown", "null"]:
        logger.info(f"Using provided channel_id: {provided_channel_id}")
        return provided_channel_id
    
    # Strategy 2: Get from user context/database
    try:
        user_context = get_user_context(user_id)
        if user_context and user_context.get('channel_info'):
            stored_channel_id = user_context['channel_info'].get('channel_id')
            if stored_channel_id and stored_channel_id not in ["", "Unknown", "null"]:
                logger.info(f"Using stored channel_id: {stored_channel_id}")
                return stored_channel_id
    except Exception as e:
        logger.warning(f"Could not get channel_id from user context: {e}")
    
    # Strategy 3: Try to get from OAuth token and auto-fetch
    try:
        from backend.App.oauth_manager import get_oauth_manager
        oauth_manager = get_oauth_manager()
        token = await oauth_manager.get_token(user_id)
        
        if token and not token.is_expired():
            logger.info(f"Found valid OAuth token for user {user_id}, attempting to fetch channel info")
            
            # Try to fetch and store channel info automatically
            channel_info = await oauth_manager._fetch_and_store_channel_info(token)
            if channel_info and channel_info.get('channel_id'):
                logger.info(f"Auto-fetched channel_id: {channel_info['channel_id']}")
                return channel_info['channel_id']
                
        elif token and token.is_expired():
            logger.info(f"OAuth token expired for user {user_id}, attempting refresh")
            
            # Try to refresh the token
            refreshed_token = await oauth_manager.refresh_token(user_id)
            if refreshed_token:
                channel_info = await oauth_manager._fetch_and_store_channel_info(refreshed_token)
                if channel_info and channel_info.get('channel_id'):
                    logger.info(f"Auto-fetched channel_id after refresh: {channel_info['channel_id']}")
                    return channel_info['channel_id']
                    
    except Exception as e:
        logger.warning(f"OAuth-based channel_id resolution failed: {e}")
    
    # Strategy 4: Try to extract from channel name or handle (future enhancement)
    # This could involve searching YouTube API by channel name
    
    logger.warning(f"Could not resolve channel_id for user {user_id}")
    return None

async def _ensure_channel_id_stored(user_id: str, channel_id: str):
    """Store the resolved channel_id in user context for future use"""
    try:
        user_context = get_user_context(user_id)
        if user_context and user_context.get('channel_info'):
            current_channel_id = user_context['channel_info'].get('channel_id')
            if not current_channel_id or current_channel_id in ["", "Unknown", "null"]:
                # Update the user context with the resolved channel_id
                from backend.App.ai_services import update_user_context
                
                channel_info = user_context['channel_info'].copy()
                channel_info['channel_id'] = channel_id
                update_user_context(user_id, "channel_info", channel_info)
                logger.info(f"Stored channel_id {channel_id} for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to store channel_id for user {user_id}: {e}")

# =============================================================================
# YouTube Analytics Endpoints
# =============================================================================

@router.post("/analytics", response_model=StandardResponse)
async def get_youtube_analytics(request: YouTubeAnalyticsRequest):
    """Get comprehensive YouTube analytics"""
    try:
        logger.info(f"Getting YouTube analytics for channel: {request.channel_id}, user_id: {request.user_id}")
        
        integration = get_youtube_integration()
        
        # Enhanced channel ID resolution with multiple fallback options
        channel_id_to_use = await _resolve_channel_id(request.channel_id, request.user_id)
        
        if not channel_id_to_use:
            # Provide helpful error with guidance
            error_message = {
                "error": "No channel ID available",
                "details": "Please connect your YouTube channel first",
                "solutions": [
                    "Use OAuth to authenticate with YouTube",
                    "Manually set your channel ID in settings",
                    "Provide channel_id in the request"
                ],
                "oauth_url": f"/api/youtube/debug/oauth-redirect/{request.user_id}"
            }
            raise HTTPException(status_code=400, detail=error_message)
        
        # Store the resolved channel_id for future use
        await _ensure_channel_id_stored(request.user_id, channel_id_to_use)
        
        # Get channel analytics (with OAuth support)
        channel_data = await integration.get_channel_data(
            channel_id_to_use,
            include_recent_videos=request.include_videos,
            video_count=request.video_count,
            user_id=request.user_id
        )
        
        if not channel_data:
            logger.error(f"No channel data returned for channel_id: {channel_id_to_use}")
            raise HTTPException(status_code=404, detail="Channel not found or API error")
        
        # Get API status
        api_status = integration.get_api_status()
        
        logger.info(f"Channel data received - Title: {channel_data.title}, Videos found: {len(channel_data.recent_videos)}")
        
        return create_success_response(
            message="YouTube analytics retrieved successfully",
            data={
                "channel_data": {
                    "basic_info": {
                        "channel_id": channel_data.channel_id,
                        "title": channel_data.title,
                        "subscriber_count": channel_data.subscriber_count,
                        "video_count": channel_data.video_count,
                        "view_count": channel_data.view_count,
                        "upload_frequency": channel_data.upload_frequency
                    },
                    "recent_performance": {
                        "avg_views_last_30": channel_data.avg_views_last_30,
                        "avg_engagement_last_30": channel_data.avg_engagement_last_30,
                        "recent_video_count": len(channel_data.recent_videos)
                    },
                    "recent_videos": [
                        {
                            "video_id": video.get("video_id") if isinstance(video, dict) else video.video_id,
                            "title": video.get("title") if isinstance(video, dict) else video.title,
                            "view_count": video.get("view_count") if isinstance(video, dict) else video.view_count,
                            "like_count": video.get("like_count") if isinstance(video, dict) else video.like_count,
                            "comment_count": video.get("comment_count") if isinstance(video, dict) else video.comment_count,
                            "ctr": video.get("ctr_actual") if isinstance(video, dict) else getattr(video, 'ctr_actual', None),
                            "published_at": video.get("published_at") if isinstance(video, dict) else video.published_at,
                            "thumbnail": video.get("thumbnail_url") if isinstance(video, dict) else video.thumbnail_url,
                            "duration": video.get("duration") if isinstance(video, dict) else video.duration,
                            "category_id": video.get("category_id") if isinstance(video, dict) else video.category_id,
                            "retention": video.get("retention_actual") if isinstance(video, dict) else getattr(video, 'retention_actual', None),
                            "analytics": video.get("analytics") if isinstance(video, dict) else video.analytics
                        }
                        for video in channel_data.recent_videos[:request.video_count if request.video_count else 50]
                    ]
                },
                "api_status": api_status
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting YouTube analytics: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"YouTube analytics failed: {e}")

@router.get("/quota")
async def get_youtube_quota():
    """Get YouTube API quota status"""
    try:
        integration = get_youtube_integration()
        quota_status = integration.quota_manager.get_quota_status()
        
        return create_success_response(
            message="YouTube quota status retrieved",
            data={"quota_status": quota_status}
        )
    
    except Exception as e:
        logger.error(f"Error getting YouTube quota: {e}")
        raise HTTPException(status_code=500, detail="Failed to get quota status")

@router.post("/auto-detect-channel", response_model=StandardResponse)
async def auto_detect_channel(user_id: str = "default_user"):
    """Automatically detect and set user's YouTube channel ID"""
    try:
        logger.info(f"Auto-detecting channel for user: {user_id}")
        
        # Try to resolve channel ID using all available methods
        channel_id = await _resolve_channel_id("", user_id)
        
        if not channel_id:
            return create_error_response(
                "Channel detection failed",
                "Could not automatically detect your YouTube channel. Please connect via OAuth or set manually.",
                status_code=404
            )
        
        # Get basic channel info to verify it works
        integration = get_youtube_integration()
        channel_data = await integration.get_channel_data(
            channel_id,
            include_recent_videos=False,
            video_count=1,
            user_id=user_id
        )
        
        if not channel_data:
            return create_error_response(
                "Channel verification failed",
                f"Detected channel ID {channel_id} but could not fetch channel data",
                status_code=400
            )
        
        # Store the detected channel_id
        await _ensure_channel_id_stored(user_id, channel_id)
        
        return create_success_response(
            "Channel detected and configured successfully",
            {
                "channel_id": channel_id,
                "channel_title": channel_data.title,
                "subscriber_count": channel_data.subscriber_count,
                "video_count": channel_data.video_count
            }
        )
        
    except Exception as e:
        logger.error(f"Error in auto-detect channel: {e}")
        raise HTTPException(status_code=500, detail="Failed to auto-detect channel")

@router.post("/set-channel-id", response_model=StandardResponse)
async def set_channel_id(channel_id: str, user_id: str = "default_user"):
    """Manually set a user's YouTube channel ID"""
    try:
        logger.info(f"Setting channel_id {channel_id} for user: {user_id}")
        
        # Validate the channel_id by trying to fetch basic data
        integration = get_youtube_integration()
        try:
            channel_data = await integration.get_channel_data(
                channel_id,
                include_recent_videos=False,
                video_count=1,
                user_id=user_id
            )
        except Exception as e:
            logger.error(f"Invalid channel_id {channel_id}: {e}")
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid channel ID '{channel_id}'. Please check the ID and try again."
            )
        
        if not channel_data:
            raise HTTPException(
                status_code=404,
                detail=f"Channel '{channel_id}' not found. Please verify the channel ID."
            )
        
        # Store the channel_id
        await _ensure_channel_id_stored(user_id, channel_id)
        
        return create_success_response(
            "Channel ID set successfully",
            {
                "channel_id": channel_id,
                "channel_title": channel_data.title,
                "subscriber_count": channel_data.subscriber_count,
                "video_count": channel_data.video_count,
                "message": f"Successfully connected to '{channel_data.title}'"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting channel ID: {e}")
        raise HTTPException(status_code=500, detail="Failed to set channel ID")

@router.get("/my-videos/{user_id}", response_model=StandardResponse)
async def get_my_videos(user_id: str, count: int = 20):
    """Get user's YouTube videos - simplified endpoint for frontend"""
    try:
        logger.info(f"Getting videos for user: {user_id}")
        
        # Use the analytics endpoint internally but simplify the response
        request = YouTubeAnalyticsRequest(
            channel_id="",  # Will be auto-resolved
            user_id=user_id,
            include_videos=True,
            video_count=count
        )
        
        # Get the analytics data
        analytics_response = await get_youtube_analytics(request)
        
        if analytics_response.get("status") != "success":
            raise HTTPException(status_code=400, detail="Failed to fetch videos")
        
        # Extract just the video data for simplified response
        channel_data = analytics_response["data"]["channel_data"]
        videos = channel_data["recent_videos"]
        
        return create_success_response(
            f"Retrieved {len(videos)} videos successfully",
            {
                "videos": videos,
                "channel_info": {
                    "title": channel_data["basic_info"]["title"],
                    "subscriber_count": channel_data["basic_info"]["subscriber_count"],
                    "total_videos": channel_data["basic_info"]["video_count"]
                },
                "total_count": len(videos)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user videos: {e}")
        raise HTTPException(status_code=500, detail="Failed to get videos")

@router.get("/channel-status/{user_id}", response_model=StandardResponse)
async def get_channel_status(user_id: str):
    """Check if user has a channel configured and get basic info"""
    try:
        # Try to resolve channel ID
        channel_id = await _resolve_channel_id("", user_id)
        
        if not channel_id:
            return create_success_response(
                "No channel configured",
                {
                    "has_channel": False,
                    "channel_id": None,
                    "suggestions": [
                        "Use OAuth to connect your YouTube channel",
                        "Manually set your channel ID",
                        "Auto-detect your channel"
                    ],
                    "endpoints": {
                        "oauth": f"/api/youtube/debug/oauth-redirect/{user_id}",
                        "auto_detect": f"/api/youtube/auto-detect-channel?user_id={user_id}",
                        "manual_set": "/api/youtube/set-channel-id"
                    }
                }
            )
        
        # Get basic channel info
        integration = get_youtube_integration()
        try:
            channel_data = await integration.get_channel_data(
                channel_id,
                include_recent_videos=False,
                video_count=1,
                user_id=user_id
            )
            
            return create_success_response(
                "Channel configured successfully",
                {
                    "has_channel": True,
                    "channel_id": channel_id,
                    "channel_title": channel_data.title,
                    "subscriber_count": channel_data.subscriber_count,
                    "video_count": channel_data.video_count,
                    "can_fetch_videos": True
                }
            )
            
        except Exception as e:
            return create_error_response(
                "Channel ID configured but inaccessible",
                f"Channel ID {channel_id} is set but cannot fetch data: {str(e)}",
                status_code=400
            )
        
    except Exception as e:
        logger.error(f"Error checking channel status: {e}")
        raise HTTPException(status_code=500, detail="Failed to check channel status")

@router.get("/oauth-status/{user_id}", response_model=StandardResponse)
async def get_oauth_status(user_id: str):
    """Get OAuth authentication status for frontend"""
    try:
        from backend.App.oauth_manager import get_oauth_manager
        
        oauth_manager = get_oauth_manager()
        token = await oauth_manager.get_token(user_id)
        
        if not token:
            return create_success_response(
                "Not authenticated",
                {
                    "authenticated": False,
                    "token_exists": False,
                    "oauth_url": f"/api/youtube/debug/oauth-redirect/{user_id}"
                }
            )
        
        return create_success_response(
            "OAuth status retrieved",
            {
                "authenticated": True,
                "token_exists": True,
                "token_expired": token.is_expired(),
                "expires_at": token.expires_at.isoformat(),
                "can_refresh": bool(token.refresh_token),
                "user_id": user_id
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting OAuth status: {e}")
        return create_error_response(
            "Failed to get OAuth status",
            str(e),
            status_code=500
        )

# =============================================================================
# YouTube Categories Endpoints
# =============================================================================

@router.get("/categories")
async def get_youtube_categories():
    """Get YouTube video categories"""
    try:
        integration = get_youtube_integration()
        
        # Get standard YouTube categories
        categories = await integration.get_video_categories()
        
        return create_success_response(
            message="YouTube categories retrieved successfully",
            data={"categories": categories}
        )
    
    except Exception as e:
        logger.error(f"Error getting YouTube categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get YouTube categories")

@router.get("/categories/{channel_id}/analysis")
async def analyze_channel_categories(channel_id: str, user_id: str = "default_user"):
    """Analyze how a channel's videos are distributed across YouTube categories"""
    try:
        logger.info(f"Analyzing category distribution for channel: {channel_id}")
        
        integration = get_youtube_integration()
        
        # Get channel data with category information
        channel_data = await integration.get_channel_data(
            channel_id,
            include_recent_videos=True,
            video_count=50,
            user_id=user_id
        )
        
        if not channel_data:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        # Analyze category distribution
        category_analysis = {}
        total_videos = len(channel_data.recent_videos)
        
        for video in channel_data.recent_videos:
            category_id = video.get("category_id") if isinstance(video, dict) else video.category_id
            if category_id:
                if category_id not in category_analysis:
                    category_analysis[category_id] = {
                        "count": 0,
                        "total_views": 0,
                        "avg_views": 0,
                        "videos": []
                    }
                
                view_count = video.get("view_count") if isinstance(video, dict) else video.view_count
                category_analysis[category_id]["count"] += 1
                category_analysis[category_id]["total_views"] += view_count or 0
                category_analysis[category_id]["videos"].append({
                    "video_id": video.get("video_id") if isinstance(video, dict) else video.video_id,
                    "title": video.get("title") if isinstance(video, dict) else video.title,
                    "view_count": view_count
                })
        
        # Calculate percentages and averages
        for category_id, data in category_analysis.items():
            data["percentage"] = (data["count"] / total_videos) * 100
            data["avg_views"] = data["total_views"] / data["count"] if data["count"] > 0 else 0
        
        # Get category names
        categories = await integration.get_video_categories()
        category_names = {cat["id"]: cat["snippet"]["title"] for cat in categories.get("items", [])}
        
        # Add category names to analysis
        for category_id, data in category_analysis.items():
            data["category_name"] = category_names.get(category_id, f"Category {category_id}")
        
        return create_success_response(
            message="Channel category analysis completed",
            data={
                "channel_id": channel_id,
                "total_videos_analyzed": total_videos,
                "category_distribution": category_analysis,
                "top_category": max(category_analysis.items(), key=lambda x: x[1]["count"])[0] if category_analysis else None
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing channel categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze channel categories")

# =============================================================================
# OAuth and Debug Endpoints
# =============================================================================

@router.get("/debug/oauth/{user_id}")
async def debug_oauth_status(user_id: str):
    """Debug OAuth status for a user"""
    try:
        from backend.App.oauth_manager import get_oauth_manager
        
        oauth_manager = get_oauth_manager()
        token = await oauth_manager.get_token(user_id)
        
        if not token:
            return create_error_response(
                "OAuth not authenticated",
                "No OAuth token found for user",
                status_code=404
            )
        
        return create_success_response(
            "OAuth status retrieved",
            {
                "authenticated": True,
                "user_id": user_id,
                "token_exists": True,
                "token_expired": token.is_expired(),
                "expires_at": token.expires_at.isoformat(),
                "scopes": token.scope,
                "created_at": token.created_at.isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error checking OAuth status for {user_id}: {e}")
        return create_error_response(
            "OAuth status check failed",
            str(e),
            status_code=500
        )

@router.get("/debug/oauth-test")
async def test_oauth_setup():
    """Test if OAuth is properly configured"""
    try:
        from backend.App.oauth_manager import get_oauth_manager
        
        oauth_manager = get_oauth_manager()
        
        # Check OAuth configuration
        config_status = {
            "client_id_exists": bool(oauth_manager.client_id),
            "client_secret_exists": bool(oauth_manager.client_secret),
            "redirect_uri_exists": bool(oauth_manager.redirect_uri),
            "redirect_uri": oauth_manager.redirect_uri,
            "scopes": oauth_manager.scopes
        }
        
        oauth_configured = all([
            oauth_manager.client_id,
            oauth_manager.client_secret, 
            oauth_manager.redirect_uri
        ])
        
        return create_success_response(
            "OAuth configuration checked",
            {
                "oauth_configured": oauth_configured,
                "config": config_status
            }
        )
        
    except Exception as e:
        return create_error_response(
            "OAuth configuration check failed",
            str(e),
            status_code=500
        )

@router.get("/debug/test-oauth/{user_id}")
async def test_oauth_flow(user_id: str):
    """Test OAuth flow for a user"""
    try:
        from backend.App.oauth_manager import get_oauth_manager
        
        oauth_manager = get_oauth_manager()
        
        # Generate authorization URL
        auth_url, state = oauth_manager.generate_authorization_url(user_id)
        
        return create_success_response(
            "OAuth test URL generated",
            {
                "user_id": user_id,
                "auth_url": auth_url,
                "state": state,
                "message": "Click the auth_url to start OAuth flow"
            }
        )
        
    except Exception as e:
        logger.error(f"Error testing OAuth flow for {user_id}: {e}")
        return create_error_response(
            "OAuth flow test failed",
            str(e),
            status_code=500
        )

@router.get("/debug/oauth-redirect/{user_id}")
async def oauth_redirect(user_id: str):
    """Redirect to OAuth flow"""
    try:
        from backend.App.oauth_manager import get_oauth_manager
        
        oauth_manager = get_oauth_manager()
        auth_url, state = oauth_manager.generate_authorization_url(user_id)
        
        return RedirectResponse(url=auth_url)
        
    except Exception as e:
        logger.error(f"Error redirecting to OAuth for {user_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/debug/fetch-channel-info/{user_id}")
async def fetch_channel_info(user_id: str):
    """Manually fetch and store channel info for a user"""
    try:
        from backend.App.oauth_manager import get_oauth_manager
        
        oauth_manager = get_oauth_manager()
        token = await oauth_manager.get_token(user_id)
        
        if not token:
            raise HTTPException(status_code=404, detail="No OAuth token found")
        
        if token.is_expired():
            # Try to refresh first
            token = await oauth_manager.refresh_token(user_id)
            if not token:
                raise HTTPException(status_code=401, detail="Token expired and refresh failed")
        
        # Fetch channel info
        await oauth_manager._fetch_and_store_channel_info(token)
        
        return create_success_response(
            "Channel info fetched successfully",
            {"user_id": user_id}
        )
        
    except Exception as e:
        logger.error(f"Error fetching channel info for {user_id}: {e}")
        return create_error_response(
            "Channel info fetch failed",
            str(e),
            status_code=500
        )

@router.get("/debug/refresh-token/{user_id}")
async def debug_refresh_token(user_id: str):
    """Debug token refresh for a user"""
    try:
        from backend.App.oauth_manager import get_oauth_manager
        
        oauth_manager = get_oauth_manager()
        
        # Check current token
        current_token = await oauth_manager.get_token(user_id)
        if not current_token:
            return create_error_response(
                "No token found",
                "No OAuth token exists for this user",
                status_code=404
            )
        
        # Try to refresh
        new_token = await oauth_manager.refresh_token(user_id)
        
        if new_token:
            return create_success_response(
                "Token refreshed successfully",
                {
                    "user_id": user_id,
                    "old_expires_at": current_token.expires_at.isoformat(),
                    "new_expires_at": new_token.expires_at.isoformat(),
                    "refreshed": True
                }
            )
        else:
            return create_error_response(
                "Token refresh failed",
                "Could not refresh the OAuth token",
                status_code=400
            )
        
    except Exception as e:
        logger.error(f"Error refreshing token for {user_id}: {e}")
        return create_error_response(
            "Token refresh error",
            str(e),
            status_code=500
        )