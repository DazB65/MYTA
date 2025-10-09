"""
Personalized Response Generator for MYTA
Creates user-specific, data-driven responses based on channel analysis
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from .channel_analyzer import get_channel_analyzer, ChannelProfile
from .agent_personalities import get_agent_personality
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.AGENT)

class PersonalizedResponseGenerator:
    """Generates personalized responses based on user's channel data"""
    
    def __init__(self):
        self.channel_analyzer = get_channel_analyzer()
    
    async def generate_personalized_prompt(
        self, 
        user_message: str, 
        agent_id: str, 
        user_id: str,
        conversation_context: List[Dict] = None
    ) -> str:
        """Generate a personalized system prompt with user's channel data"""
        
        try:
            # Get user's channel profile
            profile = await self.channel_analyzer.get_channel_profile(user_id)
            
            # Get agent personality
            agent = get_agent_personality(agent_id)
            
            # Build personalized prompt
            personalized_prompt = self._build_personalized_prompt(
                agent, profile, user_message, conversation_context, agent_id
            )

            # Enhance with YouTube knowledge
            from .knowledge_integration import get_knowledge_integration
            knowledge_integration = get_knowledge_integration()

            enhanced_prompt = knowledge_integration.enhance_prompt_with_knowledge(
                personalized_prompt, agent_id, profile, user_message
            )

            # Apply dynamic response adaptations
            from .dynamic_response_engine import get_dynamic_response_engine, ResponseContext
            from .context_analyzer import get_context_analyzer

            try:
                # Analyze conversation context
                context_analyzer = get_context_analyzer()
                conversation_context = context_analyzer.analyze_conversation_context(
                    user_message, conversation_context or []
                )

                # Create response context
                response_context = ResponseContext(
                    user_id=user_id,
                    agent_id=agent_id,
                    user_message=user_message,
                    conversation_history=conversation_context or [],
                    channel_profile=profile,
                    current_goals=profile.goals,
                    recent_performance=profile.recent_performance,
                    seasonal_factors={},
                    urgency_level="medium",
                    response_style_preference="standard"
                )

                # Generate dynamic adaptations
                dynamic_engine = get_dynamic_response_engine()
                dynamic_response = await dynamic_engine.generate_dynamic_response(response_context)

                # Enhance prompt with dynamic adaptations
                if dynamic_response.context_adaptations:
                    adaptation_section = "\\n\\n## DYNAMIC ADAPTATIONS:\\n"
                    for adaptation in dynamic_response.context_adaptations[:3]:
                        adaptation_section += f"- {adaptation}\\n"

                    enhanced_prompt += adaptation_section

                # Add suggested actions if available
                if dynamic_response.suggested_actions:
                    actions_section = "\\n\\n## SUGGESTED ACTIONS:\\n"
                    for action in dynamic_response.suggested_actions[:3]:
                        actions_section += f"- {action}\\n"

                    enhanced_prompt += actions_section

            except Exception as e:
                logger.error(f"Error applying dynamic adaptations: {e}")
                # Continue with enhanced prompt without dynamic adaptations

            return enhanced_prompt
        
        except Exception as e:
            logger.error(f"Error generating personalized prompt: {e}")
            # Fallback to basic agent prompt
            agent = get_agent_personality(agent_id)
            return agent["system_prompt"]
    
    def _build_personalized_prompt(
        self,
        agent: Dict,
        profile: ChannelProfile,
        user_message: str,
        conversation_context: List[Dict] = None,
        agent_id: str = "1"
    ) -> str:
        """Build a comprehensive personalized prompt"""
        
        # Start with base agent personality
        prompt = f"You are {agent['name']}, a {agent['role']} for MYTA. {agent['system_prompt']}\n\n"
        
        # Add user's channel context
        prompt += "## USER'S CHANNEL CONTEXT:\n"
        prompt += f"Channel: {profile.channel_name} ({profile.niche} niche)\n"
        prompt += f"Size: {profile.channel_size_tier.title()} creator ({profile.metrics.subscriber_count:,} subscribers)\n"
        prompt += f"Performance: {profile.metrics.total_views:,} total views across {profile.metrics.video_count} videos\n"
        
        if profile.metrics.avg_views_per_video > 0:
            prompt += f"Average views per video: {profile.metrics.avg_views_per_video:,.0f}\n"
        
        # Add specific metrics based on agent type
        try:
            if agent_id == "1":  # Alex - Analytics
                prompt += self._add_analytics_context(profile)
            elif agent_id == "2":  # Levi - Content
                prompt += self._add_content_context(profile)
            elif agent_id == "3":  # Maya - Engagement
                prompt += self._add_engagement_context(profile)
            elif agent_id == "4":  # Zara - Growth
                prompt += self._add_growth_context(profile)
            elif agent_id == "5":  # Kai - Technical
                prompt += self._add_technical_context(profile)
        except Exception as e:
            logger.error(f"Error adding agent-specific context: {e}")
            # Continue without agent-specific context
        
        # Add current challenges and opportunities
        if profile.challenges:
            prompt += f"\n## CURRENT CHALLENGES:\n"
            for challenge in profile.challenges[:3]:  # Top 3 challenges
                prompt += f"- {challenge}\n"
        
        if profile.opportunities:
            prompt += f"\n## OPPORTUNITIES:\n"
            for opportunity in profile.opportunities[:3]:  # Top 3 opportunities
                prompt += f"- {opportunity}\n"
        
        # Add user goals
        if profile.goals:
            prompt += f"\n## USER'S GOALS:\n"
            for goal in profile.goals[:3]:  # Top 3 goals
                prompt += f"- {goal.get('title', 'Goal')}: {goal.get('description', '')}\n"
        
        # Add conversation context if available
        if conversation_context:
            recent_topics = self._extract_recent_topics(conversation_context)
            if recent_topics:
                prompt += f"\n## RECENT CONVERSATION TOPICS:\n{', '.join(recent_topics)}\n"
        
        # Add specific instructions for personalized responses
        prompt += f"\n## RESPONSE INSTRUCTIONS:\n"
        prompt += f"- Provide specific, actionable advice based on {profile.channel_name}'s actual data\n"
        prompt += f"- Reference their {profile.channel_size_tier} creator status and {profile.niche} niche\n"
        prompt += f"- Address their specific challenges and leverage their opportunities\n"
        prompt += f"- Use concrete numbers and metrics when relevant\n"
        prompt += f"- Avoid generic advice - make it personal to their situation\n"
        prompt += f"- Consider their goals: {', '.join([g.get('title', '') for g in profile.goals[:2]])}\n"
        
        return prompt
    
    def _add_analytics_context(self, profile: ChannelProfile) -> str:
        """Add analytics-specific context for Alex"""
        context = f"\n## ANALYTICS DATA:\n"
        context += f"CTR: {profile.metrics.avg_ctr:.1%} (industry avg: 4-6%)\n"
        context += f"Retention: {profile.metrics.avg_retention:.1%} (target: 50%+)\n"
        context += f"Engagement Rate: {profile.metrics.engagement_rate:.1%}\n"
        
        if profile.recent_performance:
            trend = profile.recent_performance.get("trend", "stable")
            context += f"Recent trend: {trend}\n"
            
            if "best_performing_video" in profile.recent_performance:
                best_video = profile.recent_performance["best_performing_video"]
                context += f"Best recent video: {best_video.get('views', 0):,} views, {best_video.get('ctr', 0):.1%} CTR\n"
        
        return context
    
    def _add_content_context(self, profile: ChannelProfile) -> str:
        """Add content-specific context for Levi"""
        context = f"\n## CONTENT STRATEGY:\n"
        
        if profile.content_strategy:
            context += f"Upload schedule: {profile.content_strategy.get('upload_schedule', 'irregular')}\n"
            context += f"Content types: {', '.join(profile.content_strategy.get('content_types', []))}\n"
            context += f"Average length: {profile.content_strategy.get('average_video_length', 'unknown')}\n"
            
            gaps = profile.content_strategy.get('content_gaps', [])
            if gaps:
                context += f"Content gaps to address: {', '.join(gaps)}\n"
        
        if profile.metrics.top_performing_topics:
            context += f"Top performing topics: {', '.join(profile.metrics.top_performing_topics[:3])}\n"
        
        return context
    
    def _add_engagement_context(self, profile: ChannelProfile) -> str:
        """Add engagement-specific context for Maya"""
        context = f"\n## ENGAGEMENT DATA:\n"
        context += f"Engagement rate: {profile.metrics.engagement_rate:.1%}\n"
        
        if profile.metrics.audience_demographics:
            demo = profile.metrics.audience_demographics
            context += f"Primary audience: {demo.get('age_range', 'unknown')} age group\n"
            context += f"Top countries: {', '.join(demo.get('top_countries', [])[:3])}\n"
        
        if profile.recent_performance:
            areas = profile.recent_performance.get('areas_for_improvement', [])
            if 'engagement' in str(areas).lower():
                context += f"Recent engagement challenges identified\n"
        
        return context
    
    def _add_growth_context(self, profile: ChannelProfile) -> str:
        """Add growth-specific context for Zara"""
        context = f"\n## GROWTH METRICS:\n"
        context += f"Channel size tier: {profile.channel_size_tier} ({profile.metrics.subscriber_count:,} subs)\n"
        context += f"Upload frequency: {profile.metrics.upload_frequency:.1f} videos/week\n"
        
        if profile.recent_performance:
            growth_rate = profile.recent_performance.get('recent_growth_rate', 0)
            context += f"Recent growth rate: {growth_rate:.1%} monthly\n"
            
            trend = profile.recent_performance.get('trend', 'stable')
            context += f"Growth trend: {trend}\n"
        
        # Add size-specific growth strategies
        if profile.channel_size_tier == "micro":
            context += f"Focus: Building initial subscriber base and establishing authority\n"
        elif profile.channel_size_tier == "small":
            context += f"Focus: Breaking through small creator plateau and scaling\n"
        elif profile.channel_size_tier == "medium":
            context += f"Focus: Optimizing for algorithm and expanding reach\n"
        
        return context
    
    def _add_technical_context(self, profile: ChannelProfile) -> str:
        """Add technical-specific context for Kai"""
        context = f"\n## TECHNICAL METRICS:\n"
        context += f"Video count: {profile.metrics.video_count}\n"
        context += f"Average views per video: {profile.metrics.avg_views_per_video:,.0f}\n"
        
        if profile.content_strategy:
            consistency = profile.content_strategy.get('consistency_score', 0)
            context += f"Upload consistency: {consistency:.1%}\n"
        
        # Add technical optimization opportunities
        if profile.metrics.avg_ctr < 0.04:
            context += f"Technical priority: Thumbnail and title optimization\n"
        if profile.metrics.avg_retention < 0.40:
            context += f"Technical priority: Video structure and pacing optimization\n"
        
        return context
    
    def _extract_recent_topics(self, conversation_context: List[Dict]) -> List[str]:
        """Extract recent conversation topics"""
        topics = []
        
        try:
            # Simple keyword extraction from recent messages
            keywords = [
                "analytics", "subscribers", "views", "engagement", "retention",
                "thumbnails", "titles", "content", "upload", "algorithm",
                "monetization", "growth", "SEO", "tags", "description"
            ]
            
            recent_messages = conversation_context[-5:]  # Last 5 messages
            
            for message in recent_messages:
                content = message.get("content", "").lower()
                for keyword in keywords:
                    if keyword in content and keyword not in topics:
                        topics.append(keyword)
            
            return topics[:5]  # Return top 5 topics
        
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            return []
    
    async def get_response_suggestions(self, profile: ChannelProfile, agent_id: str) -> List[str]:
        """Get suggested responses/questions based on channel data and available tools"""

        suggestions = []

        try:
            agent = get_agent_personality(agent_id)

            # Get agent tools for enhanced suggestions
            from .agent_tools import get_agent_tools
            agent_tools = get_agent_tools()
            available_tools = agent_tools.get_available_tools(agent_id)

            if agent_id == "1":  # Alex - Analytics
                if profile.metrics.avg_ctr < 0.04:
                    suggestions.append("Run performance analysis to improve my click-through rate")
                if profile.metrics.avg_retention < 0.40:
                    suggestions.append("Analyze my audience retention patterns")
                suggestions.append("Compare my metrics against industry benchmarks")
                suggestions.append("Forecast my channel's growth potential")

            elif agent_id == "2":  # Levi - Content
                if profile.metrics.top_performing_topics:
                    suggestions.append(f"Analyze my content performance for optimization opportunities")
                suggestions.append("Optimize my video titles for better performance")
                suggestions.append("Evaluate my thumbnail design strategy")
                suggestions.append("Help me spot trending content opportunities")

            elif agent_id == "3":  # Maya - Engagement
                if profile.metrics.engagement_rate < 0.02:
                    suggestions.append("Analyze my engagement patterns and suggest improvements")
                suggestions.append("Assess my community health and growth strategies")
                suggestions.append("Optimize my audience retention techniques")
                suggestions.append("Develop a comment interaction strategy")

            elif agent_id == "4":  # Zara - Growth
                suggestions.append(f"Create a growth strategy for my {profile.channel_size_tier} channel")
                suggestions.append("Optimize my content for the YouTube algorithm")
                suggestions.append("Develop a scaling plan for my content production")
                suggestions.append("Analyze my monetization opportunities")

            elif agent_id == "5":  # Kai - Technical
                suggestions.append("Optimize my SEO and search discoverability")
                suggestions.append("Analyze and improve my video metadata")
                suggestions.append("Perform a technical audit of my channel")
                suggestions.append("Optimize my content creation workflow")

            # Add tool-specific suggestions
            if "performance_analyzer" in available_tools and profile.metrics.avg_ctr < 0.05:
                suggestions.insert(0, "Run a comprehensive performance analysis")

            if "growth_forecaster" in available_tools and profile.channel_size_tier == "micro":
                suggestions.append("Forecast when I'll reach key milestones")

            return suggestions[:4]  # Return top 4 suggestions

        except Exception as e:
            logger.error(f"Error getting response suggestions: {e}")
            return []

    async def get_tool_enhanced_suggestions(self, profile: ChannelProfile, agent_id: str, user_message: str) -> Dict[str, Any]:
        """Get tool-enhanced suggestions based on user message"""

        try:
            from .agent_tools import get_agent_tools
            agent_tools = get_agent_tools()

            # Suggest best tool for the message
            suggested_tool = agent_tools.suggest_best_tool(agent_id, user_message, profile)

            # Get tool description and benefits
            tool_benefits = {
                "performance_analyzer": "Get detailed insights into your channel's performance metrics",
                "benchmark_comparator": "See how you compare to other creators in your tier",
                "growth_forecaster": "Predict your growth timeline and milestones",
                "content_analyzer": "Discover what makes your content perform well",
                "title_optimizer": "Optimize your titles for maximum click-through",
                "thumbnail_evaluator": "Improve your thumbnail design for better CTR",
                "engagement_analyzer": "Understand your audience engagement patterns",
                "growth_strategy": "Get a comprehensive growth plan",
                "seo_optimizer": "Improve your search visibility and discoverability"
            }

            return {
                "suggested_tool": suggested_tool,
                "tool_benefit": tool_benefits.get(suggested_tool, "Get specialized analysis"),
                "why_suggested": f"Based on your question about '{user_message[:50]}...', this tool will provide the most relevant insights",
                "available_tools": agent_tools.get_available_tools(agent_id)
            }

        except Exception as e:
            logger.error(f"Error getting tool-enhanced suggestions: {e}")
            return {}

# Global generator instance
_response_generator: Optional[PersonalizedResponseGenerator] = None

def get_response_generator() -> PersonalizedResponseGenerator:
    """Get or create global response generator instance"""
    global _response_generator
    if _response_generator is None:
        _response_generator = PersonalizedResponseGenerator()
    return _response_generator
