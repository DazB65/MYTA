"""
Boss Agent Orchestration System for CreatorMate
Coordinates multiple specialized agents for YouTube analytics
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from openai import OpenAI
import os
from agent_cache import get_agent_cache
from enhanced_user_context import get_enhanced_context_manager
from realtime_data_pipeline import get_data_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryType(Enum):
    CONTENT_ANALYSIS = "content_analysis"
    AUDIENCE_INSIGHTS = "audience"
    SEO_OPTIMIZATION = "seo"
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
    
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
        
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
        Analyze this YouTube creator's message and classify the intent. Extract relevant parameters.
        
        Message: "{message}"
        
        Channel Context:
        - Channel: {channel_info.get('name', 'Unknown')}
        - Niche: {channel_info.get('niche', 'Unknown')}
        - Subscriber Count: {channel_info.get('subscriber_count', 0):,}
        
        Classify into ONE of these categories:
        1. content_analysis - analyzing video performance, best/worst performing videos, hooks, titles, thumbnails, retention, which video has most views/engagement, video rankings, content effectiveness, channel metrics (total views, total videos)
           Examples: "what is my best performing video", "which video has the most views", "what's my top video", "which content performs best", "what is my total views", "how many videos do I have"
        2. audience - audience demographics, behavior, sentiment, comments, subscribers, engagement patterns, subscriber count questions
           Examples: "who is my audience", "what are the demographics", "how many subscribers do I have"
        3. seo - search optimization, keywords, rankings, discoverability
        4. competition - competitor analysis, benchmarking, market positioning
        5. monetization - revenue optimization, sponsorships, product placement
        6. general - general questions, greetings, or unclear intent
        
        Extract these parameters if mentioned:
        - time_period: last_7d, last_30d, last_90d, or specific dates
        - specific_videos: video titles or IDs mentioned
        - competitors: competitor channels mentioned
        - metrics: specific metrics requested (views, CTR, retention, etc.)
        
        Respond with JSON:
        {{
            "intent": "category_name",
            "confidence": 0.0-1.0,
            "parameters": {{
                "time_period": "extracted_period",
                "specific_videos": ["video1", "video2"],
                "competitors": ["channel1", "channel2"],
                "metrics": ["metric1", "metric2"],
                "focus_areas": ["area1", "area2"]
            }},
            "reasoning": "Brief explanation of classification"
        }}
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": classification_prompt}],
                    temperature=0.1,
                    max_tokens=500
                )
            )
            
            raw_content = response.choices[0].message.content
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
    
    def __init__(self, agent_id: str, openai_client: OpenAI):
        self.agent_id = agent_id
        self.client = openai_client
        
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
    
    def __init__(self, openai_client: OpenAI):
        super().__init__("content_analyzer", openai_client)
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
        
        # Get response from specialized agent
        specialized_response = await self.specialized_agent.process_boss_agent_request(specialized_request)
        
        # Check if the specialized agent handled the request
        if not specialized_response.get('domain_match', True):
            # Fall back to simple content analysis
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
        """Fallback content analysis using OpenAI"""
        
        context = request.context
        
        analysis_prompt = f"""
        As a YouTube content analysis expert, analyze the performance data for channel "{context.channel_id}".
        
        Time Period: {context.time_period}
        Focus Videos: {context.specific_videos or "All recent videos"}
        
        Provide analysis in these areas:
        1. Content Performance Metrics
        2. Hook Effectiveness Analysis
        3. Title Performance Patterns
        4. Thumbnail Click-Through Optimization
        5. Content Structure Recommendations
        
        Return analysis as JSON with actionable insights and specific recommendations.
        Focus on data-driven conclusions and concrete next steps.
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
    
    def __init__(self, openai_client: OpenAI):
        super().__init__("audience_analyzer", openai_client)
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
        
        # Get response from specialized agent
        specialized_response = await self.specialized_agent.process_boss_agent_request(specialized_request)
        
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
    
    def __init__(self, openai_client: OpenAI):
        super().__init__("seo_optimizer", openai_client)
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
    
    def __init__(self, openai_client: OpenAI):
        super().__init__("competitor_analyzer", openai_client)
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
    
    def __init__(self, openai_client: OpenAI):
        super().__init__("monetization_optimizer", openai_client)
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

class BossAgent:
    """Main orchestration agent that coordinates specialized agents"""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.intent_classifier = IntentClassifier(self.client)
        
        # Initialize specialized agents
        self.agents = {
            QueryType.CONTENT_ANALYSIS: ContentAnalysisAgent(self.client),
            QueryType.AUDIENCE_INSIGHTS: AudienceInsightsAgent(self.client),
            QueryType.SEO_OPTIMIZATION: SEOOptimizationAgent(self.client),
            QueryType.COMPETITIVE_ANALYSIS: CompetitiveAnalysisAgent(self.client),
            QueryType.MONETIZATION: MonetizationAgent(self.client)
        }
        
        self.cache = get_agent_cache()
        
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
            # Get enhanced real-time context
            user_id = user_context.get('user_id')
            if user_id:
                # Register user activity for data pipeline
                await get_data_pipeline().register_user_activity(user_id, "chat")
                
                # Check OAuth status before attempting enhanced context
                from oauth_manager import get_oauth_manager
                oauth_manager = get_oauth_manager()
                oauth_status = oauth_manager.get_oauth_status(user_id)
                
                # Enhanced OAuth status logging
                is_auth = oauth_status.get('authenticated', False)
                expires_in = oauth_status.get('expires_in_seconds', 0)
                needs_refresh = oauth_status.get('needs_refresh', False)
                logger.info(f"📊 OAuth Status for {user_id}: authenticated={is_auth}, expires_in={expires_in}s, needs_refresh={needs_refresh}")
                
                if is_auth:
                    logger.info(f"✅ OAuth connected - proceeding with real-time data access")
                else:
                    logger.warning(f"❌ OAuth not connected - will use basic context only")
                
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
                    
                    if total_views > 0:
                        logger.info(f"✅ Real-time channel data available - agents can provide specific insights")
                    else:
                        logger.warning(f"⚠️ No view data available - may need fresh YouTube API call")
                    
                except Exception as e:
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
                                from ai_services import update_user_context
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
                    # Delegate to content analysis agent for detailed video analysis
                    logger.info("No top video data in enhanced context - delegating to content analysis agent")
            
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
        
        # Smart agent combinations based on intent
        if intent == QueryType.CONTENT_ANALYSIS:
            # Content analysis benefits from SEO insights
            if QueryType.SEO_OPTIMIZATION not in active_agents:
                active_agents.append(QueryType.SEO_OPTIMIZATION)
            # Also add audience insights for engagement context
            if QueryType.AUDIENCE_INSIGHTS not in active_agents:
                active_agents.append(QueryType.AUDIENCE_INSIGHTS)
        
        elif intent == QueryType.AUDIENCE_INSIGHTS:
            # Audience analysis benefits from content performance context
            if QueryType.CONTENT_ANALYSIS not in active_agents:
                active_agents.append(QueryType.CONTENT_ANALYSIS)
        
        elif intent == QueryType.SEO_OPTIMIZATION:
            # SEO benefits from content performance data
            if QueryType.CONTENT_ANALYSIS not in active_agents:
                active_agents.append(QueryType.CONTENT_ANALYSIS)
        
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
        
        # Execute agents in parallel
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and failed responses
        valid_responses = []
        for response in responses:
            if isinstance(response, AgentResponse) and response.success:
                valid_responses.append(response)
            elif isinstance(response, Exception):
                logger.error(f"Agent execution failed: {response}")
        
        return valid_responses
    
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
        
        # Create synthesis prompt
        channel_info = user_context.get("channel_info", {})
        synthesis_prompt = f"""
        As CreatorMate, answer the user's specific question using these YouTube analytics insights.
        
        User's Question: "{message}"
        User Intent: {intent.value.replace('_', ' ').title()}
        Channel: {channel_info.get('name', 'Your channel')}
        
        Channel Information Available:
        - Total Views: {channel_info.get('total_view_count', 0):,} ({channel_info.get('total_view_count', 0) and 'real-time data' or 'basic data'})
        - Subscriber Count: {channel_info.get('subscriber_count', 0):,}
        - Average Views per Video: {channel_info.get('avg_view_count', 0):,}
        - Total Videos: {channel_info.get('video_count', 0)}
        - Recent CTR: {channel_info.get('recent_ctr', 0):.1f}%
        - Recent Retention: {channel_info.get('recent_retention', 0):.1f}%
        - Recent Engagement: {channel_info.get('recent_engagement_rate', 0):.1f}%
        
        Agent Insights:
        {chr(10).join(all_insights)}
        {top_performers_info}
        
        CRITICAL INSTRUCTIONS:
        1. ALWAYS start with a DIRECT ANSWER to the user's exact question using the specific data above
        2. For "total views" questions: "Your channel has X total views" (use the exact number)
        3. For "subscribers" questions: "You have X subscribers" (use the exact number)
        4. For "best video" questions: Use the BEST PERFORMING VIDEO data above if available
        5. For performance metrics: Use the Recent CTR, Retention, Engagement data above
        6. If no specific data is available for their question, say "I don't have that specific data available" instead of generic responses
        
        Response Structure:
        - FIRST SENTENCE: Direct answer to their question with specific numbers
        - OPTIONAL: Brief additional context or insights (1-2 sentences max)
        - OPTIONAL: Recommendations ONLY if truly relevant to their question
        
        Examples:
        - Question: "What is my total views?" → "Your channel has 1,234,567 total views."
        - Question: "What's my best video?" → "Your best performing video is 'Video Title' with 50,000 views."
        
        Do NOT provide generic advice unless specifically asked for it.
        Keep the response concise and focused on answering their exact question.
        """
        
        try:
            synthesis_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": synthesis_prompt}],
                    temperature=0.3,
                    max_tokens=800
                )
            )
            
            synthesized_response = synthesis_response.choices[0].message.content
            
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