"""
Real-Time Analytics Router for MYTA
API endpoints for live analytics, insights, and optimization recommendations
"""

from fastapi import APIRouter, Depends, Request, HTTPException, BackgroundTasks
from typing import Dict, List, Optional, Any
import asyncio

from .youtube_analytics_service import get_youtube_analytics_service
from .auth_middleware import get_current_user
from .api_models import create_success_response, create_error_response
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/realtime-analytics", tags=["realtime_analytics"])

@router.get("/dashboard/{channel_id}")
async def get_realtime_dashboard(
    channel_id: str,
    time_range: str = "last_7_days",
    current_user: Dict = Depends(get_current_user)
):
    """Get real-time analytics dashboard"""
    try:
        user_id = current_user["id"]
        
        # Get user's access token (in real implementation)
        access_token = "mock_token"  # Would get from user's stored credentials
        
        async with get_youtube_analytics_service() as analytics:
            # Get comprehensive dashboard data
            dashboard_data = await analytics.get_optimization_dashboard(channel_id, access_token)
            
            # Add real-time metrics
            real_time_metrics = await analytics.get_real_time_metrics(channel_id, access_token, time_range)
            
            # Combine data
            result = {
                "dashboard": dashboard_data,
                "real_time_metrics": {
                    "views": real_time_metrics.views,
                    "watch_time_minutes": real_time_metrics.watch_time_minutes,
                    "subscribers_gained": real_time_metrics.subscribers_gained,
                    "subscribers_lost": real_time_metrics.subscribers_lost,
                    "ctr": real_time_metrics.click_through_rate,
                    "retention": real_time_metrics.audience_retention,
                    "engagement_rate": (real_time_metrics.likes + real_time_metrics.comments) / max(real_time_metrics.views, 1),
                    "revenue": real_time_metrics.revenue,
                    "last_updated": real_time_metrics.timestamp.isoformat()
                },
                "performance_status": _assess_performance_status(real_time_metrics),
                "quick_insights": _generate_quick_insights(dashboard_data, real_time_metrics)
            }
            
            return create_success_response("Real-time dashboard data retrieved", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting real-time dashboard: {e}")
        return create_error_response("Failed to retrieve dashboard data", str(e))

@router.get("/insights/{channel_id}")
async def get_realtime_insights(
    channel_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get AI-powered real-time insights"""
    try:
        access_token = "mock_token"
        
        async with get_youtube_analytics_service() as analytics:
            insights = await analytics.get_real_time_insights(channel_id, access_token)
            
            result = {
                "insights": {
                    "performance_alerts": insights.performance_alerts,
                    "optimization_recommendations": insights.optimization_recommendations,
                    "trending_opportunities": insights.trending_opportunities,
                    "competitive_insights": insights.competitive_insights,
                    "growth_predictions": insights.growth_predictions
                },
                "summary": {
                    "total_alerts": len(insights.performance_alerts or []),
                    "high_priority_items": len([
                        alert for alert in (insights.performance_alerts or [])
                        if alert.get("urgency") in ["critical", "high"]
                    ]),
                    "optimization_opportunities": len(insights.optimization_recommendations or []),
                    "trending_opportunities": len(insights.trending_opportunities or [])
                },
                "last_updated": insights.timestamp.isoformat() if insights.timestamp else None
            }
            
            return create_success_response("Real-time insights retrieved", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting real-time insights: {e}")
        return create_error_response("Failed to retrieve insights", str(e))

@router.get("/video-performance/{video_id}")
async def get_video_performance_insights(
    video_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get AI-powered insights for a specific video"""
    try:
        access_token = "mock_token"
        
        async with get_youtube_analytics_service() as analytics:
            insights = await analytics.get_video_performance_insights([video_id], access_token)
            
            if not insights:
                raise HTTPException(status_code=404, detail="Video insights not found")
            
            video_insight = insights[0]
            
            result = {
                "video_insight": {
                    "video_id": video_insight.video_id,
                    "title": video_insight.title,
                    "performance_metrics": {
                        "views": video_insight.views,
                        "ctr": video_insight.ctr,
                        "retention": video_insight.retention,
                        "engagement_score": video_insight.engagement_score
                    },
                    "ai_scores": {
                        "optimization_score": video_insight.optimization_score,
                        "trending_potential": video_insight.trending_potential,
                        "performance_grade": _calculate_performance_grade(video_insight.optimization_score)
                    },
                    "recommended_actions": video_insight.recommended_actions,
                    "improvement_areas": _identify_improvement_areas(video_insight)
                },
                "benchmarks": _get_video_benchmarks(),
                "optimization_tips": _get_optimization_tips(video_insight)
            }
            
            return create_success_response("Video performance insights retrieved", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting video performance insights: {e}")
        return create_error_response("Failed to retrieve video insights", str(e))

@router.post("/performance-alerts")
async def setup_performance_alerts(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Setup custom performance alerts"""
    try:
        body = await request.json()
        
        channel_id = body.get("channel_id")
        alert_settings = body.get("alert_settings", {})
        
        if not channel_id:
            raise HTTPException(status_code=400, detail="Channel ID is required")
        
        # Validate alert settings
        valid_settings = _validate_alert_settings(alert_settings)
        
        # Store alert settings (in real implementation, save to database)
        result = {
            "channel_id": channel_id,
            "alert_settings": valid_settings,
            "alerts_enabled": True,
            "notification_methods": body.get("notification_methods", ["email", "dashboard"]),
            "created_at": "2024-01-15T10:30:00Z"
        }
        
        return create_success_response("Performance alerts configured", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting up performance alerts: {e}")
        return create_error_response("Failed to setup alerts", str(e))

@router.get("/trending-analysis")
async def get_trending_analysis(
    niche: str = "general",
    region: str = "US",
    current_user: Dict = Depends(get_current_user)
):
    """Get trending content analysis for niche"""
    try:
        async with get_youtube_analytics_service() as analytics:
            trending_data = await analytics.get_trending_analysis(niche, region)
            
            result = {
                "trending_analysis": trending_data,
                "niche": niche,
                "region": region,
                "actionable_insights": _extract_actionable_insights(trending_data),
                "content_opportunities": _identify_content_opportunities(trending_data),
                "last_updated": "2024-01-15T10:30:00Z"
            }
            
            return create_success_response("Trending analysis retrieved", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trending analysis: {e}")
        return create_error_response("Failed to retrieve trending analysis", str(e))

@router.get("/competitor-analysis/{channel_id}")
async def get_competitor_analysis(
    channel_id: str,
    competitor_channels: str,  # Comma-separated list
    current_user: Dict = Depends(get_current_user)
):
    """Get competitive analysis against specified channels"""
    try:
        access_token = "mock_token"
        competitor_list = [ch.strip() for ch in competitor_channels.split(",")]
        
        async with get_youtube_analytics_service() as analytics:
            analysis = await analytics.get_competitor_analysis(competitor_list, access_token)
            
            result = {
                "your_channel": channel_id,
                "competitors_analyzed": competitor_list,
                "competitive_analysis": analysis,
                "your_position": _assess_competitive_position(channel_id, analysis),
                "improvement_opportunities": _identify_competitive_opportunities(analysis),
                "benchmarking": _create_competitive_benchmarks(analysis)
            }
            
            return create_success_response("Competitor analysis completed", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting competitor analysis: {e}")
        return create_error_response("Failed to retrieve competitor analysis", str(e))

@router.get("/optimization-recommendations/{channel_id}")
async def get_optimization_recommendations(
    channel_id: str,
    priority: str = "all",  # all, high, medium, low
    current_user: Dict = Depends(get_current_user)
):
    """Get AI-powered optimization recommendations"""
    try:
        access_token = "mock_token"
        
        async with get_youtube_analytics_service() as analytics:
            recommendations = await analytics.get_optimization_recommendations(channel_id, access_token)
            
            # Filter by priority if specified
            if priority != "all":
                recommendations = [
                    rec for rec in recommendations 
                    if rec.get("priority") == priority
                ]
            
            result = {
                "channel_id": channel_id,
                "recommendations": recommendations,
                "summary": {
                    "total_recommendations": len(recommendations),
                    "high_priority": len([r for r in recommendations if r.get("priority") == "high"]),
                    "medium_priority": len([r for r in recommendations if r.get("priority") == "medium"]),
                    "low_priority": len([r for r in recommendations if r.get("priority") == "low"])
                },
                "implementation_plan": _create_implementation_plan(recommendations),
                "expected_outcomes": _calculate_expected_outcomes(recommendations)
            }
            
            return create_success_response("Optimization recommendations retrieved", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting optimization recommendations: {e}")
        return create_error_response("Failed to retrieve recommendations", str(e))

@router.post("/track-implementation")
async def track_implementation(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """Track implementation of optimization recommendations"""
    try:
        body = await request.json()
        
        channel_id = body.get("channel_id")
        implemented_actions = body.get("implemented_actions", [])
        
        if not channel_id:
            raise HTTPException(status_code=400, detail="Channel ID is required")
        
        # Track implementation (in real app, save to database)
        tracking_data = {
            "channel_id": channel_id,
            "implemented_actions": implemented_actions,
            "implementation_date": "2024-01-15T10:30:00Z",
            "tracking_id": f"track_{channel_id}_{len(implemented_actions)}"
        }
        
        # Schedule follow-up analysis
        background_tasks.add_task(
            _schedule_follow_up_analysis,
            channel_id,
            implemented_actions
        )
        
        result = {
            "tracking_data": tracking_data,
            "follow_up_scheduled": True,
            "next_analysis_date": "2024-01-22T10:30:00Z",
            "expected_impact_timeline": "7-14 days"
        }
        
        return create_success_response("Implementation tracking started", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tracking implementation: {e}")
        return create_error_response("Failed to track implementation", str(e))

# Helper functions

def _assess_performance_status(metrics) -> Dict[str, Any]:
    """Assess overall performance status"""
    
    ctr_status = "good" if metrics.click_through_rate > 0.05 else "needs_improvement"
    retention_status = "good" if metrics.audience_retention > 0.45 else "needs_improvement"
    growth_status = "good" if metrics.subscribers_gained > metrics.subscribers_lost else "needs_improvement"
    
    overall_status = "good" if all(
        status == "good" for status in [ctr_status, retention_status, growth_status]
    ) else "needs_improvement"
    
    return {
        "overall": overall_status,
        "ctr": ctr_status,
        "retention": retention_status,
        "growth": growth_status,
        "areas_for_improvement": [
            area for area, status in [
                ("click_through_rate", ctr_status),
                ("audience_retention", retention_status),
                ("subscriber_growth", growth_status)
            ] if status == "needs_improvement"
        ]
    }

def _generate_quick_insights(dashboard_data: Dict, metrics) -> List[str]:
    """Generate quick actionable insights"""
    
    insights = []
    
    if metrics.click_through_rate < 0.04:
        insights.append("🎯 CTR is below average - focus on thumbnail optimization")
    
    if metrics.audience_retention < 0.40:
        insights.append("⏱️ Retention needs improvement - strengthen video hooks")
    
    if metrics.subscribers_gained < 10:
        insights.append("📈 Low subscriber growth - implement growth strategies")
    
    if metrics.revenue > 0:
        insights.append(f"💰 Revenue generated: ${metrics.revenue:.2f}")
    
    return insights[:3]  # Top 3 insights

def _calculate_performance_grade(score: float) -> str:
    """Calculate performance grade from score"""
    
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "D"

def _identify_improvement_areas(video_insight) -> List[str]:
    """Identify specific improvement areas for video"""
    
    areas = []
    
    if video_insight.ctr < 0.05:
        areas.append("Thumbnail design and title optimization")
    
    if video_insight.retention < 0.45:
        areas.append("Content structure and pacing")
    
    if video_insight.engagement_score < 50:
        areas.append("Audience engagement and interaction")
    
    return areas

def _get_video_benchmarks() -> Dict[str, Any]:
    """Get video performance benchmarks"""
    
    return {
        "ctr": {"poor": 0.02, "average": 0.05, "good": 0.08, "excellent": 0.12},
        "retention": {"poor": 0.30, "average": 0.45, "good": 0.60, "excellent": 0.75},
        "engagement": {"poor": 20, "average": 50, "good": 80, "excellent": 100}
    }

def _get_optimization_tips(video_insight) -> List[str]:
    """Get specific optimization tips for video"""
    
    tips = []
    
    if video_insight.ctr < 0.05:
        tips.append("Use high-contrast thumbnails with clear focal points")
        tips.append("Include emotional expressions in thumbnail faces")
    
    if video_insight.retention < 0.45:
        tips.append("Create stronger hooks in the first 15 seconds")
        tips.append("Use pattern interrupts every 60-90 seconds")
    
    return tips

def _validate_alert_settings(settings: Dict) -> Dict[str, Any]:
    """Validate and normalize alert settings"""
    
    valid_settings = {
        "ctr_threshold": max(0.01, min(settings.get("ctr_threshold", 0.03), 0.20)),
        "retention_threshold": max(0.20, min(settings.get("retention_threshold", 0.35), 0.80)),
        "subscriber_loss_threshold": max(1, min(settings.get("subscriber_loss_threshold", 10), 100)),
        "view_drop_threshold": max(0.10, min(settings.get("view_drop_threshold", 0.30), 0.80))
    }
    
    return valid_settings

def _extract_actionable_insights(trending_data: Dict) -> List[str]:
    """Extract actionable insights from trending data"""
    
    insights = []
    
    if trending_data.get("trending_topics"):
        insights.append(f"Create content around: {', '.join(trending_data['trending_topics'][:3])}")
    
    if trending_data.get("optimal_length"):
        insights.append(f"Optimal video length: {trending_data['optimal_length']['average']}")
    
    if trending_data.get("upload_patterns"):
        best_days = trending_data["upload_patterns"].get("best_days", [])
        if best_days:
            insights.append(f"Best upload days: {', '.join(best_days[:2])}")
    
    return insights

def _identify_content_opportunities(trending_data: Dict) -> List[Dict[str, Any]]:
    """Identify specific content opportunities"""
    
    opportunities = []
    
    if trending_data.get("trending_keywords"):
        opportunities.append({
            "type": "keyword_opportunity",
            "title": "Trending Keywords",
            "keywords": trending_data["trending_keywords"][:5],
            "urgency": "high"
        })
    
    if trending_data.get("popular_formats"):
        opportunities.append({
            "type": "format_opportunity",
            "title": "Popular Formats",
            "formats": trending_data["popular_formats"],
            "urgency": "medium"
        })
    
    return opportunities

def _assess_competitive_position(channel_id: str, analysis: Dict) -> Dict[str, Any]:
    """Assess competitive position"""
    
    return {
        "ranking": "middle",  # Simplified
        "strengths": ["consistent_uploads", "good_engagement"],
        "weaknesses": ["lower_ctr", "shorter_videos"],
        "opportunities": ["trending_topics", "collaboration"]
    }

def _identify_competitive_opportunities(analysis: Dict) -> List[str]:
    """Identify opportunities from competitive analysis"""
    
    return [
        "Increase upload frequency to match top performers",
        "Improve thumbnail quality based on competitor analysis",
        "Explore underserved content topics in your niche"
    ]

def _create_competitive_benchmarks(analysis: Dict) -> Dict[str, Any]:
    """Create competitive benchmarks"""
    
    return {
        "average_ctr": 0.055,
        "average_retention": 0.48,
        "average_upload_frequency": "2.3 videos/week",
        "top_performer_metrics": {
            "ctr": 0.085,
            "retention": 0.62,
            "growth_rate": 0.15
        }
    }

def _create_implementation_plan(recommendations: List[Dict]) -> Dict[str, Any]:
    """Create implementation plan from recommendations"""
    
    plan = {
        "week_1": [],
        "week_2": [],
        "month_1": [],
        "ongoing": []
    }
    
    for rec in recommendations:
        timeline = rec.get("timeline", "month_1")
        if "1 week" in timeline or "week" in timeline:
            plan["week_1"].append(rec["title"])
        elif "2 week" in timeline:
            plan["week_2"].append(rec["title"])
        else:
            plan["month_1"].append(rec["title"])
    
    return plan

def _calculate_expected_outcomes(recommendations: List[Dict]) -> Dict[str, Any]:
    """Calculate expected outcomes from recommendations"""
    
    total_impact = 0
    impact_areas = []
    
    for rec in recommendations:
        expected_impact = rec.get("expected_impact", "")
        if "%" in expected_impact:
            # Extract percentage
            import re
            percentages = re.findall(r'(\d+)', expected_impact)
            if percentages:
                total_impact += int(percentages[0])
        
        impact_areas.append(rec.get("category", "general"))
    
    return {
        "estimated_improvement": f"{min(total_impact, 100)}% overall improvement",
        "impact_areas": list(set(impact_areas)),
        "timeline": "4-8 weeks for full impact",
        "confidence": "medium"
    }

async def _schedule_follow_up_analysis(channel_id: str, actions: List[str]):
    """Schedule follow-up analysis after implementation"""
    
    # In real implementation, this would schedule a background job
    logger.info(f"Scheduled follow-up analysis for channel {channel_id} with {len(actions)} actions")
    
    # Simulate scheduling
    await asyncio.sleep(1)
    
    return True
