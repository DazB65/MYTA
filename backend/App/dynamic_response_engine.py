"""
Dynamic Response Engine for MYTA
Adapts agent responses based on user context, goals, and real-time data
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

from backend.App.channel_analyzer import ChannelProfile
from backend.App.agent_tools import get_agent_tools
from backend.App.youtube_knowledge import get_youtube_knowledge
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.AGENT)

@dataclass
class ResponseContext:
    """Context for dynamic response generation"""
    user_id: str
    agent_id: str
    user_message: str
    conversation_history: List[Dict[str, Any]]
    channel_profile: ChannelProfile
    current_goals: List[Dict[str, Any]]
    recent_performance: Dict[str, Any]
    seasonal_factors: Dict[str, Any]
    urgency_level: str
    response_style_preference: str

@dataclass
class DynamicResponse:
    """Dynamic response with context adaptations"""
    base_response: str
    context_adaptations: List[str]
    suggested_actions: List[str]
    tool_recommendations: List[str]
    follow_up_questions: List[str]
    urgency_indicators: List[str]
    confidence_score: float
    adaptation_reasoning: str

class DynamicResponseEngine:
    """Engine for generating context-aware, adaptive responses"""
    
    def __init__(self):
        self.agent_tools = get_agent_tools()
        self.youtube_knowledge = get_youtube_knowledge()
        self.response_patterns = self._load_response_patterns()
        self.adaptation_rules = self._load_adaptation_rules()
    
    def _load_response_patterns(self) -> Dict[str, Any]:
        """Load response patterns for different contexts"""
        return {
            "urgency_levels": {
                "critical": {
                    "tone": "immediate and focused",
                    "structure": "problem → solution → action",
                    "length": "concise",
                    "call_to_action": "strong"
                },
                "high": {
                    "tone": "proactive and solution-oriented",
                    "structure": "context → recommendation → steps",
                    "length": "detailed",
                    "call_to_action": "clear"
                },
                "medium": {
                    "tone": "supportive and educational",
                    "structure": "analysis → guidance → options",
                    "length": "comprehensive",
                    "call_to_action": "encouraging"
                },
                "low": {
                    "tone": "exploratory and strategic",
                    "structure": "overview → insights → planning",
                    "length": "thorough",
                    "call_to_action": "thoughtful"
                }
            },
            "channel_size_adaptations": {
                "micro": {
                    "focus": "foundation building",
                    "priorities": ["consistency", "quality", "engagement"],
                    "avoid": ["complex scaling", "advanced monetization"],
                    "encourage": ["community building", "niche authority"]
                },
                "small": {
                    "focus": "growth acceleration",
                    "priorities": ["optimization", "scaling", "algorithm"],
                    "avoid": ["premature monetization", "overcomplication"],
                    "encourage": ["systematic growth", "content variety"]
                },
                "medium": {
                    "focus": "optimization and scaling",
                    "priorities": ["efficiency", "monetization", "brand building"],
                    "avoid": ["basic advice", "manual processes"],
                    "encourage": ["automation", "team building"]
                },
                "large": {
                    "focus": "strategic expansion",
                    "priorities": ["diversification", "team management", "innovation"],
                    "avoid": ["micro-management", "basic tactics"],
                    "encourage": ["strategic thinking", "market leadership"]
                }
            },
            "performance_adaptations": {
                "declining": {
                    "tone": "supportive but urgent",
                    "focus": "problem identification and quick wins",
                    "tools": ["performance_analyzer", "benchmark_comparator"],
                    "timeline": "immediate action needed"
                },
                "stagnant": {
                    "tone": "motivational and strategic",
                    "focus": "breakthrough strategies and optimization",
                    "tools": ["growth_strategy", "content_analyzer"],
                    "timeline": "2-4 week improvement plan"
                },
                "growing": {
                    "tone": "encouraging and forward-looking",
                    "focus": "momentum maintenance and scaling",
                    "tools": ["growth_forecaster", "scaling_planner"],
                    "timeline": "long-term strategic planning"
                }
            }
        }
    
    def _load_adaptation_rules(self) -> Dict[str, Any]:
        """Load rules for response adaptation"""
        return {
            "goal_alignment": {
                "subscriber_growth": {
                    "emphasize": ["content consistency", "audience engagement", "SEO optimization"],
                    "tools": ["growth_strategy", "seo_optimizer"],
                    "metrics": ["subscriber_velocity", "retention_rate"]
                },
                "monetization": {
                    "emphasize": ["revenue optimization", "audience value", "brand building"],
                    "tools": ["revenue_optimizer", "audience_insights"],
                    "metrics": ["engagement_rate", "watch_time"]
                },
                "content_quality": {
                    "emphasize": ["production value", "audience retention", "creative optimization"],
                    "tools": ["content_analyzer", "title_optimizer"],
                    "metrics": ["retention_rate", "engagement_rate"]
                },
                "algorithm_optimization": {
                    "emphasize": ["technical optimization", "performance metrics", "discovery"],
                    "tools": ["algorithm_optimizer", "seo_optimizer"],
                    "metrics": ["ctr", "impressions", "reach"]
                }
            },
            "conversation_patterns": {
                "first_interaction": {
                    "include": ["welcome", "capability_overview", "goal_setting"],
                    "tone": "welcoming and informative"
                },
                "returning_user": {
                    "include": ["progress_check", "previous_recommendations", "next_steps"],
                    "tone": "familiar and progressive"
                },
                "frustrated_user": {
                    "include": ["empathy", "problem_acknowledgment", "clear_solutions"],
                    "tone": "supportive and solution-focused"
                },
                "successful_user": {
                    "include": ["celebration", "momentum_building", "advanced_strategies"],
                    "tone": "congratulatory and ambitious"
                }
            },
            "seasonal_adaptations": {
                "q4_holiday": {
                    "emphasize": ["holiday content", "seasonal trends", "gift guides"],
                    "opportunities": ["increased watch time", "seasonal monetization"]
                },
                "new_year": {
                    "emphasize": ["goal setting", "fresh starts", "planning content"],
                    "opportunities": ["resolution content", "planning videos"]
                },
                "summer": {
                    "emphasize": ["outdoor content", "vacation vlogs", "seasonal activities"],
                    "opportunities": ["travel content", "summer series"]
                },
                "back_to_school": {
                    "emphasize": ["educational content", "productivity", "learning"],
                    "opportunities": ["tutorial content", "educational series"]
                }
            }
        }
    
    async def generate_dynamic_response(self, context: ResponseContext) -> DynamicResponse:
        """Generate a dynamic, context-aware response"""
        
        try:
            # Analyze context and determine adaptations needed
            urgency_level = self._assess_urgency(context)
            performance_trend = self._analyze_performance_trend(context)
            goal_alignment = self._analyze_goal_alignment(context)
            conversation_pattern = self._identify_conversation_pattern(context)
            seasonal_factors = self._assess_seasonal_factors(context)
            
            # Generate base response structure
            response_pattern = self.response_patterns["urgency_levels"][urgency_level]
            
            # Apply channel size adaptations
            size_adaptations = self._apply_size_adaptations(context, response_pattern)
            
            # Apply performance adaptations
            performance_adaptations = self._apply_performance_adaptations(context, performance_trend)
            
            # Apply goal-specific adaptations
            goal_adaptations = self._apply_goal_adaptations(context, goal_alignment)
            
            # Apply conversation pattern adaptations
            conversation_adaptations = self._apply_conversation_adaptations(context, conversation_pattern)
            
            # Apply seasonal adaptations
            seasonal_adaptations = self._apply_seasonal_adaptations(context, seasonal_factors)
            
            # Generate tool recommendations
            tool_recommendations = self._generate_tool_recommendations(context, urgency_level)
            
            # Generate follow-up questions
            follow_up_questions = self._generate_follow_up_questions(context)
            
            # Generate suggested actions
            suggested_actions = self._generate_suggested_actions(context, urgency_level)
            
            # Compile all adaptations
            all_adaptations = (
                size_adaptations + performance_adaptations + 
                goal_adaptations + conversation_adaptations + seasonal_adaptations
            )
            
            # Generate adaptation reasoning
            reasoning = self._generate_adaptation_reasoning(
                context, urgency_level, performance_trend, goal_alignment
            )
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(context, all_adaptations)
            
            return DynamicResponse(
                base_response=self._generate_base_response(context, response_pattern),
                context_adaptations=all_adaptations,
                suggested_actions=suggested_actions,
                tool_recommendations=tool_recommendations,
                follow_up_questions=follow_up_questions,
                urgency_indicators=self._generate_urgency_indicators(urgency_level),
                confidence_score=confidence_score,
                adaptation_reasoning=reasoning
            )
        
        except Exception as e:
            logger.error(f"Error generating dynamic response: {e}")
            return self._generate_fallback_response(context)
    
    def _assess_urgency(self, context: ResponseContext) -> str:
        """Assess urgency level based on context"""
        
        profile = context.channel_profile
        message = context.user_message.lower()
        
        # Critical urgency indicators
        critical_keywords = ["emergency", "urgent", "crisis", "disaster", "help", "broken", "not working"]
        if any(keyword in message for keyword in critical_keywords):
            return "critical"
        
        # Performance-based urgency
        if profile.metrics.avg_ctr < 0.02:  # Very low CTR
            return "high"
        if profile.metrics.avg_retention < 0.30:  # Very low retention
            return "high"
        
        # Declining performance
        if profile.recent_performance.get("trend") == "declining":
            return "high"
        
        # Goal-based urgency
        urgent_goals = ["monetization", "subscriber_milestone", "algorithm_recovery"]
        if any(goal.get("priority") == "urgent" for goal in context.current_goals):
            return "high"
        
        # Growth stage urgency
        if profile.channel_size_tier == "micro" and profile.metrics.subscriber_count < 100:
            return "medium"
        
        return "low"
    
    def _analyze_performance_trend(self, context: ResponseContext) -> str:
        """Analyze current performance trend"""
        
        recent_perf = context.recent_performance
        trend = recent_perf.get("trend", "stable")
        
        growth_rate = recent_perf.get("recent_growth_rate", 0)
        
        if trend == "declining" or growth_rate < -0.05:
            return "declining"
        elif trend == "growing" or growth_rate > 0.05:
            return "growing"
        else:
            return "stagnant"
    
    def _analyze_goal_alignment(self, context: ResponseContext) -> List[str]:
        """Analyze alignment with user goals"""
        
        aligned_goals = []
        message_lower = context.user_message.lower()
        
        goal_keywords = {
            "subscriber_growth": ["subscribers", "grow", "audience", "reach"],
            "monetization": ["money", "revenue", "monetize", "income", "ads"],
            "content_quality": ["quality", "better", "improve", "content"],
            "algorithm_optimization": ["algorithm", "discovery", "recommended", "views"]
        }
        
        for goal_type, keywords in goal_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                aligned_goals.append(goal_type)
        
        # Also check user's actual goals
        for goal in context.current_goals:
            goal_type = goal.get("category", "").lower()
            if goal_type in goal_keywords:
                aligned_goals.append(goal_type)
        
        return list(set(aligned_goals))  # Remove duplicates
    
    def _identify_conversation_pattern(self, context: ResponseContext) -> str:
        """Identify conversation pattern"""
        
        history = context.conversation_history
        message = context.user_message.lower()
        
        # Check if first interaction
        if len(history) <= 1:
            return "first_interaction"
        
        # Check for frustration indicators
        frustration_keywords = ["frustrated", "confused", "not working", "help", "stuck"]
        if any(keyword in message for keyword in frustration_keywords):
            return "frustrated_user"
        
        # Check for success indicators
        success_keywords = ["working", "improved", "better", "thanks", "great", "awesome"]
        if any(keyword in message for keyword in success_keywords):
            return "successful_user"
        
        return "returning_user"
    
    def _assess_seasonal_factors(self, context: ResponseContext) -> str:
        """Assess current seasonal factors"""
        
        now = datetime.now()
        month = now.month
        
        if month in [11, 12]:  # November, December
            return "q4_holiday"
        elif month == 1:  # January
            return "new_year"
        elif month in [6, 7, 8]:  # June, July, August
            return "summer"
        elif month in [8, 9]:  # August, September
            return "back_to_school"
        else:
            return "general"
    
    def _apply_size_adaptations(self, context: ResponseContext, pattern: Dict) -> List[str]:
        """Apply channel size-specific adaptations"""
        
        size_tier = context.channel_profile.channel_size_tier
        adaptations = []
        
        size_config = self.response_patterns["channel_size_adaptations"].get(size_tier, {})
        
        focus = size_config.get("focus", "general optimization")
        adaptations.append(f"Focus on {focus} strategies appropriate for {size_tier} creators")
        
        priorities = size_config.get("priorities", [])
        if priorities:
            adaptations.append(f"Prioritize: {', '.join(priorities[:3])}")
        
        encourage = size_config.get("encourage", [])
        if encourage:
            adaptations.append(f"Emphasize: {', '.join(encourage[:2])}")
        
        return adaptations
    
    def _apply_performance_adaptations(self, context: ResponseContext, trend: str) -> List[str]:
        """Apply performance trend adaptations"""
        
        adaptations = []
        perf_config = self.response_patterns["performance_adaptations"].get(trend, {})
        
        focus = perf_config.get("focus", "general optimization")
        adaptations.append(f"Address {trend} performance with focus on {focus}")
        
        timeline = perf_config.get("timeline", "standard timeline")
        adaptations.append(f"Timeline consideration: {timeline}")
        
        return adaptations
    
    def _apply_goal_adaptations(self, context: ResponseContext, goals: List[str]) -> List[str]:
        """Apply goal-specific adaptations"""
        
        adaptations = []
        
        for goal in goals[:2]:  # Top 2 goals
            goal_config = self.adaptation_rules["goal_alignment"].get(goal, {})
            emphasize = goal_config.get("emphasize", [])
            
            if emphasize:
                adaptations.append(f"For {goal.replace('_', ' ')}: emphasize {', '.join(emphasize[:2])}")
        
        return adaptations
    
    def _apply_conversation_adaptations(self, context: ResponseContext, pattern: str) -> List[str]:
        """Apply conversation pattern adaptations"""
        
        adaptations = []
        conv_config = self.adaptation_rules["conversation_patterns"].get(pattern, {})
        
        include = conv_config.get("include", [])
        tone = conv_config.get("tone", "professional")
        
        if include:
            adaptations.append(f"Include: {', '.join(include[:2])}")
        
        adaptations.append(f"Tone: {tone}")
        
        return adaptations
    
    def _apply_seasonal_adaptations(self, context: ResponseContext, season: str) -> List[str]:
        """Apply seasonal adaptations"""
        
        adaptations = []
        
        if season != "general":
            seasonal_config = self.adaptation_rules["seasonal_adaptations"].get(season, {})
            emphasize = seasonal_config.get("emphasize", [])
            opportunities = seasonal_config.get("opportunities", [])
            
            if emphasize:
                adaptations.append(f"Seasonal focus: {', '.join(emphasize[:2])}")
            
            if opportunities:
                adaptations.append(f"Seasonal opportunities: {', '.join(opportunities[:2])}")
        
        return adaptations
    
    def _generate_tool_recommendations(self, context: ResponseContext, urgency: str) -> List[str]:
        """Generate tool recommendations based on context"""
        
        recommendations = []
        agent_id = context.agent_id
        
        # Get suggested tool based on message
        suggested_tool = self.agent_tools.suggest_best_tool(
            agent_id, context.user_message, context.channel_profile
        )
        recommendations.append(suggested_tool)
        
        # Add urgency-based tools
        if urgency in ["critical", "high"]:
            if agent_id == "1":  # Alex
                recommendations.append("performance_analyzer")
            elif agent_id == "2":  # Levi
                recommendations.append("content_analyzer")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _generate_follow_up_questions(self, context: ResponseContext) -> List[str]:
        """Generate contextual follow-up questions"""
        
        questions = []
        profile = context.channel_profile
        
        # Performance-based questions
        if profile.metrics.avg_ctr < 0.04:
            questions.append("Would you like me to analyze your thumbnail and title strategy?")
        
        if profile.metrics.avg_retention < 0.40:
            questions.append("Should we look at your video structure and pacing?")
        
        # Goal-based questions
        if profile.channel_size_tier == "micro":
            questions.append("What's your target for subscriber growth this month?")
        
        # Agent-specific questions
        if context.agent_id == "1":  # Alex
            questions.append("Would you like a detailed performance benchmark comparison?")
        elif context.agent_id == "2":  # Levi
            questions.append("Are you interested in exploring new content formats?")
        
        return questions[:3]  # Top 3 questions
    
    def _generate_suggested_actions(self, context: ResponseContext, urgency: str) -> List[str]:
        """Generate contextual suggested actions"""
        
        actions = []
        profile = context.channel_profile
        
        # Urgency-based actions
        if urgency == "critical":
            actions.append("Run immediate performance analysis")
            actions.append("Identify and fix critical issues")
        elif urgency == "high":
            actions.append("Implement quick optimization wins")
            actions.append("Monitor performance closely")
        
        # Performance-based actions
        if profile.metrics.avg_ctr < 0.04:
            actions.append("A/B test new thumbnail designs")
        
        if profile.metrics.avg_retention < 0.40:
            actions.append("Analyze audience retention graphs")
        
        # Size-based actions
        if profile.channel_size_tier == "micro":
            actions.append("Focus on consistent upload schedule")
            actions.append("Engage with every comment")
        
        return actions[:4]  # Top 4 actions
    
    def _generate_urgency_indicators(self, urgency: str) -> List[str]:
        """Generate urgency indicators"""
        
        indicators = {
            "critical": ["🚨 Immediate attention required", "⏰ Act within 24 hours"],
            "high": ["⚡ High priority action needed", "📈 Quick wins available"],
            "medium": ["📊 Optimization opportunity", "🎯 Strategic improvement"],
            "low": ["💡 Enhancement suggestion", "🔍 Exploration opportunity"]
        }
        
        return indicators.get(urgency, [])
    
    def _generate_adaptation_reasoning(
        self, 
        context: ResponseContext, 
        urgency: str, 
        trend: str, 
        goals: List[str]
    ) -> str:
        """Generate reasoning for adaptations"""
        
        reasoning_parts = []
        
        reasoning_parts.append(f"Adapted for {context.channel_profile.channel_size_tier} creator")
        reasoning_parts.append(f"Urgency level: {urgency}")
        reasoning_parts.append(f"Performance trend: {trend}")
        
        if goals:
            reasoning_parts.append(f"Aligned with goals: {', '.join(goals[:2])}")
        
        return " | ".join(reasoning_parts)
    
    def _calculate_confidence_score(self, context: ResponseContext, adaptations: List[str]) -> float:
        """Calculate confidence score for response"""
        
        base_score = 0.7
        
        # Boost for more context
        if len(context.conversation_history) > 3:
            base_score += 0.1
        
        # Boost for clear goals
        if context.current_goals:
            base_score += 0.1
        
        # Boost for more adaptations
        if len(adaptations) > 5:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _generate_base_response(self, context: ResponseContext, pattern: Dict) -> str:
        """Generate base response structure"""
        
        structure = pattern.get("structure", "analysis → guidance → action")
        tone = pattern.get("tone", "professional")
        
        return f"Response structured as: {structure} with {tone} tone"
    
    def _generate_fallback_response(self, context: ResponseContext) -> DynamicResponse:
        """Generate fallback response when dynamic generation fails"""
        
        return DynamicResponse(
            base_response="I'm here to help with your YouTube channel optimization.",
            context_adaptations=["Standard response due to processing limitation"],
            suggested_actions=["Share more details about your specific challenge"],
            tool_recommendations=["performance_analyzer"],
            follow_up_questions=["What specific aspect would you like to focus on?"],
            urgency_indicators=["💡 Standard assistance available"],
            confidence_score=0.5,
            adaptation_reasoning="Fallback response - limited context processing"
        )

# Global dynamic response engine instance
_dynamic_response_engine: Optional[DynamicResponseEngine] = None

def get_dynamic_response_engine() -> DynamicResponseEngine:
    """Get or create global dynamic response engine instance"""
    global _dynamic_response_engine
    if _dynamic_response_engine is None:
        _dynamic_response_engine = DynamicResponseEngine()
    return _dynamic_response_engine
