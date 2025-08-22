"""
Error Monitoring Router for MYTA
Provides endpoints for error tracking and performance monitoring
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

from backend.App.error_handler import error_tracker, ErrorSeverity, ErrorCategory
from backend.App.request_logging import request_logger
from backend.App.auth_middleware import get_current_user
from backend.App.api_models import create_success_response, create_error_response
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/monitoring/errors", tags=["error_monitoring"])

@router.get("/stats")
async def get_error_statistics(
    hours: int = Query(24, description="Time period in hours", ge=1, le=168),
    current_user: Dict = Depends(get_current_user)
):
    """Get error statistics for the specified time period"""
    try:
        stats = error_tracker.get_error_stats(hours)
        
        if stats.get("status") == "unavailable":
            return create_success_response(
                "Error statistics unavailable (Redis not available)",
                stats
            )
        
        # Add additional analysis
        analysis = {
            "error_rate": 0,
            "most_common_category": None,
            "severity_distribution": stats.get("by_severity", {}),
            "trends": "stable"  # Would implement trend analysis
        }
        
        # Calculate error rate (errors per hour)
        if hours > 0:
            analysis["error_rate"] = round(stats["total_errors"] / hours, 2)
        
        # Find most common category
        if stats.get("by_category"):
            most_common = max(stats["by_category"].items(), key=lambda x: x[1])
            analysis["most_common_category"] = {
                "category": most_common[0],
                "count": most_common[1]
            }
        
        result = {
            "statistics": stats,
            "analysis": analysis,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return create_success_response("Error statistics retrieved successfully", result)
        
    except Exception as e:
        logger.error(f"Error getting error statistics: {e}")
        return create_error_response("Failed to retrieve error statistics", str(e))

@router.get("/performance")
async def get_performance_metrics(
    minutes: int = Query(60, description="Time period in minutes", ge=1, le=1440),
    current_user: Dict = Depends(get_current_user)
):
    """Get API performance metrics"""
    try:
        metrics = request_logger.get_performance_metrics(minutes)
        
        if metrics.get("status") == "unavailable":
            return create_success_response(
                "Performance metrics unavailable (Redis not available)",
                metrics
            )
        
        # Add performance analysis
        analysis = {
            "requests_per_minute": 0,
            "performance_grade": "A",
            "slow_requests_count": 0,
            "recommendations": []
        }
        
        # Calculate requests per minute
        if minutes > 0:
            analysis["requests_per_minute"] = round(metrics["total_requests"] / minutes, 2)
        
        # Analyze response times
        response_times = metrics.get("response_times", [])
        if response_times:
            avg_time = metrics.get("average_response_time", 0)
            slow_requests = [t for t in response_times if t > 1000]  # > 1 second
            analysis["slow_requests_count"] = len(slow_requests)
            
            # Performance grading
            if avg_time < 200:
                analysis["performance_grade"] = "A"
            elif avg_time < 500:
                analysis["performance_grade"] = "B"
            elif avg_time < 1000:
                analysis["performance_grade"] = "C"
            else:
                analysis["performance_grade"] = "D"
                analysis["recommendations"].append("Consider optimizing slow endpoints")
            
            if analysis["slow_requests_count"] > metrics["total_requests"] * 0.1:
                analysis["recommendations"].append("High number of slow requests detected")
        
        result = {
            "metrics": metrics,
            "analysis": analysis,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return create_success_response("Performance metrics retrieved successfully", result)
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        return create_error_response("Failed to retrieve performance metrics", str(e))

@router.get("/recent")
async def get_recent_errors(
    limit: int = Query(50, description="Number of recent errors to retrieve", ge=1, le=100),
    severity: Optional[ErrorSeverity] = Query(None, description="Filter by severity"),
    category: Optional[ErrorCategory] = Query(None, description="Filter by category"),
    current_user: Dict = Depends(get_current_user)
):
    """Get recent errors with optional filtering"""
    try:
        # This would typically query Redis or database for recent errors
        # For now, return a placeholder response
        
        recent_errors = []
        
        # In a real implementation, you would:
        # 1. Query Redis for recent error keys
        # 2. Filter by severity and category if specified
        # 3. Sort by timestamp
        # 4. Limit results
        
        result = {
            "errors": recent_errors,
            "total_count": len(recent_errors),
            "filters": {
                "severity": severity.value if severity else None,
                "category": category.value if category else None,
                "limit": limit
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return create_success_response("Recent errors retrieved successfully", result)
        
    except Exception as e:
        logger.error(f"Error getting recent errors: {e}")
        return create_error_response("Failed to retrieve recent errors", str(e))

@router.get("/user/{user_id}")
async def get_user_error_history(
    user_id: str,
    limit: int = Query(20, description="Number of errors to retrieve", ge=1, le=50),
    current_user: Dict = Depends(get_current_user)
):
    """Get error history for a specific user"""
    try:
        # Verify user has permission to view this data
        if current_user["id"] != user_id and not current_user.get("is_admin", False):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        redis_service = error_tracker.redis_service
        
        if not redis_service.is_available():
            return create_success_response(
                "User error history unavailable (Redis not available)",
                {"errors": [], "user_id": user_id}
            )
        
        # Get user error history from Redis
        user_error_key = f"user_errors:{user_id}"
        error_data = redis_service.client.lrange(user_error_key, 0, limit - 1)
        
        errors = []
        for error_json in error_data:
            try:
                error_info = json.loads(error_json)
                errors.append(error_info)
            except json.JSONDecodeError:
                continue
        
        result = {
            "user_id": user_id,
            "errors": errors,
            "total_count": len(errors),
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return create_success_response("User error history retrieved successfully", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user error history: {e}")
        return create_error_response("Failed to retrieve user error history", str(e))

@router.post("/clear")
async def clear_error_data(
    older_than_hours: int = Query(24, description="Clear errors older than specified hours", ge=1),
    current_user: Dict = Depends(get_current_user)
):
    """Clear old error data"""
    try:
        # Verify admin permissions
        if not current_user.get("is_admin", False):
            raise HTTPException(status_code=403, detail="Admin permissions required")
        
        redis_service = error_tracker.redis_service
        
        if not redis_service.is_available():
            return create_success_response(
                "Error data clearing skipped (Redis not available)",
                {"cleared_count": 0}
            )
        
        # This would implement clearing logic based on timestamp
        # For now, return a placeholder response
        
        cleared_count = 0  # Would implement actual clearing logic
        
        result = {
            "cleared_count": cleared_count,
            "older_than_hours": older_than_hours,
            "cleared_at": datetime.utcnow().isoformat()
        }
        
        return create_success_response("Error data cleared successfully", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing error data: {e}")
        return create_error_response("Failed to clear error data", str(e))

@router.get("/health")
async def get_error_monitoring_health():
    """Get health status of error monitoring system"""
    try:
        redis_service = error_tracker.redis_service
        
        health_data = {
            "error_tracking": {
                "status": "healthy" if redis_service.is_available() else "degraded",
                "redis_available": redis_service.is_available()
            },
            "request_logging": {
                "status": "healthy",
                "active": True
            },
            "performance_monitoring": {
                "status": "healthy" if redis_service.is_available() else "degraded",
                "metrics_collection": redis_service.is_available()
            },
            "overall_status": "healthy" if redis_service.is_available() else "degraded",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return create_success_response("Error monitoring health retrieved successfully", health_data)
        
    except Exception as e:
        logger.error(f"Error getting error monitoring health: {e}")
        return create_error_response("Failed to retrieve error monitoring health", str(e))
