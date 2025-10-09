from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
import sqlite3
from datetime import datetime, timedelta
import json
import logging
import asyncio

try:
    from .youtube_analytics_service import get_youtube_analytics_service
    from .auth_middleware import get_current_user, AuthToken
    from .cache_service import get_cache_service
except ImportError:
    # Fallback for direct execution
    from .youtube_analytics_service import get_youtube_analytics_service
    from .auth_middleware import get_current_user, AuthToken
    from .cache_service import get_cache_service

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
logger = logging.getLogger(__name__)

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('Vidalytics.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user_oauth_token(user_id: str) -> Optional[str]:
    """Get user's OAuth token from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT access_token FROM oauth_tokens 
            WHERE user_id = ? AND expires_at > datetime('now')
        """, (user_id,))
        
        result = cursor.fetchone()
        return result['access_token'] if result else None
    finally:
        conn.close()

@router.get("/channel-health/{user_id}")
async def get_channel_health(
    user_id: str, 
    days: int = 30,
    current_user: AuthToken = Depends(get_current_user)
):
    """Get channel health analytics data"""
    
    # Ensure user can only access their own data
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Cannot access another user's analytics"
        )
    
    try:
        analytics_service = get_youtube_analytics_service()
        result = await analytics_service.get_channel_health(user_id, days)
        
        if result["status"] == "error":
            if "not available" in result["error"]:
                raise HTTPException(
                    status_code=401,
                    detail="YouTube Analytics access not available. Please connect your YouTube account."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=result["error"]
                )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching channel health for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching channel health: {str(e)}")

@router.get("/revenue/{user_id}")
async def get_revenue_analytics(
    user_id: str, 
    days: int = 30,
    current_user: AuthToken = Depends(get_current_user)
):
    """Get revenue analytics data"""
    
    # Ensure user can only access their own data
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Cannot access another user's analytics"
        )
    
    try:
        analytics_service = get_youtube_analytics_service()
        result = await analytics_service.get_revenue_data(user_id, days)
        
        if result["status"] == "error":
            if "not available" in result["error"]:
                raise HTTPException(
                    status_code=401,
                    detail="YouTube Analytics access not available. Please connect your YouTube account."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=result["error"]
                )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching revenue data for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching revenue data: {str(e)}")

@router.get("/subscribers/{user_id}")
async def get_subscriber_analytics(
    user_id: str, 
    days: int = 30,
    current_user: AuthToken = Depends(get_current_user)
):
    """Get subscriber growth analytics data"""
    
    # Ensure user can only access their own data
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Cannot access another user's analytics"
        )
    
    try:
        analytics_service = get_youtube_analytics_service()
        result = await analytics_service.get_subscriber_data(user_id, days)
        
        if result["status"] == "error":
            if "not available" in result["error"]:
                raise HTTPException(
                    status_code=401,
                    detail="YouTube Analytics access not available. Please connect your YouTube account."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=result["error"]
                )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching subscriber data for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching subscriber data: {str(e)}")

@router.get("/content-performance/{user_id}")
async def get_content_performance(
    user_id: str, 
    days: int = 30,
    current_user: AuthToken = Depends(get_current_user)
):
    """Get content performance analytics data"""
    
    # Ensure user can only access their own data
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Cannot access another user's analytics"
        )
    
    try:
        analytics_service = get_youtube_analytics_service()
        result = await analytics_service.get_content_performance(user_id, days)
        
        if result["status"] == "error":
            if "not available" in result["error"]:
                raise HTTPException(
                    status_code=401,
                    detail="YouTube Analytics access not available. Please connect your YouTube account."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=result["error"]
                )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching content performance for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching content performance: {str(e)}")

@router.get("/status/{user_id}")
async def get_analytics_status(
    user_id: str,
    current_user: AuthToken = Depends(get_current_user)
):
    """Get analytics availability status for user"""
    
    # Ensure user can only access their own status
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Cannot access another user's status"
        )
    
    try:
        token = get_user_oauth_token(user_id)
        
        # Try to get channel ID to verify access
        analytics_service = get_youtube_analytics_service()
        channel_id = analytics_service._get_channel_id(user_id)
        
        return {
            "status": "success",
            "data": {
                "youtube_connected": token is not None,
                "analytics_available": token is not None and channel_id is not None,
                "channel_id": channel_id,
                "endpoints": {
                    "channel_health": f"/api/analytics/channel-health/{user_id}",
                    "revenue": f"/api/analytics/revenue/{user_id}",
                    "subscribers": f"/api/analytics/subscribers/{user_id}",
                    "content_performance": f"/api/analytics/content-performance/{user_id}"
                },
                "available_parameters": {
                    "days": "Number of days to analyze (default: 30, max: 365)"
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics status for user {user_id}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "data": {
                "youtube_connected": False,
                "analytics_available": False,
                "channel_id": None
            }
        }

@router.get("/overview/{user_id}")
async def get_analytics_overview(
    user_id: str,
    days: int = 30,
    current_user: AuthToken = Depends(get_current_user)
):
    """Get comprehensive analytics overview combining all metrics"""
    
    # Ensure user can only access their own data
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Cannot access another user's analytics"
        )
    
    try:
        analytics_service = get_youtube_analytics_service()
        
        # Get all analytics data in parallel
        channel_health_task = analytics_service.get_channel_health(user_id, days)
        revenue_task = analytics_service.get_revenue_data(user_id, days)
        subscriber_task = analytics_service.get_subscriber_data(user_id, days)
        content_task = analytics_service.get_content_performance(user_id, days)
        
        # Wait for all results
        channel_health, revenue_data, subscriber_data, content_performance = await asyncio.gather(
            channel_health_task,
            revenue_task,
            subscriber_task,
            content_task,
            return_exceptions=True
        )
        
        # Prepare overview response
        overview = {
            "status": "success",
            "data": {
                "summary": {
                    "period": f"Last {days} days",
                    "generated_at": datetime.now().isoformat()
                },
                "channel_health": channel_health if not isinstance(channel_health, Exception) else {"status": "error", "error": str(channel_health)},
                "revenue": revenue_data if not isinstance(revenue_data, Exception) else {"status": "error", "error": str(revenue_data)},
                "subscribers": subscriber_data if not isinstance(subscriber_data, Exception) else {"status": "error", "error": str(subscriber_data)},
                "content_performance": content_performance if not isinstance(content_performance, Exception) else {"status": "error", "error": str(content_performance)}
            }
        }
        
        return overview
        
    except Exception as e:
        logger.error(f"Error getting analytics overview for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching analytics overview: {str(e)}"
        )

@router.get("/cache/stats")
async def get_cache_stats():
    """Get cache performance statistics"""
    try:
        cache = get_cache_service()
        stats = cache.get_stats()
        
        return {
            "status": "success",
            "data": stats,
            "message": "Cache statistics retrieved successfully"
        }
        
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        return {
            "status": "error",
            "error": str(e),
            "data": {}
        }

@router.delete("/cache/clear")
async def clear_cache():
    """Clear all analytics cache"""
    try:
        cache = get_cache_service()
        cleared = await cache.clear_pattern("analytics:*")
        
        return {
            "status": "success",
            "data": {
                "cleared_entries": cleared
            },
            "message": f"Cleared {cleared} cache entries"
        }
        
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing cache: {str(e)}"
        )