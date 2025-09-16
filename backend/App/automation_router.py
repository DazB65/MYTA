"""
Intelligent Automation API Router
API endpoints for automation settings, actions, and monitoring
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from .intelligent_automation_engine import (
    IntelligentAutomationEngine,
    AutomationSettings,
    AutomatedAction,
    SmartNotification,
    AutoScheduleRecommendation,
    AutomationType,
    NotificationPriority
)

logger = logging.getLogger(__name__)

# Initialize router and automation engine
router = APIRouter(prefix="/api/automation", tags=["Automation"])
automation_engine = IntelligentAutomationEngine()

# Request/Response Models
class AutomationSettingsRequest(BaseModel):
    auto_scheduling_enabled: Optional[bool] = None
    auto_responses_enabled: Optional[bool] = None
    seo_optimization_enabled: Optional[bool] = None
    content_ideas_enabled: Optional[bool] = None
    smart_notifications_enabled: Optional[bool] = None
    auto_descriptions_enabled: Optional[bool] = None
    preferred_posting_days: Optional[List[str]] = None
    max_posts_per_week: Optional[int] = None
    auto_response_types: Optional[List[str]] = None
    response_tone: Optional[str] = None
    notification_frequency: Optional[str] = None

class AutomationSettingsResponse(BaseModel):
    success: bool
    settings: Optional[Dict[str, Any]]
    message: str

class ScheduleContentRequest(BaseModel):
    content_id: str = Field(..., description="Content identifier")
    title: str = Field(..., description="Content title")
    content_type: str = Field(default="video", description="Type of content")
    description: Optional[str] = Field(default=None, description="Content description")
    tags: Optional[List[str]] = Field(default=[], description="Content tags")

class ScheduleContentResponse(BaseModel):
    success: bool
    recommendation: Optional[Dict[str, Any]]
    message: str

class AutoResponseRequest(BaseModel):
    comment_id: str = Field(..., description="Comment identifier")
    comment_text: str = Field(..., description="Comment text")
    video_id: Optional[str] = Field(default=None, description="Related video ID")
    commenter_name: Optional[str] = Field(default=None, description="Commenter name")

class AutoResponseResponse(BaseModel):
    success: bool
    response: Optional[Dict[str, Any]]
    requires_escalation: bool
    message: str

class SEOOptimizationRequest(BaseModel):
    content_id: str = Field(..., description="Content identifier")
    title: str = Field(..., description="Current title")
    description: str = Field(..., description="Current description")
    tags: List[str] = Field(default=[], description="Current tags")
    content_type: str = Field(default="video", description="Content type")

class SEOOptimizationResponse(BaseModel):
    success: bool
    optimized_content: Optional[Dict[str, Any]]
    improvements: Optional[Dict[str, Any]]
    message: str

class NotificationsResponse(BaseModel):
    success: bool
    notifications: List[Dict[str, Any]]
    unread_count: int

class AutomationDashboardResponse(BaseModel):
    success: bool
    dashboard_data: Dict[str, Any]

# Dependency to get user ID (simplified for demo)
async def get_current_user_id() -> str:
    # In production, extract from JWT token or session
    return "demo_user_123"

@router.get("/settings", response_model=AutomationSettingsResponse)
async def get_automation_settings(user_id: str = Depends(get_current_user_id)):
    """
    Get user's automation settings and preferences
    
    Returns current automation configuration including:
    - Enabled/disabled automation features
    - Scheduling preferences
    - Response settings
    - Notification preferences
    """
    try:
        logger.info(f"🔧 Getting automation settings for user {user_id}")
        
        settings = await automation_engine.get_user_automation_settings(user_id)
        
        return AutomationSettingsResponse(
            success=True,
            settings={
                'auto_scheduling_enabled': settings.auto_scheduling_enabled,
                'auto_responses_enabled': settings.auto_responses_enabled,
                'seo_optimization_enabled': settings.seo_optimization_enabled,
                'content_ideas_enabled': settings.content_ideas_enabled,
                'smart_notifications_enabled': settings.smart_notifications_enabled,
                'auto_descriptions_enabled': settings.auto_descriptions_enabled,
                'preferred_posting_days': settings.preferred_posting_days,
                'max_posts_per_week': settings.max_posts_per_week,
                'auto_response_types': settings.auto_response_types,
                'response_tone': settings.response_tone,
                'notification_frequency': settings.notification_frequency,
                'min_notification_priority': settings.min_notification_priority.value
            },
            message="Automation settings retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error getting automation settings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get settings: {str(e)}")

@router.post("/settings", response_model=AutomationSettingsResponse)
async def update_automation_settings(
    request: AutomationSettingsRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Update user's automation settings
    
    Allows users to configure:
    - Which automation features to enable/disable
    - Scheduling preferences and constraints
    - Auto-response behavior and tone
    - Notification frequency and priorities
    """
    try:
        logger.info(f"🔧 Updating automation settings for user {user_id}")
        
        # Convert request to dict, excluding None values
        settings_update = {k: v for k, v in request.dict().items() if v is not None}
        
        updated_settings = await automation_engine.update_automation_settings(
            user_id, settings_update
        )
        
        return AutomationSettingsResponse(
            success=True,
            settings={
                'auto_scheduling_enabled': updated_settings.auto_scheduling_enabled,
                'auto_responses_enabled': updated_settings.auto_responses_enabled,
                'seo_optimization_enabled': updated_settings.seo_optimization_enabled,
                'content_ideas_enabled': updated_settings.content_ideas_enabled,
                'smart_notifications_enabled': updated_settings.smart_notifications_enabled,
                'auto_descriptions_enabled': updated_settings.auto_descriptions_enabled,
                'preferred_posting_days': updated_settings.preferred_posting_days,
                'max_posts_per_week': updated_settings.max_posts_per_week,
                'auto_response_types': updated_settings.auto_response_types,
                'response_tone': updated_settings.response_tone,
                'notification_frequency': updated_settings.notification_frequency
            },
            message="Automation settings updated successfully"
        )
        
    except Exception as e:
        logger.error(f"Error updating automation settings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")

@router.post("/schedule-content", response_model=ScheduleContentResponse)
async def auto_schedule_content(
    request: ScheduleContentRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Get automatic scheduling recommendation for content
    
    Analyzes optimal posting time based on:
    - Audience activity patterns
    - Historical performance data
    - User preferences and constraints
    - Content type and characteristics
    """
    try:
        logger.info(f"📅 Auto-scheduling content for user {user_id}")
        
        content_data = {
            'id': request.content_id,
            'title': request.title,
            'type': request.content_type,
            'description': request.description,
            'tags': request.tags
        }
        
        recommendation = await automation_engine.auto_schedule_content(
            user_id, content_data
        )
        
        if not recommendation:
            return ScheduleContentResponse(
                success=False,
                recommendation=None,
                message="Auto-scheduling is disabled or insufficient data available"
            )
        
        return ScheduleContentResponse(
            success=True,
            recommendation={
                'recommended_time': recommendation.recommended_time.isoformat(),
                'confidence_score': recommendation.confidence_score,
                'expected_performance_boost': recommendation.expected_performance_boost,
                'reasoning': recommendation.reasoning,
                'alternative_times': [
                    {
                        'time': alt['time'].isoformat(),
                        'confidence': alt['confidence'],
                        'reasoning': alt['reasoning']
                    }
                    for alt in recommendation.alternative_times
                ]
            },
            message=f"Content scheduled for {recommendation.recommended_time.strftime('%Y-%m-%d %H:%M')} with {recommendation.expected_performance_boost:.1%} expected boost"
        )
        
    except Exception as e:
        logger.error(f"Error auto-scheduling content: {e}")
        raise HTTPException(status_code=500, detail=f"Auto-scheduling failed: {str(e)}")

@router.post("/auto-response", response_model=AutoResponseResponse)
async def generate_auto_response(
    request: AutoResponseRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Generate automatic response to comment
    
    Analyzes comment and generates appropriate response based on:
    - Comment sentiment and type
    - User's response preferences and tone
    - Escalation rules and keywords
    - Historical response patterns
    """
    try:
        logger.info(f"💬 Generating auto-response for user {user_id}")
        
        comment_data = {
            'id': request.comment_id,
            'text': request.comment_text,
            'video_id': request.video_id,
            'commenter_name': request.commenter_name
        }
        
        response = await automation_engine.auto_generate_response(
            user_id, comment_data
        )
        
        if not response:
            return AutoResponseResponse(
                success=True,
                response=None,
                requires_escalation=True,
                message="Comment requires manual review and response"
            )
        
        return AutoResponseResponse(
            success=True,
            response={
                'text': response['text'],
                'type': response['type'],
                'tone': response['tone'],
                'confidence': response['confidence'],
                'requires_review': response['requires_review']
            },
            requires_escalation=False,
            message="Auto-response generated successfully"
        )
        
    except Exception as e:
        logger.error(f"Error generating auto-response: {e}")
        raise HTTPException(status_code=500, detail=f"Auto-response generation failed: {str(e)}")

@router.post("/optimize-seo", response_model=SEOOptimizationResponse)
async def auto_optimize_seo(
    request: SEOOptimizationRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Automatically optimize content for SEO
    
    Provides optimization for:
    - Title enhancement with trending keywords
    - Description optimization for discoverability
    - Tag suggestions and improvements
    - SEO score and improvement predictions
    """
    try:
        logger.info(f"🔍 Auto-optimizing SEO for user {user_id}")
        
        content_data = {
            'id': request.content_id,
            'title': request.title,
            'description': request.description,
            'tags': request.tags,
            'type': request.content_type
        }
        
        optimization_result = await automation_engine.auto_optimize_seo(
            user_id, content_data
        )
        
        return SEOOptimizationResponse(
            success=True,
            optimized_content=optimization_result.get('optimized_content'),
            improvements=optimization_result.get('improvements'),
            message=f"SEO optimization completed with {optimization_result.get('improvements', {}).get('predicted_improvement', 0):.1%} expected improvement"
        )
        
    except Exception as e:
        logger.error(f"Error optimizing SEO: {e}")
        raise HTTPException(status_code=500, detail=f"SEO optimization failed: {str(e)}")

@router.get("/notifications", response_model=NotificationsResponse)
async def get_smart_notifications(user_id: str = Depends(get_current_user_id)):
    """
    Get intelligent notifications for user
    
    Returns prioritized notifications including:
    - Performance alerts and optimization suggestions
    - Trending opportunities in user's niche
    - Content calendar reminders
    - Automation status updates
    """
    try:
        logger.info(f"🔔 Getting smart notifications for user {user_id}")
        
        notifications = await automation_engine.generate_smart_notifications(user_id)
        
        notification_data = []
        for notification in notifications:
            notification_data.append({
                'id': notification.notification_id,
                'priority': notification.priority.value,
                'title': notification.title,
                'message': notification.message,
                'action_required': notification.action_required,
                'suggested_actions': notification.suggested_actions,
                'related_content': notification.related_content,
                'created_at': notification.created_at.isoformat(),
                'expires_at': notification.expires_at.isoformat() if notification.expires_at else None
            })
        
        unread_count = len([n for n in notifications if n.priority in [NotificationPriority.HIGH, NotificationPriority.URGENT]])
        
        return NotificationsResponse(
            success=True,
            notifications=notification_data,
            unread_count=unread_count
        )
        
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get notifications: {str(e)}")

@router.get("/dashboard", response_model=AutomationDashboardResponse)
async def get_automation_dashboard(user_id: str = Depends(get_current_user_id)):
    """
    Get automation dashboard overview
    
    Provides comprehensive automation status including:
    - Active automations and their status
    - Recent automated actions
    - Performance metrics and improvements
    - Upcoming scheduled actions
    """
    try:
        logger.info(f"📊 Getting automation dashboard for user {user_id}")
        
        # Get user settings
        settings = await automation_engine.get_user_automation_settings(user_id)
        
        # Get recent notifications
        notifications = await automation_engine.generate_smart_notifications(user_id)
        recent_notifications = notifications[:5]
        
        dashboard_data = {
            'automation_status': {
                'auto_scheduling': settings.auto_scheduling_enabled,
                'auto_responses': settings.auto_responses_enabled,
                'seo_optimization': settings.seo_optimization_enabled,
                'smart_notifications': settings.smart_notifications_enabled
            },
            'recent_notifications': [
                {
                    'title': n.title,
                    'priority': n.priority.value,
                    'created_at': n.created_at.isoformat()
                }
                for n in recent_notifications
            ],
            'automation_stats': {
                'total_automations_enabled': sum([
                    settings.auto_scheduling_enabled,
                    settings.auto_responses_enabled,
                    settings.seo_optimization_enabled,
                    settings.smart_notifications_enabled
                ]),
                'notification_frequency': settings.notification_frequency,
                'preferred_posting_days': settings.preferred_posting_days
            },
            'quick_actions': [
                'Review pending auto-responses',
                'Check scheduled content',
                'Update automation settings',
                'View performance alerts'
            ]
        }
        
        return AutomationDashboardResponse(
            success=True,
            dashboard_data=dashboard_data
        )
        
    except Exception as e:
        logger.error(f"Error getting automation dashboard: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard: {str(e)}")
