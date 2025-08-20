"""
Smart Notification Router for MYTA
API endpoints for intelligent notifications and user preferences
"""

from fastapi import APIRouter, Depends, Request, HTTPException, BackgroundTasks
from typing import Dict, List, Optional, Any
import asyncio

from backend.App.smart_notification_engine import (
    get_notification_engine, 
    NotificationPreferences, 
    NotificationChannel, 
    NotificationPriority,
    NotificationType,
    NotificationRule
)
from backend.App.auth_middleware import get_current_user
from backend.App.response_utils import create_success_response, create_error_response
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/notifications", tags=["notifications"])

@router.get("/")
async def get_notifications(
    limit: int = 20,
    unread_only: bool = False,
    priority: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Get user notifications"""
    try:
        user_id = current_user["id"]
        
        notification_engine = get_notification_engine()
        notifications = await notification_engine.get_user_notifications(
            user_id, limit, unread_only
        )
        
        # Filter by priority if specified
        if priority:
            try:
                priority_filter = NotificationPriority(priority)
                notifications = [n for n in notifications if n.priority == priority_filter]
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid priority value")
        
        # Format notifications for response
        formatted_notifications = []
        for notification in notifications:
            formatted_notifications.append({
                "id": notification.notification_id,
                "type": notification.notification_type.value,
                "priority": notification.priority.value,
                "title": notification.title,
                "message": notification.message,
                "data": notification.data,
                "channels": [ch.value for ch in notification.channels],
                "created_at": notification.created_at.isoformat(),
                "read_at": notification.read_at.isoformat() if notification.read_at else None,
                "expires_at": notification.expires_at.isoformat() if notification.expires_at else None,
                "is_read": notification.read_at is not None,
                "is_expired": notification.expires_at and notification.expires_at < notification.created_at
            })
        
        # Calculate summary stats
        total_notifications = len(notifications)
        unread_count = len([n for n in notifications if n.read_at is None])
        priority_counts = {}
        for notification in notifications:
            priority = notification.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        result = {
            "notifications": formatted_notifications,
            "summary": {
                "total": total_notifications,
                "unread": unread_count,
                "priority_breakdown": priority_counts
            },
            "pagination": {
                "limit": limit,
                "has_more": total_notifications == limit  # Simple check
            }
        }
        
        return create_success_response("Notifications retrieved", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        return create_error_response("Failed to retrieve notifications", str(e))

@router.post("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Mark notification as read"""
    try:
        user_id = current_user["id"]
        
        notification_engine = get_notification_engine()
        success = await notification_engine.mark_notification_read(notification_id, user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return create_success_response("Notification marked as read", {
            "notification_id": notification_id,
            "read_at": "now"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking notification read: {e}")
        return create_error_response("Failed to mark notification as read", str(e))

@router.post("/mark-all-read")
async def mark_all_notifications_read(
    current_user: Dict = Depends(get_current_user)
):
    """Mark all notifications as read"""
    try:
        user_id = current_user["id"]
        
        notification_engine = get_notification_engine()
        notifications = await notification_engine.get_user_notifications(user_id, unread_only=True)
        
        marked_count = 0
        for notification in notifications:
            success = await notification_engine.mark_notification_read(
                notification.notification_id, user_id
            )
            if success:
                marked_count += 1
        
        return create_success_response("All notifications marked as read", {
            "marked_count": marked_count,
            "total_notifications": len(notifications)
        })
        
    except Exception as e:
        logger.error(f"Error marking all notifications read: {e}")
        return create_error_response("Failed to mark all notifications as read", str(e))

@router.get("/preferences")
async def get_notification_preferences(
    current_user: Dict = Depends(get_current_user)
):
    """Get user notification preferences"""
    try:
        user_id = current_user["id"]
        
        notification_engine = get_notification_engine()
        preferences = await notification_engine._get_user_preferences(user_id)
        
        result = {
            "user_id": preferences.user_id,
            "enabled_channels": [ch.value for ch in preferences.enabled_channels],
            "priority_threshold": preferences.priority_threshold.value,
            "quiet_hours": preferences.quiet_hours,
            "frequency_limits": {
                nt.value: limit for nt, limit in preferences.frequency_limits.items()
            },
            "agent_notifications": preferences.agent_notifications,
            "available_channels": [ch.value for ch in NotificationChannel],
            "available_priorities": [p.value for p in NotificationPriority],
            "available_types": [nt.value for nt in NotificationType]
        }
        
        return create_success_response("Notification preferences retrieved", result)
        
    except Exception as e:
        logger.error(f"Error getting notification preferences: {e}")
        return create_error_response("Failed to retrieve preferences", str(e))

@router.post("/preferences")
async def update_notification_preferences(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update user notification preferences"""
    try:
        body = await request.json()
        user_id = current_user["id"]
        
        # Parse enabled channels
        enabled_channels = []
        for channel_str in body.get("enabled_channels", []):
            try:
                enabled_channels.append(NotificationChannel(channel_str))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid channel: {channel_str}")
        
        # Parse priority threshold
        try:
            priority_threshold = NotificationPriority(body.get("priority_threshold", "medium"))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid priority threshold")
        
        # Parse frequency limits
        frequency_limits = {}
        for type_str, limit in body.get("frequency_limits", {}).items():
            try:
                notification_type = NotificationType(type_str)
                frequency_limits[notification_type] = limit
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid notification type: {type_str}")
        
        # Create preferences object
        preferences = NotificationPreferences(
            user_id=user_id,
            enabled_channels=enabled_channels,
            priority_threshold=priority_threshold,
            quiet_hours=body.get("quiet_hours", {"start": "22:00", "end": "08:00", "timezone": "UTC"}),
            frequency_limits=frequency_limits,
            custom_rules=[],  # Custom rules handled separately
            agent_notifications=body.get("agent_notifications", {
                "1": True, "2": True, "3": True, "4": True, "5": True
            })
        )
        
        # Update preferences
        notification_engine = get_notification_engine()
        success = await notification_engine.update_notification_preferences(user_id, preferences)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update preferences")
        
        return create_success_response("Notification preferences updated", {
            "user_id": user_id,
            "updated_at": "now"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating notification preferences: {e}")
        return create_error_response("Failed to update preferences", str(e))

@router.post("/monitor/{channel_id}")
async def trigger_monitoring(
    channel_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """Trigger notification monitoring for a channel"""
    try:
        user_id = current_user["id"]
        
        # Add monitoring task to background
        background_tasks.add_task(
            _run_monitoring_task,
            user_id,
            channel_id
        )
        
        return create_success_response("Monitoring triggered", {
            "channel_id": channel_id,
            "user_id": user_id,
            "status": "monitoring_started"
        })
        
    except Exception as e:
        logger.error(f"Error triggering monitoring: {e}")
        return create_error_response("Failed to trigger monitoring", str(e))

@router.get("/rules")
async def get_notification_rules(
    current_user: Dict = Depends(get_current_user)
):
    """Get available notification rules"""
    try:
        user_id = current_user["id"]
        
        notification_engine = get_notification_engine()
        active_rules = await notification_engine._get_active_rules(user_id)
        
        formatted_rules = []
        for rule in active_rules:
            formatted_rules.append({
                "rule_id": rule.rule_id,
                "name": rule.name,
                "description": rule.description,
                "type": rule.notification_type.value,
                "priority": rule.priority.value,
                "channels": [ch.value for ch in rule.channels],
                "frequency_limit": rule.frequency_limit,
                "enabled": rule.enabled,
                "condition": rule.condition
            })
        
        return create_success_response("Notification rules retrieved", {
            "rules": formatted_rules,
            "total_rules": len(formatted_rules)
        })
        
    except Exception as e:
        logger.error(f"Error getting notification rules: {e}")
        return create_error_response("Failed to retrieve notification rules", str(e))

@router.post("/test")
async def test_notification(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Send a test notification"""
    try:
        body = await request.json()
        user_id = current_user["id"]
        
        notification_type = body.get("type", "info")
        title = body.get("title", "Test Notification")
        message = body.get("message", "This is a test notification from MYTA")
        
        # Create test notification
        from backend.App.smart_notification_engine import Notification
        from datetime import datetime
        
        test_notification = Notification(
            notification_id=f"test_{user_id}_{int(datetime.now().timestamp())}",
            user_id=user_id,
            channel_id=None,
            notification_type=NotificationType.SYSTEM_UPDATE,
            priority=NotificationPriority.INFO,
            title=title,
            message=message,
            data={"test": True, "sent_at": datetime.now().isoformat()},
            channels=[NotificationChannel.IN_APP],
            created_at=datetime.now()
        )
        
        # Store test notification
        notification_engine = get_notification_engine()
        await notification_engine._store_notification(test_notification)
        
        return create_success_response("Test notification sent", {
            "notification_id": test_notification.notification_id,
            "title": title,
            "message": message,
            "type": notification_type
        })
        
    except Exception as e:
        logger.error(f"Error sending test notification: {e}")
        return create_error_response("Failed to send test notification", str(e))

@router.get("/stats")
async def get_notification_stats(
    days: int = 30,
    current_user: Dict = Depends(get_current_user)
):
    """Get notification statistics"""
    try:
        user_id = current_user["id"]
        
        notification_engine = get_notification_engine()
        all_notifications = await notification_engine.get_user_notifications(user_id, limit=1000)
        
        # Filter by date range
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_notifications = [
            n for n in all_notifications 
            if n.created_at > cutoff_date
        ]
        
        # Calculate stats
        total_notifications = len(recent_notifications)
        read_notifications = len([n for n in recent_notifications if n.read_at])
        unread_notifications = total_notifications - read_notifications
        
        # Type breakdown
        type_breakdown = {}
        for notification in recent_notifications:
            type_name = notification.notification_type.value
            type_breakdown[type_name] = type_breakdown.get(type_name, 0) + 1
        
        # Priority breakdown
        priority_breakdown = {}
        for notification in recent_notifications:
            priority_name = notification.priority.value
            priority_breakdown[priority_name] = priority_breakdown.get(priority_name, 0) + 1
        
        # Read rate
        read_rate = (read_notifications / total_notifications * 100) if total_notifications > 0 else 0
        
        stats = {
            "period_days": days,
            "total_notifications": total_notifications,
            "read_notifications": read_notifications,
            "unread_notifications": unread_notifications,
            "read_rate_percentage": round(read_rate, 1),
            "type_breakdown": type_breakdown,
            "priority_breakdown": priority_breakdown,
            "most_common_type": max(type_breakdown.items(), key=lambda x: x[1])[0] if type_breakdown else None,
            "average_per_day": round(total_notifications / days, 1) if days > 0 else 0
        }
        
        return create_success_response("Notification statistics retrieved", stats)
        
    except Exception as e:
        logger.error(f"Error getting notification stats: {e}")
        return create_error_response("Failed to retrieve notification statistics", str(e))

# Background task functions

async def _run_monitoring_task(user_id: str, channel_id: str):
    """Background task to run notification monitoring"""
    try:
        notification_engine = get_notification_engine()
        notifications = await notification_engine.monitor_and_notify(user_id, channel_id)
        
        logger.info(f"Monitoring completed for user {user_id}, channel {channel_id}. Generated {len(notifications)} notifications.")
        
    except Exception as e:
        logger.error(f"Error in monitoring task: {e}")

# Helper functions

def _format_notification_for_response(notification) -> Dict[str, Any]:
    """Format notification for API response"""
    return {
        "id": notification.notification_id,
        "type": notification.notification_type.value,
        "priority": notification.priority.value,
        "title": notification.title,
        "message": notification.message,
        "data": notification.data,
        "channels": [ch.value for ch in notification.channels],
        "created_at": notification.created_at.isoformat(),
        "read_at": notification.read_at.isoformat() if notification.read_at else None,
        "expires_at": notification.expires_at.isoformat() if notification.expires_at else None,
        "is_read": notification.read_at is not None,
        "is_expired": notification.expires_at and notification.expires_at < notification.created_at
    }
