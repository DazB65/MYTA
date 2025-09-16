"""
Proactive Agent Collaboration System
Enables agents to proactively suggest collaboration and share insights
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid

logger = logging.getLogger(__name__)

class InsightType(Enum):
    SUGGESTION = "suggestion"           # Suggesting an action or approach
    WARNING = "warning"                 # Alerting about potential issues
    OPPORTUNITY = "opportunity"         # Highlighting potential opportunities
    CORRELATION = "correlation"         # Noting relationships between data points
    ENHANCEMENT = "enhancement"         # Suggesting improvements to existing analysis

class UrgencyLevel(Enum):
    LOW = "low"                        # Can wait, informational
    MEDIUM = "medium"                  # Should be addressed soon
    HIGH = "high"                      # Needs immediate attention
    CRITICAL = "critical"              # Urgent action required

class CollaborationReason(Enum):
    EXPERTISE_NEEDED = "expertise_needed"           # Need specialized knowledge
    DATA_CORRELATION = "data_correlation"           # Found related data patterns
    OPPORTUNITY_ENHANCEMENT = "opportunity_enhancement"  # Can enhance an opportunity
    PROBLEM_SOLVING = "problem_solving"             # Need help solving a problem
    VALIDATION_NEEDED = "validation_needed"         # Need second opinion
    CROSS_DOMAIN_INSIGHT = "cross_domain_insight"   # Insight spans multiple domains

@dataclass
class ProactiveInsight:
    insight_id: str
    insight_type: InsightType
    source_agent: str
    target_agents: List[str]
    insight_data: Dict[str, Any]
    confidence_score: float  # 0.0 to 1.0
    urgency_level: UrgencyLevel
    created_at: datetime
    expires_at: Optional[datetime]
    context: Dict[str, Any]
    
    def is_expired(self) -> bool:
        return self.expires_at and datetime.now() > self.expires_at
    
    def is_relevant_to_agent(self, agent_name: str) -> bool:
        return agent_name in self.target_agents or "all" in self.target_agents

@dataclass
class CollaborationSuggestion:
    suggestion_id: str
    source_agent: str
    suggested_agents: List[str]
    collaboration_reason: CollaborationReason
    trigger_condition: str
    expected_outcome: str
    supporting_data: Dict[str, Any]
    confidence_score: float
    urgency_level: UrgencyLevel
    created_at: datetime
    user_context: Dict[str, Any]

@dataclass
class CollaborationSession:
    session_id: str
    participating_agents: List[str]
    session_topic: str
    session_goal: str
    shared_context: Dict[str, Any]
    insights_shared: List[ProactiveInsight]
    collaboration_results: Dict[str, Any]
    start_time: datetime
    end_time: Optional[datetime]
    status: str  # "active", "completed", "cancelled"

class ProactiveCollaborationEngine:
    """Central engine for managing proactive agent collaboration"""
    
    def __init__(self):
        self.active_insights: Dict[str, ProactiveInsight] = {}
        self.collaboration_suggestions: Dict[str, CollaborationSuggestion] = {}
        self.active_sessions: Dict[str, CollaborationSession] = {}
        self.agent_collaboration_patterns = self._load_collaboration_patterns()
        self.insight_sharing_rules = self._load_insight_sharing_rules()
    
    def _load_collaboration_patterns(self) -> Dict[str, Any]:
        """Load patterns that trigger agent collaboration"""
        return {
            "content_analysis": {
                "low_engagement": {
                    "suggested_agents": ["audience_insights", "seo_optimization"],
                    "reason": CollaborationReason.PROBLEM_SOLVING,
                    "trigger_threshold": 0.3  # Below 30% engagement
                },
                "viral_potential": {
                    "suggested_agents": ["competitive_analysis", "monetization"],
                    "reason": CollaborationReason.OPPORTUNITY_ENHANCEMENT,
                    "trigger_threshold": 0.8  # Above 80% viral score
                },
                "content_quality_issues": {
                    "suggested_agents": ["seo_optimization", "audience_insights"],
                    "reason": CollaborationReason.EXPERTISE_NEEDED,
                    "trigger_threshold": 0.4  # Below 40% quality score
                }
            },
            "audience_insights": {
                "demographic_shift": {
                    "suggested_agents": ["monetization", "content_analysis"],
                    "reason": CollaborationReason.DATA_CORRELATION,
                    "trigger_threshold": 0.2  # 20% demographic change
                },
                "engagement_anomaly": {
                    "suggested_agents": ["content_analysis", "competitive_analysis"],
                    "reason": CollaborationReason.VALIDATION_NEEDED,
                    "trigger_threshold": 0.3  # 30% engagement deviation
                },
                "new_audience_segment": {
                    "suggested_agents": ["monetization", "seo_optimization"],
                    "reason": CollaborationReason.OPPORTUNITY_ENHANCEMENT,
                    "trigger_threshold": 0.15  # 15% new audience
                }
            },
            "seo_optimization": {
                "keyword_opportunity": {
                    "suggested_agents": ["competitive_analysis", "content_analysis"],
                    "reason": CollaborationReason.OPPORTUNITY_ENHANCEMENT,
                    "trigger_threshold": 0.7  # High opportunity score
                },
                "search_visibility_drop": {
                    "suggested_agents": ["content_analysis", "competitive_analysis"],
                    "reason": CollaborationReason.PROBLEM_SOLVING,
                    "trigger_threshold": 0.3  # 30% visibility drop
                },
                "trending_keywords": {
                    "suggested_agents": ["content_analysis", "audience_insights"],
                    "reason": CollaborationReason.CROSS_DOMAIN_INSIGHT,
                    "trigger_threshold": 0.8  # High trending score
                }
            },
            "competitive_analysis": {
                "market_opportunity": {
                    "suggested_agents": ["content_analysis", "seo_optimization"],
                    "reason": CollaborationReason.OPPORTUNITY_ENHANCEMENT,
                    "trigger_threshold": 0.75  # High opportunity score
                },
                "competitor_threat": {
                    "suggested_agents": ["audience_insights", "monetization"],
                    "reason": CollaborationReason.PROBLEM_SOLVING,
                    "trigger_threshold": 0.6  # Significant threat level
                },
                "blue_ocean_market": {
                    "suggested_agents": ["content_analysis", "seo_optimization", "monetization"],
                    "reason": CollaborationReason.OPPORTUNITY_ENHANCEMENT,
                    "trigger_threshold": 0.9  # Very high opportunity
                }
            },
            "monetization": {
                "revenue_optimization": {
                    "suggested_agents": ["audience_insights", "competitive_analysis"],
                    "reason": CollaborationReason.EXPERTISE_NEEDED,
                    "trigger_threshold": 0.6  # Good optimization potential
                },
                "sponsorship_opportunity": {
                    "suggested_agents": ["content_analysis", "audience_insights"],
                    "reason": CollaborationReason.OPPORTUNITY_ENHANCEMENT,
                    "trigger_threshold": 0.8  # High sponsorship potential
                },
                "revenue_decline": {
                    "suggested_agents": ["audience_insights", "content_analysis"],
                    "reason": CollaborationReason.PROBLEM_SOLVING,
                    "trigger_threshold": 0.2  # 20% revenue decline
                }
            }
        }
    
    def _load_insight_sharing_rules(self) -> Dict[str, Any]:
        """Load rules for when agents should share insights with each other"""
        return {
            "content_analysis": {
                "shares_with": {
                    "seo_optimization": ["content_quality", "engagement_patterns", "hook_analysis"],
                    "audience_insights": ["engagement_data", "retention_patterns", "content_preferences"],
                    "competitive_analysis": ["performance_benchmarks", "content_gaps"],
                    "monetization": ["high_performing_content", "audience_engagement"]
                }
            },
            "audience_insights": {
                "shares_with": {
                    "content_analysis": ["audience_preferences", "demographic_data", "behavior_patterns"],
                    "seo_optimization": ["search_behavior", "keyword_preferences", "audience_intent"],
                    "competitive_analysis": ["audience_overlap", "demographic_comparisons"],
                    "monetization": ["purchasing_behavior", "engagement_value", "audience_segments"]
                }
            },
            "seo_optimization": {
                "shares_with": {
                    "content_analysis": ["keyword_performance", "search_trends", "optimization_opportunities"],
                    "audience_insights": ["search_intent", "keyword_demographics"],
                    "competitive_analysis": ["keyword_gaps", "search_competition"],
                    "monetization": ["high_value_keywords", "commercial_intent"]
                }
            },
            "competitive_analysis": {
                "shares_with": {
                    "content_analysis": ["competitor_strategies", "market_trends", "content_gaps"],
                    "audience_insights": ["competitor_audiences", "market_demographics"],
                    "seo_optimization": ["competitor_keywords", "search_strategies"],
                    "monetization": ["competitor_monetization", "market_opportunities"]
                }
            },
            "monetization": {
                "shares_with": {
                    "content_analysis": ["revenue_patterns", "monetization_performance"],
                    "audience_insights": ["valuable_segments", "purchasing_patterns"],
                    "seo_optimization": ["commercial_keywords", "revenue_opportunities"],
                    "competitive_analysis": ["monetization_strategies", "market_value"]
                }
            }
        }
    
    async def analyze_for_collaboration_opportunities(
        self, 
        agent_name: str, 
        analysis_results: Dict[str, Any], 
        user_context: Dict[str, Any]
    ) -> List[CollaborationSuggestion]:
        """Analyze agent results to identify collaboration opportunities"""
        
        suggestions = []
        
        if agent_name not in self.agent_collaboration_patterns:
            return suggestions
        
        patterns = self.agent_collaboration_patterns[agent_name]
        
        for pattern_name, pattern_config in patterns.items():
            # Check if this pattern is triggered
            if await self._is_pattern_triggered(pattern_name, analysis_results, pattern_config):
                suggestion = CollaborationSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    source_agent=agent_name,
                    suggested_agents=pattern_config["suggested_agents"],
                    collaboration_reason=pattern_config["reason"],
                    trigger_condition=pattern_name,
                    expected_outcome=self._generate_expected_outcome(pattern_name, pattern_config),
                    supporting_data=self._extract_supporting_data(pattern_name, analysis_results),
                    confidence_score=self._calculate_confidence_score(pattern_name, analysis_results),
                    urgency_level=self._determine_urgency_level(pattern_name, analysis_results),
                    created_at=datetime.now(),
                    user_context=user_context
                )
                
                suggestions.append(suggestion)
                self.collaboration_suggestions[suggestion.suggestion_id] = suggestion
                
                logger.info(f"🤝 {agent_name} suggests collaboration: {pattern_name} -> {pattern_config['suggested_agents']}")
        
        return suggestions
    
    async def generate_proactive_insights(
        self, 
        agent_name: str, 
        analysis_results: Dict[str, Any], 
        user_context: Dict[str, Any]
    ) -> List[ProactiveInsight]:
        """Generate insights that might be valuable to other agents"""
        
        insights = []
        
        if agent_name not in self.insight_sharing_rules:
            return insights
        
        sharing_rules = self.insight_sharing_rules[agent_name]["shares_with"]
        
        for target_agent, shared_data_types in sharing_rules.items():
            for data_type in shared_data_types:
                if data_type in analysis_results:
                    insight = ProactiveInsight(
                        insight_id=str(uuid.uuid4()),
                        insight_type=self._determine_insight_type(data_type, analysis_results[data_type]),
                        source_agent=agent_name,
                        target_agents=[target_agent],
                        insight_data={
                            "data_type": data_type,
                            "data": analysis_results[data_type],
                            "interpretation": self._generate_insight_interpretation(agent_name, data_type, analysis_results[data_type])
                        },
                        confidence_score=self._calculate_insight_confidence(data_type, analysis_results[data_type]),
                        urgency_level=self._determine_insight_urgency(data_type, analysis_results[data_type]),
                        created_at=datetime.now(),
                        expires_at=datetime.now() + timedelta(hours=24),  # Insights expire after 24 hours
                        context=user_context
                    )
                    
                    insights.append(insight)
                    self.active_insights[insight.insight_id] = insight
                    
                    logger.info(f"💡 {agent_name} shares insight with {target_agent}: {data_type}")
        
        return insights

    async def _is_pattern_triggered(self, pattern_name: str, analysis_results: Dict[str, Any], pattern_config: Dict[str, Any]) -> bool:
        """Check if a collaboration pattern is triggered by the analysis results"""

        threshold = pattern_config.get("trigger_threshold", 0.5)

        # Pattern-specific trigger logic
        if pattern_name == "low_engagement":
            engagement_score = analysis_results.get("engagement_score", 0.5)
            return engagement_score < threshold

        elif pattern_name == "viral_potential":
            viral_score = analysis_results.get("viral_potential_score", 0.0)
            return viral_score > threshold

        elif pattern_name == "content_quality_issues":
            quality_score = analysis_results.get("content_quality_score", 0.5)
            return quality_score < threshold

        elif pattern_name == "demographic_shift":
            demographic_change = analysis_results.get("demographic_change_percentage", 0.0)
            return demographic_change > threshold

        elif pattern_name == "engagement_anomaly":
            engagement_deviation = analysis_results.get("engagement_deviation", 0.0)
            return abs(engagement_deviation) > threshold

        elif pattern_name == "new_audience_segment":
            new_audience_percentage = analysis_results.get("new_audience_percentage", 0.0)
            return new_audience_percentage > threshold

        elif pattern_name == "keyword_opportunity":
            opportunity_score = analysis_results.get("keyword_opportunity_score", 0.0)
            return opportunity_score > threshold

        elif pattern_name == "search_visibility_drop":
            visibility_change = analysis_results.get("search_visibility_change", 0.0)
            return visibility_change < -threshold

        elif pattern_name == "trending_keywords":
            trending_score = analysis_results.get("trending_keywords_score", 0.0)
            return trending_score > threshold

        elif pattern_name == "market_opportunity":
            market_score = analysis_results.get("market_opportunity_score", 0.0)
            return market_score > threshold

        elif pattern_name == "competitor_threat":
            threat_level = analysis_results.get("competitor_threat_level", 0.0)
            return threat_level > threshold

        elif pattern_name == "blue_ocean_market":
            blue_ocean_score = analysis_results.get("blue_ocean_score", 0.0)
            return blue_ocean_score > threshold

        elif pattern_name == "revenue_optimization":
            optimization_potential = analysis_results.get("revenue_optimization_potential", 0.0)
            return optimization_potential > threshold

        elif pattern_name == "sponsorship_opportunity":
            sponsorship_score = analysis_results.get("sponsorship_opportunity_score", 0.0)
            return sponsorship_score > threshold

        elif pattern_name == "revenue_decline":
            revenue_change = analysis_results.get("revenue_change_percentage", 0.0)
            return revenue_change < -threshold

        return False

    def _generate_expected_outcome(self, pattern_name: str, pattern_config: Dict[str, Any]) -> str:
        """Generate expected outcome description for collaboration"""

        outcome_map = {
            "low_engagement": "Identify root causes of low engagement and develop improvement strategies",
            "viral_potential": "Maximize viral potential through competitive positioning and monetization",
            "content_quality_issues": "Improve content quality through SEO optimization and audience insights",
            "demographic_shift": "Adapt content and monetization strategies for new demographics",
            "engagement_anomaly": "Investigate engagement anomaly and validate findings",
            "new_audience_segment": "Develop strategies to engage and monetize new audience segment",
            "keyword_opportunity": "Develop content strategy to capitalize on keyword opportunities",
            "search_visibility_drop": "Diagnose and fix search visibility issues",
            "trending_keywords": "Create content strategy around trending keywords",
            "market_opportunity": "Develop comprehensive strategy to capture market opportunity",
            "competitor_threat": "Develop defensive strategies against competitive threats",
            "blue_ocean_market": "Create comprehensive strategy for blue ocean market entry",
            "revenue_optimization": "Optimize revenue through audience and competitive insights",
            "sponsorship_opportunity": "Develop sponsorship strategy based on content and audience analysis",
            "revenue_decline": "Diagnose revenue decline and develop recovery strategies"
        }

        return outcome_map.get(pattern_name, "Collaborate to enhance analysis and recommendations")

    def _extract_supporting_data(self, pattern_name: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant supporting data for collaboration suggestion"""

        supporting_data = {}

        # Extract pattern-specific supporting data
        if pattern_name == "low_engagement":
            supporting_data = {
                "engagement_score": analysis_results.get("engagement_score", 0),
                "retention_rate": analysis_results.get("retention_rate", 0),
                "click_through_rate": analysis_results.get("click_through_rate", 0)
            }
        elif pattern_name == "viral_potential":
            supporting_data = {
                "viral_score": analysis_results.get("viral_potential_score", 0),
                "share_rate": analysis_results.get("share_rate", 0),
                "engagement_velocity": analysis_results.get("engagement_velocity", 0)
            }
        elif pattern_name == "demographic_shift":
            supporting_data = {
                "demographic_change": analysis_results.get("demographic_change_percentage", 0),
                "new_demographics": analysis_results.get("new_demographics", {}),
                "audience_growth": analysis_results.get("audience_growth_rate", 0)
            }
        elif pattern_name == "keyword_opportunity":
            supporting_data = {
                "opportunity_score": analysis_results.get("keyword_opportunity_score", 0),
                "target_keywords": analysis_results.get("high_opportunity_keywords", []),
                "search_volume": analysis_results.get("total_search_volume", 0)
            }
        elif pattern_name == "market_opportunity":
            supporting_data = {
                "market_score": analysis_results.get("market_opportunity_score", 0),
                "market_size": analysis_results.get("addressable_market_size", 0),
                "competition_level": analysis_results.get("competition_level", 0)
            }

        return supporting_data

    def _calculate_confidence_score(self, pattern_name: str, analysis_results: Dict[str, Any]) -> float:
        """Calculate confidence score for collaboration suggestion"""

        # Base confidence on data quality and pattern strength
        data_quality = analysis_results.get("data_quality_score", 0.5)
        pattern_strength = analysis_results.get(f"{pattern_name}_strength", 0.5)

        # Combine factors
        confidence = (data_quality * 0.4) + (pattern_strength * 0.6)

        return min(max(confidence, 0.0), 1.0)

    def _determine_urgency_level(self, pattern_name: str, analysis_results: Dict[str, Any]) -> UrgencyLevel:
        """Determine urgency level for collaboration suggestion"""

        urgent_patterns = ["revenue_decline", "competitor_threat", "search_visibility_drop"]
        high_patterns = ["viral_potential", "blue_ocean_market", "sponsorship_opportunity"]
        medium_patterns = ["demographic_shift", "engagement_anomaly", "market_opportunity"]

        if pattern_name in urgent_patterns:
            return UrgencyLevel.CRITICAL
        elif pattern_name in high_patterns:
            return UrgencyLevel.HIGH
        elif pattern_name in medium_patterns:
            return UrgencyLevel.MEDIUM
        else:
            return UrgencyLevel.LOW

    def _determine_insight_type(self, data_type: str, data: Any) -> InsightType:
        """Determine the type of insight based on data type and content"""

        if "opportunity" in data_type.lower():
            return InsightType.OPPORTUNITY
        elif "warning" in data_type.lower() or "decline" in data_type.lower():
            return InsightType.WARNING
        elif "correlation" in data_type.lower() or "pattern" in data_type.lower():
            return InsightType.CORRELATION
        elif "enhancement" in data_type.lower() or "optimization" in data_type.lower():
            return InsightType.ENHANCEMENT
        else:
            return InsightType.SUGGESTION

    def _generate_insight_interpretation(self, source_agent: str, data_type: str, data: Any) -> str:
        """Generate human-readable interpretation of the insight"""

        interpretations = {
            "content_analysis": {
                "engagement_patterns": f"Content engagement shows specific patterns that could inform strategy",
                "retention_patterns": f"Viewer retention data reveals optimization opportunities",
                "content_quality": f"Content quality metrics indicate areas for improvement"
            },
            "audience_insights": {
                "demographic_data": f"Audience demographics provide targeting opportunities",
                "behavior_patterns": f"Audience behavior patterns suggest content preferences",
                "engagement_value": f"Audience engagement value indicates monetization potential"
            },
            "seo_optimization": {
                "keyword_performance": f"Keyword performance data shows optimization opportunities",
                "search_trends": f"Search trend analysis reveals content opportunities",
                "optimization_opportunities": f"SEO optimization opportunities identified"
            },
            "competitive_analysis": {
                "competitor_strategies": f"Competitor strategy analysis reveals market positioning opportunities",
                "market_trends": f"Market trend analysis shows strategic directions",
                "content_gaps": f"Content gap analysis identifies untapped opportunities"
            },
            "monetization": {
                "revenue_patterns": f"Revenue pattern analysis shows optimization opportunities",
                "monetization_performance": f"Monetization performance indicates strategy effectiveness",
                "valuable_segments": f"High-value audience segments identified for targeting"
            }
        }

        agent_interpretations = interpretations.get(source_agent, {})
        return agent_interpretations.get(data_type, f"{source_agent} identified relevant {data_type} data")

    def _calculate_insight_confidence(self, data_type: str, data: Any) -> float:
        """Calculate confidence score for an insight"""

        # Base confidence on data completeness and relevance
        if isinstance(data, dict):
            completeness = len([v for v in data.values() if v is not None]) / max(len(data), 1)
        elif isinstance(data, list):
            completeness = min(len(data) / 10, 1.0)  # Assume 10 items is "complete"
        else:
            completeness = 1.0 if data is not None else 0.0

        # Adjust based on data type importance
        importance_weights = {
            "engagement_patterns": 0.9,
            "demographic_data": 0.8,
            "keyword_performance": 0.85,
            "competitor_strategies": 0.8,
            "revenue_patterns": 0.9
        }

        importance = importance_weights.get(data_type, 0.7)

        return min(completeness * importance, 1.0)

    def _determine_insight_urgency(self, data_type: str, data: Any) -> UrgencyLevel:
        """Determine urgency level for an insight"""

        urgent_data_types = ["revenue_decline", "competitor_threat", "engagement_drop"]
        high_data_types = ["viral_potential", "market_opportunity", "trending_keywords"]
        medium_data_types = ["demographic_shift", "keyword_opportunity", "content_gaps"]

        if any(urgent in data_type.lower() for urgent in urgent_data_types):
            return UrgencyLevel.CRITICAL
        elif any(high in data_type.lower() for high in high_data_types):
            return UrgencyLevel.HIGH
        elif any(medium in data_type.lower() for medium in medium_data_types):
            return UrgencyLevel.MEDIUM
        else:
            return UrgencyLevel.LOW

    async def create_collaboration_session(
        self,
        participating_agents: List[str],
        session_topic: str,
        session_goal: str,
        shared_context: Dict[str, Any]
    ) -> CollaborationSession:
        """Create a new real-time collaboration session"""

        session = CollaborationSession(
            session_id=str(uuid.uuid4()),
            participating_agents=participating_agents,
            session_topic=session_topic,
            session_goal=session_goal,
            shared_context=shared_context,
            insights_shared=[],
            collaboration_results={},
            start_time=datetime.now(),
            end_time=None,
            status="active"
        )

        self.active_sessions[session.session_id] = session

        logger.info(f"🤝 Created collaboration session: {session.session_id} with agents: {participating_agents}")

        return session

    async def add_insight_to_session(self, session_id: str, insight: ProactiveInsight) -> bool:
        """Add an insight to an active collaboration session"""

        if session_id not in self.active_sessions:
            return False

        session = self.active_sessions[session_id]
        session.insights_shared.append(insight)

        logger.info(f"💡 Added insight to session {session_id}: {insight.insight_type.value}")

        return True

    async def complete_collaboration_session(self, session_id: str, results: Dict[str, Any]) -> bool:
        """Complete a collaboration session with results"""

        if session_id not in self.active_sessions:
            return False

        session = self.active_sessions[session_id]
        session.collaboration_results = results
        session.end_time = datetime.now()
        session.status = "completed"

        logger.info(f"✅ Completed collaboration session: {session_id}")

        return True

    async def get_relevant_insights_for_agent(self, agent_name: str, context: Dict[str, Any]) -> List[ProactiveInsight]:
        """Get insights that are relevant to a specific agent"""

        relevant_insights = []

        for insight in self.active_insights.values():
            if not insight.is_expired() and insight.is_relevant_to_agent(agent_name):
                # Check if insight is contextually relevant
                if self._is_insight_contextually_relevant(insight, context):
                    relevant_insights.append(insight)

        # Sort by urgency and confidence
        relevant_insights.sort(
            key=lambda x: (x.urgency_level.value, x.confidence_score),
            reverse=True
        )

        return relevant_insights

    def _is_insight_contextually_relevant(self, insight: ProactiveInsight, context: Dict[str, Any]) -> bool:
        """Check if an insight is contextually relevant to the current situation"""

        # Check if the insight context matches current context
        insight_context = insight.context

        # Match user context
        if insight_context.get("user_id") != context.get("user_id"):
            return False

        # Check temporal relevance (insights are more relevant if recent)
        age_hours = (datetime.now() - insight.created_at).total_seconds() / 3600
        if age_hours > 24:  # Insights older than 24 hours are less relevant
            return False

        # Check content relevance
        if "content_type" in insight_context and "content_type" in context:
            if insight_context["content_type"] != context["content_type"]:
                return False

        return True

    async def cleanup_expired_insights(self) -> int:
        """Clean up expired insights and return count of removed insights"""

        expired_insights = [
            insight_id for insight_id, insight in self.active_insights.items()
            if insight.is_expired()
        ]

        for insight_id in expired_insights:
            del self.active_insights[insight_id]

        if expired_insights:
            logger.info(f"🧹 Cleaned up {len(expired_insights)} expired insights")

        return len(expired_insights)

    def get_collaboration_statistics(self) -> Dict[str, Any]:
        """Get statistics about collaboration activity"""

        total_insights = len(self.active_insights)
        total_suggestions = len(self.collaboration_suggestions)
        active_sessions = len([s for s in self.active_sessions.values() if s.status == "active"])

        # Agent activity statistics
        agent_activity = {}
        for insight in self.active_insights.values():
            agent = insight.source_agent
            if agent not in agent_activity:
                agent_activity[agent] = {"insights_shared": 0, "avg_confidence": 0.0}
            agent_activity[agent]["insights_shared"] += 1
            agent_activity[agent]["avg_confidence"] += insight.confidence_score

        # Calculate averages
        for agent, stats in agent_activity.items():
            if stats["insights_shared"] > 0:
                stats["avg_confidence"] /= stats["insights_shared"]

        return {
            "total_active_insights": total_insights,
            "total_collaboration_suggestions": total_suggestions,
            "active_collaboration_sessions": active_sessions,
            "agent_activity": agent_activity,
            "most_active_agent": max(agent_activity.keys(), key=lambda x: agent_activity[x]["insights_shared"]) if agent_activity else None
        }

# Global proactive collaboration engine instance
proactive_collaboration_engine = ProactiveCollaborationEngine()

async def analyze_for_collaboration_opportunities(
    agent_name: str,
    analysis_results: Dict[str, Any],
    user_context: Dict[str, Any]
) -> List[CollaborationSuggestion]:
    """Analyze agent results for collaboration opportunities"""
    return await proactive_collaboration_engine.analyze_for_collaboration_opportunities(
        agent_name, analysis_results, user_context
    )

async def generate_proactive_insights(
    agent_name: str,
    analysis_results: Dict[str, Any],
    user_context: Dict[str, Any]
) -> List[ProactiveInsight]:
    """Generate proactive insights for sharing with other agents"""
    return await proactive_collaboration_engine.generate_proactive_insights(
        agent_name, analysis_results, user_context
    )

async def get_relevant_insights_for_agent(agent_name: str, context: Dict[str, Any]) -> List[ProactiveInsight]:
    """Get insights relevant to a specific agent"""
    return await proactive_collaboration_engine.get_relevant_insights_for_agent(agent_name, context)

async def create_collaboration_session(
    participating_agents: List[str],
    session_topic: str,
    session_goal: str,
    shared_context: Dict[str, Any]
) -> CollaborationSession:
    """Create a new collaboration session"""
    return await proactive_collaboration_engine.create_collaboration_session(
        participating_agents, session_topic, session_goal, shared_context
    )

def get_collaboration_statistics() -> Dict[str, Any]:
    """Get collaboration statistics"""
    return proactive_collaboration_engine.get_collaboration_statistics()
