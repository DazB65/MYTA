"""
CreatorMate Multi-Agent API - Refactored Main Application
Modular FastAPI application with separated routers for better maintainability
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import logging
import traceback
import os
from pydantic import ValidationError
from slowapi.errors import RateLimitExceeded

# Import security middleware
from security_middleware import add_security_middleware
from security_config import get_security_config

# Import API models
from api_models import (
    ChannelInfo, StandardResponse, HealthResponse, SystemHealthResponse,
    create_error_response, create_success_response
)

# Import routers
from agent_router import router as agent_router
from youtube_router import router as youtube_router
from pillars_router import router as pillars_router
from analytics_router import router as analytics_router
from oauth_endpoints import oauth_router
from content_cards_router import router as content_cards_router

# Import services
from ai_services import update_user_context, get_user_context

# Import rate limiting
from rate_limiter import limiter, custom_rate_limit_handler, get_rate_limit

# Security helpers
def add_security_headers(response):
    """Add security headers to response"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY" 
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CreatorMate Multi-Agent API", 
    version="2.0.0",
    description="Hierarchical multi-agent system for YouTube analytics and optimization"
)

# Add rate limiter to app state
app.state.limiter = limiter

# Add rate limit exceeded handler
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

# =============================================================================
# System Initialization
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize the CreatorMate multi-agent system"""
    try:
        from api_startup import initialize_creatormate_system
        initialization_result = await initialize_creatormate_system()
        
        if initialization_result["overall_status"] == "success":
            logger.info("🚀 CreatorMate Multi-Agent System started successfully")
        else:
            logger.warning(f"⚠️ CreatorMate started with warnings: {initialization_result['overall_status']}")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize CreatorMate system: {e}")
        # Don't crash the server, but log the error

# =============================================================================
# Exception Handlers
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unexpected errors"""
    logger.error(f"Global exception handler caught: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content=create_error_response(
            "Internal server error",
            "An unexpected error occurred. Please try again later.",
            status_code=500
        )
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    """Validation error handler"""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content=create_error_response(
            "Validation error",
            str(exc),
            status_code=422
        )
    )

# =============================================================================
# Middleware Configuration
# =============================================================================

# Add security middleware first (order matters)
add_security_middleware(app)

# Add CORS middleware
security_config = get_security_config()
allowed_origins = ["http://localhost:3000", "http://localhost:8888"] if not security_config.is_production() else ["https://your-domain.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# =============================================================================
# Include Routers
# =============================================================================

# Include agent router (handles chat, quick actions, specialized agents)
app.include_router(agent_router)

# Include YouTube router (handles analytics, categories, OAuth)
app.include_router(youtube_router)

# Include content pillars router (handles pillars CRUD, video allocation)
app.include_router(pillars_router)

# Include analytics router (handles dashboard analytics data)
app.include_router(analytics_router)

# Include OAuth router (handles authentication flow)
app.include_router(oauth_router)

# Include content cards router (handles Content Studio functionality)
app.include_router(content_cards_router)

# =============================================================================
# Core API Endpoints
# =============================================================================

@app.post("/api/agent/set-channel-info", response_model=StandardResponse)
@limiter.limit(get_rate_limit("public", "default"))
async def set_channel_info(request: Request, channel_info: ChannelInfo):
    """Endpoint to manually set channel information"""
    try:
        # Validate channel info
        channel_info.validate_metrics()
        
        logger.info(f"Updating channel info for user: {channel_info.user_id}")
        
        # Extract channel info fields
        info = {
            "name": channel_info.name,
            "niche": channel_info.niche,
            "content_type": channel_info.content_type,
            "subscriber_count": channel_info.subscriber_count,
            "avg_view_count": channel_info.avg_view_count,
            "ctr": channel_info.ctr,
            "retention": channel_info.retention,
            "upload_frequency": channel_info.upload_frequency,
            "video_length": channel_info.video_length,
            "monetization_status": channel_info.monetization_status,
            "primary_goal": channel_info.primary_goal,
            "notes": channel_info.notes
        }
        
        # Update user context
        result = update_user_context(channel_info.user_id, "channel_info", info)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to update channel information")
        
        return create_success_response("Channel information updated successfully")
    
    except ValueError as e:
        logger.error(f"Validation error in set_channel_info: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in set_channel_info: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to update channel information")

@app.get("/api/agent/insights/{user_id}")
async def get_insights(user_id: str):
    """Get dynamic insights for a user"""
    try:
        logger.info(f"Getting insights for user: {user_id}")
        
        from insights_engine import insights_engine
        
        # Generate new insights
        new_insights = insights_engine.generate_insights_for_user(user_id, limit=3)
        
        # Get existing insights
        existing_insights = insights_engine.get_user_insights(user_id, limit=5)
        
        # Combine and deduplicate
        all_insights = new_insights + existing_insights
        seen_titles = set()
        unique_insights = []
        
        for insight in all_insights:
            if insight["title"] not in seen_titles:
                seen_titles.add(insight["title"])
                unique_insights.append(insight)
        
        return create_success_response(
            "Insights retrieved successfully",
            {"insights": unique_insights[:5]}
        )
    
    except Exception as e:
        logger.error(f"Unexpected error in get_insights: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to get insights")

@app.get("/api/agent/context/{user_id}")
async def get_user_context_endpoint(user_id: str):
    """Get user context including channel information"""
    try:
        logger.info(f"📡 Getting context for user: {user_id}")
        
        # Get user context
        context = get_user_context(user_id)
        
        # Log what we're returning so we can debug
        channel_info = context["channel_info"]
        logger.info(f"📊 Returning channel info for {user_id}: '{channel_info['name']}' with {channel_info['subscriber_count']} subscribers")
        
        return create_success_response(
            "User context retrieved successfully",
            {"channel_info": channel_info}
        )
    
    except Exception as e:
        logger.error(f"Unexpected error in get_user_context_endpoint: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to get user context")

@app.get("/api/get-user-profile")
async def get_user_profile(request: Request):
    """Get user profile with YouTube channel banner"""
    try:
        # Get user_id from cookie or header
        user_id = request.cookies.get("user_id") or request.headers.get("X-User-Id")
        if not user_id:
            # Try to get from query params as fallback
            user_id = request.query_params.get("user_id")
            
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found")
        
        # Get user context
        context = get_user_context(user_id)
        if not context:
            raise HTTPException(status_code=404, detail="User not found")
        
        channel_info = context.get("channel_info", {})
        
        # Check if we have YouTube integration data
        youtube_data = None
        banner_url = None
        debug_info = {}
        
        # Try to get YouTube channel data if OAuth is connected
        try:
            from oauth_manager import get_oauth_manager
            from youtube_api_integration import get_youtube_integration
            
            logger.info(f"Getting user profile for user_id: {user_id}")
            
            oauth_manager = get_oauth_manager()
            oauth_token = await oauth_manager.get_valid_token(user_id)
            
            debug_info["oauth_token_exists"] = oauth_token is not None
            debug_info["has_access_token"] = bool(oauth_token and oauth_token.access_token)
            
            logger.info(f"OAuth token for user {user_id}: {oauth_token}")
            
            # Get channel ID from user context
            user_channel_id = channel_info.get("channel_id")
            debug_info["channel_id_from_context"] = user_channel_id
            
            # Try to get channel data
            if user_channel_id:
                logger.info(f"Found channel ID {user_channel_id} for user {user_id}")
                
                # Get YouTube API integration instance
                youtube_api = get_youtube_integration()
                
                try:
                    # Try to get channel data with banner using the YouTube API integration
                    channel_metrics = await youtube_api.get_channel_data(
                        channel_id=user_channel_id,
                        user_id=user_id,
                        include_recent_videos=False
                    )
                    
                    debug_info["channel_metrics_returned"] = channel_metrics is not None
                    
                    if channel_metrics:
                        banner_url = channel_metrics.banner_url
                        debug_info["banner_url_from_integration"] = banner_url
                        logger.info(f"Found banner URL from integration: {banner_url}")
                        
                        # Log all the channel metrics for debugging
                        logger.info(f"Channel metrics: title={channel_metrics.title}, banner_url={channel_metrics.banner_url}")
                    else:
                        logger.warning(f"No channel metrics returned for channel {user_channel_id}")
                        
                except Exception as e:
                    debug_info["channel_fetch_error"] = str(e)
                    logger.warning(f"Failed to fetch YouTube channel data: {e}")
            
            # If no channel ID but we have a channel name, try known mappings
            elif channel_info.get("name") and channel_info.get("name") != "Unknown":
                channel_name = channel_info.get("name")
                logger.info(f"No channel ID found, checking known channel mappings for: {channel_name}")
                
                # Temporary solution: known channel mappings
                # TODO: Implement proper channel search or fix OAuth to save channel IDs
                known_channels = {
                    "THE AUSTRALIA STORY  - History, Legends and Land": "UCsLRPnpYsl2E4ficU5wfHWg"
                }
                
                if channel_name in known_channels:
                    found_channel_id = known_channels[channel_name]
                    logger.info(f"Found known channel ID: {found_channel_id}")
                    
                    # Get YouTube API integration instance
                    youtube_api = get_youtube_integration()
                    
                    try:
                        # Get channel data with banner
                        channel_metrics = await youtube_api.get_channel_data(
                            channel_id=found_channel_id,
                            user_id=user_id,
                            include_recent_videos=False
                        )
                        
                        if channel_metrics:
                            banner_url = channel_metrics.banner_url
                            debug_info["banner_url_from_known"] = banner_url
                            logger.info(f"Found banner URL from known channel: {banner_url}")
                            
                            # Update the user's channel_id for future use
                            from ai_services import update_user_context
                            update_user_context(user_id, "channel_info", {
                                **channel_info,
                                "channel_id": found_channel_id
                            })
                            logger.info(f"Updated channel_id for user {user_id}")
                        else:
                            logger.warning(f"No channel metrics returned for known channel {found_channel_id}")
                            
                    except Exception as e:
                        debug_info["known_channel_error"] = str(e)
                        logger.warning(f"Failed to fetch known channel data: {e}")
                else:
                    debug_info["channel_not_in_known_list"] = True
                    logger.info(f"Channel '{channel_name}' not in known mappings")
            
            # Fallback: try OAuth if available
            elif oauth_token and oauth_token.access_token:
                logger.info(f"No channel ID found, trying OAuth approach for user {user_id}")
                
                try:
                    # Try to get channel data using OAuth
                    youtube_service = await oauth_manager.get_youtube_service(user_id)
                    
                    if youtube_service:
                        # Get the user's channel data with branding settings
                        channels_response = youtube_service.channels().list(
                            part='snippet,statistics,brandingSettings',
                            mine=True
                        ).execute()
                        
                        debug_info["youtube_api_response"] = bool(channels_response.get('items'))
                        
                        if channels_response.get('items'):
                            channel = channels_response['items'][0]
                            branding_settings = channel.get('brandingSettings', {})
                            
                            # Extract banner URL from branding settings
                            if branding_settings and 'image' in branding_settings:
                                banner_url = branding_settings['image'].get('bannerExternalUrl')
                                debug_info["banner_url_from_oauth"] = banner_url
                                logger.info(f"Found banner URL from OAuth: {banner_url}")
                            else:
                                debug_info["no_branding_settings"] = True
                                logger.info("No branding settings found in YouTube API response")
                        else:
                            debug_info["no_channel_data"] = True
                            logger.warning("No channel data returned from YouTube API")
                    else:
                        debug_info["no_youtube_service"] = True
                        logger.warning("Could not get YouTube service for user")
                        
                except Exception as e:
                    debug_info["oauth_fetch_error"] = str(e)
                    logger.warning(f"Failed to fetch YouTube channel data via OAuth: {e}")
            else:
                debug_info["no_channel_id_or_oauth"] = True
                logger.info(f"No channel ID or valid OAuth for user {user_id}")
        except Exception as e:
            debug_info["integration_error"] = str(e)
            logger.warning(f"Failed to access YouTube integration: {e}")
        
        # Return user profile data
        result = {
            "userName": channel_info.get("name", "Creator"),
            "bannerUrl": banner_url
        }
        
        # Add debug info in development (remove this in production)
        if request.query_params.get("debug") == "true":
            result["debug"] = debug_info
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_user_profile: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to retrieve user profile")

# =============================================================================
# Health Check Endpoints
# =============================================================================

@app.get("/health", response_model=HealthResponse)
@limiter.limit(get_rate_limit("public", "health"))
def health_check(request: Request):
    """Basic health check endpoint"""
    response = JSONResponse(content={
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "CreatorMate Multi-Agent API",
        "version": "2.0.0"
    })
    return add_security_headers(response)

@app.get("/api/health/system", response_model=SystemHealthResponse)
def system_health():
    """Comprehensive system health check"""
    try:
        from api_startup import get_system_status
        system_status = get_system_status()
        
        # Calculate overall health score
        health_components = [
            system_status.get("model_integrations", {}).get("overall_health", 0.5),
            system_status.get("youtube_api", {}).get("health_score", 0.5),
            system_status.get("cache_system", {}).get("health_score", 0.8),
            1.0 if system_status.get("ready_for_requests", False) else 0.0
        ]
        
        overall_health = sum(health_components) / len(health_components)
        
        return SystemHealthResponse(
            overall_health=overall_health,
            model_integrations=system_status.get("model_integrations", {}),
            youtube_api=system_status.get("youtube_api", {}),
            cache_system=system_status.get("cache_system", {}),
            timestamp=datetime.now().isoformat(),
            status="healthy" if overall_health > 0.7 else "degraded" if overall_health > 0.4 else "unhealthy"
        )
    
    except Exception as e:
        logger.error(f"Error in system health check: {e}")
        return SystemHealthResponse(
            overall_health=0.0,
            model_integrations={"error": str(e)},
            youtube_api={"error": str(e)},
            cache_system={"error": str(e)},
            timestamp=datetime.now().isoformat(),
            status="unhealthy"
        )

# =============================================================================
# Static File Serving
# =============================================================================

# Mount static files (React build) with proper SPA routing
if os.path.exists("../frontend-dist"):
    # Mount static assets (CSS, JS, images)
    app.mount("/assets", StaticFiles(directory="../frontend-dist/assets"), name="assets")
    
    # Root route
    @app.get("/")
    def serve_root():
        """Serve the React SPA for root route"""
        return FileResponse("../frontend-dist/index.html")
    
    # Catch-all route for SPA routing - serve index.html for non-API frontend routes only
    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        """Serve the React SPA for frontend routes"""
        # Let API and auth routes pass through to their handlers (should not reach here)
        if full_path.startswith("api/") or full_path.startswith("auth/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # For frontend routes like /videos, /pillars, etc., serve the React app
        frontend_routes = ["dashboard", "videos", "pillars", "settings", "channel", "health"]
        if any(full_path.startswith(route) for route in frontend_routes) or full_path == "":
            return FileResponse("../frontend-dist/index.html")
        
        # For unknown routes, also serve React (let React handle 404s)
        return FileResponse("../frontend-dist/index.html")
    
    logger.info("📁 Frontend SPA configured with proper routing support")
else:
    logger.warning("⚠️ Frontend build directory not found. Run 'npm run build' in frontend-new/")

# =============================================================================
# Application Info
# =============================================================================

@app.get("/api/info")
def get_app_info():
    """Get application information"""
    return create_success_response(
        "Application info retrieved",
        {
            "name": "CreatorMate Multi-Agent API",
            "version": "2.0.0",
            "description": "Hierarchical multi-agent system for YouTube analytics and optimization",
            "architecture": "modular_fastapi_with_routers",
            "agents": [
                "boss_agent", 
                "content_analysis", 
                "audience_insights", 
                "seo_discoverability", 
                "competitive_analysis", 
                "monetization_strategy"
            ],
            "features": [
                "Multi-agent orchestration",
                "YouTube analytics integration", 
                "OAuth authentication",
                "Intelligent caching",
                "Real-time chat interface",
                "Quick action tools",
                "Content pillars management",
                "Video allocation system",
                "Pillar analytics"
            ],
            "endpoints": {
                "agent": "/api/agent/*",
                "youtube": "/api/youtube/*",
                "pillars": "/api/pillars/*, /api/videos/*",
                "oauth": "/auth/*",
                "health": "/health, /api/health/*"
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)