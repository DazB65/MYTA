"""
Agent Performance Tracking System
Real-time performance monitoring and metrics collection for the multi-agent system
"""

import time
import uuid
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Callable
from contextlib import asynccontextmanager
from dataclasses import asdict
import sqlite3
from threading import Lock
import logging

from .agent_performance_models import (
    AgentPerformanceMetric, AgentHealthSnapshot, SystemPerformanceSnapshot,
    PerformanceAlert, AgentType, ModelProvider, RequestStatus, AlertSeverity,
    ModelUsage, MonitoringConfiguration, get_performance_tables_schema
)
from .database import get_database_manager
import sqlite3
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.PERFORMANCE)

class PerformanceTracker:
    """Central performance tracking system for multi-agent monitoring"""
    
    def __init__(self, config: MonitoringConfiguration = None):
        self.config = config or MonitoringConfiguration()
        self._metrics_buffer: List[AgentPerformanceMetric] = []
        self._buffer_lock = Lock()
        self._last_flush = datetime.now()
        self._alert_callbacks: List[Callable] = []
        
        # Initialize database schema
        self._init_database()
        
        logger.info("Performance tracker initialized", extra={
            'category': LogCategory.MONITORING.value,
            'metadata': {
                'config': asdict(self.config) if hasattr(self.config, '__dict__') else str(self.config)
            }
        })
    
    def _init_database(self):
        """Initialize performance tracking database schema"""
        try:
            db_manager = get_database_manager()
            with sqlite3.connect(db_manager.db_path) as conn:
                cursor = conn.cursor()
                
                # Create all performance tracking tables
                for schema_sql in get_performance_tables_schema():
                    cursor.execute(schema_sql)
                
                conn.commit()
                logger.info("Performance tracking database schema initialized")
                
        except Exception as e:
            logger.error(f"Failed to initialize performance database: {e}", exc_info=True)
            raise
    
    @asynccontextmanager
    async def track_agent_request(
        self, 
        agent_type: AgentType, 
        user_id: str, 
        request_type: str,
        analysis_depth: str = "standard"
    ):
        """Context manager for tracking agent request performance"""
        
        request_id = str(uuid.uuid4())
        start_time = time.time()
        model_start_time = None
        cache_start_time = None
        
        # Initialize metric object
        metric = AgentPerformanceMetric(
            request_id=request_id,
            agent_type=agent_type,
            user_id=user_id,
            request_type=request_type,
            analysis_depth=analysis_depth,
            request_size_bytes=0,  # Will be updated
            response_size_bytes=0,  # Will be updated
            total_latency_ms=0,
            agent_processing_time_ms=0,
            model_latency_ms=0,
            model_usage=ModelUsage(
                model_name="",
                provider=ModelProvider.OPENAI,
                input_tokens=0,
                output_tokens=0,
                cost_estimate=0.0,
                latency_ms=0.0
            ),
            status=RequestStatus.SUCCESS
        )
        
        # Create tracking context
        tracking_context = {
            'metric': metric,
            'start_time': start_time,
            'model_start_time': None,
            'cache_start_time': None
        }
        
        try:
            yield tracking_context
            
            # Calculate final metrics
            end_time = time.time()
            metric.total_latency_ms = (end_time - start_time) * 1000
            metric.agent_processing_time_ms = metric.total_latency_ms - metric.model_latency_ms
            
            if metric.cache_lookup_time_ms:
                metric.agent_processing_time_ms -= metric.cache_lookup_time_ms
            
            # Record successful completion
            self._record_metric(metric)
            
        except Exception as e:
            # Record error
            end_time = time.time()
            metric.total_latency_ms = (end_time - start_time) * 1000
            metric.status = RequestStatus.ERROR
            metric.error_message = str(e)
            metric.error_type = type(e).__name__
            
            self._record_metric(metric)
            
            # Re-raise the exception
            raise
    
    def track_model_usage(
        self, 
        tracking_context: Dict[str, Any],
        model_name: str,
        provider: ModelProvider,
        input_tokens: int,
        output_tokens: int,
        cost_estimate: float
    ):
        """Track model usage within a request context"""
        
        if not tracking_context.get('model_start_time'):
            tracking_context['model_start_time'] = time.time()
        
        model_end_time = time.time()
        model_latency = (model_end_time - tracking_context['model_start_time']) * 1000
        
        # Update model usage in metric
        metric = tracking_context['metric']
        metric.model_usage = ModelUsage(
            model_name=model_name,
            provider=provider,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_estimate=cost_estimate,
            latency_ms=model_latency
        )
        metric.model_latency_ms = model_latency
    
    def track_cache_operation(
        self,
        tracking_context: Dict[str, Any],
        cache_hit: bool,
        cache_key: str = None,
        cache_ttl_remaining: int = None
    ):
        """Track cache operation performance"""
        
        if not tracking_context.get('cache_start_time'):
            tracking_context['cache_start_time'] = time.time()
        
        cache_end_time = time.time()
        cache_latency = (cache_end_time - tracking_context['cache_start_time']) * 1000
        
        # Update cache metrics
        metric = tracking_context['metric']
        metric.cache_hit = cache_hit
        metric.cache_key = cache_key
        metric.cache_ttl_remaining = cache_ttl_remaining
        metric.cache_lookup_time_ms = cache_latency
        
        if cache_hit:
            metric.status = RequestStatus.CACHE_HIT
    
    def track_fallback_usage(
        self,
        tracking_context: Dict[str, Any],
        fallback_model: str
    ):
        """Track when fallback models are used"""
        
        metric = tracking_context['metric']
        metric.fallback_used = True
        metric.fallback_model = fallback_model
    
    def track_request_size(
        self,
        tracking_context: Dict[str, Any],
        request_size_bytes: int,
        response_size_bytes: int
    ):
        """Track request and response sizes"""
        
        metric = tracking_context['metric']
        metric.request_size_bytes = request_size_bytes
        metric.response_size_bytes = response_size_bytes
    
    def track_confidence_score(
        self,
        tracking_context: Dict[str, Any],
        confidence_score: float
    ):
        """Track agent confidence score"""
        
        metric = tracking_context['metric']
        metric.confidence_score = confidence_score
    
    def _record_metric(self, metric: AgentPerformanceMetric):
        """Record a performance metric"""
        
        try:
            # Add to buffer
            with self._buffer_lock:
                self._metrics_buffer.append(metric)
            
            # Check if we need to flush
            if len(self._metrics_buffer) >= 50 or \
               (datetime.now() - self._last_flush).seconds >= 30:
                asyncio.create_task(self._flush_metrics())
            
            # Check for alerts
            self._check_for_alerts(metric)
            
        except Exception as e:
            logger.error(f"Failed to record performance metric: {e}", exc_info=True)
    
    async def _flush_metrics(self):
        """Flush metrics buffer to database"""
        
        if not self._metrics_buffer:
            return
        
        try:
            # Get metrics to flush
            with self._buffer_lock:
                metrics_to_flush = self._metrics_buffer.copy()
                self._metrics_buffer.clear()
                self._last_flush = datetime.now()
            
            # Insert into database
            db_manager = get_database_manager()
            with sqlite3.connect(db_manager.db_path) as conn:
                cursor = conn.cursor()
                
                for metric in metrics_to_flush:
                    cursor.execute("""
                        INSERT INTO agent_performance_metrics (
                            request_id, agent_type, timestamp, user_id, request_type,
                            request_size_bytes, response_size_bytes, total_latency_ms,
                            agent_processing_time_ms, model_latency_ms, cache_lookup_time_ms,
                            model_name, model_provider, input_tokens, output_tokens,
                            cost_estimate, fallback_used, fallback_model, status,
                            error_message, error_type, cache_hit, cache_key,
                            cache_ttl_remaining, analysis_depth, confidence_score
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        metric.request_id, metric.agent_type.value, metric.timestamp,
                        metric.user_id, metric.request_type, metric.request_size_bytes,
                        metric.response_size_bytes, metric.total_latency_ms,
                        metric.agent_processing_time_ms, metric.model_latency_ms,
                        metric.cache_lookup_time_ms, metric.model_usage.model_name,
                        metric.model_usage.provider.value, metric.model_usage.input_tokens,
                        metric.model_usage.output_tokens, metric.model_usage.cost_estimate,
                        metric.fallback_used, metric.fallback_model, metric.status.value,
                        metric.error_message, metric.error_type, metric.cache_hit,
                        metric.cache_key, metric.cache_ttl_remaining, metric.analysis_depth,
                        metric.confidence_score
                    ))
                
                conn.commit()
                
            logger.info(f"Flushed {len(metrics_to_flush)} performance metrics to database")
            
        except Exception as e:
            logger.error(f"Failed to flush performance metrics: {e}", exc_info=True)
    
    def _check_for_alerts(self, metric: AgentPerformanceMetric):
        """Check if metric triggers any alerts"""
        
        try:
            alerts = []
            
            # High latency alert
            if metric.total_latency_ms > self.config.latency_alert_threshold_ms:
                alerts.append(PerformanceAlert(
                    alert_id=str(uuid.uuid4()),
                    severity=AlertSeverity.HIGH if metric.total_latency_ms > self.config.latency_alert_threshold_ms * 2 else AlertSeverity.MEDIUM,
                    alert_type="high_latency",
                    agent_type=metric.agent_type,
                    metric_name="total_latency_ms",
                    current_value=metric.total_latency_ms,
                    threshold_value=self.config.latency_alert_threshold_ms,
                    description=f"High latency detected for {metric.agent_type.value}: {metric.total_latency_ms:.2f}ms",
                    recommendation="Check model performance and consider optimization",
                    time_window_minutes=1
                ))
            
            # Error alert
            if metric.status == RequestStatus.ERROR:
                alerts.append(PerformanceAlert(
                    alert_id=str(uuid.uuid4()),
                    severity=AlertSeverity.HIGH,
                    alert_type="agent_error",
                    agent_type=metric.agent_type,
                    metric_name="error_rate",
                    current_value=1.0,
                    threshold_value=0.0,
                    description=f"Agent error in {metric.agent_type.value}: {metric.error_message}",
                    recommendation="Investigate error cause and implement fix",
                    time_window_minutes=1
                ))
            
            # High cost alert
            if metric.model_usage.cost_estimate > 1.0:  # $1 per request is high
                alerts.append(PerformanceAlert(
                    alert_id=str(uuid.uuid4()),
                    severity=AlertSeverity.MEDIUM,
                    alert_type="high_cost",
                    agent_type=metric.agent_type,
                    metric_name="cost_per_request",
                    current_value=metric.model_usage.cost_estimate,
                    threshold_value=1.0,
                    description=f"High cost request for {metric.agent_type.value}: ${metric.model_usage.cost_estimate:.2f}",
                    recommendation="Consider model optimization or caching improvements",
                    time_window_minutes=1
                ))
            
            # Record alerts
            for alert in alerts:
                self._record_alert(alert)
                
        except Exception as e:
            logger.error(f"Failed to check for alerts: {e}", exc_info=True)
    
    def _record_alert(self, alert: PerformanceAlert):
        """Record a performance alert"""
        
        try:
            db_manager = get_database_manager()
            with sqlite3.connect(db_manager.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO performance_alerts (
                        alert_id, timestamp, severity, alert_type, agent_type,
                        metric_name, current_value, threshold_value, description,
                        recommendation, time_window_minutes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert.alert_id, alert.timestamp, alert.severity.value,
                    alert.alert_type, alert.agent_type.value if alert.agent_type else None,
                    alert.metric_name, alert.current_value, alert.threshold_value,
                    alert.description, alert.recommendation, alert.time_window_minutes
                ))
                
                conn.commit()
            
            # Trigger alert callbacks
            for callback in self._alert_callbacks:
                try:
                    callback(alert)
                except Exception as e:
                    logger.error(f"Alert callback failed: {e}")
            
            logger.warning(f"Performance alert triggered: {alert.alert_type} - {alert.description}")
            
        except Exception as e:
            logger.error(f"Failed to record alert: {e}", exc_info=True)
    
    def add_alert_callback(self, callback: Callable[[PerformanceAlert], None]):
        """Add callback for performance alerts"""
        self._alert_callbacks.append(callback)
    
    async def get_agent_health(self, agent_type: AgentType = None, time_window_minutes: int = 60) -> List[AgentHealthSnapshot]:
        """Get agent health metrics for specified time window"""
        
        try:
            db_manager = get_database_manager()
            with sqlite3.connect(db_manager.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate time window
                start_time = datetime.now() - timedelta(minutes=time_window_minutes)
                
                # Build query
                where_clause = "timestamp >= ?"
                params = [start_time]
                
                if agent_type:
                    where_clause += " AND agent_type = ?"
                    params.append(agent_type.value)
                
                # Get aggregated metrics (using parameterized query)
                query = """
                    SELECT
                        agent_type,
                        COUNT(*) as total_requests,
                        SUM(CASE WHEN status = 'success' OR status = 'cache_hit' THEN 1 ELSE 0 END) as successful_requests,
                        SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as failed_requests,
                        SUM(CASE WHEN status = 'timeout' THEN 1 ELSE 0 END) as timeout_requests,
                        SUM(CASE WHEN status = 'rate_limited' THEN 1 ELSE 0 END) as rate_limited_requests,
                        SUM(CASE WHEN cache_hit = 1 THEN 1 ELSE 0 END) as cache_hits,
                        AVG(total_latency_ms) as avg_latency_ms,
                        MAX(total_latency_ms) as max_latency_ms,
                        SUM(input_tokens) as total_input_tokens,
                        SUM(output_tokens) as total_output_tokens,
                        SUM(cost_estimate) as total_cost_estimate,
                        AVG(CASE WHEN cache_lookup_time_ms IS NOT NULL THEN cache_lookup_time_ms ELSE 0 END) as avg_cache_lookup_time_ms
                    FROM agent_performance_metrics
                    WHERE """ + where_clause + """
                    GROUP BY agent_type
                """
                cursor.execute(query, params)
                
                results = cursor.fetchall()
                health_snapshots = []
                
                for row in results:
                    (agent_type_str, total_requests, successful_requests, failed_requests,
                     timeout_requests, rate_limited_requests, cache_hits, avg_latency_ms, max_latency_ms, total_input_tokens,
                     total_output_tokens, total_cost_estimate, avg_cache_lookup_time_ms) = row
                    
                    # Calculate percentiles (simplified)
                    cursor.execute(f"""
                        SELECT total_latency_ms 
                        FROM agent_performance_metrics 
                        WHERE agent_type = ? AND timestamp >= ?
                        ORDER BY total_latency_ms
                    """, [agent_type_str, start_time])
                    
                    latencies = [row[0] for row in cursor.fetchall()]
                    p95_latency = latencies[int(len(latencies) * 0.95)] if latencies else 0
                    p99_latency = latencies[int(len(latencies) * 0.99)] if latencies else 0
                    
                    # Calculate rates
                    error_rate = failed_requests / total_requests if total_requests > 0 else 0
                    timeout_rate = timeout_requests / total_requests if total_requests > 0 else 0
                    rate_limit_rate = rate_limited_requests / total_requests if total_requests > 0 else 0
                    cache_hit_rate = cache_hits / total_requests if total_requests > 0 else 0
                    
                    # Calculate health score
                    health_score = self._calculate_health_score(
                        error_rate, avg_latency_ms, cache_hit_rate
                    )
                    
                    health_snapshot = AgentHealthSnapshot(
                        agent_type=AgentType(agent_type_str),
                        time_window_minutes=time_window_minutes,
                        total_requests=total_requests,
                        successful_requests=successful_requests,
                        failed_requests=failed_requests,
                        cache_hits=cache_hits,
                        avg_latency_ms=avg_latency_ms or 0,
                        p95_latency_ms=p95_latency,
                        p99_latency_ms=p99_latency,
                        max_latency_ms=max_latency_ms or 0,
                        total_input_tokens=total_input_tokens or 0,
                        total_output_tokens=total_output_tokens or 0,
                        total_cost_estimate=total_cost_estimate or 0,
                        error_rate=error_rate,
                        timeout_rate=timeout_rate,
                        rate_limit_rate=rate_limit_rate,
                        cache_hit_rate=cache_hit_rate,
                        avg_cache_lookup_time_ms=avg_cache_lookup_time_ms or 0,
                        health_score=health_score
                    )
                    
                    health_snapshots.append(health_snapshot)
                
                return health_snapshots
                
        except Exception as e:
            logger.error(f"Failed to get agent health: {e}", exc_info=True)
            return []
    
    def _calculate_health_score(self, error_rate: float, avg_latency_ms: float, cache_hit_rate: float) -> float:
        """Calculate health score based on performance metrics"""
        
        # Start with perfect score
        score = 100.0
        
        # Penalize high error rates
        score -= error_rate * 50  # 50 point penalty for 100% error rate
        
        # Penalize high latency
        if avg_latency_ms > 1000:  # 1 second
            score -= min(30, (avg_latency_ms - 1000) / 100)  # Up to 30 points
        
        # Reward good cache hit rate
        if cache_hit_rate > 0.5:
            score += (cache_hit_rate - 0.5) * 20  # Up to 10 points bonus
        
        return max(0, min(100, score))

# Global performance tracker instance
_performance_tracker = None

def get_performance_tracker() -> PerformanceTracker:
    """Get global performance tracker instance"""
    global _performance_tracker
    if _performance_tracker is None:
        _performance_tracker = PerformanceTracker()
    return _performance_tracker

def init_performance_tracking():
    """Initialize performance tracking system"""
    get_performance_tracker()
    logger.info("Performance tracking system initialized")