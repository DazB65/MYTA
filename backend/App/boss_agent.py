"""
Boss Agent Orchestration System for Vidalytics
Coordinates multiple specialized agents for YouTube analytics
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import os
from backend import get_agent_cache
from backend import migrate_openai_call_to_integration
from enhanced_user_context import get_enhanced_context_manager
from realtime_data_pipeline import get_data_pipeline
from boss_agent_auth import get_boss_agent_authenticator
from data_access_monitor import get_data_access_monitor
# Use centralized model integration
from model_integrations import create_agent_call_to_integration

# Configure advanced logging
from logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.AGENT)

class QueryType(Enum):
    CONTENT_ANALYSIS = "content_analysis"  # Including viral potential and hook analysis
    AUDIENCE_INSIGHTS = "audience"  # Including collaboration potential and community health
    SEO_OPTIMIZATION = "seo"  # Including algorithm favorability prediction
    COMPETITIVE_ANALYSIS = "competition"
    MONETIZATION = "monetization"
    GENERAL = "general"

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5

@dataclass
class TimeRange:
    start_date: Optional[str] = None
    end_date: Optional[str] = None

@dataclass
class Context:
    channel_id: str
    time_period: str = "last_30d"
    custom_range: Optional[TimeRange] = None
    specific_videos: List[str] = None
    competitors: List[str] = None

@dataclass
class CachedData:
    cache_key: str
    cache_ttl: int = 3600
    data_freshness: str = None

@dataclass
class TokenBudget:
    input_tokens: int = 3000
    output_tokens: int = 1500

@dataclass
class AgentRequest:
    request_id: str
    timestamp: str
    query_type: QueryType
    priority: Priority
    context: Context
    cached_data: Optional[CachedData] = None
    token_budget: TokenBudget = None
    user_context: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        return {
            "request_id": self.request_id,
            "timestamp": self.timestamp,
            "query_type": self.query_type.value,
            "priority": self.priority.value,
            "context": asdict(self.context),
            "cached_data": asdict(self.cached_data) if self.cached_data else None,
            "token_budget": asdict(self.token_budget) if self.token_budget else None
        }

@dataclass
class AgentResponse:
    agent_id: str
    request_id: str
    timestamp: str
    success: bool
    data: Dict[str, Any]
    confidence: float
    processing_time: float
    tokens_used: int
    error_message: Optional[str] = None

class IntentClassifier:
    """Classifies user messages into query intents"""
    
    def __init__(self):
        # No longer needs OpenAI client - uses centralized model integration
        pass
        
    async def classify_intent(self, message: str, context: Dict) -> Tuple[QueryType, Dict]:
        """
        Classify user message intent and extract parameters
        
        Args:
            message: User's message
            context: Channel context and user data
            
        Returns:
            Tuple of (QueryType, extracted parameters)
        """
        
        channel_info = context.get('channel_info', {})
        classification_prompt = f"""
        You are Vidalytics's AI intent classifier. Analyze this YouTube creator's message with precision and extract actionable parameters.
        
        CREATOR MESSAGE: "{message}"
        
        CHANNEL CONTEXT:
        - Channel: {channel_info.get('name', 'Unknown')}
        - Niche: {channel_info.get('niche', 'Unknown')} 
        - Subscribers: {channel_info.get('subscriber_count', 0):,}
        - Total Views: {channel_info.get('total_view_count', 0):,}
        - Recent Performance: {channel_info.get('recent_views', 0):,} views (last 7d)
        
        INTENT CLASSIFICATION:
        Classify into the MOST SPECIFIC category:
        
        1. **content_analysis** - Video performance, analytics, metrics, rankings
           • Triggers: "best video", "top performing", "most views", "analytics", "performance", "total views", "video count", "CTR", "retention"
           • Examples: "what's my best video?", "total views?", "which content performs best?"
        
        2. **audience** - Demographics, behavior, engagement, subscriber insights  
           • Triggers: "audience", "subscribers", "demographics", "engagement", "comments", "who watches"
           • Examples: "who is my audience?", "how many subscribers?", "engagement rate?"
        
        3. **seo** - Search optimization, keywords, discoverability, algorithm
           • Triggers: "SEO", "keywords", "search", "ranking", "discoverability", "algorithm"
           • Examples: "optimize my titles", "keyword research", "search rankings"
        
        4. **competition** - Competitor analysis, benchmarking, market research
           • Triggers: "competitors", "compare", "benchmark", "similar channels", "market"
           • Examples: "analyze competitors", "how do I compare?", "market positioning"
        
        5. **monetization** - Revenue, sponsorships, monetization strategies
           • Triggers: "revenue", "money", "monetize", "sponsorship", "ads", "earnings"
           • Examples: "how to monetize?", "revenue optimization", "sponsorship rates"
        
        6. **general** - Greetings, unclear requests, or out-of-scope questions
           • Triggers: "hello", "help", unclear or non-YouTube related content
        
        PARAMETER EXTRACTION:
        Extract specific, actionable parameters:
        - time_period: "last_7d", "last_30d", "last_90d", or "all_time"
        - specific_videos: Exact video titles or IDs mentioned
        - competitors: Specific channel names mentioned
        - metrics: Specific metrics requested (views, CTR, retention, engagement, revenue)
        - focus_areas: Specific aspects to analyze
        
        RESPONSE FORMAT:
        {{
            "intent": "most_specific_category",
            "confidence": 0.85-1.0,
            "parameters": {{
                "time_period": "extracted_or_default_last_30d",
                "specific_videos": ["exact_titles_mentioned"],
                "competitors": ["exact_channel_names"],
                "metrics": ["specific_metrics_requested"],
                "focus_areas": ["specific_analysis_areas"]
            }},
            "reasoning": "Specific trigger words and context that led to this classification"
        }}
        """
        
        try:
            # Use model integration system for better model selection and fallbacks
            messages = [{"role": "user", "content": classification_prompt}]
            raw_content = await migrate_openai_call_to_integration(
                "boss_agent", messages, "quick"
            )
            logger.info(f"GPT-4o classification response: {raw_content}")
            
            # Try to extract JSON from the response
            if "```json" in raw_content:
                # Extract JSON from code block
                import re
                json_match = re.search(r'```json\s*(.*?)\s*```', raw_content, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1)
                else:
                    json_content = raw_content
            else:
                json_content = raw_content
            
            result = json.loads(json_content)
            intent = QueryType(result["intent"])
            
            return intent, result["parameters"]
            
        except json.JSONDecodeError as e:
            logger.error(f"Intent classification JSON parse failed: {e}")
            logger.error(f"Raw response: {raw_content}")
            # Fall back to manual parsing for content analysis
            if any(keyword in message.lower() for keyword in ["best video", "top video", "performing", "views", "analytics"]):
                return QueryType.CONTENT_ANALYSIS, {"time_period": "last_30d"}
            return QueryType.GENERAL, {}
        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            return QueryType.GENERAL, {}

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
        You are Vidalytics's Content Analysis Expert. Analyze this YouTube channel's performance with precision.
        
        {self._get_voice_guidelines()}
        
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
        from backend.App.audience_insights_agent import get_audience_insights_agent
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

class SEOOptimizationAgent(SpecializedAgent):
    """Handles SEO and discoverability optimization using the specialized SEO & Discoverability Agent"""
    
    def __init__(self):
        super().__init__("seo_optimizer")
        # Import the specialized agent
        from seo_discoverability_agent import get_seo_discoverability_agent
        self.specialized_agent = get_seo_discoverability_agent()
    
    async def _generate_response(self, request: AgentRequest) -> Dict[str, Any]:
        """Delegate to the specialized SEO & Discoverability Agent"""
        
        # Convert boss agent request to specialized agent format
        specialized_request = {
            'request_id': request.request_id,
            'query_type': 'seo_discoverability',
            'context': {
                'channel_id': request.context.channel_id,
                'time_period': request.context.time_period,
                'specific_videos': request.context.specific_videos or [],
                'competitors': request.context.competitors or []
            },
            'token_budget': {
                'input_tokens': request.token_budget.input_tokens if request.token_budget else 3000,
                'output_tokens': request.token_budget.output_tokens if request.token_budget else 1500
            },
            'analysis_depth': 'standard',
            'include_keyword_analysis': True,
            'include_competitor_keywords': True,
            'include_optimization_suggestions': True
        }
        
        # Add boss agent authentication
        authenticator = get_boss_agent_authenticator()
        specialized_request = authenticator.create_authenticated_request(specialized_request)
        
        # Get response from specialized agent
        specialized_response = await self.specialized_agent.process_boss_agent_request(specialized_request)
        
        # Check if the specialized agent handled the request
        if not specialized_response.get('domain_match', True):
            # Fall back to simple SEO analysis
            return await self._simple_seo_analysis(request)
        
        # Extract relevant data from specialized agent response
        analysis_data = specialized_response.get('analysis', {})
        
        return {
            "analysis_type": "seo_optimization",
            "insights": analysis_data.get('summary', 'SEO analysis completed'),
            "recommendations": [
                rec.get('recommendation', '') 
                for rec in analysis_data.get('recommendations', [])[:5]
            ],
            "keyword_opportunities": [
                insight.get('insight', '') 
                for insight in analysis_data.get('key_insights', [])[:3]
            ],
            "optimization_priorities": [
                rec.get('recommendation', '') 
                for rec in analysis_data.get('recommendations', [])[1:4]
            ],
            "seo_metrics": analysis_data.get('metrics', {}),
            "detailed_analysis": analysis_data.get('detailed_analysis', {}),
            "confidence": specialized_response.get('confidence_score', 0.85),
            "processing_time": specialized_response.get('processing_time', 0)
        }
    
    async def _simple_seo_analysis(self, request: AgentRequest) -> Dict[str, Any]:
        """Fallback SEO analysis using OpenAI"""
        
        context = request.context
        
        seo_prompt = f"""
        As a YouTube SEO specialist, optimize discoverability for channel "{context.channel_id}".
        
        Time Period: {context.time_period}
        Target Videos: {context.specific_videos or "Recent uploads"}
        
        Analyze and optimize:
        1. Keyword Research & Implementation
        2. Title Optimization Strategies
        3. Description & Tag Optimization
        4. Search Ranking Improvements
        5. Algorithm Favorability Factors
        
        Provide specific SEO recommendations and keyword strategies.
        """
        
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": seo_prompt}],
                temperature=0.2,
                max_tokens=1000
            )
        )
        
        return {
            "analysis_type": "seo_optimization",
            "insights": response.choices[0].message.content,
            "keyword_opportunities": [
                "Long-tail keywords with high search volume",
                "Trending topics in niche",
                "Competitor keyword gaps"
            ],
            "optimization_priorities": [
                "Update video descriptions",
                "Implement keyword clusters",
                "Optimize channel tags"
            ]
        }

class CompetitiveAnalysisAgent(SpecializedAgent):
    """Analyzes competitor performance and market positioning using the specialized Competitive Analysis Agent"""
    
    def __init__(self):
        super().__init__("competitor_analyzer")
        # Import the specialized agent
        from competitive_analysis_agent import get_competitive_analysis_agent
        self.specialized_agent = get_competitive_analysis_agent()
    
    async def _generate_response(self, request: AgentRequest) -> Dict[str, Any]:
        """Delegate to the specialized Competitive Analysis Agent"""
        
        # Convert boss agent request to specialized agent format
        specialized_request = {
            'request_id': request.request_id,
            'query_type': 'competitive_analysis',
            'context': {
                'channel_id': request.context.channel_id,
                'time_period': request.context.time_period,
                'specific_videos': request.context.specific_videos or [],
                'competitor_channels': request.context.competitors or []
            },
            'token_budget': {
                'input_tokens': request.token_budget.input_tokens if request.token_budget else 5000,
                'output_tokens': request.token_budget.output_tokens if request.token_budget else 2500
            },
            'analysis_depth': 'standard',
            'include_content_strategy': True,
            'include_performance_benchmarking': True,
            'include_trend_analysis': True
        }
        
        # Add boss agent authentication
        authenticator = get_boss_agent_authenticator()
        specialized_request = authenticator.create_authenticated_request(specialized_request)
        
        # Get response from specialized agent
        specialized_response = await self.specialized_agent.process_boss_agent_request(specialized_request)
        
        # Check if the specialized agent handled the request
        if not specialized_response.get('domain_match', True):
            # Fall back to simple competitive analysis
            return await self._simple_competitive_analysis(request)
        
        # Extract relevant data from specialized agent response
        analysis_data = specialized_response.get('analysis', {})
        
        return {
            "analysis_type": "competitive_analysis",
            "insights": analysis_data.get('summary', 'Competitive analysis completed'),
            "recommendations": [
                rec.get('recommendation', '') 
                for rec in analysis_data.get('recommendations', [])[:5]
            ],
            "competitive_advantages": [
                insight.get('insight', '') 
                for insight in analysis_data.get('key_insights', [])[:3]
            ],
            "improvement_opportunities": [
                rec.get('recommendation', '') 
                for rec in analysis_data.get('recommendations', [])[1:4]
            ],
            "competitive_metrics": analysis_data.get('metrics', {}),
            "detailed_analysis": analysis_data.get('detailed_analysis', {}),
            "confidence": specialized_response.get('confidence_score', 0.88),
            "processing_time": specialized_response.get('processing_time', 0)
        }
    
    async def _simple_competitive_analysis(self, request: AgentRequest) -> Dict[str, Any]:
        """Fallback competitive analysis using OpenAI"""
        
        context = request.context
        
        competitive_prompt = f"""
        As a competitive analysis expert, analyze market positioning for channel "{context.channel_id}".
        
        Competitor Channels: {context.competitors or "Top channels in niche"}
        Analysis Period: {context.time_period}
        
        Provide analysis on:
        1. Competitive Landscape Overview
        2. Content Strategy Comparison
        3. Performance Benchmarking
        4. Market Opportunity Gaps
        5. Differentiation Strategies
        
        Focus on actionable competitive insights and positioning recommendations.
        """
        
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": competitive_prompt}],
                temperature=0.2,
                max_tokens=1000
            )
        )
        
        return {
            "analysis_type": "competitive_analysis",
            "insights": response.choices[0].message.content,
            "competitive_advantages": [
                "Unique content angles",
                "Better engagement rates",
                "Stronger community building"
            ],
            "improvement_opportunities": [
                "Content format diversification",
                "Upload frequency optimization",
                "Collaboration opportunities"
            ]
        }

class MonetizationAgent(SpecializedAgent):
    """Analyzes monetization opportunities and revenue optimization using the specialized Monetization Strategy Agent"""
    
    def __init__(self):
        super().__init__("monetization_optimizer")
        # Import the specialized agent
        from monetization_strategy_agent import get_monetization_strategy_agent
        self.specialized_agent = get_monetization_strategy_agent()
    
    async def _generate_response(self, request: AgentRequest) -> Dict[str, Any]:
        """Delegate to the specialized Monetization Strategy Agent"""
        
        # Convert boss agent request to specialized agent format
        specialized_request = {
            'request_id': request.request_id,
            'query_type': 'monetization_strategy',
            'context': {
                'channel_id': request.context.channel_id,
                'time_period': request.context.time_period,
                'specific_videos': request.context.specific_videos or [],
                'competitors': request.context.competitors or []
            },
            'token_budget': {
                'input_tokens': request.token_budget.input_tokens if request.token_budget else 3500,
                'output_tokens': request.token_budget.output_tokens if request.token_budget else 1750
            },
            'analysis_depth': 'standard',
            'include_revenue_analysis': True,
            'include_sponsorship_opportunities': True,
            'include_alternative_streams': True,
            'include_optimization_suggestions': True
        }
        
        # Add boss agent authentication
        authenticator = get_boss_agent_authenticator()
        specialized_request = authenticator.create_authenticated_request(specialized_request)
        
        # Get response from specialized agent
        specialized_response = await self.specialized_agent.process_boss_agent_request(specialized_request)
        
        # Check if the specialized agent handled the request
        if not specialized_response.get('domain_match', True):
            # Fall back to simple monetization analysis
            return await self._simple_monetization_analysis(request)
        
        # Extract relevant data from specialized agent response
        analysis_data = specialized_response.get('analysis', {})
        
        return {
            "analysis_type": "monetization_optimization",
            "insights": analysis_data.get('summary', 'Monetization analysis completed'),
            "recommendations": [
                rec.get('recommendation', '') 
                for rec in analysis_data.get('recommendations', [])[:5]
            ],
            "revenue_opportunities": [
                insight.get('insight', '') 
                for insight in analysis_data.get('key_insights', [])[:3]
            ],
            "optimization_strategies": [
                rec.get('recommendation', '') 
                for rec in analysis_data.get('recommendations', [])[1:4]
            ],
            "monetization_metrics": analysis_data.get('metrics', {}),
            "detailed_analysis": analysis_data.get('detailed_analysis', {}),
            "confidence": specialized_response.get('confidence_score', 0.86),
            "processing_time": specialized_response.get('processing_time', 0)
        }
    
    async def _simple_monetization_analysis(self, request: AgentRequest) -> Dict[str, Any]:
        """Fallback monetization analysis using OpenAI"""
        
        context = request.context
        
        monetization_prompt = f"""
        As a YouTube monetization specialist, optimize revenue for channel "{context.channel_id}".
        
        Analysis Period: {context.time_period}
        
        Analyze:
        1. Current Revenue Streams Performance
        2. Monetization Opportunity Assessment
        3. Sponsorship & Brand Deal Potential
        4. Product/Service Integration Options
        5. Long-term Revenue Strategy
        
        Provide specific monetization recommendations and revenue optimization strategies.
        """
        
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": monetization_prompt}],
                temperature=0.2,
                max_tokens=1000
            )
        )
        
        return {
            "analysis_type": "monetization_optimization",
            "insights": response.choices[0].message.content,
            "revenue_opportunities": [
                "Sponsored content integration",
                "Product placement optimization",
                "Affiliate marketing expansion"
            ],
            "optimization_strategies": [
                "Improve ad placement timing",
                "Diversify revenue streams",
                "Build premium content offerings"
            ]
        }

class VoiceAnalyzer:
    """Analyzes and matches content voice and style"""

    def __init__(self):
        # No longer needs OpenAI client - uses centralized model integration
        pass

    async def analyze_channel_voice(self, channel_content: List[Dict], channel_context: Dict) -> Dict[str, Any]:
        """Analyze channel's voice and writing style"""
        try:
            # Prepare content for analysis
            titles = [content.get('title', '') for content in channel_content]
            descriptions = [content.get('description', '') for content in channel_content]
            transcripts = [content.get('transcript', '') for content in channel_content if content.get('transcript')]

            # Voice analysis prompt
            analysis_prompt = f"""
            Analyze this YouTube channel's voice and writing style based on their content.

            Channel Context:
            - Niche: {channel_context.get('niche', 'Unknown')}
            - Style: {channel_context.get('content_type', 'Unknown')}
            - Personality: {channel_context.get('personality', 'Professional')}

            Content Examples:
            Titles: {json.dumps(titles[:5], indent=2)}
            Descriptions: {json.dumps(descriptions[:5], indent=2)}
            Transcript Samples: {json.dumps(transcripts[:2], indent=2) if transcripts else 'No transcripts available'}

            Analyze:
            1. Tone and Voice Characteristics
            2. Writing Style Patterns
            3. Vocabulary and Language Level
            4. Audience Address Methods
            5. Storytelling Techniques

            Return structured JSON with style profile.
            """

            # Use centralized model integration
            result = await create_agent_call_to_integration(
                agent_type="boss_agent",
                use_case="voice_analysis", 
                prompt_data={
                    "prompt": analysis_prompt,
                    "analysis_depth": "standard",
                    "system_message": "You are an expert voice and writing style analyzer for YouTube content creators."
                }
            )

            # Parse response
            analysis_text = result["content"] if result["success"] else ""
            try:
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    voice_profile = json.loads(json_match.group())
                else:
                    voice_profile = self._parse_voice_analysis(analysis_text)
            except:
                voice_profile = self._parse_voice_analysis(analysis_text)

            return voice_profile

        except Exception as e:
            logger.error(f"Voice analysis failed: {e}")
            return self._generate_fallback_profile()

    async def generate_voice_matched_content(self, content_type: str, topic: str, voice_profile: Dict, target_length: int = 500) -> Dict[str, Any]:
        """Generate content matching the channel's voice"""
        try:
            generation_prompt = f"""
            Generate {content_type} content for a YouTube channel matching this voice profile:

            Voice Characteristics:
            {json.dumps(voice_profile.get('voice_characteristics', {}), indent=2)}

            Writing Style:
            {json.dumps(voice_profile.get('writing_style', {}), indent=2)}

            Topic: {topic}
            Target Length: {target_length} words

            CRITICAL INSTRUCTIONS:
            1. Match the exact voice characteristics above
            2. Use the same writing style patterns
            3. Maintain consistent tone and personality
            4. Use similar vocabulary and language level
            5. Apply the same storytelling techniques

            Generate the content in their voice.
            """

            # Use centralized model integration
            result = await create_agent_call_to_integration(
                agent_type="boss_agent",
                use_case="content_generation",
                prompt_data={
                    "prompt": generation_prompt,
                    "analysis_depth": "deep",
                    "system_message": "You are an expert content creator who can match any writing style and voice perfectly."
                }
            )

            generated_content = result["content"] if result["success"] else "Content generation failed"

            # Verify style match
            match_score = await self._verify_style_match(
                generated_content,
                voice_profile
            )

            return {
                "content": generated_content,
                "style_match_score": match_score,
                "voice_characteristics_used": voice_profile.get('voice_characteristics', {}),
                "writing_style_used": voice_profile.get('writing_style', {})
            }

        except Exception as e:
            logger.error(f"Voice-matched content generation failed: {e}")
            return {
                "content": "Content generation failed",
                "style_match_score": 0,
                "error": str(e)
            }

    async def _verify_style_match(self, content: str, voice_profile: Dict) -> float:
        """Verify how well generated content matches voice profile"""
        try:
            verification_prompt = f"""
            Compare this content against the voice profile to calculate style match score.

            Content:
            {content}

            Voice Profile:
            {json.dumps(voice_profile, indent=2)}

            Score these aspects (0-100):
            1. Tone match
            2. Vocabulary match
            3. Writing style match
            4. Storytelling match
            5. Overall authenticity

            Return only the average score as a number.
            """

            # Use centralized model integration
            result = await create_agent_call_to_integration(
                agent_type="boss_agent",
                use_case="style_verification",
                prompt_data={
                    "prompt": verification_prompt,
                    "analysis_depth": "quick",
                    "system_message": "You are a precise style match analyzer. Return only numeric scores."
                }
            )

            score_text = result["content"] if result["success"] else "0.7"
            try:
                score = float(score_text.strip())
                return min(100, max(0, score)) / 100  # Normalize to 0-1
            except:
                return 0.7  # Default reasonable score

        except Exception as e:
            logger.error(f"Style match verification failed: {e}")
            return 0.5  # Default moderate score

    def _parse_voice_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Parse voice analysis text into structured format"""
        return {
            "voice_characteristics": {
                "tone": "Professional yet approachable",
                "formality_level": "Semi-formal",
                "personality": "Educational expert",
                "emotional_range": "Measured enthusiasm"
            },
            "writing_style": {
                "sentence_structure": "Clear and concise",
                "vocabulary_level": "Industry-specific, accessible",
                "pacing": "Steady, methodical",
                "storytelling_elements": ["Examples", "Analogies", "Step-by-step explanations"]
            },
            "audience_interaction": {
                "address_style": "Direct, second-person",
                "engagement_techniques": ["Questions", "Calls to action", "Practical applications"],
                "teaching_style": "Expert guiding learner"
            },
            "raw_analysis": analysis_text
        }

    def _generate_fallback_profile(self) -> Dict[str, Any]:
        """Generate fallback voice profile when analysis fails"""
        return {
            "voice_characteristics": {
                "tone": "Professional",
                "formality_level": "Balanced",
                "personality": "Authentic",
                "emotional_range": "Moderate"
            },
            "writing_style": {
                "sentence_structure": "Clear",
                "vocabulary_level": "Accessible",
                "pacing": "Balanced",
                "storytelling_elements": ["Examples", "Explanations"]
            },
            "audience_interaction": {
                "address_style": "Direct",
                "engagement_techniques": ["Questions", "Calls to action"],
                "teaching_style": "Friendly guide"
            }
        }

class BossAgent:
    """Main orchestration agent that coordinates specialized agents"""
    
    # Standardized voice and personality across all agents
    AGENT_VOICE_PROFILE = {
        "tone": "Expert yet approachable YouTube strategist",
        "personality": "Data-driven, actionable, encouraging",
        "communication_style": "Direct answers first, then context",
        "expertise_level": "Professional consultant with deep YouTube knowledge",
        "response_format": "Specific numbers + context + actionable next step"
    }
    
    def __init__(self, openai_api_key: str):
        # Store API key for backward compatibility but use centralized integration
        self.openai_api_key = openai_api_key
        self.intent_classifier = IntentClassifier()
        self.voice_analyzer = VoiceAnalyzer()
        
        # Initialize specialized agents
        self.agents = {
            QueryType.CONTENT_ANALYSIS: ContentAnalysisAgent(),
            QueryType.AUDIENCE_INSIGHTS: AudienceInsightsAgent(),
            QueryType.SEO_OPTIMIZATION: SEOOptimizationAgent(),
            QueryType.COMPETITIVE_ANALYSIS: CompetitiveAnalysisAgent(),
            QueryType.MONETIZATION: MonetizationAgent()
        }
        
        self.cache = get_agent_cache()
        self.monitor = get_data_access_monitor()
    
    def _get_voice_guidelines(self) -> str:
        """Get standardized voice guidelines for all agent prompts"""
        return f"""
        VOICE & PERSONALITY GUIDELINES:
        • Tone: {self.AGENT_VOICE_PROFILE['tone']}
        • Personality: {self.AGENT_VOICE_PROFILE['personality']}
        • Style: {self.AGENT_VOICE_PROFILE['communication_style']}
        • Expertise: {self.AGENT_VOICE_PROFILE['expertise_level']}
        • Format: {self.AGENT_VOICE_PROFILE['response_format']}
        
        RESPONSE STANDARDS:
        ✓ Start with specific numbers/data answering their exact question
        ✓ Provide context relative to YouTube benchmarks
        ✓ Include one actionable next step
        ✓ Use encouraging, professional tone
        ✓ Keep response focused and under 200 words unless complex analysis requested
        """
        
    async def generate_voice_matched_content(self, content_type: str, topic: str, user_context: Dict) -> Dict[str, Any]:
        """Generate content that matches the user's channel voice"""
        try:
            # Get channel content for voice analysis
            channel_content = await self._get_channel_content(user_context)
            
            # Analyze channel voice
            voice_profile = await self.voice_analyzer.analyze_channel_voice(
                channel_content,
                user_context.get('channel_info', {})
            )
            
            # Generate matched content
            generated_content = await self.voice_analyzer.generate_voice_matched_content(
                content_type,
                topic,
                voice_profile
            )
            
            return {
                'success': True,
                'content': generated_content.get('content'),
                'style_match_score': generated_content.get('style_match_score'),
                'voice_profile': voice_profile
            }
            
        except Exception as e:
            logger.error(f"Voice-matched content generation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _get_channel_content(self, user_context: Dict) -> List[Dict]:
        """Get channel content for voice analysis"""
        try:
            channel_id = user_context.get('channel_info', {}).get('channel_id')
            if not channel_id:
                return []
            
            # Import YouTube integration
            from youtube_api_integration import get_youtube_integration
            youtube_service = get_youtube_integration()
            
            # Get recent videos with transcripts
            videos = await youtube_service.get_recent_videos(
                channel_id=channel_id,
                count=10,  # Analyze last 10 videos
                include_transcripts=True
            )
            
            return [{
                'title': video.title,
                'description': video.description,
                'transcript': video.transcript if hasattr(video, 'transcript') else None
            } for video in videos]
            
        except Exception as e:
            logger.error(f"Error getting channel content: {e}")
            return []
    
    async def process_user_query(self, message: str, user_context: Dict) -> Dict[str, Any]:
        """
        Main entry point for processing user queries
        
        Args:
            message: User's message
            user_context: User channel context and data
            
        Returns:
            Synthesized response from appropriate agents
        """
        
        try:
            # Monitor query start
            user_id = user_context.get('user_id', 'unknown')
            await self.monitor.log_event(user_id, 'query_processing', 'boss_agent', 'start', 
                                        {'message_preview': message[:50]})
            
            # Get enhanced real-time context
            if user_id:
                # Register user activity for data pipeline
                await get_data_pipeline().register_user_activity(user_id, "chat")
                
                # Monitor OAuth status check
                await self.monitor.log_event(user_id, 'oauth_check', 'boss_agent', 'start')
                
                # Check OAuth status before attempting enhanced context
                from oauth_manager import get_oauth_manager
                oauth_manager = get_oauth_manager()
                oauth_status = oauth_manager.get_oauth_status(user_id)
                
                # Enhanced OAuth status logging
                is_auth = oauth_status.get('authenticated', False)
                expires_in = oauth_status.get('expires_in_seconds', 0)
                needs_refresh = oauth_status.get('needs_refresh', False)
                logger.info(f"📊 OAuth Status for {user_id}: authenticated={is_auth}, expires_in={expires_in}s, needs_refresh={needs_refresh}")
                
                await self.monitor.log_event(user_id, 'oauth_check', 'boss_agent', 'success', 
                                           {'authenticated': is_auth, 'needs_refresh': needs_refresh})
                
                if is_auth:
                    logger.info(f"✅ OAuth connected - proceeding with real-time data access")
                else:
                    logger.warning(f"❌ OAuth not connected - will use basic context only")
                
                # Monitor enhanced context fetching
                await self.monitor.log_event(user_id, 'context_fetch', 'boss_agent', 'start')
                
                # Get enhanced context with real-time data
                try:
                    enhanced_context = await get_enhanced_context_manager().get_enhanced_context(user_id)
                    channel_info = enhanced_context.get("channel_info", {})
                    realtime_data = enhanced_context.get("realtime_data", {})
                    
                    # Add OAuth status to context for debugging
                    enhanced_context['oauth_status'] = oauth_status
                    
                    # Enhanced context logging
                    total_views = channel_info.get('total_view_count', 0)
                    recent_views = channel_info.get('recent_views', 0)
                    has_realtime = bool(realtime_data)
                    data_quality = enhanced_context.get('data_quality', 'unknown')
                    
                    logger.info(f"📈 Enhanced context for {user_id}: total_views={total_views}, recent_views={recent_views}, realtime_data={has_realtime}, quality={data_quality}")
                    
                    await self.monitor.log_event(user_id, 'context_fetch', 'boss_agent', 'success',
                                               {'total_views': total_views, 'data_quality': data_quality})
                    
                    if total_views > 0:
                        logger.info(f"✅ Real-time channel data available - agents can provide specific insights")
                    else:
                        logger.warning(f"⚠️ No view data available - may need fresh YouTube API call")
                    
                except Exception as e:
                    await self.monitor.log_event(user_id, 'context_fetch', 'boss_agent', 'failure', error_message=str(e))
                    logger.warning(f"Failed to get enhanced context for {user_id}: {e}")
                    enhanced_context = user_context
                    channel_info = user_context.get("channel_info", {})
                    realtime_data = {}
                    enhanced_context['oauth_status'] = oauth_status
            else:
                enhanced_context = user_context
                channel_info = user_context.get("channel_info", {})
                realtime_data = {}
            
            message_lower = message.lower()
            
            # Enhanced direct answers with real-time data
            if "total views" in message_lower or "total view" in message_lower:
                total_views = channel_info.get('total_view_count', 0)
                recent_views = channel_info.get('recent_views', 0)
                views_trend = channel_info.get('views_trend', 'stable')
                
                if total_views > 0:
                    # Create enhanced response with real-time insights
                    response_parts = [f"Your channel has {total_views:,} total views."]
                    
                    if recent_views > 0:
                        response_parts.append(f"In the last 7 days, you got {recent_views:,} views")
                        if views_trend == 'up':
                            response_parts.append("📈 (trending upward!)")
                        elif views_trend == 'down':
                            response_parts.append("📉 (down from previous week)")
                        else:
                            response_parts.append("(stable performance)")
                    
                    # Add key insights if available
                    key_insights = channel_info.get('key_insights', [])
                    if key_insights:
                        response_parts.append(f"\n💡 {key_insights[0]}")
                    
                    # Add data freshness indicator for real-time data
                    data_quality = enhanced_context.get('data_quality', 'unknown')
                    if data_quality == 'real-time':
                        response_parts.append("\n📊 (Real-time data from YouTube Analytics)")
                    
                    return {
                        "success": True,
                        "response": " ".join(response_parts),
                        "intent": "content_analysis",
                        "agents_used": ["enhanced_direct_answer"],
                        "processing_time": 0.1,
                        "confidence": 1.0,
                        "real_time_data": True,
                        "oauth_status": "connected"
                    }
                else:
                    # Need to fetch fresh data from YouTube API
                    logger.info("Total views is 0 or not available, fetching fresh channel data")
                    channel_id = channel_info.get('channel_id')
                    user_id = user_context.get('user_id')
                    oauth_status = enhanced_context.get('oauth_status', {}) if 'enhanced_context' in locals() else {}
                    
                    # Provide helpful feedback about OAuth status
                    if not oauth_status.get('authenticated', False):
                        error_msg = oauth_status.get('error', '')
                        
                        if 'No OAuth token found' in error_msg:
                            oauth_response = "I need to access your YouTube Analytics to get your current total view count, but I don't see a connected YouTube account. " \
                                           "Please connect your YouTube account using the OAuth connection button in the app settings to enable real-time analytics."
                        elif oauth_status.get('needs_refresh', False):
                            oauth_response = "I need to fetch your latest channel data from YouTube, but your authentication has expired. " \
                                           "Please refresh your YouTube connection in the app settings, and I'll be able to get your current analytics data."
                        else:
                            oauth_response = "I need to fetch your latest channel data from YouTube to get your current total view count. " \
                                           "However, there seems to be an issue with your YouTube connection. Please check your OAuth connection in the app settings."
                        
                        logger.info(f"OAuth not available for {user_id}: {oauth_status}")
                        return {
                            "success": True,
                            "response": oauth_response,
                            "intent": "content_analysis", 
                            "agents_used": ["oauth_status_check"],
                            "processing_time": 0.1,
                            "confidence": 0.9,
                            "real_time_data": False,
                            "oauth_required": True
                        }
                    
                    if channel_id:
                        try:
                            # Import and use YouTube API integration to get fresh data
                            from youtube_api_integration import get_youtube_integration
                            youtube_service = get_youtube_integration()
                            
                            # Get fresh channel data
                            fresh_channel_data = await youtube_service.get_channel_data(
                                channel_id=channel_id,
                                include_recent_videos=False,
                                user_id=user_id
                            )
                            
                            if fresh_channel_data and fresh_channel_data.view_count > 0:
                                # Update database with fresh data
                                from backend.App.ai_services import update_user_context
                                channel_info['total_view_count'] = fresh_channel_data.view_count
                                channel_info['subscriber_count'] = fresh_channel_data.subscriber_count
                                channel_info['video_count'] = fresh_channel_data.video_count
                                update_user_context(user_id, "channel_info", channel_info)
                                
                                return {
                                    "success": True,
                                    "response": f"Your channel has {fresh_channel_data.view_count:,} total views.",
                                    "intent": "content_analysis",
                                    "agents_used": ["fresh_data_fetch"],
                                    "processing_time": 0.5,
                                    "confidence": 1.0
                                }
                            else:
                                logger.warning(f"Could not fetch fresh data or channel has 0 views: {channel_id}")
                        except Exception as e:
                            logger.error(f"Error fetching fresh channel data: {e}")
                    
                    # If we still can't get data, let the normal flow handle it
            
            elif "how many subscribers" in message_lower or "subscriber count" in message_lower:
                subscribers = channel_info.get('subscriber_count', 0)
                recent_sub_change = channel_info.get('recent_subscriber_change', 0)
                sub_trend = channel_info.get('subscriber_trend', 'stable')
                
                response_parts = [f"You have {subscribers:,} subscribers."]
                
                if recent_sub_change != 0:
                    if recent_sub_change > 0:
                        response_parts.append(f"You gained {recent_sub_change:,} subscribers this week")
                        if sub_trend == 'up':
                            response_parts.append("🚀 (growing fast!)")
                    else:
                        response_parts.append(f"You lost {abs(recent_sub_change):,} subscribers this week")
                        response_parts.append("📉 (consider reviewing content strategy)")
                
                # Add performance insights
                performance_alerts = channel_info.get('performance_alerts', [])
                if performance_alerts:
                    subscriber_alert = next((alert for alert in performance_alerts if 'subscriber' in alert.lower()), None)
                    if subscriber_alert:
                        response_parts.append(f"\n💡 {subscriber_alert}")
                
                return {
                    "success": True,
                    "response": " ".join(response_parts),
                    "intent": "audience",
                    "agents_used": ["enhanced_direct_answer"],
                    "processing_time": 0.1,
                    "confidence": 1.0,
                    "real_time_data": True
                }
            
            elif "how many videos" in message_lower or "video count" in message_lower:
                video_count = channel_info.get('video_count', 0)
                return {
                    "success": True,
                    "response": f"Your channel has {video_count} videos.",
                    "intent": "content_analysis",
                    "agents_used": ["direct_answer"],
                    "processing_time": 0.1,
                    "confidence": 1.0
                }
            
            # CTR (Click-through rate) questions
            elif any(keyword in message_lower for keyword in ["ctr", "click through rate", "click-through rate", "thumbnail performance"]):
                ctr = channel_info.get('recent_ctr', 0)
                ctr_trend = channel_info.get('ctr_trend', 'stable')
                
                if ctr > 0:
                    response_parts = [f"Your CTR is {ctr:.1f}%."]
                else:
                    response_parts = ["I don't have your current CTR data. CTR (click-through rate) measures how often people click your thumbnails when they see them. You can check this in YouTube Studio > Analytics > Reach tab."]
                
                if ctr >= 8:
                    response_parts.append("🎯 Excellent CTR! Your thumbnails are performing very well.")
                elif ctr >= 5:
                    response_parts.append("👍 Good CTR - above average performance.")
                elif ctr >= 3:
                    response_parts.append("📊 Average CTR - consider testing new thumbnail styles.")
                else:
                    response_parts.append("📸 Low CTR - focus on more compelling thumbnails and titles.")
                
                if ctr_trend == 'up':
                    response_parts.append("📈 (trending upward!)")
                elif ctr_trend == 'down':
                    response_parts.append("📉 (declining recently)")
                
                return {
                    "success": True,
                    "response": " ".join(response_parts),
                    "intent": "content_analysis",
                    "agents_used": ["enhanced_direct_answer"],
                    "processing_time": 0.1,
                    "confidence": 1.0,
                    "real_time_data": True
                }
            
            # Retention rate questions
            elif any(keyword in message_lower for keyword in ["retention", "retention rate", "audience retention", "how long do people watch"]):
                retention = channel_info.get('recent_retention', 0)
                retention_trend = channel_info.get('retention_trend', 'stable')
                
                if retention > 0:
                    response_parts = [f"Your average retention rate is {retention:.1f}%."]
                else:
                    response_parts = ["I don't have your current retention data. Retention rate shows what percentage of your video people actually watch. You can check this in YouTube Studio > Analytics > Engagement tab."]
                
                if retention >= 70:
                    response_parts.append("🎉 Excellent retention! Your content keeps viewers highly engaged.")
                elif retention >= 50:
                    response_parts.append("👍 Good retention - your content structure is working well.")
                elif retention >= 30:
                    response_parts.append("📊 Average retention - consider shorter intros and pattern interrupts.")
                else:
                    response_parts.append("⏱️ Low retention - focus on engaging openings and content pacing.")
                
                if retention_trend == 'up':
                    response_parts.append("📈 (improving recently!)")
                elif retention_trend == 'down':
                    response_parts.append("📉 (declining - analyze drop-off points)")
                
                return {
                    "success": True,
                    "response": " ".join(response_parts),
                    "intent": "content_analysis",
                    "agents_used": ["enhanced_direct_answer"],
                    "processing_time": 0.1,
                    "confidence": 1.0,
                    "real_time_data": True
                }
            
            # Engagement rate questions
            elif any(keyword in message_lower for keyword in ["engagement", "engagement rate", "likes", "comments", "interaction"]):
                engagement = channel_info.get('recent_engagement_rate', 0)
                recent_views = channel_info.get('recent_views', 0)
                
                if engagement > 0:
                    response_parts = [f"Your engagement rate is {engagement:.1f}%."]
                else:
                    response_parts = ["I don't have your current engagement data. Engagement rate measures likes, comments, and shares relative to views. You can check this in YouTube Studio > Analytics > Engagement tab."]
                
                if engagement >= 5:
                    response_parts.append("🚀 Outstanding engagement! Your audience is highly interactive.")
                elif engagement >= 3:
                    response_parts.append("👍 Good engagement - your content resonates with viewers.")
                elif engagement >= 1.5:
                    response_parts.append("📊 Average engagement - consider more calls-to-action.")
                else:
                    response_parts.append("💬 Low engagement - try asking questions and encouraging interaction.")
                
                if recent_views > 0:
                    response_parts.append(f"(Based on {recent_views:,} recent views)")
                
                return {
                    "success": True,
                    "response": " ".join(response_parts),
                    "intent": "audience",
                    "agents_used": ["enhanced_direct_answer"],
                    "processing_time": 0.1,
                    "confidence": 1.0,
                    "real_time_data": True
                }
            
            # Traffic source questions
            elif any(keyword in message_lower for keyword in ["traffic source", "where do views come from", "discovery", "how do people find"]):
                traffic_breakdown = channel_info.get('traffic_source_breakdown', {})
                top_source = channel_info.get('top_traffic_source', 'Unknown')
                
                if traffic_breakdown:
                    youtube_search = traffic_breakdown.get('YouTube Search', 0)
                    suggested = traffic_breakdown.get('Suggested Videos', 0)
                    external = traffic_breakdown.get('External', 0)
                    
                    response_parts = [f"Your top traffic source is {top_source}."]
                    response_parts.append(f"Breakdown: YouTube Search ({youtube_search:.1f}%), Suggested Videos ({suggested:.1f}%), External ({external:.1f}%)")
                    
                    if youtube_search > 40:
                        response_parts.append("🔍 Strong search performance - your SEO is working well!")
                    elif suggested > 40:
                        response_parts.append("📺 Algorithm loves your content - great for viral growth!")
                    elif external > 20:
                        response_parts.append("🌐 Good external promotion - social media is paying off!")
                else:
                    # Graceful degradation - provide general guidance
                    response_parts = ["I don't have access to your traffic source data right now. To see where your views come from, you can check YouTube Studio > Analytics > Reach tab. Common sources include YouTube Search, Suggested Videos, and External traffic."]
                
                return {
                    "success": True,
                    "response": " ".join(response_parts),
                    "intent": "seo",
                    "agents_used": ["enhanced_direct_answer"],
                    "processing_time": 0.1,
                    "confidence": 1.0,
                    "real_time_data": bool(traffic_breakdown)
                }
            
            # Growth and trends questions
            elif any(keyword in message_lower for keyword in ["growth", "trend", "trending", "growing", "decline", "performance trend"]):
                views_trend = channel_info.get('views_trend', 'stable')
                subscriber_trend = channel_info.get('subscriber_trend', 'stable')
                recent_sub_change = channel_info.get('recent_subscriber_change', 0)
                recent_views = channel_info.get('recent_views', 0)
                
                response_parts = []
                
                # Views trend
                if views_trend == 'up':
                    response_parts.append(f"📈 Your views are trending upward! ({recent_views:,} recent views)")
                elif views_trend == 'down':
                    response_parts.append(f"📉 Your views are declining ({recent_views:,} recent views)")
                else:
                    response_parts.append(f"📊 Your views are stable ({recent_views:,} recent views)")
                
                # Subscriber trend
                if recent_sub_change > 0:
                    response_parts.append(f"You gained {recent_sub_change:,} subscribers recently.")
                elif recent_sub_change < 0:
                    response_parts.append(f"You lost {abs(recent_sub_change):,} subscribers recently.")
                
                # Performance alerts
                alerts = channel_info.get('performance_alerts', [])
                if alerts:
                    response_parts.append(f"💡 {alerts[0]}")
                
                return {
                    "success": True,
                    "response": " ".join(response_parts),
                    "intent": "content_analysis",
                    "agents_used": ["enhanced_direct_answer"],
                    "processing_time": 0.1,
                    "confidence": 1.0,
                    "real_time_data": True
                }
            
            # Best/Top performing content questions
            elif any(keyword in message_lower for keyword in ["best video", "top video", "best performing", "most views", "most popular", "highest performing"]):
                # Check if we have enhanced context with video performance data
                realtime_data = enhanced_context.get("realtime_data", {}) if 'enhanced_context' in locals() else {}
                oauth_status = enhanced_context.get('oauth_status', {}) if 'enhanced_context' in locals() else {}
                
                if realtime_data and realtime_data.get('top_video'):
                    top_video = realtime_data['top_video']
                    response = f"Your best performing video is \"{top_video['title']}\" with {top_video['views']:,} views and {top_video.get('engagement_rate', 0):.1f}% engagement rate."
                    
                    return {
                        "success": True,
                        "response": response,
                        "intent": "content_analysis",
                        "agents_used": ["enhanced_direct_answer"],
                        "processing_time": 0.1,
                        "confidence": 1.0,
                        "real_time_data": True
                    }
                else:
                    # Check OAuth status and provide appropriate response
                    is_auth = oauth_status.get('authenticated', False)
                    needs_refresh = oauth_status.get('needs_refresh', False)
                    
                    if not is_auth:
                        return {
                            "success": True,
                            "response": "I need access to your YouTube data to find your best performing video. Please connect your YouTube account in Settings > YouTube Integration to see detailed performance analytics.",
                            "intent": "content_analysis",
                            "agents_used": ["oauth_check"],
                            "processing_time": 0.1,
                            "confidence": 1.0,
                            "oauth_required": True
                        }
                    elif needs_refresh:
                        return {
                            "success": True,
                            "response": "Your YouTube connection needs to be refreshed. Please go to Settings > YouTube Integration and reconnect your account to see your best performing videos.",
                            "intent": "content_analysis",
                            "agents_used": ["oauth_refresh_needed"],
                            "processing_time": 0.1,
                            "confidence": 1.0,
                            "refresh_required": True
                        }
                    else:
                        # OAuth is connected but no data - try to fetch fresh data
                        logger.info("No top video data in enhanced context - will attempt fresh data fetch via content analysis agent")
                        # Continue to full agent processing for fresh data fetch
            
            # Step 1: Parse message and classify intent
            intent, parameters = await self.intent_classifier.classify_intent(message, user_context)
            
            logger.info(f"Classified intent: {intent.value} with parameters: {parameters}")
            
            # Step 2: Check cache for existing response
            cached_response = self.cache.get(message, user_context, intent.value)
            if cached_response:
                logger.info(f"Returning cached response for intent: {intent.value}")
                return cached_response
            
            # Step 3: Determine which agents to activate
            active_agents = self._determine_agents(intent, parameters)
            
            # Step 4: Create agent requests with enhanced context
            requests = self._create_agent_requests(intent, parameters, enhanced_context if user_id else user_context)
            
            # Step 5: Execute agents (parallel where possible)
            agent_responses = await self._execute_agents(active_agents, requests)
            
            # Step 6: Synthesize final response with enhanced context
            final_response = await self._synthesize_response(intent, agent_responses, enhanced_context if user_id else user_context, message)
            
            # Step 7: Cache the response
            if final_response.get("success", False):
                self.cache.set(message, user_context, final_response, intent.value)
            
            return final_response
            
        except Exception as e:
            logger.error(f"Boss agent processing failed: {e}")
            return {
                "success": False,
                "response": "I encountered an error processing your request. Please try again.",
                "error": str(e)
            }
    
    def _determine_agents(self, intent: QueryType, parameters: Dict) -> List[QueryType]:
        """Determine which agents should be activated based on intent"""
        
        # Primary agent based on intent
        active_agents = [intent] if intent != QueryType.GENERAL else []
        
        # Enhanced multi-agent coordination based on query complexity
        if parameters.get("competitors"):
            if QueryType.COMPETITIVE_ANALYSIS not in active_agents:
                active_agents.append(QueryType.COMPETITIVE_ANALYSIS)
        
        if parameters.get("metrics") and any(metric in ["revenue", "monetization"] for metric in parameters.get("metrics", [])):
            if QueryType.MONETIZATION not in active_agents:
                active_agents.append(QueryType.MONETIZATION)
        
        # Enhanced agent combinations based on intent and new features
        if intent == QueryType.CONTENT_ANALYSIS:
            # Content analysis now includes viral potential and needs broader insights
            if QueryType.SEO_OPTIMIZATION not in active_agents:
                active_agents.append(QueryType.SEO_OPTIMIZATION)  # For algorithm prediction
            if QueryType.AUDIENCE_INSIGHTS not in active_agents:
                active_agents.append(QueryType.AUDIENCE_INSIGHTS)  # For engagement and virality
        
        elif intent == QueryType.AUDIENCE_INSIGHTS:
            # Audience analysis now includes collaboration features
            if QueryType.CONTENT_ANALYSIS not in active_agents:
                active_agents.append(QueryType.CONTENT_ANALYSIS)  # For content compatibility
            if QueryType.COMPETITIVE_ANALYSIS not in active_agents:
                active_agents.append(QueryType.COMPETITIVE_ANALYSIS)  # For collaboration opportunities
        
        elif intent == QueryType.SEO_OPTIMIZATION:
            # SEO now includes algorithm favorability prediction
            if QueryType.CONTENT_ANALYSIS not in active_agents:
                active_agents.append(QueryType.CONTENT_ANALYSIS)  # For performance correlation
            if QueryType.AUDIENCE_INSIGHTS not in active_agents:
                active_agents.append(QueryType.AUDIENCE_INSIGHTS)  # For engagement signals
        
        elif intent == QueryType.MONETIZATION:
            # Monetization needs audience and content insights
            if QueryType.AUDIENCE_INSIGHTS not in active_agents:
                active_agents.append(QueryType.AUDIENCE_INSIGHTS)
            if QueryType.CONTENT_ANALYSIS not in active_agents:
                active_agents.append(QueryType.CONTENT_ANALYSIS)
        
        # For comprehensive analysis questions, activate multiple agents
        if intent == QueryType.GENERAL or len(active_agents) == 0:
            # Default to content analysis for general questions
            active_agents = [QueryType.CONTENT_ANALYSIS, QueryType.AUDIENCE_INSIGHTS]
        
        # Remove duplicates and ensure we have at least one agent
        active_agents = list(set(active_agents))
        if not active_agents:
            active_agents = [QueryType.CONTENT_ANALYSIS]  # Default fallback
        
        return active_agents
    
    def _create_agent_requests(self, intent: QueryType, parameters: Dict, user_context: Dict) -> List[AgentRequest]:
        """Create agent requests with proper context"""
        
        # Extract time period
        time_period = parameters.get("time_period", "last_30d")
        if "7" in str(parameters.get("time_period", "")):
            time_period = "last_7d"
        elif "90" in str(parameters.get("time_period", "")):
            time_period = "last_90d"
        
        # Create context - properly access nested channel_info
        channel_info = user_context.get("channel_info", {})
        # Use channel_id if available, fallback to name
        channel_identifier = channel_info.get("channel_id") or channel_info.get("name", "unknown")
        context = Context(
            channel_id=channel_identifier,
            time_period=time_period,
            specific_videos=parameters.get("specific_videos", []),
            competitors=parameters.get("competitors", [])
        )
        
        # Create request with full user context
        request = AgentRequest(
            request_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            query_type=intent,
            priority=Priority.MEDIUM,
            context=context,
            token_budget=TokenBudget(input_tokens=3000, output_tokens=1500),
            user_context=user_context  # Store full user context for specialized agents
        )
        
        return [request]
    
    async def _execute_agents(self, active_agents: List[QueryType], requests: List[AgentRequest]) -> List[AgentResponse]:
        """Execute the specified agents with their requests"""
        
        tasks = []
        for agent_type in active_agents:
            if agent_type in self.agents:
                agent = self.agents[agent_type]
                # Use the first request for now (could be enhanced for multiple requests)
                task = agent.process_request(requests[0])
                tasks.append(task)
        
        # Execute agents in parallel with enhanced error handling
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Enhanced error handling and response validation
        valid_responses = []
        failed_agents = []
        
        for i, response in enumerate(responses):
            agent_type = active_agents[i] if i < len(active_agents) else "unknown"
            
            if isinstance(response, AgentResponse):
                if response.success and response.confidence >= 0.5:
                    valid_responses.append(response)
                    logger.info(f"✅ {agent_type.value} agent succeeded (confidence: {response.confidence:.2f})")
                else:
                    failed_agents.append(agent_type.value)
                    logger.warning(f"⚠️ {agent_type.value} agent low confidence: {response.confidence:.2f}")
                    if response.confidence >= 0.3:  # Still use low confidence responses as backup
                        valid_responses.append(response)
            elif isinstance(response, Exception):
                failed_agents.append(agent_type.value)
                logger.error(f"❌ {agent_type.value} agent failed: {response}")
                
                # Try to recover with simplified fallback
                try:
                    fallback_response = await self._create_fallback_response(agent_type, requests[0])
                    if fallback_response:
                        valid_responses.append(fallback_response)
                        logger.info(f"🔄 {agent_type.value} fallback recovery successful")
                except Exception as fallback_error:
                    logger.error(f"💥 {agent_type.value} fallback also failed: {fallback_error}")
        
        # Log overall success rate
        success_rate = len(valid_responses) / len(active_agents) if active_agents else 0
        logger.info(f"📊 Agent execution success rate: {success_rate:.1%} ({len(valid_responses)}/{len(active_agents)})")
        
        if failed_agents:
            logger.warning(f"⚠️ Failed agents: {', '.join(failed_agents)}")
        
        return valid_responses
    
    async def _create_fallback_response(self, agent_type: QueryType, request: AgentRequest) -> Optional[AgentResponse]:
        """Create a simplified fallback response when an agent fails"""
        
        try:
            start_time = datetime.now()
            user_context = request.user_context or {}
            channel_info = user_context.get('channel_info', {})
            
            fallback_prompts = {
                QueryType.CONTENT_ANALYSIS: f"""
                Provide basic YouTube content analysis for channel: {channel_info.get('name', 'Creator')}
                Recent metrics: {channel_info.get('recent_views', 0):,} views, {channel_info.get('recent_ctr', 0):.1f}% CTR
                Give 3 actionable content improvement suggestions based on standard YouTube best practices.
                """,
                QueryType.AUDIENCE_INSIGHTS: f"""
                Analyze audience for channel: {channel_info.get('name', 'Creator')} 
                Subscribers: {channel_info.get('subscriber_count', 0):,}
                Provide 3 insights about audience growth and engagement strategies.
                """,
                QueryType.SEO_OPTIMIZATION: f"""
                SEO analysis for channel: {channel_info.get('name', 'Creator')}
                Niche: {channel_info.get('niche', 'General')}
                Suggest 3 SEO optimization strategies for better discoverability.
                """,
                QueryType.COMPETITIVE_ANALYSIS: f"""
                Competitive analysis for {channel_info.get('niche', 'YouTube')} channel
                Provide 3 competitive positioning strategies and market opportunities.
                """,
                QueryType.MONETIZATION: f"""
                Monetization analysis for channel with {channel_info.get('subscriber_count', 0):,} subscribers
                Suggest 3 revenue optimization strategies appropriate for this channel size.
                """
            }
            
            prompt = fallback_prompts.get(agent_type, "Provide general YouTube growth advice.")
            
            # Use model integration for better fallback handling
            messages = [{"role": "user", "content": prompt}]
            response_content = await migrate_openai_call_to_integration(
                "boss_agent", messages, "quick"
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResponse(
                agent_id=f"{agent_type.value}_fallback",
                request_id=request.request_id,
                timestamp=datetime.now().isoformat(),
                success=True,
                data={
                    "analysis_type": f"{agent_type.value}_fallback",
                    "insights": response_content,
                    "recommendations": ["Review and optimize based on analytics data"],
                    "fallback_response": True
                },
                confidence=0.6,  # Lower confidence for fallback responses
                processing_time=processing_time,
                tokens_used=300
            )
            
        except Exception as e:
            logger.error(f"Fallback response creation failed for {agent_type.value}: {e}")
            return None
    
    async def _synthesize_response(self, intent: QueryType, agent_responses: List[AgentResponse], user_context: Dict, message: str) -> Dict[str, Any]:
        """Synthesize final response from agent outputs"""
        
        if not agent_responses:
            return {
                "success": False,
                "response": "I couldn't gather the analytics data you requested. Please try again or be more specific about what you'd like to know.",
                "intent": intent.value
            }
        
        # Collect insights from all agents
        all_insights = []
        all_recommendations = []
        
        for response in agent_responses:
            data = response.data
            if "insights" in data:
                all_insights.append(f"**{response.agent_id.replace('_', ' ').title()}:**\n{data['insights']}")
            
            if "recommendations" in data:
                all_recommendations.extend(data.get("recommendations", []))
        
        # Extract top performers data if available
        top_performers_info = ""
        for response in agent_responses:
            if response.data.get('top_performers'):
                tp = response.data['top_performers']
                if tp.get('best_overall'):
                    best = tp['best_overall']
                    top_performers_info = f"""
                    
                    BEST PERFORMING VIDEO:
                    Title: "{best['title']}"
                    Views: {best['views']:,}
                    Engagement Rate: {best['engagement_rate']:.1f}%
                    """
        
        # Create enhanced synthesis prompt with confidence weighting
        channel_info = user_context.get("channel_info", {})
        
        # Calculate confidence-weighted insights
        high_confidence_insights = []
        medium_confidence_insights = []
        low_confidence_insights = []
        
        for response in agent_responses:
            confidence = response.confidence
            agent_name = response.agent_id.replace('_', ' ').title()
            data = response.data
            
            if "insights" in data:
                insight_text = f"**{agent_name}** (confidence: {confidence:.1f}): {data['insights']}"
                if confidence >= 0.85:
                    high_confidence_insights.append(insight_text)
                elif confidence >= 0.70:
                    medium_confidence_insights.append(insight_text)
                else:
                    low_confidence_insights.append(insight_text)
        
        # Prioritize high confidence insights
        prioritized_insights = high_confidence_insights + medium_confidence_insights + low_confidence_insights
        
        synthesis_prompt = f"""
        You are Vidalytics's AI assistant. Provide an expert, data-driven response to this YouTube creator's question.
        
        {self._get_voice_guidelines()}
        
        CREATOR'S QUESTION: "{message}"
        DETECTED INTENT: {intent.value.replace('_', ' ').title()}
        CHANNEL: {channel_info.get('name', 'Creator')}
        
        REAL-TIME CHANNEL DATA:
        • Total Views: {channel_info.get('total_view_count', 0):,}
        • Subscribers: {channel_info.get('subscriber_count', 0):,}
        • Total Videos: {channel_info.get('video_count', 0)}
        • Recent Performance (7d): {channel_info.get('recent_views', 0):,} views
        • Current CTR: {channel_info.get('recent_ctr', 0):.1f}%
        • Retention Rate: {channel_info.get('recent_retention', 0):.1f}%
        • Engagement Rate: {channel_info.get('recent_engagement_rate', 0):.1f}%
        
        AI AGENT ANALYSIS (Prioritized by Confidence):
        {chr(10).join(prioritized_insights)}
        {top_performers_info}
        
        RESPONSE GUIDELINES:
        1. **DIRECT ANSWER FIRST**: Start with exact numbers answering their specific question
        2. **DATA-DRIVEN**: Use only the real metrics provided above - no generic estimates
        3. **CONTEXT-AWARE**: Reference their channel's specific performance levels
        4. **ACTIONABLE**: Include 1-2 specific next steps if relevant to their question
        5. **PROFESSIONAL TONE**: Expert but approachable, like a seasoned YouTube strategist
        
        QUALITY STANDARDS:
        ✓ Answer must be specific to their exact question
        ✓ Use precise numbers from the data above
        ✓ Provide context relative to YouTube benchmarks when relevant
        ✓ Keep total response under 200 words unless complex analysis requested
        ✓ End with actionable next step if applicable
        
        RESPONSE STRUCTURE:
        [Direct numerical answer] + [Brief context] + [Actionable insight if relevant]
        
        EXAMPLES:
        Q: "Total views?" → "Your channel has 1,234,567 total views, which puts you in the top 15% of creators in your niche."
        Q: "Best video?" → "Your top video is 'Title' with 89K views (8.2% CTR) - consider analyzing what made it successful."
        """
        
        try:
            # Use centralized model integration
            result = await create_agent_call_to_integration(
                agent_type="boss_agent",
                use_case="response_synthesis",
                prompt_data={
                    "prompt": synthesis_prompt,
                    "analysis_depth": "standard",
                    "system_message": "You are the main Vidalytics AI orchestrating agent responses."
                }
            )
            
            synthesized_response = result["content"] if result["success"] else "Unable to synthesize response"
            
        except Exception as e:
            logger.error(f"Response synthesis failed: {e}")
            # Fallback to simple concatenation
            synthesized_response = f"Based on your {intent.value.replace('_', ' ')} request, here's what I found:\n\n" + "\n\n".join(all_insights)
        
        return {
            "success": True,
            "response": synthesized_response,
            "intent": intent.value,
            "agents_used": [r.agent_id for r in agent_responses],
            "recommendations": all_recommendations[:5],  # Top 5 recommendations
            "processing_time": sum(r.processing_time for r in agent_responses),
            "confidence": sum(r.confidence for r in agent_responses) / len(agent_responses)
        }

# Initialize boss agent instance
boss_agent = None

def get_boss_agent():
    """Get or create boss agent instance"""
    global boss_agent
    if boss_agent is None:
        # Load from .env file first for security
        from dotenv import dotenv_values
        env_vars = dotenv_values()
        api_key = env_vars.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        boss_agent = BossAgent(api_key)
    return boss_agent

async def process_user_message(message: str, user_context: Dict) -> Dict[str, Any]:
    """
    Main function to process user messages through the boss agent system
    
    Args:
        message: User's message
        user_context: User channel context
        
    Returns:
        Processed response from boss agent orchestration
    """
    agent = get_boss_agent()
    return await agent.process_user_query(message, user_context)