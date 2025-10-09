"""
Knowledge Integration Service for MYTA
Integrates YouTube knowledge base with personalized responses
"""

from typing import Dict, List, Any, Optional
from .youtube_knowledge import get_youtube_knowledge
from .channel_analyzer import ChannelProfile
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.AGENT)

class KnowledgeIntegration:
    """Integrates YouTube knowledge with user-specific data"""
    
    def __init__(self):
        self.youtube_knowledge = get_youtube_knowledge()
    
    def enhance_prompt_with_knowledge(
        self, 
        base_prompt: str, 
        agent_id: str, 
        profile: ChannelProfile,
        user_message: str
    ) -> str:
        """Enhance prompt with relevant YouTube knowledge"""
        
        try:
            # Get agent-specific knowledge
            agent_knowledge = self.youtube_knowledge.get_knowledge_for_agent(agent_id)
            
            # Identify relevant topics from user message
            relevant_topics = self._identify_topics(user_message)
            
            # Build knowledge section
            knowledge_section = self._build_knowledge_section(
                agent_id, agent_knowledge, relevant_topics, profile
            )
            
            # Insert knowledge before response instructions
            enhanced_prompt = base_prompt.replace(
                "## RESPONSE INSTRUCTIONS:",
                f"{knowledge_section}\n\n## RESPONSE INSTRUCTIONS:"
            )
            
            return enhanced_prompt
        
        except Exception as e:
            logger.error(f"Error enhancing prompt with knowledge: {e}")
            return base_prompt
    
    def _identify_topics(self, user_message: str) -> List[str]:
        """Identify relevant YouTube topics from user message"""
        
        message_lower = user_message.lower()
        
        topic_keywords = {
            "thumbnails": ["thumbnail", "thumb", "image", "visual", "click"],
            "titles": ["title", "headline", "name", "call"],
            "analytics": ["analytics", "views", "ctr", "retention", "performance", "metrics"],
            "algorithm": ["algorithm", "reach", "discovery", "recommended", "suggested"],
            "seo": ["seo", "search", "keywords", "tags", "ranking", "optimize"],
            "monetization": ["money", "revenue", "monetize", "ads", "sponsor", "income"],
            "engagement": ["engagement", "comments", "likes", "community", "audience"],
            "content": ["content", "video", "create", "ideas", "topics"],
            "growth": ["growth", "grow", "scale", "subscribers", "increase"],
            "retention": ["retention", "watch time", "drop off", "boring", "keep watching"]
        }
        
        identified_topics = []
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                identified_topics.append(topic)
        
        return identified_topics[:3]  # Return top 3 most relevant topics
    
    def _build_knowledge_section(
        self, 
        agent_id: str, 
        agent_knowledge: Dict, 
        topics: List[str], 
        profile: ChannelProfile
    ) -> str:
        """Build knowledge section for prompt"""
        
        knowledge_section = "## YOUTUBE EXPERTISE:\n"
        
        # Add agent specialties
        if "specialties" in agent_knowledge:
            knowledge_section += f"Your specialties: {', '.join(agent_knowledge['specialties'])}\n\n"
        
        # Add topic-specific knowledge
        for topic in topics:
            topic_guidance = self.youtube_knowledge.get_topic_guidance(
                topic, profile.channel_size_tier
            )
            
            if topic_guidance:
                knowledge_section += f"### {topic.title()} Best Practices:\n"
                knowledge_section += self._format_topic_guidance(topic, topic_guidance)
                knowledge_section += "\n"
        
        # Add channel-size specific insights
        knowledge_section += self._get_size_specific_insights(profile.channel_size_tier)
        
        # Add performance benchmarks relevant to user's metrics
        knowledge_section += self._get_relevant_benchmarks(profile)
        
        return knowledge_section
    
    def _format_topic_guidance(self, topic: str, guidance: Dict) -> str:
        """Format topic guidance for prompt"""
        
        formatted = ""
        
        if topic == "thumbnails":
            if "design_principles" in guidance:
                formatted += f"Design principles: {', '.join(guidance['design_principles'][:3])}\n"
            if "technical_specs" in guidance:
                specs = guidance["technical_specs"]
                formatted += f"Technical specs: {specs.get('resolution', '')}, {specs.get('aspect_ratio', '')}\n"
        
        elif topic == "titles":
            if "best_practices" in guidance:
                formatted += f"Best practices: {', '.join(guidance['best_practices'][:3])}\n"
            if "title_formulas" in guidance:
                formatted += f"Proven formulas: {', '.join(guidance['title_formulas'][:2])}\n"
        
        elif topic == "analytics":
            if "performance_benchmarks" in guidance:
                benchmarks = guidance["performance_benchmarks"]
                formatted += f"CTR benchmarks: {benchmarks.get('click_through_rate', {})}\n"
                formatted += f"Retention benchmarks: {benchmarks.get('audience_retention', {})}\n"
        
        elif topic == "algorithm":
            if "ranking_factors" in guidance:
                factors = guidance["ranking_factors"]
                formatted += f"Primary factors: {', '.join(factors.get('primary', [])[:3])}\n"
            if "optimization_tips" in guidance:
                tips = guidance["optimization_tips"]
                formatted += f"Key insights: {tips.get('first_24_hours', '')}, {tips.get('retention_targets', '')}\n"
        
        elif topic == "seo":
            if "keyword_research" in guidance:
                formatted += f"SEO tactics: {', '.join(guidance['keyword_research'][:3])}\n"
            if "tag_optimization" in guidance:
                formatted += f"Tag strategy: {', '.join(guidance['tag_optimization'][:3])}\n"
        
        elif topic == "monetization":
            if "youtube_partner_program" in guidance:
                ypp = guidance["youtube_partner_program"]
                req = ypp.get("requirements", {})
                formatted += f"YPP requirements: {req.get('subscribers', 0)} subs, {req.get('watch_hours', 0)} hours\n"
            if "optimization_tips" in guidance and "sponsorship_rates" in guidance["optimization_tips"]:
                rates = guidance["optimization_tips"]["sponsorship_rates"]
                formatted += f"Sponsorship rates: {rates}\n"
        
        # Add size-specific tips if available
        if "size_specific_tips" in guidance:
            formatted += f"For {guidance.get('channel_size', 'your')} creators: {', '.join(guidance['size_specific_tips'][:2])}\n"
        
        return formatted
    
    def _get_size_specific_insights(self, channel_size: str) -> str:
        """Get insights specific to channel size"""
        
        insights = f"### {channel_size.title()} Creator Insights:\n"
        
        if channel_size == "micro":
            insights += "- Focus on consistency over perfection\n"
            insights += "- Engage with every comment to build community\n"
            insights += "- Use trending hashtags strategically\n"
            insights += "- Collaborate with similar-sized creators\n"
        
        elif channel_size == "small":
            insights += "- Develop your signature content style\n"
            insights += "- Start building an email list\n"
            insights += "- Consider live streaming for engagement\n"
            insights += "- Begin reaching out for brand partnerships\n"
        
        elif channel_size == "medium":
            insights += "- Optimize heavily for algorithm performance\n"
            insights += "- Expand reach through cross-platform content\n"
            insights += "- Build strategic brand partnerships\n"
            insights += "- Consider hiring help for production\n"
        
        elif channel_size == "large":
            insights += "- Scale content production systematically\n"
            insights += "- Diversify revenue streams\n"
            insights += "- Expand to multiple platforms\n"
            insights += "- Build a team and delegate effectively\n"
        
        return insights + "\n"
    
    def _get_relevant_benchmarks(self, profile: ChannelProfile) -> str:
        """Get benchmarks relevant to user's current performance"""
        
        benchmarks = "### Performance Context:\n"
        
        # CTR analysis
        ctr = profile.metrics.avg_ctr
        if ctr < 0.04:
            benchmarks += f"Your CTR ({ctr:.1%}) is below average (4-6%) - focus on thumbnail/title optimization\n"
        elif ctr > 0.06:
            benchmarks += f"Your CTR ({ctr:.1%}) is above average - leverage this strength for growth\n"
        
        # Retention analysis
        retention = profile.metrics.avg_retention
        if retention < 0.40:
            benchmarks += f"Your retention ({retention:.1%}) needs improvement - target 50%+ for good performance\n"
        elif retention > 0.50:
            benchmarks += f"Your retention ({retention:.1%}) is good - use this for longer content\n"
        
        # Engagement analysis
        engagement = profile.metrics.engagement_rate
        if engagement < 0.02:
            benchmarks += f"Your engagement ({engagement:.1%}) is low - encourage more interaction\n"
        elif engagement > 0.04:
            benchmarks += f"Your engagement ({engagement:.1%}) is strong - build on this community connection\n"
        
        return benchmarks + "\n"
    
    def get_topic_specific_advice(
        self, 
        topic: str, 
        profile: ChannelProfile, 
        agent_id: str
    ) -> Dict[str, Any]:
        """Get specific advice for a topic based on user's channel"""
        
        try:
            # Get base topic guidance
            guidance = self.youtube_knowledge.get_topic_guidance(topic, profile.channel_size_tier)
            
            # Add user-specific context
            user_context = self._analyze_user_context_for_topic(topic, profile)
            
            # Get agent-specific perspective
            agent_perspective = self._get_agent_perspective(topic, agent_id)
            
            return {
                "topic": topic,
                "general_guidance": guidance,
                "user_specific_context": user_context,
                "agent_perspective": agent_perspective,
                "action_items": self._generate_action_items(topic, profile, guidance)
            }
        
        except Exception as e:
            logger.error(f"Error getting topic-specific advice: {e}")
            return {"topic": topic, "error": str(e)}
    
    def _analyze_user_context_for_topic(self, topic: str, profile: ChannelProfile) -> Dict[str, Any]:
        """Analyze user's specific context for a topic"""
        
        context = {}
        
        if topic == "analytics":
            context = {
                "current_ctr": profile.metrics.avg_ctr,
                "current_retention": profile.metrics.avg_retention,
                "current_engagement": profile.metrics.engagement_rate,
                "performance_vs_benchmarks": {
                    "ctr_status": "good" if profile.metrics.avg_ctr >= 0.06 else "needs_improvement",
                    "retention_status": "good" if profile.metrics.avg_retention >= 0.50 else "needs_improvement",
                    "engagement_status": "good" if profile.metrics.engagement_rate >= 0.04 else "needs_improvement"
                }
            }
        
        elif topic == "growth":
            context = {
                "current_size": profile.channel_size_tier,
                "subscriber_count": profile.metrics.subscriber_count,
                "growth_stage": self._determine_growth_stage(profile),
                "primary_challenges": profile.challenges[:2],
                "top_opportunities": profile.opportunities[:2]
            }
        
        elif topic == "monetization":
            context = {
                "ypp_eligible": profile.metrics.subscriber_count >= 1000,
                "estimated_revenue_potential": self._estimate_revenue_potential(profile),
                "monetization_readiness": self._assess_monetization_readiness(profile)
            }
        
        return context
    
    def _get_agent_perspective(self, topic: str, agent_id: str) -> str:
        """Get agent-specific perspective on a topic"""
        
        perspectives = {
            "1": {  # Alex - Analytics
                "analytics": "Focus on data interpretation and performance optimization",
                "growth": "Analyze growth metrics and identify performance bottlenecks",
                "monetization": "Calculate ROI and revenue optimization strategies"
            },
            "2": {  # Levi - Content
                "content": "Creative approaches to content ideation and production",
                "thumbnails": "Design principles and creative optimization",
                "titles": "Creative title formulas and emotional triggers"
            },
            "4": {  # Zara - Growth
                "growth": "Systematic scaling strategies and algorithm optimization",
                "algorithm": "Strategic algorithm insights and growth hacking",
                "monetization": "Revenue scaling and partnership development"
            },
            "5": {  # Kai - Technical
                "seo": "Technical SEO optimization and keyword strategies",
                "algorithm": "Technical algorithm mechanics and optimization",
                "analytics": "Technical setup and advanced tracking"
            }
        }
        
        agent_perspectives = perspectives.get(agent_id, {})
        return agent_perspectives.get(topic, f"Specialized {topic} guidance from agent perspective")
    
    def _generate_action_items(self, topic: str, profile: ChannelProfile, guidance: Dict) -> List[str]:
        """Generate specific action items based on topic and user context"""
        
        action_items = []
        
        if topic == "thumbnails" and profile.metrics.avg_ctr < 0.04:
            action_items = [
                "A/B test 3 different thumbnail styles this week",
                "Analyze top 5 competitors' thumbnail strategies",
                "Create templates for consistent branding"
            ]
        
        elif topic == "retention" and profile.metrics.avg_retention < 0.40:
            action_items = [
                "Analyze drop-off points in recent videos",
                "Create stronger hooks for next 3 videos",
                "Implement pattern interrupts every 60 seconds"
            ]
        
        elif topic == "growth" and profile.channel_size_tier == "micro":
            action_items = [
                "Establish consistent weekly upload schedule",
                "Engage with 10 comments daily",
                "Research and use 3 trending hashtags per video"
            ]
        
        return action_items
    
    def _determine_growth_stage(self, profile: ChannelProfile) -> str:
        """Determine what growth stage the channel is in"""
        
        if profile.metrics.subscriber_count < 100:
            return "foundation_building"
        elif profile.metrics.subscriber_count < 1000:
            return "initial_growth"
        elif profile.metrics.subscriber_count < 10000:
            return "scaling_up"
        elif profile.metrics.subscriber_count < 100000:
            return "optimization_phase"
        else:
            return "mature_scaling"
    
    def _estimate_revenue_potential(self, profile: ChannelProfile) -> Dict[str, Any]:
        """Estimate revenue potential based on channel metrics"""
        
        monthly_views = profile.metrics.avg_views_per_video * 4  # Assuming weekly uploads
        
        return {
            "ad_revenue_estimate": monthly_views * 0.001,  # $1 per 1000 views rough estimate
            "sponsorship_potential": monthly_views * 0.01 if profile.metrics.subscriber_count > 1000 else 0,
            "ypp_eligible": profile.metrics.subscriber_count >= 1000
        }
    
    def _assess_monetization_readiness(self, profile: ChannelProfile) -> str:
        """Assess how ready the channel is for monetization"""
        
        if profile.metrics.subscriber_count >= 1000 and profile.metrics.avg_retention > 0.40:
            return "ready"
        elif profile.metrics.subscriber_count >= 500:
            return "almost_ready"
        else:
            return "focus_on_growth"

# Global knowledge integration instance
_knowledge_integration: Optional[KnowledgeIntegration] = None

def get_knowledge_integration() -> KnowledgeIntegration:
    """Get or create global knowledge integration instance"""
    global _knowledge_integration
    if _knowledge_integration is None:
        _knowledge_integration = KnowledgeIntegration()
    return _knowledge_integration
