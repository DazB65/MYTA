"""
Advanced Intelligence API Router
API endpoints for content prediction, learning engine, and real-time optimization
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field

from .advanced_prediction_engine import get_prediction_engine, ContentPrediction
from .learning_adaptation_engine import get_learning_engine, AdaptationRecommendation
from .realtime_optimization_engine import get_optimization_engine
from .user_context import get_user_context

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/intelligence", tags=["Advanced Intelligence"])

# Request/Response Models
class ContentPredictionRequest(BaseModel):
    title: str = Field(..., description="Video title")
    description: str = Field(default="", description="Video description")
    topic: str = Field(default="", description="Video topic/category")
    tags: List[str] = Field(default=[], description="Video tags")
    scheduled_time: Optional[str] = Field(default=None, description="Scheduled publish time (ISO format)")
    prediction_type: str = Field(default="comprehensive", description="Prediction depth")

class ContentPredictionResponse(BaseModel):
    success: bool
    prediction: Optional[Dict[str, Any]]
    confidence_level: float
    optimization_suggestions: List[str]
    timing_recommendations: Dict[str, Any]
    risk_factors: List[str]
    processing_time_ms: float

class LearningAnalysisRequest(BaseModel):
    force_refresh: bool = Field(default=False, description="Force re-analysis of patterns")
    analysis_period_days: int = Field(default=90, description="Days to analyze")

class LearningAnalysisResponse(BaseModel):
    success: bool
    patterns_identified: int
    recommendations: List[Dict[str, Any]]
    insights: List[Dict[str, Any]]
    confidence_score: float
    last_updated: str

class RealTimeMonitoringRequest(BaseModel):
    video_id: str = Field(..., description="Video ID to monitor")
    hours_since_publish: Optional[float] = Field(default=None, description="Hours since video was published")

class RealTimeMonitoringResponse(BaseModel):
    success: bool
    video_id: str
    health_score: float
    alerts: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    action_plan: Dict[str, Any]
    next_review: str

# Dependency to get user ID (simplified for demo)
async def get_current_user_id() -> str:
    # In production, extract from JWT token or session
    return "demo_user_123"

@router.post("/predict-content-performance", response_model=ContentPredictionResponse)
async def predict_content_performance(
    request: ContentPredictionRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Predict content performance before publishing
    
    Uses advanced ML models and user-specific data to predict:
    - Expected views, CTR, engagement, retention
    - Success probability and performance score
    - Optimization suggestions and timing recommendations
    - Risk factors and confidence levels
    """
    try:
        start_time = datetime.now()
        logger.info(f"🔮 Predicting content performance for user {user_id}")
        
        # Get prediction engine
        prediction_engine = get_prediction_engine()
        
        # Prepare content data
        content_data = {
            'title': request.title,
            'description': request.description,
            'topic': request.topic,
            'tags': request.tags,
            'scheduled_time': request.scheduled_time
        }
        
        # Generate prediction
        prediction = await prediction_engine.predict_content_performance(
            user_id=user_id,
            content_data=content_data,
            prediction_type=request.prediction_type
        )
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return ContentPredictionResponse(
            success=True,
            prediction={
                'predicted_views': prediction.predicted_views,
                'predicted_ctr': prediction.predicted_ctr,
                'predicted_engagement_rate': prediction.predicted_engagement_rate,
                'predicted_retention': prediction.predicted_retention,
                'success_probability': prediction.success_probability,
                'performance_score': prediction.performance_score,
                'predicted_metrics': prediction.predicted_metrics
            },
            confidence_level=prediction.confidence_level,
            optimization_suggestions=prediction.optimization_suggestions,
            timing_recommendations=prediction.timing_recommendations,
            risk_factors=prediction.risk_factors,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error predicting content performance: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/analyze-learning-patterns", response_model=LearningAnalysisResponse)
async def analyze_learning_patterns(
    request: LearningAnalysisRequest,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user_id)
):
    """
    Analyze user's content patterns and generate adaptive recommendations
    
    Uses machine learning to identify:
    - Successful content patterns (titles, timing, topics, etc.)
    - Performance trends and optimization opportunities
    - Personalized recommendations based on user's success history
    - Confidence scores and supporting data
    """
    try:
        logger.info(f"🧠 Analyzing learning patterns for user {user_id}")
        
        # Get learning engine
        learning_engine = get_learning_engine()
        
        # Analyze patterns (run in background if not forced)
        if request.force_refresh:
            patterns = await learning_engine.analyze_user_patterns(user_id)
        else:
            # Try to get existing patterns first
            patterns = await learning_engine._get_user_patterns(user_id)
            if not patterns:
                # Run analysis in background
                background_tasks.add_task(learning_engine.analyze_user_patterns, user_id)
                patterns = []
        
        # Generate recommendations
        recommendations = await learning_engine.generate_adaptive_recommendations(user_id)
        
        # Calculate overall confidence
        avg_confidence = sum(p.confidence_score for p in patterns) / len(patterns) if patterns else 0.5
        
        return LearningAnalysisResponse(
            success=True,
            patterns_identified=len(patterns),
            recommendations=[
                {
                    'title': rec.title,
                    'description': rec.description,
                    'action': rec.specific_action,
                    'expected_improvement': f"{rec.expected_improvement:.1%}",
                    'confidence': rec.confidence,
                    'priority': rec.priority
                }
                for rec in recommendations[:10]
            ],
            insights=[
                {
                    'pattern_type': pattern.pattern_type,
                    'confidence': pattern.confidence_score,
                    'sample_size': pattern.sample_size,
                    'performance_improvement': f"{(sum(pattern.pattern_data.get('performance_ratios', {}).values()) / len(pattern.pattern_data.get('performance_ratios', {})) - 1) * 100:.1f}%" if pattern.pattern_data.get('performance_ratios') else "N/A"
                }
                for pattern in patterns[:5]
            ],
            confidence_score=avg_confidence,
            last_updated=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error analyzing learning patterns: {e}")
        raise HTTPException(status_code=500, detail=f"Learning analysis failed: {str(e)}")

@router.post("/monitor-realtime-performance", response_model=RealTimeMonitoringResponse)
async def monitor_realtime_performance(
    request: RealTimeMonitoringRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Monitor video performance in real-time with optimization recommendations
    
    Provides:
    - Real-time performance alerts and health scoring
    - Immediate optimization recommendations
    - Actionable insights for performance improvement
    - Monitoring schedule and next review times
    """
    try:
        logger.info(f"📊 Monitoring real-time performance for video {request.video_id}")
        
        # Get optimization engine
        optimization_engine = get_optimization_engine()
        
        # Monitor video performance
        monitoring_result = await optimization_engine.monitor_video_performance(
            user_id=user_id,
            video_id=request.video_id,
            hours_since_publish=request.hours_since_publish
        )
        
        if monitoring_result.get('error'):
            raise HTTPException(status_code=500, detail=monitoring_result['error'])
        
        return RealTimeMonitoringResponse(
            success=True,
            video_id=request.video_id,
            health_score=monitoring_result.get('health_score', 0),
            alerts=monitoring_result.get('alerts', []),
            recommendations=monitoring_result.get('recommendations', []),
            action_plan=monitoring_result.get('action_plan', {}),
            next_review=monitoring_result.get('action_plan', {}).get('next_review', datetime.now().isoformat())
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error monitoring real-time performance: {e}")
        raise HTTPException(status_code=500, detail=f"Real-time monitoring failed: {str(e)}")

@router.get("/optimization-dashboard")
async def get_optimization_dashboard(user_id: str = Depends(get_current_user_id)):
    """
    Get comprehensive optimization dashboard
    
    Provides overview of:
    - All monitored videos and their health scores
    - Active alerts and recommendations
    - Overall performance trends
    - Prioritized action items
    """
    try:
        logger.info(f"📊 Generating optimization dashboard for user {user_id}")
        
        # Get optimization engine
        optimization_engine = get_optimization_engine()
        
        # Generate dashboard
        dashboard = await optimization_engine.get_optimization_dashboard(user_id)
        
        if dashboard.get('error'):
            raise HTTPException(status_code=500, detail=dashboard['error'])
        
        return {
            'success': True,
            'dashboard': dashboard
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating optimization dashboard: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {str(e)}")

@router.get("/learning-recommendations")
async def get_learning_recommendations(
    limit: int = 10,
    user_id: str = Depends(get_current_user_id)
):
    """
    Get current adaptive learning recommendations
    
    Returns personalized recommendations based on:
    - User's historical success patterns
    - Recent performance trends
    - Optimization opportunities
    """
    try:
        logger.info(f"🎯 Getting learning recommendations for user {user_id}")
        
        # Get learning engine
        learning_engine = get_learning_engine()
        
        # Get recommendations
        recommendations = await learning_engine.get_user_recommendations(user_id, limit)
        
        return {
            'success': True,
            'recommendations': [
                {
                    'id': rec.recommendation_id,
                    'type': rec.recommendation_type,
                    'title': rec.title,
                    'description': rec.description,
                    'action': rec.specific_action,
                    'expected_improvement': f"{rec.expected_improvement:.1%}",
                    'confidence': rec.confidence,
                    'priority': rec.priority,
                    'expires_at': rec.expires_at.isoformat() if rec.expires_at else None
                }
                for rec in recommendations
            ],
            'total_count': len(recommendations)
        }
        
    except Exception as e:
        logger.error(f"Error getting learning recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@router.post("/quick-content-score")
async def quick_content_score(
    title: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Quick content scoring for title optimization
    
    Provides instant feedback on:
    - Title effectiveness score
    - Quick optimization suggestions
    - Predicted CTR impact
    """
    try:
        logger.info(f"⚡ Quick content scoring for user {user_id}")
        
        # Get prediction engine
        prediction_engine = get_prediction_engine()
        
        # Quick prediction with minimal data
        content_data = {'title': title, 'description': '', 'topic': ''}
        prediction = await prediction_engine.predict_content_performance(
            user_id=user_id,
            content_data=content_data,
            prediction_type="quick"
        )
        
        return {
            'success': True,
            'title_score': prediction.performance_score,
            'predicted_ctr': prediction.predicted_ctr,
            'quick_suggestions': prediction.optimization_suggestions[:3],
            'confidence': prediction.confidence_level
        }
        
    except Exception as e:
        logger.error(f"Error in quick content scoring: {e}")
        raise HTTPException(status_code=500, detail=f"Quick scoring failed: {str(e)}")
