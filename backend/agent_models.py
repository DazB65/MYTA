"""
Agent Data Models and Enums for CreatorMate Boss Agent System
Common data structures used across the multi-agent system
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

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