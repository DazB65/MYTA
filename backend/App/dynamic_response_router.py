"""
Dynamic Response Router for MYTA
API endpoints for dynamic response system and context analysis
"""

from fastapi import APIRouter, Depends, Request, HTTPException
from typing import Dict, List, Optional, Any

from backend.App.dynamic_response_engine import get_dynamic_response_engine, ResponseContext
from backend.App.context_analyzer import get_context_analyzer
from backend.App.channel_analyzer import get_channel_analyzer
from backend.App.auth_middleware import get_current_user
from backend.App.api_models import create_success_response, create_error_response
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/dynamic-response", tags=["dynamic_response"])

@router.post("/analyze-context")
async def analyze_conversation_context(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Analyze conversation context and user patterns"""
    try:
        body = await request.json()
        user_message = body.get("message", "")
        conversation_history = body.get("conversation_history", [])
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Analyze conversation context
        context_analyzer = get_context_analyzer()
        conversation_context = context_analyzer.analyze_conversation_context(
            user_message, conversation_history
        )
        
        # Analyze user patterns
        user_patterns = context_analyzer.analyze_user_patterns(conversation_history)
        
        result = {
            "conversation_context": {
                "user_intent": conversation_context.user_intent,
                "emotional_state": conversation_context.emotional_state,
                "expertise_level": conversation_context.expertise_level,
                "question_type": conversation_context.question_type,
                "topic_focus": conversation_context.topic_focus,
                "urgency_signals": conversation_context.urgency_signals,
                "conversation_stage": conversation_context.conversation_stage
            },
            "user_patterns": {
                "communication_style": user_patterns.preferred_communication_style,
                "question_types": user_patterns.typical_question_types,
                "engagement_level": user_patterns.engagement_level,
                "learning_pace": user_patterns.learning_pace,
                "goal_orientation": user_patterns.goal_orientation,
                "technical_comfort": user_patterns.technical_comfort,
                "response_preferences": user_patterns.response_preferences
            },
            "analysis_insights": {
                "primary_intent": conversation_context.user_intent,
                "emotional_tone": conversation_context.emotional_state,
                "expertise_assessment": conversation_context.expertise_level,
                "conversation_maturity": conversation_context.conversation_stage
            }
        }
        
        return create_success_response("Context analysis completed", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing conversation context: {e}")
        return create_error_response("Failed to analyze context", str(e))

@router.post("/generate-dynamic-response")
async def generate_dynamic_response(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Generate dynamic response with context adaptations"""
    try:
        body = await request.json()
        agent_id = body.get("agent_id", "1")
        user_message = body.get("message", "")
        conversation_history = body.get("conversation_history", [])
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        if agent_id not in ["1", "2", "3", "4", "5"]:
            raise HTTPException(status_code=400, detail="Invalid agent ID")
        
        user_id = current_user["id"]
        
        # Get user's channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Create response context
        response_context = ResponseContext(
            user_id=user_id,
            agent_id=agent_id,
            user_message=user_message,
            conversation_history=conversation_history,
            channel_profile=profile,
            current_goals=profile.goals,
            recent_performance=profile.recent_performance,
            seasonal_factors={},
            urgency_level="medium",
            response_style_preference="standard"
        )
        
        # Generate dynamic response
        dynamic_engine = get_dynamic_response_engine()
        dynamic_response = await dynamic_engine.generate_dynamic_response(response_context)
        
        # Get agent info
        from backend.App.agent_personalities import get_agent_personality
        agent = get_agent_personality(agent_id)
        
        result = {
            "agent": {
                "id": agent_id,
                "name": agent["name"],
                "role": agent["role"],
                "color": agent["color"]
            },
            "dynamic_response": {
                "base_response": dynamic_response.base_response,
                "context_adaptations": dynamic_response.context_adaptations,
                "suggested_actions": dynamic_response.suggested_actions,
                "tool_recommendations": dynamic_response.tool_recommendations,
                "follow_up_questions": dynamic_response.follow_up_questions,
                "urgency_indicators": dynamic_response.urgency_indicators,
                "confidence_score": dynamic_response.confidence_score,
                "adaptation_reasoning": dynamic_response.adaptation_reasoning
            },
            "channel_context": {
                "name": profile.channel_name,
                "size_tier": profile.channel_size_tier,
                "niche": profile.niche,
                "subscriber_count": profile.metrics.subscriber_count
            }
        }
        
        return create_success_response("Dynamic response generated", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating dynamic response: {e}")
        return create_error_response("Failed to generate dynamic response", str(e))

@router.get("/response-adaptations/{agent_id}")
async def get_response_adaptations(
    agent_id: str,
    message: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get available response adaptations for a specific context"""
    try:
        if agent_id not in ["1", "2", "3", "4", "5"]:
            raise HTTPException(status_code=400, detail="Invalid agent ID")
        
        user_id = current_user["id"]
        
        # Get user's channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Analyze context
        context_analyzer = get_context_analyzer()
        conversation_context = context_analyzer.analyze_conversation_context(message, [])
        
        # Get dynamic engine
        dynamic_engine = get_dynamic_response_engine()
        
        # Determine adaptations
        urgency_level = dynamic_engine._assess_urgency(ResponseContext(
            user_id=user_id,
            agent_id=agent_id,
            user_message=message,
            conversation_history=[],
            channel_profile=profile,
            current_goals=profile.goals,
            recent_performance=profile.recent_performance,
            seasonal_factors={},
            urgency_level="medium",
            response_style_preference="standard"
        ))
        
        # Get adaptation options
        adaptations = {
            "urgency_level": urgency_level,
            "channel_size_adaptations": {
                "current_tier": profile.channel_size_tier,
                "focus_areas": dynamic_engine.response_patterns["channel_size_adaptations"].get(
                    profile.channel_size_tier, {}
                ).get("priorities", [])
            },
            "conversation_context": {
                "intent": conversation_context.user_intent,
                "emotional_state": conversation_context.emotional_state,
                "expertise_level": conversation_context.expertise_level,
                "topic_focus": conversation_context.topic_focus
            },
            "performance_adaptations": {
                "trend": profile.recent_performance.get("trend", "stable"),
                "key_metrics": {
                    "ctr": profile.metrics.avg_ctr,
                    "retention": profile.metrics.avg_retention,
                    "engagement": profile.metrics.engagement_rate
                }
            }
        }
        
        return create_success_response("Response adaptations retrieved", adaptations)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting response adaptations: {e}")
        return create_error_response("Failed to get response adaptations", str(e))

@router.post("/conversation-insights")
async def get_conversation_insights(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Get insights about conversation patterns and user behavior"""
    try:
        body = await request.json()
        conversation_history = body.get("conversation_history", [])
        
        if not conversation_history:
            raise HTTPException(status_code=400, detail="Conversation history is required")
        
        # Analyze patterns
        context_analyzer = get_context_analyzer()
        user_patterns = context_analyzer.analyze_user_patterns(conversation_history)
        
        # Extract conversation insights
        insights = {
            "conversation_summary": {
                "total_messages": len(conversation_history),
                "communication_style": user_patterns.preferred_communication_style,
                "engagement_level": user_patterns.engagement_level,
                "learning_pace": user_patterns.learning_pace
            },
            "user_behavior": {
                "typical_questions": user_patterns.typical_question_types,
                "goal_orientation": user_patterns.goal_orientation,
                "technical_comfort": user_patterns.technical_comfort,
                "response_preferences": user_patterns.response_preferences
            },
            "conversation_evolution": {
                "stages_covered": self._analyze_conversation_stages(conversation_history),
                "topic_progression": self._analyze_topic_progression(conversation_history),
                "complexity_trend": self._analyze_complexity_trend(conversation_history)
            },
            "recommendations": {
                "optimal_response_style": self._recommend_response_style(user_patterns),
                "suggested_adaptations": self._suggest_adaptations(user_patterns),
                "engagement_strategies": self._suggest_engagement_strategies(user_patterns)
            }
        }
        
        return create_success_response("Conversation insights generated", insights)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating conversation insights: {e}")
        return create_error_response("Failed to generate insights", str(e))

@router.get("/seasonal-adaptations")
async def get_seasonal_adaptations(current_user: Dict = Depends(get_current_user)):
    """Get current seasonal adaptations and opportunities"""
    try:
        # Get dynamic engine
        dynamic_engine = get_dynamic_response_engine()
        
        # Assess current seasonal factors
        from datetime import datetime
        now = datetime.now()
        month = now.month
        
        seasonal_info = {
            "current_season": self._get_current_season(month),
            "seasonal_opportunities": self._get_seasonal_opportunities(month),
            "content_suggestions": self._get_seasonal_content_suggestions(month),
            "trending_topics": self._get_seasonal_trending_topics(month),
            "optimization_tips": self._get_seasonal_optimization_tips(month)
        }
        
        return create_success_response("Seasonal adaptations retrieved", seasonal_info)
        
    except Exception as e:
        logger.error(f"Error getting seasonal adaptations: {e}")
        return create_error_response("Failed to get seasonal adaptations", str(e))

def _analyze_conversation_stages(conversation_history: List[Dict]) -> List[str]:
    """Analyze conversation stages covered"""
    stages = []
    
    if len(conversation_history) <= 3:
        stages.append("initial_exploration")
    if len(conversation_history) > 3:
        stages.append("problem_identification")
    if len(conversation_history) > 8:
        stages.append("solution_development")
    if len(conversation_history) > 15:
        stages.append("optimization_phase")
    
    return stages

def _analyze_topic_progression(conversation_history: List[Dict]) -> List[str]:
    """Analyze how topics have progressed"""
    context_analyzer = get_context_analyzer()
    
    topics_over_time = []
    for msg in conversation_history[-5:]:  # Last 5 messages
        content = msg.get("content", "")
        topics = context_analyzer._extract_topic_focus(content)
        topics_over_time.extend(topics)
    
    # Return unique topics in order
    unique_topics = []
    for topic in topics_over_time:
        if topic not in unique_topics:
            unique_topics.append(topic)
    
    return unique_topics

def _analyze_complexity_trend(conversation_history: List[Dict]) -> str:
    """Analyze complexity trend in conversation"""
    if not conversation_history:
        return "stable"
    
    # Simple analysis based on message length and technical terms
    recent_complexity = 0
    early_complexity = 0
    
    technical_terms = ["algorithm", "optimization", "analytics", "strategy", "systematic"]
    
    # Analyze recent messages
    for msg in conversation_history[-3:]:
        content = msg.get("content", "")
        recent_complexity += len(content) + sum(1 for term in technical_terms if term in content.lower())
    
    # Analyze early messages
    for msg in conversation_history[:3]:
        content = msg.get("content", "")
        early_complexity += len(content) + sum(1 for term in technical_terms if term in content.lower())
    
    if recent_complexity > early_complexity * 1.2:
        return "increasing"
    elif recent_complexity < early_complexity * 0.8:
        return "decreasing"
    else:
        return "stable"

def _recommend_response_style(user_patterns) -> str:
    """Recommend optimal response style"""
    
    if user_patterns.technical_comfort == "high" and user_patterns.learning_pace == "fast":
        return "technical_detailed"
    elif user_patterns.preferred_communication_style == "concise":
        return "concise_actionable"
    elif user_patterns.expertise_level == "beginner":
        return "educational_supportive"
    else:
        return "balanced_comprehensive"

def _suggest_adaptations(user_patterns) -> List[str]:
    """Suggest response adaptations"""
    
    adaptations = []
    
    if user_patterns.learning_pace == "slow":
        adaptations.append("Break down complex concepts into smaller steps")
    
    if user_patterns.technical_comfort == "low":
        adaptations.append("Avoid technical jargon and explain terms clearly")
    
    if user_patterns.goal_orientation == "tactical":
        adaptations.append("Focus on immediate actionable steps")
    
    if user_patterns.preferred_communication_style == "detailed":
        adaptations.append("Provide comprehensive explanations with examples")
    
    return adaptations

def _suggest_engagement_strategies(user_patterns) -> List[str]:
    """Suggest engagement strategies"""
    
    strategies = []
    
    if user_patterns.engagement_level == "high":
        strategies.append("Provide advanced challenges and optimization opportunities")
    
    if user_patterns.response_preferences.get("examples_preferred", True):
        strategies.append("Include concrete examples and case studies")
    
    if user_patterns.response_preferences.get("follow_up_questions", True):
        strategies.append("Ask targeted follow-up questions to deepen understanding")
    
    return strategies

def _get_current_season(month: int) -> str:
    """Get current season based on month"""
    if month in [11, 12]:
        return "Q4 Holiday Season"
    elif month == 1:
        return "New Year Planning"
    elif month in [6, 7, 8]:
        return "Summer Content Season"
    elif month in [8, 9]:
        return "Back to School Season"
    else:
        return "General Season"

def _get_seasonal_opportunities(month: int) -> List[str]:
    """Get seasonal opportunities"""
    if month in [11, 12]:
        return ["Holiday content", "Gift guides", "Year-end reviews", "Holiday monetization"]
    elif month == 1:
        return ["Goal-setting content", "New year planning", "Resolution videos", "Fresh start series"]
    elif month in [6, 7, 8]:
        return ["Summer activities", "Vacation content", "Outdoor videos", "Travel vlogs"]
    elif month in [8, 9]:
        return ["Educational content", "Back to school", "Learning series", "Productivity tips"]
    else:
        return ["Evergreen content", "Consistent series", "Community building"]

def _get_seasonal_content_suggestions(month: int) -> List[str]:
    """Get seasonal content suggestions"""
    if month in [11, 12]:
        return ["Holiday tutorials", "Gift recommendation videos", "Year in review", "Holiday challenges"]
    elif month == 1:
        return ["Goal setting guides", "Planning tutorials", "New year challenges", "Fresh start content"]
    elif month in [6, 7, 8]:
        return ["Summer project tutorials", "Outdoor activity guides", "Travel preparation", "Summer series"]
    else:
        return ["Educational tutorials", "Skill-building content", "How-to guides", "Learning series"]

def _get_seasonal_trending_topics(month: int) -> List[str]:
    """Get seasonal trending topics"""
    if month in [11, 12]:
        return ["Black Friday", "Cyber Monday", "Holiday shopping", "Christmas", "New Year"]
    elif month == 1:
        return ["New Year resolutions", "Goal setting", "Planning", "Fresh start", "Productivity"]
    elif month in [6, 7, 8]:
        return ["Summer vacation", "Travel", "Outdoor activities", "Summer projects"]
    else:
        return ["Education", "Learning", "Productivity", "Skill building"]

def _get_seasonal_optimization_tips(month: int) -> List[str]:
    """Get seasonal optimization tips"""
    if month in [11, 12]:
        return ["Optimize for holiday keywords", "Create gift guide content", "Leverage holiday traffic"]
    elif month == 1:
        return ["Target resolution keywords", "Create planning content", "Capitalize on motivation"]
    elif month in [6, 7, 8]:
        return ["Focus on summer activities", "Create travel content", "Optimize for vacation searches"]
    else:
        return ["Focus on evergreen content", "Build consistent series", "Optimize for search"]
