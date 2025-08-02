"""
Base Agent System for Vidalytics
Provides common functionality and abstractions for all specialized agents
"""

import json
import uuid
import hashlib
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Import performance tracking
from backend.App.agent_performance_tracker import get_performance_tracker
from backend.App.agent_performance_models import AgentType as PerfAgentType, ModelProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# Common Data Classes and Enums
# =============================================================================

class AgentType(Enum):
    """Enumeration of all agent types in the system"""
    BOSS = "boss_agent"
    CONTENT_ANALYSIS = "content_analysis"
    AUDIENCE_INSIGHTS = "audience_insights"
    SEO_DISCOVERABILITY = "seo_discoverability"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    MONETIZATION_STRATEGY = "monetization_strategy"

class AnalysisDepth(Enum):
    """Analysis depth levels"""
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"

class Priority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5

@dataclass
class TokenBudget:
    """Token allocation for agent requests"""
    input_tokens: int = 3000
    output_tokens: int = 1500
    
    def to_dict(self) -> Dict[str, int]:
        return asdict(self)

@dataclass
class CacheInfo:
    """Cache information for responses"""
    cache_hit: bool = False
    cache_key: str = ""
    ttl_remaining: int = 3600
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class TokenUsage:
    """Token usage tracking"""
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AgentInsight:
    """Standard insight structure"""
    insight: str
    evidence: str
    impact: str = "Medium"  # High, Medium, Low
    confidence: float = 0.8
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AgentRecommendation:
    """Standard recommendation structure"""
    recommendation: str
    expected_impact: str = "Medium"  # High, Medium, Low
    implementation_difficulty: str = "Medium"  # Easy, Medium, Hard
    reasoning: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AgentAnalysis:
    """Standard analysis result structure"""
    summary: str
    metrics: Dict[str, Any] = None
    key_insights: List[AgentInsight] = None
    recommendations: List[AgentRecommendation] = None
    detailed_analysis: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {}
        if self.key_insights is None:
            self.key_insights = []
        if self.recommendations is None:
            self.recommendations = []
        if self.detailed_analysis is None:
            self.detailed_analysis = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "metrics": self.metrics,
            "key_insights": [insight.to_dict() for insight in self.key_insights],
            "recommendations": [rec.to_dict() for rec in self.recommendations],
            "detailed_analysis": self.detailed_analysis
        }

@dataclass
class AgentRequest:
    """Standard request structure for all agents"""
    request_id: str
    agent_type: AgentType
    query_type: str
    context: Dict[str, Any]
    token_budget: TokenBudget = None
    analysis_depth: AnalysisDepth = AnalysisDepth.STANDARD
    boss_agent_token: str = ""
    timestamp: str = ""
    user_context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.token_budget is None:
            self.token_budget = TokenBudget()
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if self.user_context is None:
            self.user_context = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "agent_type": self.agent_type.value,
            "query_type": self.query_type,
            "context": self.context,
            "token_budget": self.token_budget.to_dict(),
            "analysis_depth": self.analysis_depth.value,
            "boss_agent_token": self.boss_agent_token,
            "timestamp": self.timestamp,
            "user_context": self.user_context
        }

@dataclass
class AgentResponse:
    """Standard response structure for all agents"""
    agent_type: AgentType
    response_id: str
    request_id: str
    timestamp: str
    confidence_score: float
    data_freshness: str
    domain_match: bool
    analysis: AgentAnalysis
    token_usage: TokenUsage = None
    cache_info: CacheInfo = None
    processing_time: float = 0.0
    for_boss_agent_only: bool = True
    
    def __post_init__(self):
        if self.token_usage is None:
            self.token_usage = TokenUsage()
        if self.cache_info is None:
            self.cache_info = CacheInfo()
        if not self.data_freshness:
            self.data_freshness = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_type": self.agent_type.value,
            "response_id": self.response_id,
            "request_id": self.request_id,
            "timestamp": self.timestamp,
            "confidence_score": self.confidence_score,
            "data_freshness": self.data_freshness,
            "domain_match": self.domain_match,
            "analysis": self.analysis.to_dict(),
            "token_usage": self.token_usage.to_dict(),
            "cache_info": self.cache_info.to_dict(),
            "processing_time": self.processing_time,
            "for_boss_agent_only": self.for_boss_agent_only
        }

# =============================================================================
# Base Agent Cache
# =============================================================================

class BaseAgentCache:
    """Shared caching functionality for all agents"""
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl: Dict[str, int] = {
            AnalysisDepth.QUICK.value: 1800,      # 30 minutes
            AnalysisDepth.STANDARD.value: 3600,   # 1 hour
            AnalysisDepth.DEEP.value: 7200        # 2 hours
        }
    
    def generate_cache_key(self, request: AgentRequest) -> str:
        """Generate cache key for request"""
        cache_data = {
            'agent_type': request.agent_type.value,
            'query_type': request.query_type,
            'context': sorted(request.context.items()) if request.context else [],
            'analysis_depth': request.analysis_depth.value
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, request: AgentRequest) -> Optional[AgentResponse]:
        """Get cached response"""
        cache_key = self.generate_cache_key(request)
        
        if cache_key not in self.cache:
            return None
        
        cached_item = self.cache[cache_key]
        ttl = self.default_ttl.get(request.analysis_depth.value, 3600)
        
        # Check if cache is still valid
        if time.time() - cached_item['timestamp'] > ttl:
            del self.cache[cache_key]
            return None
        
        logger.info(f"Cache hit for agent {request.agent_type.value}: {cache_key[:8]}...")
        return cached_item['response']
    
    def set(self, request: AgentRequest, response: AgentResponse):
        """Cache response"""
        cache_key = self.generate_cache_key(request)
        
        self.cache[cache_key] = {
            'response': response,
            'timestamp': time.time()
        }
        
        logger.info(f"Cached response for agent {request.agent_type.value}: {cache_key[:8]}...")
    
    def clear_expired(self) -> int:
        """Clear expired cache entries"""
        current_time = time.time()
        expired_keys = []
        
        for cache_key, cached_item in self.cache.items():
            age = current_time - cached_item['timestamp']
            if age > max(self.default_ttl.values()):
                expired_keys.append(cache_key)
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)

# =============================================================================
# Base Agent Class
# =============================================================================

class BaseSpecializedAgent(ABC):
    """
    Abstract base class for all specialized agents
    Provides common functionality and enforces consistent interface
    """
    
    def __init__(self, 
                 agent_type: AgentType,
                 youtube_api_key: str = None,
                 ai_api_key: str = None,
                 model_name: str = ""):
        self.agent_type = agent_type
        self.agent_id = agent_type.value
        self.youtube_api_key = youtube_api_key
        self.ai_api_key = ai_api_key
        self.model_name = model_name
        
        # Initialize cache
        self.cache = BaseAgentCache()
        
        # Initialize performance tracker
        self.performance_tracker = get_performance_tracker()
        
        # Map agent type to performance agent type
        self.perf_agent_type = self._map_to_perf_agent_type(agent_type)
        
        # Domain-specific keywords for validation
        self.domain_keywords = self._get_domain_keywords()
        
        logger.info(f"{self.agent_type.value} agent initialized")
    
    def _map_to_perf_agent_type(self, agent_type: AgentType) -> PerfAgentType:
        """Map base agent type to performance agent type"""
        mapping = {
            AgentType.BOSS: PerfAgentType.BOSS,
            AgentType.CONTENT_ANALYSIS: PerfAgentType.CONTENT_ANALYSIS,
            AgentType.AUDIENCE_INSIGHTS: PerfAgentType.AUDIENCE_INSIGHTS,
            AgentType.SEO_DISCOVERABILITY: PerfAgentType.SEO_DISCOVERABILITY,
            AgentType.COMPETITIVE_ANALYSIS: PerfAgentType.COMPETITIVE_ANALYSIS,
            AgentType.MONETIZATION_STRATEGY: PerfAgentType.MONETIZATION_STRATEGY
        }
        return mapping.get(agent_type, PerfAgentType.BOSS)
    
    @abstractmethod
    def _get_domain_keywords(self) -> List[str]:
        """Return domain-specific keywords for this agent"""
        pass
    
    @abstractmethod
    async def _perform_analysis(self, request: AgentRequest) -> AgentAnalysis:
        """Perform the core analysis - implemented by each agent"""
        pass
    
    async def _perform_analysis_with_tracking(self, request: AgentRequest, tracking_context: Dict[str, Any]) -> AgentAnalysis:
        """Wrapper for analysis that includes performance tracking"""
        return await self._perform_analysis(request)
    
    def track_model_usage(self, tracking_context: Dict[str, Any], model_name: str, 
                         provider: ModelProvider, input_tokens: int, output_tokens: int, cost_estimate: float):
        """Helper method for subclasses to track model usage"""
        self.performance_tracker.track_model_usage(
            tracking_context, model_name, provider, input_tokens, output_tokens, cost_estimate
        )
    
    def track_fallback_usage(self, tracking_context: Dict[str, Any], fallback_model: str):
        """Helper method for subclasses to track fallback model usage"""
        self.performance_tracker.track_fallback_usage(tracking_context, fallback_model)
    
    async def process_boss_agent_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for boss agent requests
        This is the standardized interface all agents must implement
        """
        request_id = request_data.get('request_id', str(uuid.uuid4()))
        user_id = request_data.get('user_id', 'unknown')
        request_type = request_data.get('query_type', 'general')
        analysis_depth = request_data.get('analysis_depth', 'standard')
        
        # Start performance tracking
        async with self.performance_tracker.track_agent_request(
            agent_type=self.perf_agent_type,
            user_id=user_id,
            request_type=request_type,
            analysis_depth=analysis_depth
        ) as tracking_context:
            
            try:
                # Parse and validate request
                request = self._parse_boss_request(request_data)
                
                # Track request size
                request_size = len(json.dumps(request_data).encode())
                
                # Validate domain match
                if not self._is_valid_domain_request(request_data):
                    response_data = self._create_domain_mismatch_response(request_id, time.time())
                    response_size = len(json.dumps(response_data).encode())
                    self.performance_tracker.track_request_size(tracking_context, request_size, response_size)
                    return response_data
                
                # Check cache first
                cache_start = time.time()
                tracking_context['cache_start_time'] = cache_start
                
                cached_response = self.cache.get(request)
                if cached_response:
                    self.performance_tracker.track_cache_operation(
                        tracking_context, 
                        cache_hit=True,
                        cache_key=self.cache.generate_cache_key(request)
                    )
                    response_data = self._format_cached_response(cached_response, request_id, time.time())
                    response_size = len(json.dumps(response_data).encode())
                    self.performance_tracker.track_request_size(tracking_context, request_size, response_size)
                    return response_data
                else:
                    self.performance_tracker.track_cache_operation(
                        tracking_context, 
                        cache_hit=False,
                        cache_key=self.cache.generate_cache_key(request)
                    )
                
                # Perform analysis with model tracking
                tracking_context['model_start_time'] = time.time()
                analysis_result = await self._perform_analysis_with_tracking(request, tracking_context)
                
                # Create response
                response = self._create_success_response(
                    request, 
                    analysis_result, 
                    request_id, 
                    time.time()
                )
                
                # Track confidence score
                self.performance_tracker.track_confidence_score(tracking_context, response.confidence_score)
                
                # Cache the response
                self.cache.set(request, response)
                
                # Track response size
                response_data = response.to_dict()
                response_size = len(json.dumps(response_data).encode())
                self.performance_tracker.track_request_size(tracking_context, request_size, response_size)
                
                logger.info(f"{self.agent_type.value} completed task: {request_id}")
                return response_data
                
            except Exception as e:
                logger.error(f"{self.agent_type.value} error: {e}")
                response_data = self._create_error_response(request_id, str(e), time.time())
                response_size = len(json.dumps(response_data).encode())
                self.performance_tracker.track_request_size(tracking_context, 
                    len(json.dumps(request_data).encode()), response_size)
                return response_data
    
    def _parse_boss_request(self, request_data: Dict[str, Any]) -> AgentRequest:
        """Parse boss agent request into standard format"""
        context = request_data.get('context', {})
        token_budget_data = request_data.get('token_budget', {})
        
        return AgentRequest(
            request_id=request_data.get('request_id', str(uuid.uuid4())),
            agent_type=self.agent_type,
            query_type=request_data.get('query_type', ''),
            context=context,
            token_budget=TokenBudget(
                input_tokens=token_budget_data.get('input_tokens', 3000),
                output_tokens=token_budget_data.get('output_tokens', 1500)
            ),
            analysis_depth=AnalysisDepth(request_data.get('analysis_depth', 'standard')),
            boss_agent_token=request_data.get('boss_agent_token', ''),
            timestamp=request_data.get('timestamp', datetime.now().isoformat()),
            user_context=request_data.get('user_context', {})
        )
    
    def _is_valid_domain_request(self, request_data: Dict[str, Any]) -> bool:
        """Check if request is within this agent's domain"""
        query_type = request_data.get('query_type', '').lower()
        message_content = request_data.get('message', '').lower()
        
        # Check if agent type matches
        if query_type == self.agent_type.value:
            return True
        
        # Check domain keywords
        return any(keyword in message_content for keyword in self.domain_keywords)
    
    def _create_success_response(self, 
                               request: AgentRequest, 
                               analysis: AgentAnalysis,
                               request_id: str,
                               start_time: float) -> AgentResponse:
        """Create successful response"""
        processing_time = time.time() - start_time
        
        return AgentResponse(
            agent_type=self.agent_type,
            response_id=str(uuid.uuid4()),
            request_id=request_id,
            timestamp=datetime.now().isoformat(),
            confidence_score=self._calculate_confidence_score(analysis),
            data_freshness=datetime.now().isoformat(),
            domain_match=True,
            analysis=analysis,
            token_usage=TokenUsage(
                input_tokens=request.token_budget.input_tokens,
                output_tokens=request.token_budget.output_tokens,
                model=self.model_name
            ),
            cache_info=CacheInfo(
                cache_hit=False,
                cache_key=self.cache.generate_cache_key(request),
                ttl_remaining=self.cache.default_ttl.get(request.analysis_depth.value, 3600)
            ),
            processing_time=round(processing_time, 2),
            for_boss_agent_only=True
        )
    
    def _format_cached_response(self, 
                              cached_response: AgentResponse, 
                              request_id: str, 
                              start_time: float) -> Dict[str, Any]:
        """Format cached response with updated metadata"""
        processing_time = time.time() - start_time
        
        # Update response metadata
        cached_response.request_id = request_id
        cached_response.timestamp = datetime.now().isoformat()
        cached_response.processing_time = round(processing_time, 2)
        cached_response.cache_info.cache_hit = True
        
        return cached_response.to_dict()
    
    def _create_domain_mismatch_response(self, request_id: str, start_time: float) -> Dict[str, Any]:
        """Create response for out-of-domain requests"""
        processing_time = time.time() - start_time
        
        analysis = AgentAnalysis(
            summary="Request outside agent domain",
            key_insights=[AgentInsight(
                insight="This request should be handled by a different specialized agent",
                evidence="Domain keywords do not match agent specialization",
                impact="Low",
                confidence=1.0
            )]
        )
        
        response = AgentResponse(
            agent_type=self.agent_type,
            response_id=str(uuid.uuid4()),
            request_id=request_id,
            timestamp=datetime.now().isoformat(),
            confidence_score=0.0,
            data_freshness=datetime.now().isoformat(),
            domain_match=False,
            analysis=analysis,
            processing_time=round(processing_time, 2),
            for_boss_agent_only=True
        )
        
        return response.to_dict()
    
    def _create_error_response(self, request_id: str, error_message: str, start_time: float) -> Dict[str, Any]:
        """Create error response"""
        processing_time = time.time() - start_time
        
        analysis = AgentAnalysis(
            summary=f"{self.agent_type.value} analysis failed",
            key_insights=[AgentInsight(
                insight=f"Analysis error: {error_message}",
                evidence="Exception occurred during processing",
                impact="High",
                confidence=1.0
            )]
        )
        
        response = AgentResponse(
            agent_type=self.agent_type,
            response_id=str(uuid.uuid4()),
            request_id=request_id,
            timestamp=datetime.now().isoformat(),
            confidence_score=0.0,
            data_freshness=datetime.now().isoformat(),
            domain_match=True,
            analysis=analysis,
            processing_time=round(processing_time, 2),
            for_boss_agent_only=True
        )
        
        return response.to_dict()
    
    def _calculate_confidence_score(self, analysis: AgentAnalysis) -> float:
        """Calculate confidence score based on analysis quality"""
        if not analysis.key_insights:
            return 0.5
        
        # Average confidence from insights
        total_confidence = sum(insight.confidence for insight in analysis.key_insights)
        avg_confidence = total_confidence / len(analysis.key_insights)
        
        # Adjust based on number of insights (more insights = higher confidence)
        insight_factor = min(len(analysis.key_insights) / 5, 1.0)
        
        # Adjust based on recommendations (actionable = higher confidence)
        rec_factor = min(len(analysis.recommendations) / 3, 1.0) * 0.1
        
        final_confidence = (avg_confidence * 0.8) + (insight_factor * 0.1) + rec_factor
        return round(min(final_confidence, 1.0), 2)

# =============================================================================
# Utility Functions
# =============================================================================

def get_channel_context(user_context: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize channel context from user data"""
    if not user_context or 'channel_info' not in user_context:
        return {
            'name': 'Unknown',
            'niche': 'Unknown',
            'subscriber_count': 0,
            'avg_view_count': 0,
            'content_type': 'Unknown'
        }
    
    channel_info = user_context['channel_info']
    return {
        'name': channel_info.get('name', 'Unknown'),
        'niche': channel_info.get('niche', 'Unknown'),
        'subscriber_count': channel_info.get('subscriber_count', 0),
        'avg_view_count': channel_info.get('avg_view_count', 0),
        'content_type': channel_info.get('content_type', 'Unknown'),
        'upload_frequency': channel_info.get('upload_frequency', 'Unknown'),
        'monetization_status': channel_info.get('monetization_status', 'Unknown'),
        'primary_goal': channel_info.get('primary_goal', 'Unknown')
    }

def create_insight(insight: str, evidence: str, impact: str = "Medium", confidence: float = 0.8) -> AgentInsight:
    """Helper function to create standardized insights"""
    return AgentInsight(
        insight=insight,
        evidence=evidence,
        impact=impact,
        confidence=confidence
    )

def create_recommendation(recommendation: str, 
                        expected_impact: str = "Medium",
                        implementation_difficulty: str = "Medium",
                        reasoning: str = "") -> AgentRecommendation:
    """Helper function to create standardized recommendations"""
    return AgentRecommendation(
        recommendation=recommendation,
        expected_impact=expected_impact,
        implementation_difficulty=implementation_difficulty,
        reasoning=reasoning
    )

def validate_api_keys(**api_keys) -> Dict[str, bool]:
    """Validate that required API keys are available"""
    validation_results = {}
    for key_name, key_value in api_keys.items():
        validation_results[key_name] = bool(key_value and key_value != "demo_key")
    return validation_results