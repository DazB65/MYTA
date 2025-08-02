"""
Agent Performance Monitoring Data Models
Comprehensive performance tracking for the multi-agent system
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic.v1 import BaseModel, Field
from dataclasses import dataclass
import json

class AgentType(str, Enum):
    """Enum for different agent types in the system"""
    BOSS = "boss_agent"
    CONTENT_ANALYSIS = "content_analysis_agent"
    AUDIENCE_INSIGHTS = "audience_insights_agent"
    SEO_DISCOVERABILITY = "seo_discoverability_agent"
    COMPETITIVE_ANALYSIS = "competitive_analysis_agent"
    MONETIZATION_STRATEGY = "monetization_strategy_agent"

class ModelProvider(str, Enum):
    """Enum for AI model providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"

class RequestStatus(str, Enum):
    """Enum for request status tracking"""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    CACHE_HIT = "cache_hit"

class AlertSeverity(str, Enum):
    """Enum for alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ModelUsage:
    """Data class for tracking model usage metrics"""
    model_name: str
    provider: ModelProvider
    input_tokens: int
    output_tokens: int
    cost_estimate: float
    latency_ms: float

class AgentPerformanceMetric(BaseModel):
    """Individual performance metric for an agent request"""
    
    # Request identification
    request_id: str
    agent_type: AgentType
    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: str
    
    # Request details
    request_type: str  # e.g., "content_analysis", "quick_analysis"
    request_size_bytes: int
    response_size_bytes: int
    
    # Performance metrics
    total_latency_ms: float
    agent_processing_time_ms: float
    model_latency_ms: float
    cache_lookup_time_ms: Optional[float] = None
    
    # Model usage
    model_usage: ModelUsage
    fallback_used: bool = False
    fallback_model: Optional[str] = None
    
    # Status and errors
    status: RequestStatus
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    
    # Cache performance
    cache_hit: bool = False
    cache_key: Optional[str] = None
    cache_ttl_remaining: Optional[int] = None
    
    # Business metrics
    analysis_depth: str  # "quick", "standard", "deep"
    confidence_score: Optional[float] = None
    
    class Config:
        use_enum_values = True

class AgentHealthSnapshot(BaseModel):
    """Aggregated health metrics for an agent over a time period"""
    
    agent_type: AgentType
    timestamp: datetime = Field(default_factory=datetime.now)
    time_window_minutes: int = Field(default=60)
    
    # Volume metrics
    total_requests: int
    successful_requests: int
    failed_requests: int
    cache_hits: int
    
    # Performance metrics
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    max_latency_ms: float
    
    # Model usage metrics
    total_input_tokens: int
    total_output_tokens: int
    total_cost_estimate: float
    
    # Error analysis
    error_rate: float
    timeout_rate: float
    rate_limit_rate: float
    
    # Cache performance
    cache_hit_rate: float
    avg_cache_lookup_time_ms: float
    
    # Health score (0-100)
    health_score: float
    
    class Config:
        use_enum_values = True

class SystemPerformanceSnapshot(BaseModel):
    """Overall system performance metrics"""
    
    timestamp: datetime = Field(default_factory=datetime.now)
    time_window_minutes: int = Field(default=60)
    
    # System-wide metrics
    total_requests: int
    total_users: int
    avg_requests_per_user: float
    
    # Performance distribution
    boss_agent_bottleneck_rate: float  # % of requests where boss agent is slowest
    avg_agent_coordination_time_ms: float
    
    # Cost metrics
    total_cost_estimate: float
    cost_per_request: float
    cost_per_user: float
    
    # Agent health summary
    agent_health_scores: Dict[str, float]
    unhealthy_agents: List[str]
    
    # System health score (0-100)
    overall_health_score: float
    
    class Config:
        use_enum_values = True

class PerformanceAlert(BaseModel):
    """Performance alert model"""
    
    alert_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    severity: AlertSeverity
    alert_type: str  # e.g., "high_latency", "error_spike", "cost_spike"
    
    # Alert details
    agent_type: Optional[AgentType] = None
    metric_name: str
    current_value: float
    threshold_value: float
    
    # Context
    description: str
    recommendation: str
    time_window_minutes: int
    
    # Status
    acknowledged: bool = False
    resolved: bool = False
    acknowledged_by: Optional[str] = None
    resolved_by: Optional[str] = None
    
    class Config:
        use_enum_values = True

class CostOptimizationRecommendation(BaseModel):
    """Cost optimization recommendation"""
    
    recommendation_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Recommendation details
    type: str  # e.g., "model_selection", "caching_improvement", "request_batching"
    priority: str  # "high", "medium", "low"
    estimated_savings_per_day: float
    implementation_effort: str  # "low", "medium", "high"
    
    # Context
    description: str
    current_cost_per_day: float
    projected_cost_per_day: float
    affected_agents: List[AgentType]
    
    # Implementation
    implementation_steps: List[str]
    risks: List[str]
    
    # Status
    implemented: bool = False
    implemented_date: Optional[datetime] = None
    actual_savings: Optional[float] = None
    
    class Config:
        use_enum_values = True

class MonitoringConfiguration(BaseModel):
    """Configuration for monitoring system"""
    
    # Metric collection settings
    collect_detailed_metrics: bool = True
    metric_retention_days: int = 30
    aggregate_interval_minutes: int = 5
    
    # Alert thresholds
    latency_alert_threshold_ms: float = 5000
    error_rate_alert_threshold: float = 0.05
    cost_spike_threshold_multiplier: float = 2.0
    health_score_alert_threshold: float = 70.0
    
    # Cache settings
    enable_performance_caching: bool = True
    cache_metrics_ttl_seconds: int = 300
    
    # Cost tracking
    track_detailed_costs: bool = True
    cost_alert_threshold_per_day: float = 100.0
    
    # Dashboard settings
    dashboard_refresh_interval_seconds: int = 30
    max_dashboard_history_hours: int = 24

# Database schema helper
def get_performance_tables_schema() -> List[str]:
    """Get SQL schema for performance monitoring tables"""
    return [
        """
        CREATE TABLE IF NOT EXISTS agent_performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT NOT NULL,
            agent_type TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            user_id TEXT NOT NULL,
            request_type TEXT NOT NULL,
            request_size_bytes INTEGER,
            response_size_bytes INTEGER,
            total_latency_ms REAL,
            agent_processing_time_ms REAL,
            model_latency_ms REAL,
            cache_lookup_time_ms REAL,
            model_name TEXT,
            model_provider TEXT,
            input_tokens INTEGER,
            output_tokens INTEGER,
            cost_estimate REAL,
            fallback_used BOOLEAN,
            fallback_model TEXT,
            status TEXT NOT NULL,
            error_message TEXT,
            error_type TEXT,
            cache_hit BOOLEAN,
            cache_key TEXT,
            cache_ttl_remaining INTEGER,
            analysis_depth TEXT,
            confidence_score REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS agent_health_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_type TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            time_window_minutes INTEGER,
            total_requests INTEGER,
            successful_requests INTEGER,
            failed_requests INTEGER,
            cache_hits INTEGER,
            avg_latency_ms REAL,
            p95_latency_ms REAL,
            p99_latency_ms REAL,
            max_latency_ms REAL,
            total_input_tokens INTEGER,
            total_output_tokens INTEGER,
            total_cost_estimate REAL,
            error_rate REAL,
            timeout_rate REAL,
            rate_limit_rate REAL,
            cache_hit_rate REAL,
            avg_cache_lookup_time_ms REAL,
            health_score REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS system_performance_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            time_window_minutes INTEGER,
            total_requests INTEGER,
            total_users INTEGER,
            avg_requests_per_user REAL,
            boss_agent_bottleneck_rate REAL,
            avg_agent_coordination_time_ms REAL,
            total_cost_estimate REAL,
            cost_per_request REAL,
            cost_per_user REAL,
            agent_health_scores TEXT, -- JSON
            unhealthy_agents TEXT, -- JSON
            overall_health_score REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS performance_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_id TEXT UNIQUE NOT NULL,
            timestamp DATETIME NOT NULL,
            severity TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            agent_type TEXT,
            metric_name TEXT NOT NULL,
            current_value REAL,
            threshold_value REAL,
            description TEXT,
            recommendation TEXT,
            time_window_minutes INTEGER,
            acknowledged BOOLEAN DEFAULT FALSE,
            resolved BOOLEAN DEFAULT FALSE,
            acknowledged_by TEXT,
            resolved_by TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_agent_metrics_timestamp ON agent_performance_metrics(timestamp);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_agent_metrics_agent_type ON agent_performance_metrics(agent_type);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_agent_metrics_user_id ON agent_performance_metrics(user_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_health_snapshots_timestamp ON agent_health_snapshots(timestamp);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_performance_alerts_timestamp ON performance_alerts(timestamp);
        """
    ]