"""
Channel Data Router for MYTA
Manages user's channel data and analytics for personalized AI responses
"""

from fastapi import APIRouter, Depends, Request, HTTPException
from typing import Dict, List, Optional, Any

from .channel_analyzer import get_channel_analyzer
from .personalized_responses import get_response_generator
from .auth_middleware import get_current_user
from .api_models import create_success_response, create_error_response
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/channel", tags=["channel_data"])

@router.get("/profile")
async def get_channel_profile(current_user: Dict = Depends(get_current_user)):
    """Get user's complete channel profile for personalized responses"""
    try:
        user_id = current_user["id"]
        channel_analyzer = get_channel_analyzer()
        
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Convert to dict for JSON response
        profile_data = {
            "user_id": profile.user_id,
            "channel_id": profile.channel_id,
            "channel_name": profile.channel_name,
            "niche": profile.niche,
            "channel_size_tier": profile.channel_size_tier,
            "metrics": {
                "subscriber_count": profile.metrics.subscriber_count,
                "total_views": profile.metrics.total_views,
                "video_count": profile.metrics.video_count,
                "avg_views_per_video": profile.metrics.avg_views_per_video,
                "avg_ctr": profile.metrics.avg_ctr,
                "avg_retention": profile.metrics.avg_retention,
                "engagement_rate": profile.metrics.engagement_rate,
                "upload_frequency": profile.metrics.upload_frequency,
                "top_performing_topics": profile.metrics.top_performing_topics,
                "audience_demographics": profile.metrics.audience_demographics,
                "revenue_metrics": profile.metrics.revenue_metrics
            },
            "goals": profile.goals,
            "recent_performance": profile.recent_performance,
            "content_strategy": profile.content_strategy,
            "challenges": profile.challenges,
            "opportunities": profile.opportunities
        }
        
        return create_success_response("Channel profile retrieved successfully", profile_data)
        
    except Exception as e:
        logger.error(f"Error getting channel profile: {e}")
        return create_error_response("Failed to retrieve channel profile", str(e))

@router.put("/profile")
async def update_channel_profile(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update user's channel profile data"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        # Update user settings with channel data
        from .supabase_client import get_supabase_service
        supabase = get_supabase_service()
        
        update_data = {}
        
        # Channel basic info
        if "channel_name" in body:
            update_data["channel_name"] = body["channel_name"]
        if "channel_niche" in body:
            update_data["channel_niche"] = body["channel_niche"]
        if "youtube_channel_id" in body:
            update_data["youtube_channel_id"] = body["youtube_channel_id"]
        
        # Channel metrics
        if "subscriber_count" in body:
            update_data["subscriber_count"] = body["subscriber_count"]
        if "total_views" in body:
            update_data["total_views"] = body["total_views"]
        if "video_count" in body:
            update_data["video_count"] = body["video_count"]
        
        if update_data:
            result = supabase.update("user_settings", update_data, {"user_id": user_id})
            
            if result["success"]:
                # Invalidate cache
                channel_analyzer = get_channel_analyzer()
                await channel_analyzer.invalidate_cache(user_id)
                
                return create_success_response("Channel profile updated successfully")
            else:
                return create_error_response("Failed to update channel profile", result["error"])
        else:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating channel profile: {e}")
        return create_error_response("Failed to update channel profile", str(e))

@router.get("/suggestions/{agent_id}")
async def get_agent_suggestions(
    agent_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get personalized suggestions for specific agent based on channel data"""
    try:
        if agent_id not in ["1", "2", "3", "4", "5"]:
            raise HTTPException(status_code=400, detail="Invalid agent ID")
        
        user_id = current_user["id"]
        
        # Get channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Get personalized suggestions
        response_generator = get_response_generator()
        suggestions = await response_generator.get_response_suggestions(profile, agent_id)
        
        # Get agent info
        from .agent_personalities import get_agent_personality
        agent = get_agent_personality(agent_id)
        
        result = {
            "agent": {
                "id": agent_id,
                "name": agent["name"],
                "role": agent["role"],
                "color": agent["color"]
            },
            "suggestions": suggestions,
            "channel_context": {
                "name": profile.channel_name,
                "size_tier": profile.channel_size_tier,
                "niche": profile.niche,
                "subscriber_count": profile.metrics.subscriber_count
            }
        }
        
        return create_success_response("Agent suggestions retrieved successfully", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent suggestions: {e}")
        return create_error_response("Failed to retrieve agent suggestions", str(e))

@router.get("/analytics/summary")
async def get_analytics_summary(current_user: Dict = Depends(get_current_user)):
    """Get analytics summary for dashboard"""
    try:
        user_id = current_user["id"]
        
        # Get channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Create analytics summary
        summary = {
            "channel_overview": {
                "name": profile.channel_name,
                "niche": profile.niche,
                "size_tier": profile.channel_size_tier,
                "subscriber_count": profile.metrics.subscriber_count,
                "total_views": profile.metrics.total_views,
                "video_count": profile.metrics.video_count
            },
            "performance_metrics": {
                "avg_views_per_video": profile.metrics.avg_views_per_video,
                "click_through_rate": profile.metrics.avg_ctr,
                "audience_retention": profile.metrics.avg_retention,
                "engagement_rate": profile.metrics.engagement_rate,
                "upload_frequency": profile.metrics.upload_frequency
            },
            "insights": {
                "top_challenges": profile.challenges[:3],
                "top_opportunities": profile.opportunities[:3],
                "recent_trend": profile.recent_performance.get("trend", "stable"),
                "growth_rate": profile.recent_performance.get("recent_growth_rate", 0)
            },
            "recommendations": {
                "priority_areas": [],
                "next_steps": []
            }
        }
        
        # Add priority recommendations based on metrics
        if profile.metrics.avg_ctr < 0.04:
            summary["recommendations"]["priority_areas"].append("Improve click-through rate")
            summary["recommendations"]["next_steps"].append("Optimize thumbnails and titles")
        
        if profile.metrics.avg_retention < 0.40:
            summary["recommendations"]["priority_areas"].append("Increase audience retention")
            summary["recommendations"]["next_steps"].append("Improve video structure and pacing")
        
        if profile.metrics.engagement_rate < 0.02:
            summary["recommendations"]["priority_areas"].append("Boost engagement")
            summary["recommendations"]["next_steps"].append("Encourage more comments and interactions")
        
        return create_success_response("Analytics summary retrieved successfully", summary)
        
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        return create_error_response("Failed to retrieve analytics summary", str(e))

@router.post("/refresh")
async def refresh_channel_data(current_user: Dict = Depends(get_current_user)):
    """Refresh channel data and clear cache"""
    try:
        user_id = current_user["id"]
        
        # Invalidate cache to force fresh data fetch
        channel_analyzer = get_channel_analyzer()
        await channel_analyzer.invalidate_cache(user_id)
        
        # Get fresh profile
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        return create_success_response("Channel data refreshed successfully", {
            "channel_name": profile.channel_name,
            "last_updated": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error refreshing channel data: {e}")
        return create_error_response("Failed to refresh channel data", str(e))

@router.get("/insights/{insight_type}")
async def get_channel_insights(
    insight_type: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get specific channel insights"""
    try:
        if insight_type not in ["challenges", "opportunities", "performance", "content"]:
            raise HTTPException(status_code=400, detail="Invalid insight type")
        
        user_id = current_user["id"]
        
        # Get channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        insights = {}
        
        if insight_type == "challenges":
            insights = {
                "type": "challenges",
                "items": profile.challenges,
                "description": "Areas that need improvement based on your channel data"
            }
        elif insight_type == "opportunities":
            insights = {
                "type": "opportunities", 
                "items": profile.opportunities,
                "description": "Growth opportunities identified from your performance"
            }
        elif insight_type == "performance":
            insights = {
                "type": "performance",
                "metrics": {
                    "ctr": {"value": profile.metrics.avg_ctr, "benchmark": 0.05, "status": "good" if profile.metrics.avg_ctr >= 0.05 else "needs_improvement"},
                    "retention": {"value": profile.metrics.avg_retention, "benchmark": 0.50, "status": "good" if profile.metrics.avg_retention >= 0.50 else "needs_improvement"},
                    "engagement": {"value": profile.metrics.engagement_rate, "benchmark": 0.03, "status": "good" if profile.metrics.engagement_rate >= 0.03 else "needs_improvement"}
                },
                "description": "Performance metrics compared to industry benchmarks"
            }
        elif insight_type == "content":
            insights = {
                "type": "content",
                "strategy": profile.content_strategy,
                "top_topics": profile.metrics.top_performing_topics,
                "description": "Content strategy analysis and recommendations"
            }
        
        return create_success_response(f"{insight_type.title()} insights retrieved successfully", insights)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting channel insights: {e}")
        return create_error_response("Failed to retrieve channel insights", str(e))
