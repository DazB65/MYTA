"""
Agent Performance Analytics API Router
Provides endpoints for tracking and analyzing agent performance
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from backend.App.agent_performance_analytics import (
    record_agent_performance,
    record_collaboration_metrics,
    get_agent_analytics,
    get_collaboration_analytics,
    get_performance_comparison,
    generate_performance_report,
    update_user_feedback,
    AnalyticsTimeframe
)
from backend.App.auth_middleware import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/performance-analytics", tags=["Performance Analytics"])

# Request/Response Models
class PerformanceRecordRequest(BaseModel):
    agent_name: str = Field(..., description="Name of the agent")
    user_id: str = Field(..., description="User identifier")
    success: bool = Field(..., description="Whether the execution was successful")
    response_time: float = Field(..., description="Response time in seconds")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")
    collaboration_partners: Optional[List[str]] = Field(default=None, description="Collaborating agents")
    insights_generated: int = Field(default=0, description="Number of insights generated")
    recommendations_provided: int = Field(default=0, description="Number of recommendations provided")
    proactive_suggestions: int = Field(default=0, description="Number of proactive suggestions")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Execution context")

class CollaborationMetricsRequest(BaseModel):
    participating_agents: List[str] = Field(..., description="Agents that participated")
    total_duration: float = Field(..., description="Total collaboration duration in seconds")
    success: bool = Field(..., description="Whether the collaboration was successful")
    synergy_score: float = Field(..., ge=0.0, le=1.0, description="Agent synergy score (0.0-1.0)")
    handoff_efficiency: float = Field(..., ge=0.0, le=1.0, description="Context handoff efficiency (0.0-1.0)")
    outcome_quality: float = Field(..., ge=0.0, le=1.0, description="Quality of final outcome (0.0-1.0)")

class UserFeedbackRequest(BaseModel):
    record_id: str = Field(..., description="Performance record ID")
    feedback_score: float = Field(..., ge=1.0, le=5.0, description="User feedback score (1.0-5.0)")

class PerformanceReportRequest(BaseModel):
    agent_names: List[str] = Field(..., description="Agents to include in report")
    timeframe: str = Field(..., description="Analysis timeframe")
    include_recommendations: bool = Field(default=True, description="Include recommendations in report")

@router.post("/record-performance")
async def record_performance_endpoint(
    request: PerformanceRecordRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Record agent performance metrics"""
    try:
        record_id = await record_agent_performance(
            agent_name=request.agent_name,
            user_id=request.user_id,
            success=request.success,
            response_time=request.response_time,
            confidence_score=request.confidence_score,
            collaboration_partners=request.collaboration_partners,
            insights_generated=request.insights_generated,
            recommendations_provided=request.recommendations_provided,
            proactive_suggestions=request.proactive_suggestions,
            context=request.context
        )
        
        return {
            "success": True,
            "record_id": record_id,
            "message": f"Performance recorded for {request.agent_name}"
        }
        
    except Exception as e:
        logger.error(f"Failed to record performance: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to record performance: {str(e)}")

@router.post("/record-collaboration")
async def record_collaboration_endpoint(
    request: CollaborationMetricsRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Record collaboration performance metrics"""
    try:
        collaboration_id = await record_collaboration_metrics(
            participating_agents=request.participating_agents,
            total_duration=request.total_duration,
            success=request.success,
            synergy_score=request.synergy_score,
            handoff_efficiency=request.handoff_efficiency,
            outcome_quality=request.outcome_quality
        )
        
        return {
            "success": True,
            "collaboration_id": collaboration_id,
            "message": f"Collaboration metrics recorded for {len(request.participating_agents)} agents"
        }
        
    except Exception as e:
        logger.error(f"Failed to record collaboration metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to record collaboration metrics: {str(e)}")

@router.post("/update-feedback")
async def update_feedback_endpoint(
    request: UserFeedbackRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Update user feedback for a performance record"""
    try:
        success = await update_user_feedback(request.record_id, request.feedback_score)
        
        if success:
            return {
                "success": True,
                "message": f"Feedback updated: {request.feedback_score}/5.0"
            }
        else:
            raise HTTPException(status_code=404, detail="Performance record not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update feedback: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update feedback: {str(e)}")

@router.get("/agent/{agent_name}")
async def get_agent_analytics_endpoint(
    agent_name: str,
    timeframe: str = Query(..., description="Analysis timeframe"),
    current_user: Dict = Depends(get_current_user)
):
    """Get analytics for a specific agent"""
    try:
        # Validate timeframe
        try:
            analytics_timeframe = AnalyticsTimeframe(timeframe)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid timeframe: {timeframe}")
        
        analytics = await get_agent_analytics(agent_name, analytics_timeframe)
        
        return {
            "success": True,
            "agent_name": agent_name,
            "analytics": {
                "agent_name": analytics.agent_name,
                "timeframe": analytics.timeframe.value,
                "period_start": analytics.period_start.isoformat(),
                "period_end": analytics.period_end.isoformat(),
                "total_executions": analytics.total_executions,
                "successful_executions": analytics.successful_executions,
                "success_rate": analytics.success_rate,
                "average_response_time": analytics.average_response_time,
                "average_confidence": analytics.average_confidence,
                "average_user_satisfaction": analytics.average_user_satisfaction,
                "collaboration_count": analytics.collaboration_count,
                "insights_generated": analytics.insights_generated,
                "recommendations_provided": analytics.recommendations_provided,
                "proactive_suggestions": analytics.proactive_suggestions,
                "top_collaboration_partners": analytics.top_collaboration_partners,
                "performance_trend": analytics.performance_trend
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent analytics for {agent_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get agent analytics: {str(e)}")

@router.get("/collaboration")
async def get_collaboration_analytics_endpoint(
    timeframe: str = Query(..., description="Analysis timeframe"),
    current_user: Dict = Depends(get_current_user)
):
    """Get collaboration analytics"""
    try:
        # Validate timeframe
        try:
            analytics_timeframe = AnalyticsTimeframe(timeframe)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid timeframe: {timeframe}")
        
        analytics = await get_collaboration_analytics(analytics_timeframe)
        
        return {
            "success": True,
            "collaboration_analytics": analytics
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get collaboration analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get collaboration analytics: {str(e)}")

@router.post("/compare")
async def compare_performance_endpoint(
    agent_names: List[str],
    timeframe: str = Query(..., description="Analysis timeframe"),
    current_user: Dict = Depends(get_current_user)
):
    """Compare performance across multiple agents"""
    try:
        # Validate timeframe
        try:
            analytics_timeframe = AnalyticsTimeframe(timeframe)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid timeframe: {timeframe}")
        
        if len(agent_names) < 2:
            raise HTTPException(status_code=400, detail="At least 2 agents required for comparison")
        
        comparison = await get_performance_comparison(agent_names, analytics_timeframe)
        
        return {
            "success": True,
            "performance_comparison": comparison
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to compare performance: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to compare performance: {str(e)}")

@router.post("/generate-report")
async def generate_report_endpoint(
    request: PerformanceReportRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Generate comprehensive performance report"""
    try:
        # Validate timeframe
        try:
            analytics_timeframe = AnalyticsTimeframe(request.timeframe)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid timeframe: {request.timeframe}")
        
        report = await generate_performance_report(
            agent_names=request.agent_names,
            timeframe=analytics_timeframe,
            include_recommendations=request.include_recommendations
        )
        
        return {
            "success": True,
            "performance_report": report
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate performance report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate performance report: {str(e)}")

@router.get("/timeframes")
async def get_available_timeframes(
    current_user: Dict = Depends(get_current_user)
):
    """Get available analysis timeframes"""
    try:
        timeframes = [
            {
                "value": timeframe.value,
                "name": timeframe.value.title(),
                "description": f"Analysis for the last {timeframe.value}"
            }
            for timeframe in AnalyticsTimeframe
        ]
        
        return {
            "success": True,
            "timeframes": timeframes
        }
        
    except Exception as e:
        logger.error(f"Failed to get timeframes: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get timeframes: {str(e)}")

@router.get("/dashboard-summary")
async def get_dashboard_summary(
    timeframe: str = Query(default="week", description="Analysis timeframe"),
    current_user: Dict = Depends(get_current_user)
):
    """Get summary data for performance dashboard"""
    try:
        # Validate timeframe
        try:
            analytics_timeframe = AnalyticsTimeframe(timeframe)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid timeframe: {timeframe}")
        
        # Get analytics for all main agents
        main_agents = ["content_analysis", "audience_insights", "seo_optimization", "competitive_analysis", "monetization"]
        
        agent_summaries = {}
        for agent in main_agents:
            try:
                analytics = await get_agent_analytics(agent, analytics_timeframe)
                agent_summaries[agent] = {
                    "total_executions": analytics.total_executions,
                    "success_rate": analytics.success_rate,
                    "average_response_time": analytics.average_response_time,
                    "performance_trend": analytics.performance_trend
                }
            except Exception:
                # Agent might not have data yet
                agent_summaries[agent] = {
                    "total_executions": 0,
                    "success_rate": 0.0,
                    "average_response_time": 0.0,
                    "performance_trend": "stable"
                }
        
        # Get collaboration summary
        collaboration_summary = await get_collaboration_analytics(analytics_timeframe)
        
        return {
            "success": True,
            "timeframe": timeframe,
            "agent_summaries": agent_summaries,
            "collaboration_summary": {
                "total_collaborations": collaboration_summary.get("total_collaborations", 0),
                "success_rate": collaboration_summary.get("success_rate", 0.0),
                "average_synergy_score": collaboration_summary.get("average_synergy_score", 0.0)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard summary: {str(e)}")
