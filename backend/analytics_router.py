from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
import sqlite3
from datetime import datetime, timedelta
import json

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('creatormate.db')
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
async def get_channel_health(user_id: str):
    """Get channel health analytics data"""
    
    # Check if user has valid OAuth token
    token = get_user_oauth_token(user_id)
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="YouTube account not connected or token expired"
        )
    
    try:
        # TODO: Implement YouTube Analytics API calls
        # For now, return structure without data
        return {
            "status": "success",
            "data": None,  # Will be populated with real analytics data
            "message": "Channel health data endpoint ready - YouTube Analytics integration needed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching channel health: {str(e)}")

@router.get("/revenue/{user_id}")
async def get_revenue_analytics(user_id: str):
    """Get revenue analytics data"""
    
    # Check if user has valid OAuth token
    token = get_user_oauth_token(user_id)
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="YouTube account not connected or token expired"
        )
    
    try:
        # TODO: Implement YouTube Analytics API calls for revenue data
        return {
            "status": "success",
            "data": None,  # Will be populated with real revenue data
            "message": "Revenue analytics endpoint ready - YouTube Analytics integration needed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching revenue data: {str(e)}")

@router.get("/subscribers/{user_id}")
async def get_subscriber_analytics(user_id: str):
    """Get subscriber growth analytics data"""
    
    # Check if user has valid OAuth token
    token = get_user_oauth_token(user_id)
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="YouTube account not connected or token expired"
        )
    
    try:
        # TODO: Implement YouTube Analytics API calls for subscriber data
        return {
            "status": "success",
            "data": None,  # Will be populated with real subscriber data
            "message": "Subscriber analytics endpoint ready - YouTube Analytics integration needed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subscriber data: {str(e)}")

@router.get("/content-performance/{user_id}")
async def get_content_performance(user_id: str):
    """Get content performance analytics data"""
    
    # Check if user has valid OAuth token
    token = get_user_oauth_token(user_id)
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="YouTube account not connected or token expired"
        )
    
    try:
        # TODO: Implement YouTube Analytics API calls for content performance
        return {
            "status": "success",
            "data": None,  # Will be populated with real content performance data
            "message": "Content performance endpoint ready - YouTube Analytics integration needed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching content performance: {str(e)}")

@router.get("/status/{user_id}")
async def get_analytics_status(user_id: str):
    """Get analytics availability status for user"""
    
    token = get_user_oauth_token(user_id)
    
    return {
        "status": "success",
        "data": {
            "youtube_connected": token is not None,
            "analytics_available": token is not None,
            "endpoints": {
                "channel_health": f"/api/analytics/channel-health/{user_id}",
                "revenue": f"/api/analytics/revenue/{user_id}",
                "subscribers": f"/api/analytics/subscribers/{user_id}",
                "content_performance": f"/api/analytics/content-performance/{user_id}"
            }
        }
    }