"""
Usage Tracking Router for MYTA
Provides endpoints for monitoring user usage and limits
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging
from datetime import datetime

# Import authentication and utilities
from .auth_middleware import get_current_user
from .api_models import create_success_response, create_error_response
from .usage_tracking_service import UsageTrackingService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/usage", tags=["Usage Tracking"])

# Initialize usage tracking service
usage_service = UsageTrackingService()

@router.get("/current")
async def get_current_usage(current_user = Depends(get_current_user)):
    """Get current usage statistics for the authenticated user"""
    try:
        user_id = current_user.user_id
        logger.info(f"Fetching usage data for user {user_id}")
        
        # Get current usage from service
        usage_data = await usage_service.get_user_usage_summary(user_id)
        
        return create_success_response(
            "Usage data retrieved successfully",
            usage_data
        )
        
    except Exception as e:
        logger.error(f"Error fetching usage data: {e}")
        return create_error_response(
            "Failed to fetch usage data",
            str(e)
        )

@router.get("/limits")
async def get_usage_limits(current_user = Depends(get_current_user)):
    """Get usage limits for the authenticated user's plan"""
    try:
        user_id = current_user.user_id
        logger.info(f"Fetching usage limits for user {user_id}")
        
        # Get user's subscription and limits
        limits = await usage_service.get_user_limits(user_id)
        
        return create_success_response(
            "Usage limits retrieved successfully",
            limits
        )
        
    except Exception as e:
        logger.error(f"Error fetching usage limits: {e}")
        return create_error_response(
            "Failed to fetch usage limits",
            str(e)
        )

@router.get("/alerts")
async def get_usage_alerts(current_user = Depends(get_current_user)):
    """Get usage alerts for the authenticated user"""
    try:
        user_id = current_user.user_id
        logger.info(f"Fetching usage alerts for user {user_id}")
        
        # Get usage alerts
        alerts = await usage_service.get_user_alerts(user_id)
        
        return create_success_response(
            "Usage alerts retrieved successfully",
            alerts
        )
        
    except Exception as e:
        logger.error(f"Error fetching usage alerts: {e}")
        return create_error_response(
            "Failed to fetch usage alerts",
            str(e)
        )

@router.post("/alerts/{alert_id}/read")
async def mark_alert_read(alert_id: int, current_user = Depends(get_current_user)):
    """Mark a usage alert as read"""
    try:
        user_id = current_user.user_id
        logger.info(f"Marking alert {alert_id} as read for user {user_id}")
        
        # Mark alert as read
        success = await usage_service.mark_alert_read(user_id, alert_id)
        
        if success:
            return create_success_response(
                "Alert marked as read successfully",
                {"alert_id": alert_id, "is_read": True}
            )
        else:
            raise HTTPException(status_code=404, detail="Alert not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking alert as read: {e}")
        return create_error_response(
            "Failed to mark alert as read",
            str(e)
        )

@router.get("/summary")
async def get_usage_summary(current_user = Depends(get_current_user)):
    """Get comprehensive usage summary including current usage, limits, and alerts"""
    try:
        user_id = current_user.user_id
        logger.info(f"Fetching usage summary for user {user_id}")
        
        # Get comprehensive usage summary
        summary = await usage_service.get_comprehensive_summary(user_id)
        
        return create_success_response(
            "Usage summary retrieved successfully",
            summary
        )
        
    except Exception as e:
        logger.error(f"Error fetching usage summary: {e}")
        return create_error_response(
            "Failed to fetch usage summary",
            str(e)
        )

@router.get("/health")
async def usage_health_check():
    """Health check for usage tracking system"""
    try:
        # Check if usage tracking service is working
        health_status = await usage_service.health_check()
        
        return {
            "status": "healthy",
            "service": "usage_tracking",
            "timestamp": datetime.now().isoformat(),
            "details": health_status
        }
        
    except Exception as e:
        logger.error(f"Usage tracking health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "usage_tracking",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }
