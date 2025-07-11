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
        
        classification_prompt = f"""
        Analyze this YouTube creator's message and classify the intent. Extract relevant parameters.
        
        Message: "{message}"
        
        Channel Context:
        - Channel: {context.get('channel_name', 'Unknown')}
        - Niche: {context.get('niche', 'Unknown')}
        - Subscriber Count: {context.get('subscriber_count', 0):,}
        
        Classify into ONE of these categories:
        1. content_analysis - analyzing video performance, hooks, titles, thumbnails, retention
        2. audience - audience demographics, behavior, sentiment, comments, subscribers, engagement patterns
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
            
            result = json.loads(response.choices[0].message.content)
            intent = QueryType(result["intent"])
            
            return intent, result["parameters"]
            
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
            
            # Step 4: Create agent requests
            requests = self._create_agent_requests(intent, parameters, user_context)
            
            # Step 5: Execute agents (parallel where possible)
            agent_responses = await self._execute_agents(active_agents, requests)
            
            # Step 6: Synthesize final response
            final_response = await self._synthesize_response(intent, agent_responses, user_context)
            
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
        
        # Add complementary agents based on parameters
        if parameters.get("competitors"):
            if QueryType.COMPETITIVE_ANALYSIS not in active_agents:
                active_agents.append(QueryType.COMPETITIVE_ANALYSIS)
        
        if parameters.get("metrics") and any(metric in ["revenue", "monetization"] for metric in parameters.get("metrics", [])):
            if QueryType.MONETIZATION not in active_agents:
                active_agents.append(QueryType.MONETIZATION)
        
        # For content analysis, often include SEO insights
        if intent == QueryType.CONTENT_ANALYSIS:
            active_agents.append(QueryType.SEO_OPTIMIZATION)
        
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
        
        # Create context
        context = Context(
            channel_id=user_context.get("channel_name", "unknown"),
            time_period=time_period,
            specific_videos=parameters.get("specific_videos", []),
            competitors=parameters.get("competitors", [])
        )
        
        # Create request
        request = AgentRequest(
            request_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            query_type=intent,
            priority=Priority.MEDIUM,
            context=context,
            token_budget=TokenBudget(input_tokens=3000, output_tokens=1500)
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
    
    async def _synthesize_response(self, intent: QueryType, agent_responses: List[AgentResponse], user_context: Dict) -> Dict[str, Any]:
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
        
        # Create synthesis prompt
        synthesis_prompt = f"""
        As CreatorMate, synthesize these YouTube analytics insights for the user.
        
        User Intent: {intent.value.replace('_', ' ').title()}
        Channel: {user_context.get('channel_name', 'Your channel')}
        
        Agent Insights:
        {chr(10).join(all_insights)}
        
        Create a cohesive, actionable response that:
        1. Directly addresses the user's question
        2. Prioritizes the most impactful insights
        3. Provides clear next steps
        4. Maintains a helpful, expert tone
        5. Is concise but comprehensive
        
        Format as a natural conversation response, not a list or bullet points.
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