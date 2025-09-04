"""
Vidalytics Multi-Agent API - Refactored Main Application
Modular FastAPI application with separated routers for better maintainability
"""

from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
from typing import Optional, Dict, Any
import traceback
import os
import sqlite3
from slowapi.errors import RateLimitExceeded

# Import security middleware
from .security_middleware import add_security_middleware
from .config import get_settings
# Import new security features
from .env_validator import validate_environment
from .enhanced_security_middleware import EnhancedSecurityMiddleware, RateLimitMiddleware

# Import API models
from .api_models import (
    ChannelInfo, StandardResponse, HealthResponse, SystemHealthResponse,
    create_success_response
)

# Import constants
from .constants import DEFAULT_SESSION_TIMEOUT_HOURS

# Import routers
from .agent_router import router as agent_router
from .youtube_router import router as youtube_router
from .pillars_router import router as pillars_router
from .analytics_router import router as analytics_router
from .oauth_endpoints import oauth_router
from .content_cards_router import router as content_cards_router
from .session_router import router as session_router
from .backup_router import router as backup_router
from .monitoring_router import router as monitoring_router
from .subscription_router import router as subscription_router
from .tasks_router import router as tasks_router
from .goals_router import router as goals_router
from .notes_router import router as notes_router
from .settings_router import router as settings_router
from .chat_router import router as chat_router
from .error_monitoring_router import router as error_monitoring_router
from .channel_data_router import router as channel_data_router
from .agent_tools_router import router as agent_tools_router
from .dynamic_response_router import router as dynamic_response_router
from .collaboration_router import router as collaboration_router
from .realtime_analytics_router import router as realtime_analytics_router
from .notification_router import router as notification_router
from .security_dashboard_router import router as security_router
from .team_router import router as team_router
from .youtube_channel_endpoints import router as youtube_channel_router
from .content_router import router as content_router
from .usage_router import router as usage_router
from .auth_router import router as auth_router
from .request_logging import log_request_middleware
from .error_handler import create_error_response, MYTAError

# Import services
from .ai_services import update_user_context
from .enhanced_user_context import get_user_context

# Import rate limiting
from .rate_limiter import limiter, custom_rate_limit_handler, get_rate_limit

# Import authentication
from .auth_middleware import get_current_user, get_optional_user, get_user_id_from_request, AuthToken, create_session_token, auth_middleware

# Import CSRF protection
from .csrf_protection import setup_csrf_protection

# Import secure error handling
from .secure_error_handler import create_secure_exception_handlers

# Import monitoring and logging
from .logging_config import get_logging_manager, get_logger, LogCategory
from .monitoring_middleware import setup_monitoring_middleware

# Import health checks

# Import session management
from .session_middleware import SessionMiddleware

# Security helpers
def add_security_headers(response):
    """Add security headers to response"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY" 
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Load configuration
settings = get_settings()

# Configure advanced logging system
logging_manager = get_logging_manager()
logger = get_logger(__name__, LogCategory.SYSTEM)

# Create FastAPI app with comprehensive documentation
app = FastAPI(
    title="Vidalytics Multi-Agent API",
    version="2.0.0",
    description="""
    **Vidalytics** is a sophisticated hierarchical multi-agent system designed for YouTube content creators 
    to optimize their channel performance, content strategy, and audience engagement.
    
    ## Key Features
    
    * **🤖 Multi-Agent Architecture**: Specialized AI agents for different aspects of content optimization
    * **📊 YouTube Analytics**: Deep integration with YouTube Data API for comprehensive analytics
    * **🎯 Content Pillars**: Strategic content organization and planning system
    * **🔐 Session Management**: Secure Redis-based session handling
    * **⚡ Real-time Chat**: Interactive AI-powered content advisory
    * **📈 Performance Monitoring**: Advanced metrics and health monitoring
    
    ## Agent System
    
    The system consists of specialized agents:
    - **Boss Agent**: Central orchestrator using Claude 3.5 Sonnet
    - **Content Analysis Agent**: Video performance analysis using Gemini 2.5 Pro
    - **Audience Insights Agent**: Demographics and sentiment analysis using Claude 3.5 Sonnet
    - **SEO & Discoverability Agent**: Search optimization using Claude 3.5 Haiku
    - **Competitive Analysis Agent**: Market positioning using Gemini 2.5 Pro
    - **Monetization Strategy Agent**: Revenue optimization using Claude 3.5 Haiku
    
    ## Authentication
    
    The API uses Redis-based session management. Most endpoints require authentication.
    Use the `/api/session/login` endpoint to create a session.
    """,
    summary="Your AI team for YouTube growth - coordinated agents working together",
    debug=settings.debug,
    docs_url="/docs" if getattr(settings, "enable_api_docs", True) else None,
    redoc_url="/redoc" if getattr(settings, "enable_api_docs", True) else None,
    openapi_url="/openapi.json" if getattr(settings, "enable_api_docs", True) else None,
    contact={
        "name": "Vidalytics Support",
        "url": "https://github.com/Vidalytics/api",
        "email": "support@Vidalytics.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {
            "url": "http://localhost:8888",
            "description": "Development server"
        },
        {
            "url": "https://api.Vidalytics.com",
            "description": "Production server"
        }
    ],
    tags_metadata=[
        {
            "name": "agent",
            "description": "Multi-agent system operations including chat, quick actions, and specialized agent interactions."
        },
        {
            "name": "session",
            "description": "Redis-based session management for secure authentication and user state."
        },
        {
            "name": "youtube",
            "description": "YouTube Data API integration for analytics, video data, and OAuth authentication."
        },
        {
            "name": "pillars",
            "description": "Content pillars management for strategic content organization and planning."
        },
        {
            "name": "analytics",
            "description": "Dashboard analytics and performance metrics for data-driven insights."
        },
        {
            "name": "oauth",
            "description": "OAuth 2.0 authentication flow for YouTube and other third-party integrations."
        },
        {
            "name": "content-cards",
            "description": "Content Studio functionality for content creation and management workflows."
        },
        {
            "name": "health",
            "description": "System health checks and monitoring endpoints for operational oversight."
        },
        {
            "name": "auth",
            "description": "User authentication and authorization endpoints."
        }
    ]
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
    """Initialize the Vidalytics multi-agent system"""
    try:
        # Validate environment variables first
        logger.info("Validating environment variables...")
        validate_environment()
        logger.info("Environment validation completed successfully")
        
        logger.info(
            "Starting Vidalytics Multi-Agent System",
            extra={
                'category': LogCategory.SYSTEM.value,
                'metadata': {
                    'environment': str(settings.environment),
                    'version': '2.0.0',
                    'debug_mode': settings.debug
                }
            }
        )
        
        from .api_startup import initialize_Vidalytics_system
        initialization_result = await initialize_Vidalytics_system()
        
        # Initialize performance tracking system
        try:
            from .agent_performance_tracker import init_performance_tracking
            init_performance_tracking()
            
            logger.info(
                "Performance tracking system initialized",
                extra={
                    'category': LogCategory.SYSTEM.value,
                    'metadata': {'performance_tracking': True}
                }
            )
        except Exception as e:
            logger.error(
                f"Failed to initialize performance tracking: {e}",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {'error': str(e)}
                }
            )
        
        # Initialize alert system
        try:
            from .alert_manager import init_alert_system
            await init_alert_system()
            
            logger.info(
                "Alert system initialized",
                extra={
                    'category': LogCategory.SYSTEM.value,
                    'metadata': {'alert_system': True}
                }
            )
        except Exception as e:
            logger.error(
                f"Failed to initialize alert system: {e}",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {'error': str(e)}
                }
            )
        
        # Initialize backup service
        try:
            from .backup_service import get_backup_service
            backup_config = settings.get_backup_config()
            
            # Get database path from settings
            db_path = settings.database_url.replace("sqlite:///", "").replace("./", "")
            
            # Initialize backup service with configuration
            backup_service = get_backup_service(
                db_path=db_path,
                schedule_config=backup_config["schedule"],
                alert_config=backup_config["alerts"]
            )
            
            # Start the backup service
            backup_service.start()
            
            logger.info(
                "Backup service started successfully",
                extra={
                    'category': LogCategory.SYSTEM.value,
                    'metadata': {
                        'frequency': backup_config["schedule"].frequency.value,
                        'time': backup_config["schedule"].time,
                        'enabled': backup_config["schedule"].enabled
                    }
                }
            )
            
        except Exception as e:
            logger.error(
                f"Failed to start backup service: {e}",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {'error': str(e)}
                }
            )
        
        if initialization_result["overall_status"] == "success":
            logger.info(
                "Vidalytics Multi-Agent System started successfully",
                extra={
                    'category': LogCategory.SYSTEM.value,
                    'metadata': initialization_result
                }
            )
        else:
            logger.warning(
                f"Vidalytics started with warnings: {initialization_result['overall_status']}",
                extra={
                    'category': LogCategory.SYSTEM.value,
                    'metadata': initialization_result
                }
            )
            
    except Exception as e:
        logger.error(
            "Failed to initialize Vidalytics system",
            extra={
                'category': LogCategory.ERROR.value,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    try:
        logger.info("Shutting down Vidalytics Multi-Agent System")
        
        # Stop backup service
        try:
            from .backup_service import get_backup_service
            backup_service = get_backup_service()
            backup_service.stop()
            logger.info("Backup service stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping backup service: {e}")
        
        # Stop alert monitoring
        try:
            from .alert_manager import get_alert_manager
            alert_manager = get_alert_manager()
            await alert_manager.stop_monitoring()
            logger.info("Alert monitoring stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping alert monitoring: {e}")
        
        # Cleanup connection pools
        from .connection_pool import cleanup_connections
        await cleanup_connections()
        
        logger.info("Vidalytics shutdown completed successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)

# =============================================================================
# Exception Handlers (Secure)
# =============================================================================

# Setup secure exception handlers
create_secure_exception_handlers(app)

# =============================================================================
# Middleware Configuration
# =============================================================================

# Add enhanced security middleware first (highest priority)
app.add_middleware(
    EnhancedSecurityMiddleware, 
    strict_mode=settings.security_headers_strict if hasattr(settings, 'security_headers_strict') else True
)

# Add enhanced rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=settings.rate_limit_per_minute if hasattr(settings, 'rate_limit_per_minute') else 60,
    burst_size=settings.rate_limit_burst if hasattr(settings, 'rate_limit_burst') else 10
)

# Add existing security middleware (order matters)
add_security_middleware(app)

# Add CSRF protection
setup_csrf_protection(app, settings.boss_agent_secret_key or "fallback-secret")

# Add monitoring middleware (before CORS for complete request tracking)
setup_monitoring_middleware(app)

# Add usage tracking middleware (after monitoring, before session)
# TODO: Enable after fixing import issues
# from .usage_middleware import UsageTrackingMiddleware
# app.add_middleware(UsageTrackingMiddleware)

# Add Redis session middleware (after monitoring, before CORS)
app.add_middleware(SessionMiddleware)

# Add request logging middleware (before CORS)
app.middleware("http")(log_request_middleware)

# Add CORS middleware with environment-specific configuration
cors_config = settings.get_cors_config()
app.add_middleware(CORSMiddleware, **cors_config)

# =============================================================================
# Include Routers
# =============================================================================

# Include authentication router (handles user registration, login, logout)
app.include_router(auth_router)

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

# Include session router (handles Redis-based session management)
app.include_router(session_router)

# Include backup router (handles database backup management)
app.include_router(backup_router)

# Include monitoring router (handles performance monitoring and dashboard)
app.include_router(monitoring_router)

# Include subscription router (handles LemonSqueezy integration and billing)
app.include_router(subscription_router)

# Include tasks router (handles task management)
app.include_router(tasks_router)

# Include goals router (handles goal management)
app.include_router(goals_router)

# Include notes router (handles note management)
app.include_router(notes_router)

# Include settings router (handles user settings and agent preferences)
app.include_router(settings_router)

# Include chat router (handles real-time chat and WebSocket connections)
app.include_router(chat_router)

# Include error monitoring router (handles error tracking and performance monitoring)
app.include_router(error_monitoring_router)

# Include channel data router (handles user channel analysis and personalized responses)
app.include_router(channel_data_router)

# Include agent tools router (handles specialized agent tools and capabilities)
app.include_router(agent_tools_router)

# Include dynamic response router (handles context-aware adaptive responses)
app.include_router(dynamic_response_router)

# Include collaboration router (handles multi-agent collaboration and analysis)
app.include_router(collaboration_router)

# Include real-time analytics router (handles live analytics and AI insights)
app.include_router(realtime_analytics_router)

# Include notification router (handles smart notifications and user preferences)
app.include_router(notification_router)

# Include security dashboard router (handles security monitoring and metrics)
app.include_router(security_router)

# Include team router (handles team collaboration and member management)
app.include_router(team_router)

# Include YouTube channel router (handles channel data fetching and OAuth)
app.include_router(youtube_channel_router)

# Include content router (handles AI-powered content generation)
app.include_router(content_router)

# Include usage router (handles usage tracking and limits)
app.include_router(usage_router)

# =============================================================================
# Global Exception Handlers
# =============================================================================

@app.exception_handler(MYTAError)
async def myta_error_handler(request: Request, exc: MYTAError):
    """Handle custom MYTA errors"""
    return create_error_response(exc, request)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions"""
    from .error_handler import MYTAError, ErrorCode, ErrorCategory, ErrorSeverity

    # Convert HTTPException to MYTAError for consistent handling
    if exc.status_code == 401:
        error = MYTAError(
            message=str(exc.detail),
            error_code=ErrorCode.INVALID_CREDENTIALS,
            category=ErrorCategory.AUTHENTICATION,
            severity=ErrorSeverity.MEDIUM
        )
    elif exc.status_code == 403:
        error = MYTAError(
            message=str(exc.detail),
            error_code=ErrorCode.INSUFFICIENT_PERMISSIONS,
            category=ErrorCategory.AUTHORIZATION,
            severity=ErrorSeverity.MEDIUM
        )
    elif exc.status_code == 404:
        error = MYTAError(
            message=str(exc.detail),
            error_code=ErrorCode.RECORD_NOT_FOUND,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW
        )
    elif exc.status_code == 422:
        error = MYTAError(
            message=str(exc.detail),
            error_code=ErrorCode.INVALID_INPUT,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW
        )
    elif exc.status_code == 429:
        error = MYTAError(
            message="Rate limit exceeded",
            error_code=ErrorCode.API_RATE_LIMIT_EXCEEDED,
            category=ErrorCategory.RATE_LIMIT,
            severity=ErrorSeverity.MEDIUM
        )
    else:
        error = MYTAError(
            message=str(exc.detail),
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.HIGH
        )

    return create_error_response(error, request)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    from .error_handler import MYTAError, ErrorCode, ErrorCategory, ErrorSeverity

    # Log the full exception for debugging
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # Create a generic error response
    error = MYTAError(
        message=f"Internal server error: {type(exc).__name__}",
        error_code=ErrorCode.INTERNAL_SERVER_ERROR,
        category=ErrorCategory.SYSTEM,
        severity=ErrorSeverity.CRITICAL,
        details={"exception_type": type(exc).__name__},
        recoverable=False
    )

    return create_error_response(error, request)

# =============================================================================
# Authentication Endpoints
# =============================================================================

@app.post("/api/auth/login")
@limiter.limit(get_rate_limit("public", "auth"))
async def login(request: Request):
    """Temporary login endpoint for development - creates session token"""
    try:
        body = await request.json()
        user_id = body.get('user_id', 'default_user')
        
        # In production, validate credentials here
        # For now, just create a token for any user_id
        token = create_session_token(user_id)
        
        logger.info(
            "Session token created",
            extra={
                'category': LogCategory.AUTHENTICATION.value,
                'user_id': user_id,
                'metadata': {
                    'action': 'login',
                    'token_expires_in': 28800
                }
            }
        )
        
        return create_success_response(
            "Login successful",
            {
                "token": token,
                "user_id": user_id,
                "expires_in": DEFAULT_SESSION_TIMEOUT_HOURS * 3600  # Convert hours to seconds
            }
        )
        
    except Exception as e:
        logger.error(
            "Login failed",
            extra={
                'category': LogCategory.AUTHENTICATION.value,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        raise HTTPException(status_code=400, detail="Login failed")

@app.post("/api/auth/logout")
async def logout(request: Request, response: Response, current_user: AuthToken = Depends(get_current_user)):
    """Logout endpoint - invalidates session"""
    try:
        # Get the current token to blacklist it
        token = None
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
        else:
            token = auth_middleware.get_token_from_cookie(request)

        # Blacklist the token
        if token:
            auth_middleware.blacklist_token(token)

        # Clear authentication cookie
        auth_middleware.clear_auth_cookie(response)

        logger.info(
            "User logged out",
            extra={
                'category': LogCategory.AUTHENTICATION.value,
                'user_id': current_user.user_id,
                'metadata': {
                    'action': 'logout',
                    'session_id': current_user.session_id
                }
            }
        )

        return create_success_response("Logout successful")
        
    except Exception as e:
        logger.error(
            "Logout failed",
            extra={
                'category': LogCategory.AUTHENTICATION.value,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        raise HTTPException(status_code=400, detail="Logout failed")

@app.get("/api/auth/me")
async def get_current_user_info(current_user: AuthToken = Depends(get_current_user)):
    """Get current authenticated user information"""
    return create_success_response(
        "User information retrieved",
        {
            "user_id": current_user.user_id,
            "session_id": current_user.session_id,
            "permissions": current_user.permissions,
            "expires_at": current_user.expires_at.isoformat()
        }
    )

# =============================================================================
# Core API Endpoints
# =============================================================================

@app.post("/api/agent/set-channel-info", response_model=StandardResponse)
@limiter.limit(get_rate_limit("public", "default"))
async def set_channel_info(
    request: Request, 
    channel_info: ChannelInfo, 
    current_user: AuthToken = Depends(get_optional_user)
):
    """Endpoint to manually set channel information"""
    try:
        # Get user ID from authentication or fallback to legacy method
        user_id = current_user.user_id if current_user else await get_user_id_from_request(request)
        
        # Validate that the user can only update their own channel info
        if channel_info.user_id != user_id:
            raise HTTPException(status_code=403, detail="Cannot update other user's channel information")
        
        # Validate channel info
        channel_info.validate_metrics()
        
        logger.info(
            "Updating channel information",
            extra={
                'category': LogCategory.USER_ACTION.value,
                'user_id': user_id,
                'metadata': {
                    'action': 'update_channel_info',
                    'channel_name': channel_info.name,
                    'niche': channel_info.niche
                }
            }
        )
        
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
        result = update_user_context(user_id, "channel_info", info)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to update channel information")
        
        return create_success_response("Channel information updated successfully")
    
    except ValueError as e:
        logger.error(
            "Channel info validation failed",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': user_id,
                'metadata': {
                    'error_type': 'ValidationError',
                    'error_message': str(e)
                }
            }
        )
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
    except Exception as e:
        logger.error(
            "Unexpected error updating channel info",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': user_id,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to update channel information")

@app.get("/api/agent/insights/{user_id}")
async def get_insights(user_id: str):
    """Get dynamic insights for a user"""
    try:
        logger.info(
            "Retrieving user insights",
            extra={
                'category': LogCategory.USER_ACTION.value,
                'user_id': user_id,
                'metadata': {
                    'action': 'get_insights'
                }
            }
        )
        
        from .insights_engine import insights_engine
        
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
        logger.error(
            "Failed to retrieve insights",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': user_id,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to get insights")

@app.get("/api/agent/context/{user_id}")
async def get_user_context_endpoint(user_id: str):
    """Get user context including channel information"""
    try:
        logger.info(
            "Getting user context",
            extra={
                'category': LogCategory.USER_ACTION.value,
                'user_id': user_id,
                'metadata': {
                    'action': 'get_user_context'
                }
            }
        )
        
        # Get user context
        context = get_user_context(user_id)
        
        # Log what we're returning so we can debug
        channel_info = context["channel_info"]
        logger.info(
            "Returning channel context",
            extra={
                'category': LogCategory.USER_ACTION.value,
                'user_id': user_id,
                'metadata': {
                    'channel_name': channel_info['name'],
                    'subscriber_count': channel_info['subscriber_count']
                }
            }
        )
        
        return create_success_response(
            "User context retrieved successfully",
            {"channel_info": channel_info}
        )
    
    except Exception as e:
        logger.error(
            "Failed to get user context",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': user_id,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to get user context")

@app.get("/api/get-user-profile")
async def get_user_profile(
    request: Request,
    current_user: AuthToken = Depends(get_optional_user)
):
    """Get user profile with YouTube channel banner"""
    try:
        # Get user ID from authentication or fallback to legacy method
        user_id = current_user.user_id if current_user else await get_user_id_from_request(request)
        
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
            from .oauth_manager import get_oauth_manager
            from .youtube_api_integration import get_youtube_integration
            
            logger.info(f"Getting user profile for user_id: {user_id}")
            
            oauth_manager = get_oauth_manager()
            oauth_token = await oauth_manager.get_valid_token(user_id)
            
            debug_info["oauth_token_exists"] = oauth_token is not None
            debug_info["has_access_token"] = bool(oauth_token and oauth_token.access_token)
            
            logger.info(
                "OAuth token status checked",
                extra={
                    'category': LogCategory.AUTHENTICATION.value,
                    'user_id': user_id,
                    'metadata': {
                        'has_access_token': bool(oauth_token and oauth_token.access_token)
                    }
                }
            )
            
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
                
                # Implement proper channel search using YouTube API
                found_channel_id = await search_channel_by_name(channel_name, user_id)

                if found_channel_id:
                    logger.info(f"Found channel ID via search: {found_channel_id}")
                    # Update user's channel info with the found ID
                    await update_user_channel_id(user_id, found_channel_id)
                    
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
                            from .ai_services import update_user_context
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
        
        # Add debug info only when app is in debug mode and explicitly requested
        if getattr(settings, "debug", False) and request.query_params.get("debug") == "true":
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
        "service": "MYTA - Your AI Team for YouTube Growth",
        "version": "2.0.0"
    })
    return add_security_headers(response)

@app.get("/api/health/system", response_model=SystemHealthResponse)
def system_health():
    """Comprehensive system health check"""
    try:
        from .api_startup import get_system_status
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
        logger.error(
            "System health check failed",
            extra={
                'category': LogCategory.SYSTEM.value,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
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
# Removed legacy React SPA static serving. Frontend is served by the Nuxt Nitro container.


# =============================================================================
# Application Info
# =============================================================================

@app.get("/api/info")
def get_app_info():
    """Get application information"""
    return create_success_response(
        "Application info retrieved",
        {
            "name": "Vidalytics Multi-Agent API",
            "version": "2.0.0",
            "description": "Your AI team for YouTube growth - coordinated multi-agent system for strategic channel development",
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

# Helper functions for channel resolution
async def search_channel_by_name(channel_name: str, user_id: str) -> Optional[str]:
    """Search for a channel ID by name using YouTube API"""
    try:
        youtube_service = await get_youtube_service(user_id)
        if not youtube_service:
            return None

        # Search for channels by name
        search_response = youtube_service.search().list(
            q=channel_name,
            type='channel',
            part='snippet',
            maxResults=5
        ).execute()

        # Look for exact or close matches
        for item in search_response.get('items', []):
            if item['snippet']['title'].lower() == channel_name.lower():
                return item['snippet']['channelId']

        # If no exact match, return the first result if available
        if search_response.get('items'):
            return search_response['items'][0]['snippet']['channelId']

        return None
    except Exception as e:
        logger.error(f"Error searching for channel by name: {e}")
        return None

async def update_user_channel_id(user_id: str, channel_id: str) -> None:
    """Update user's stored channel ID"""
    try:
        db_manager = get_database_manager()
        with sqlite3.connect(db_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user_youtube_data
                SET channel_id = ?
                WHERE user_id = ?
            """, (channel_id, user_id))
            conn.commit()
            logger.info(f"Updated channel ID for user {user_id}")
    except Exception as e:
        logger.error(f"Error updating user channel ID: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)