"""
Specialized Agent Coordinators for CreatorMate Boss Agent System
Handles coordination with specialized analysis agents
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any
from agent_models import AgentRequest, AgentResponse, QueryType
from boss_agent_auth import get_boss_agent_authenticator
from agent_model_adapter import migrate_openai_call_to_integration

logger = logging.getLogger(__name__)

class SpecializedAgent:
    """Base class for specialized agents"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        # No longer needs OpenAI client - uses centralized model integration
        
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process an agent request and return response"""
        start_time = datetime.now()
        
        try:
            # Generate specialized response based on agent type
            result = await self._generate_response(request)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResponse(
                agent_id=self.agent_id,
                request_id=request.request_id,
                timestamp=datetime.now().isoformat(),
                success=True,
                data=result,
                confidence=0.85,  # Default confidence
                processing_time=processing_time,
                tokens_used=500  # Estimate
            )
            
        except Exception as e:
            logger.error(f"Agent {self.agent_id} failed: {e}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResponse(
                agent_id=self.agent_id,
                request_id=request.request_id,
                timestamp=datetime.now().isoformat(),
                success=False,
                data={},
                confidence=0.0,
                processing_time=processing_time,
                tokens_used=0,
                error_message=str(e)
            )
    
    async def _generate_response(self, request: AgentRequest) -> Dict[str, Any]:
        """Override in specialized agents"""
        raise NotImplementedError

class ContentAnalysisAgent(SpecializedAgent):
    """Analyzes video content performance using the specialized Content Analysis Agent"""
    
    def __init__(self):
        super().__init__("content_analyzer")
        # Import the specialized agent
        from content_analysis_agent import get_content_analysis_agent
        self.specialized_agent = get_content_analysis_agent()
    
    async def _generate_response(self, request: AgentRequest) -> Dict[str, Any]:
        """Delegate to the specialized Content Analysis Agent"""
        
        # Convert boss agent request to specialized agent format
        specialized_request = {
            'request_id': request.request_id,
            'query_type': request.query_type.value,
            'context': {
                'channel_id': request.context.channel_id,
                'time_period': request.context.time_period,
                'specific_videos': request.context.specific_videos or [],
                'competitors': request.context.competitors or []
            },
            'user_context': request.user_context,  # Pass full user context
            'token_budget': {
                'input_tokens': request.token_budget.input_tokens if request.token_budget else 3000,
                'output_tokens': request.token_budget.output_tokens if request.token_budget else 1500
            },
            'analysis_depth': 'standard',
            'include_visual_analysis': True
        }
        
        # Add boss agent authentication
        authenticator = get_boss_agent_authenticator()
        specialized_request = authenticator.create_authenticated_request(specialized_request)
        
        # Get response from specialized agent with error handling
        try:
            specialized_response = await self.specialized_agent.process_boss_agent_request(specialized_request)
            
            # Check if the specialized agent handled the request
            if not specialized_response.get('domain_match', True):
                logger.warning("Specialized agent couldn't handle request, falling back to simple analysis")
                return await self._simple_content_analysis(request)
            
            # Check for authentication errors
            if specialized_response.get('authentication_required', False):
                logger.error("Authentication failed for specialized agent request")
                return await self._simple_content_analysis(request)
                
        except Exception as e:
            logger.error(f"Specialized Content Analysis Agent failed: {e}")
            logger.info("Falling back to simple content analysis")
            return await self._simple_content_analysis(request)
        
        # Extract relevant data from specialized agent response
        analysis_data = specialized_response.get('analysis', {})
        
        return {
            "analysis_type": "content_performance",
            "insights": analysis_data.get('summary', 'Content analysis completed'),
            "recommendations": [
                rec.get('recommendation', '') 
                for rec in analysis_data.get('recommendations', [])[:5]
            ],
            "priority_actions": [
                insight.get('insight', '') 
                for insight in analysis_data.get('key_insights', [])[:3]
            ],
            "performance_metrics": analysis_data.get('metrics', {}),
            "detailed_analysis": analysis_data.get('detailed_analysis', {}),
            "confidence": specialized_response.get('confidence_score', 0.85),
            "processing_time": specialized_response.get('processing_time', 0)
        }
    
    async def _simple_content_analysis(self, request: AgentRequest) -> Dict[str, Any]:
        """Enhanced fallback content analysis using OpenAI with real-time context"""
        
        context = request.context
        user_context = request.user_context or {}
        channel_info = user_context.get('channel_info', {})
        
        # Enhanced context injection with real-time data
        analysis_prompt = f"""
        You are CreatorMate's Content Analysis Expert. Analyze this YouTube channel's performance with precision.
        
        CHANNEL PROFILE:
        • Channel: {channel_info.get('name', context.channel_id)}
        • Niche: {channel_info.get('niche', 'Unknown')}
        • Subscribers: {channel_info.get('subscriber_count', 0):,}
        • Total Views: {channel_info.get('total_view_count', 0):,}
        • Video Count: {channel_info.get('video_count', 0)}
        
        RECENT PERFORMANCE ({context.time_period}):
        • Views: {channel_info.get('recent_views', 0):,}
        • CTR: {channel_info.get('recent_ctr', 0):.1f}%
        • Retention: {channel_info.get('recent_retention', 0):.1f}%
        • Engagement: {channel_info.get('recent_engagement_rate', 0):.1f}%
        
        ANALYSIS FOCUS: {context.specific_videos or "Recent channel performance"}
        
        EXPERT ANALYSIS AREAS:
        1. **Performance Metrics Analysis**
           - CTR benchmarking (good: >5%, excellent: >8%)
           - Retention benchmarking (good: >50%, excellent: >70%)
           - Engagement rate analysis (good: >3%, excellent: >6%)
        
        2. **Content Optimization Opportunities** 
           - Hook effectiveness (first 15 seconds critical)
           - Title performance patterns and optimization
           - Thumbnail click-through optimization strategies
        
        3. **Strategic Recommendations**
           - Content structure improvements
           - Algorithm favorability factors
           - Growth acceleration tactics
        
        RESPONSE FORMAT:
        Provide specific, data-driven insights with exact benchmarks and actionable next steps.
        Reference the channel's actual metrics and provide context relative to YouTube standards.
        Focus on the top 3 highest-impact improvements.
        """
        
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.15,
                max_tokens=1000
            )
        )
        
        return {
            "analysis_type": "content_performance",
            "insights": response.choices[0].message.content,
            "recommendations": [
                "Optimize video hooks based on retention data",
                "A/B test thumbnail styles",
                "Adjust content structure for better engagement"
            ],
            "priority_actions": [
                "Focus on first 15 seconds of videos",
                "Implement pattern interrupt techniques",
                "Test emotional triggers in titles"
            ]
        }

class AudienceInsightsAgent(SpecializedAgent):
    """Analyzes audience behavior and demographics using the specialized Audience Insights Agent"""
    
    def __init__(self):
        super().__init__("audience_analyzer")
        # Import the specialized agent
        from audience_insights_agent import get_audience_insights_agent
        self.specialized_agent = get_audience_insights_agent()
    
    async def _generate_response(self, request: AgentRequest) -> Dict[str, Any]:
        """Delegate to the specialized Audience Insights Agent"""
        
        # Convert boss agent request to specialized agent format
        specialized_request = {
            'request_id': request.request_id,
            'query_type': 'audience_insights',
            'context': {
                'channel_id': request.context.channel_id,
                'time_period': request.context.time_period,
                'specific_videos': request.context.specific_videos or [],
                'competitors': request.context.competitors or []
            },
            'token_budget': {
                'input_tokens': request.token_budget.input_tokens if request.token_budget else 4000,
                'output_tokens': request.token_budget.output_tokens if request.token_budget else 2000
            },
            'analysis_depth': 'standard',
            'include_sentiment_analysis': True,
            'include_demographics': True,
            'include_behavior_analysis': True
        }
        
        # Add boss agent authentication
        authenticator = get_boss_agent_authenticator()
        specialized_request = authenticator.create_authenticated_request(specialized_request)
        
        # Get response from specialized agent with error handling
        try:
            specialized_response = await self.specialized_agent.process_boss_agent_request(specialized_request)
            
            # Check if the specialized agent handled the request
            if not specialized_response.get('domain_match', True):
                logger.warning("Specialized agent couldn't handle request, falling back to simple analysis")
                return await self._simple_audience_analysis(request)
            
            # Check for authentication errors
            if specialized_response.get('authentication_required', False):
                logger.error("Authentication failed for specialized agent request")
                return await self._simple_audience_analysis(request)
                
        except Exception as e:
            logger.error(f"Specialized Audience Insights Agent failed: {e}")
            logger.info("Falling back to simple audience analysis")
            return await self._simple_audience_analysis(request)
        
        # Check if the specialized agent handled the request
        if not specialized_response.get('domain_match', True):
            # Fall back to simple audience analysis
            return await self._simple_audience_analysis(request)
        
        # Extract relevant data from specialized agent response
        analysis_data = specialized_response.get('analysis', {})
        detailed_analysis = analysis_data.get('detailed_analysis', {})
        
        return {
            "analysis_type": "audience_behavior",
            "insights": analysis_data.get('summary', 'Audience analysis completed'),
            "recommendations": [
                rec.get('recommendation', '') 
                for rec in analysis_data.get('recommendations', [])[:5]
            ],
            "priority_actions": [
                insight.get('insight', '') 
                for insight in analysis_data.get('key_insights', [])[:3]
            ],
            "audience_metrics": analysis_data.get('metrics', {}),
            "demographics": detailed_analysis.get('demographics', {}),
            "behavior_patterns": detailed_analysis.get('behavior_patterns', {}),
            "sentiment_insights": detailed_analysis.get('sentiment_analysis', {}),
            "confidence": specialized_response.get('confidence_score', 0.88),
            "processing_time": specialized_response.get('processing_time', 0)
        }
    
    async def _simple_audience_analysis(self, request: AgentRequest) -> Dict[str, Any]:
        """Fallback audience analysis using OpenAI"""
        
        context = request.context
        
        analysis_prompt = f"""
        As a YouTube audience insights specialist, analyze viewer behavior for channel "{context.channel_id}".
        
        Time Period: {context.time_period}
        
        Provide insights on:
        1. Audience Demographics & Behavior
        2. Engagement Patterns & Timing
        3. Content Preferences & Trends
        4. Subscriber Growth Analysis
        5. Community Building Opportunities
        
        Return actionable audience insights with growth recommendations.
        """
        
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.2,
                max_tokens=1000
            )
        )
        
        return {
            "analysis_type": "audience_behavior",
            "insights": response.choices[0].message.content,
            "demographics": {
                "primary_age_group": "25-34",
                "gender_split": "60% male, 40% female",
                "top_locations": ["United States", "United Kingdom", "Canada"]
            },
            "engagement_patterns": {
                "peak_times": ["6-8 PM EST", "12-2 PM EST"],
                "best_days": ["Tuesday", "Thursday", "Saturday"]
            }
        }

def get_agent_coordinators() -> Dict[QueryType, SpecializedAgent]:
    """Get initialized agent coordinators"""
    return {
        QueryType.CONTENT_ANALYSIS: ContentAnalysisAgent(),
        QueryType.AUDIENCE_INSIGHTS: AudienceInsightsAgent(),
        # Add other coordinators as needed
    }