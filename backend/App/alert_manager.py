"""
Real-time Alert Management System
Handles alert generation, notification, and resolution for performance monitoring
"""

import asyncio
import smtplib
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass
from enum import Enum
import logging

from .agent_performance_models import (
    PerformanceAlert, AlertSeverity, AgentType,
    AgentHealthSnapshot, SystemPerformanceSnapshot
)
from .agent_performance_tracker import get_performance_tracker
from .database import get_database_manager
from .logging_config import get_logger, LogCategory
from .config import get_settings

logger = get_logger(__name__, LogCategory.MONITORING)

class AlertChannel(Enum):
    """Available alert notification channels"""
    EMAIL = "email"
    WEBHOOK = "webhook"
    LOG = "log"
    DASHBOARD = "dashboard"

@dataclass
class AlertRule:
    """Configuration for alert rules"""
    rule_id: str
    name: str
    description: str
    metric: str
    operator: str  # "gt", "lt", "eq", "gte", "lte"
    threshold: float
    severity: AlertSeverity
    time_window_minutes: int
    agent_type: Optional[AgentType] = None
    enabled: bool = True
    channels: List[AlertChannel] = None
    
    def __post_init__(self):
        if self.channels is None:
            self.channels = [AlertChannel.LOG, AlertChannel.DASHBOARD]

class AlertManager:
    """Manages real-time alerting for performance monitoring"""
    
    def __init__(self):
        self.settings = get_settings()
        self.alert_rules = self._load_default_alert_rules()
        self.notification_handlers = {
            AlertChannel.EMAIL: self._send_email_alert,
            AlertChannel.WEBHOOK: self._send_webhook_alert,
            AlertChannel.LOG: self._log_alert,
            AlertChannel.DASHBOARD: self._update_dashboard_alert
        }
        self.alert_history = {}  # Track recent alerts to prevent spam
        self.alert_callbacks = []
        
        # Start background monitoring task
        self.monitoring_task = None
        self.is_monitoring = False
        
        logger.info("Alert manager initialized")
    
    def _load_default_alert_rules(self) -> List[AlertRule]:
        """Load default alert rules configuration"""
        return [
            # High latency alerts
            AlertRule(
                rule_id="high_latency_critical",
                name="Critical High Latency",
                description="Agent response time exceeds critical threshold",
                metric="avg_latency_ms",
                operator="gt",
                threshold=10000.0,  # 10 seconds
                severity=AlertSeverity.CRITICAL,
                time_window_minutes=5,
                channels=[AlertChannel.EMAIL, AlertChannel.LOG, AlertChannel.DASHBOARD]
            ),
            AlertRule(
                rule_id="high_latency_warning",
                name="High Latency Warning",
                description="Agent response time exceeds warning threshold",
                metric="avg_latency_ms",
                operator="gt",
                threshold=5000.0,  # 5 seconds
                severity=AlertSeverity.HIGH,
                time_window_minutes=5,
                channels=[AlertChannel.LOG, AlertChannel.DASHBOARD]
            ),
            
            # Error rate alerts
            AlertRule(
                rule_id="high_error_rate",
                name="High Error Rate",
                description="Agent error rate exceeds acceptable threshold",
                metric="error_rate",
                operator="gt",
                threshold=0.1,  # 10%
                severity=AlertSeverity.HIGH,
                time_window_minutes=10,
                channels=[AlertChannel.EMAIL, AlertChannel.LOG, AlertChannel.DASHBOARD]
            ),
            
            # Health score alerts
            AlertRule(
                rule_id="low_health_score",
                name="Low Agent Health Score",
                description="Agent health score indicates poor performance",
                metric="health_score",
                operator="lt",
                threshold=60.0,
                severity=AlertSeverity.MEDIUM,
                time_window_minutes=15,
                channels=[AlertChannel.LOG, AlertChannel.DASHBOARD]
            ),
            
            # Cost alerts
            AlertRule(
                rule_id="high_cost_spike",
                name="High Cost Spike",
                description="API costs are unusually high",
                metric="total_cost_estimate",
                operator="gt",
                threshold=50.0,  # $50 in time window
                severity=AlertSeverity.MEDIUM,
                time_window_minutes=60,
                channels=[AlertChannel.EMAIL, AlertChannel.LOG, AlertChannel.DASHBOARD]
            ),
            
            # Cache performance alerts
            AlertRule(
                rule_id="low_cache_hit_rate",
                name="Low Cache Hit Rate",
                description="Cache hit rate is below optimal threshold",
                metric="cache_hit_rate",
                operator="lt",
                threshold=0.3,  # 30%
                severity=AlertSeverity.LOW,
                time_window_minutes=30,
                channels=[AlertChannel.LOG, AlertChannel.DASHBOARD]
            )
        ]
    
    async def start_monitoring(self):
        """Start the real-time monitoring task"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("Alert monitoring started")
    
    async def stop_monitoring(self):
        """Stop the real-time monitoring task"""
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("Alert monitoring stopped")
    
    async def _monitoring_loop(self):
        """Main monitoring loop that checks for alert conditions"""
        while self.is_monitoring:
            try:
                await self._check_alert_conditions()
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}", exc_info=True)
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _check_alert_conditions(self):
        """Check all alert rules against current system state"""
        try:
            performance_tracker = get_performance_tracker()
            
            # Get recent health data for all agents
            agent_health_data = await performance_tracker.get_agent_health(time_window_minutes=5)
            
            for agent_health in agent_health_data:
                await self._evaluate_agent_alerts(agent_health)
            
            # Check system-wide alerts
            await self._evaluate_system_alerts(agent_health_data)
            
        except Exception as e:
            logger.error(f"Failed to check alert conditions: {e}", exc_info=True)
    
    async def _evaluate_agent_alerts(self, agent_health: AgentHealthSnapshot):
        """Evaluate alert rules for a specific agent"""
        for rule in self.alert_rules:
            if not rule.enabled:
                continue
            
            # Skip if rule is for a different agent type
            if rule.agent_type and rule.agent_type != agent_health.agent_type:
                continue
            
            # Get metric value
            metric_value = self._get_metric_value(agent_health, rule.metric)
            if metric_value is None:
                continue
            
            # Check threshold
            if self._evaluate_threshold(metric_value, rule.operator, rule.threshold):
                # Check if we should suppress duplicate alerts
                if not self._should_trigger_alert(rule, agent_health.agent_type):
                    continue
                
                # Create and trigger alert
                alert = self._create_alert(
                    rule=rule,
                    current_value=metric_value,
                    agent_type=agent_health.agent_type,
                    context={"agent_health": agent_health}
                )
                
                await self._trigger_alert(alert)
    
    async def _evaluate_system_alerts(self, agent_health_data: List[AgentHealthSnapshot]):
        """Evaluate system-wide alert conditions"""
        if not agent_health_data:
            return
        
        # Calculate system metrics
        total_requests = sum(agent.total_requests for agent in agent_health_data)
        total_cost = sum(agent.total_cost_estimate for agent in agent_health_data)
        avg_health = sum(agent.health_score for agent in agent_health_data) / len(agent_health_data)
        
        # Check system-wide rules
        system_metrics = {
            "total_requests": total_requests,
            "total_cost_estimate": total_cost,
            "avg_health_score": avg_health,
            "unhealthy_agents": len([a for a in agent_health_data if a.health_score < 60])
        }
        
        for rule in self.alert_rules:
            if not rule.enabled or rule.agent_type is not None:
                continue
            
            metric_value = system_metrics.get(rule.metric)
            if metric_value is None:
                continue
            
            if self._evaluate_threshold(metric_value, rule.operator, rule.threshold):
                if not self._should_trigger_alert(rule, None):
                    continue
                
                alert = self._create_alert(
                    rule=rule,
                    current_value=metric_value,
                    context={"system_metrics": system_metrics}
                )
                
                await self._trigger_alert(alert)
    
    def _get_metric_value(self, agent_health: AgentHealthSnapshot, metric: str) -> Optional[float]:
        """Extract metric value from agent health data"""
        metric_map = {
            "avg_latency_ms": agent_health.avg_latency_ms,
            "p95_latency_ms": agent_health.p95_latency_ms,
            "p99_latency_ms": agent_health.p99_latency_ms,
            "error_rate": agent_health.error_rate,
            "cache_hit_rate": agent_health.cache_hit_rate,
            "health_score": agent_health.health_score,
            "total_cost_estimate": agent_health.total_cost_estimate,
            "total_requests": float(agent_health.total_requests)
        }
        return metric_map.get(metric)
    
    def _evaluate_threshold(self, value: float, operator: str, threshold: float) -> bool:
        """Evaluate if value meets threshold condition"""
        operators = {
            "gt": lambda v, t: v > t,
            "gte": lambda v, t: v >= t,
            "lt": lambda v, t: v < t,
            "lte": lambda v, t: v <= t,
            "eq": lambda v, t: abs(v - t) < 0.001
        }
        return operators.get(operator, lambda v, t: False)(value, threshold)
    
    def _should_trigger_alert(self, rule: AlertRule, agent_type: Optional[AgentType]) -> bool:
        """Check if alert should be triggered (avoid spam)"""
        key = f"{rule.rule_id}_{agent_type.value if agent_type else 'system'}"
        
        # Check last alert time
        last_alert_time = self.alert_history.get(key)
        if last_alert_time:
            # Don't trigger same alert within cooldown period
            cooldown_minutes = {
                AlertSeverity.CRITICAL: 5,
                AlertSeverity.HIGH: 15,
                AlertSeverity.MEDIUM: 30,
                AlertSeverity.LOW: 60
            }.get(rule.severity, 30)
            
            if datetime.now() - last_alert_time < timedelta(minutes=cooldown_minutes):
                return False
        
        # Update alert history
        self.alert_history[key] = datetime.now()
        return True
    
    def _create_alert(self, rule: AlertRule, current_value: float, 
                     agent_type: Optional[AgentType] = None, context: Dict[str, Any] = None) -> PerformanceAlert:
        """Create a performance alert"""
        import uuid
        
        # Generate description with context
        if agent_type:
            description = f"{rule.description} - Agent: {agent_type.value}, Value: {current_value:.2f}"
        else:
            description = f"{rule.description} - System-wide, Value: {current_value:.2f}"
        
        # Generate recommendation
        recommendation = self._generate_recommendation(rule, current_value, agent_type, context)
        
        return PerformanceAlert(
            alert_id=str(uuid.uuid4()),
            severity=rule.severity,
            alert_type=rule.rule_id,
            agent_type=agent_type,
            metric_name=rule.metric,
            current_value=current_value,
            threshold_value=rule.threshold,
            description=description,
            recommendation=recommendation,
            time_window_minutes=rule.time_window_minutes
        )
    
    def _generate_recommendation(self, rule: AlertRule, current_value: float, 
                               agent_type: Optional[AgentType], context: Dict[str, Any]) -> str:
        """Generate contextual recommendations for alerts"""
        recommendations = {
            "high_latency_critical": "Immediate investigation required. Check model performance, API status, and system resources.",
            "high_latency_warning": "Monitor closely. Consider optimizing queries or increasing cache TTL.",
            "high_error_rate": "Check agent logs for error patterns. Verify API keys and model availability.",
            "low_health_score": "Review agent performance metrics and consider optimization or model switching.",
            "high_cost_spike": "Review recent usage patterns. Consider implementing request batching or cache optimization.",
            "low_cache_hit_rate": "Increase cache TTL or review cache key generation strategy."
        }
        
        base_recommendation = recommendations.get(rule.rule_id, "Review performance metrics and investigate root cause.")
        
        # Add context-specific recommendations
        if agent_type and current_value > rule.threshold * 2:
            base_recommendation += " Alert severity is high - immediate action recommended."
        
        return base_recommendation
    
    async def _trigger_alert(self, alert: PerformanceAlert):
        """Trigger alert through configured channels"""
        try:
            # Find the rule to get channel configuration
            rule = next((r for r in self.alert_rules if r.rule_id == alert.alert_type), None)
            if not rule:
                rule = AlertRule(
                    rule_id=alert.alert_type,
                    name="Unknown Alert",
                    description="Alert triggered without rule configuration",
                    metric=alert.metric_name,
                    operator="gt",
                    threshold=alert.threshold_value,
                    severity=alert.severity,
                    time_window_minutes=5,
                    channels=[AlertChannel.LOG, AlertChannel.DASHBOARD]
                )
            
            # Store alert in database
            await self._store_alert(alert)
            
            # Send notifications through configured channels
            for channel in rule.channels:
                handler = self.notification_handlers.get(channel)
                if handler:
                    try:
                        await handler(alert, rule)
                    except Exception as e:
                        logger.error(f"Failed to send alert via {channel.value}: {e}")
            
            # Trigger callbacks
            for callback in self.alert_callbacks:
                try:
                    await callback(alert)
                except Exception as e:
                    logger.error(f"Alert callback failed: {e}")
            
        except Exception as e:
            logger.error(f"Failed to trigger alert: {e}", exc_info=True)
    
    async def _store_alert(self, alert: PerformanceAlert):
        """Store alert in database"""
        try:
            with get_db_connection() as conn:
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
                
        except Exception as e:
            logger.error(f"Failed to store alert: {e}", exc_info=True)
    
    async def _send_email_alert(self, alert: PerformanceAlert, rule: AlertRule):
        """Send alert via email"""
        try:
            # Skip if email not configured
            email_config = getattr(self.settings, 'email_alerts', None)
            if not email_config or not getattr(email_config, 'enabled', False):
                return
            
            # Create email content
            subject = f"[Vidalytics] {alert.severity.value.upper()} Alert: {rule.name}"
            
            body = f"""
Performance Alert Triggered

Alert Details:
- Severity: {alert.severity.value.upper()}
- Agent: {alert.agent_type.value if alert.agent_type else 'System-wide'}
- Metric: {alert.metric_name}
- Current Value: {alert.current_value:.2f}
- Threshold: {alert.threshold_value:.2f}
- Time Window: {alert.time_window_minutes} minutes

Description:
{alert.description}

Recommendation:
{alert.recommendation}

Timestamp: {alert.timestamp}
Alert ID: {alert.alert_id}

This is an automated message from Vidalytics Performance Monitoring.
            """
            
            # Send email (would need actual SMTP configuration)
            logger.info(f"Email alert would be sent: {subject}")
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
    
    async def _send_webhook_alert(self, alert: PerformanceAlert, rule: AlertRule):
        """Send alert via webhook"""
        try:
            # Implementation for webhook notifications
            webhook_payload = {
                "alert_id": alert.alert_id,
                "severity": alert.severity.value,
                "agent_type": alert.agent_type.value if alert.agent_type else None,
                "metric_name": alert.metric_name,
                "current_value": alert.current_value,
                "threshold_value": alert.threshold_value,
                "description": alert.description,
                "recommendation": alert.recommendation,
                "timestamp": alert.timestamp.isoformat()
            }
            
            logger.info(f"Webhook alert would be sent: {json.dumps(webhook_payload, indent=2)}")
            
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")
    
    async def _log_alert(self, alert: PerformanceAlert, rule: AlertRule):
        """Log alert to system logs"""
        log_level = {
            AlertSeverity.CRITICAL: logging.CRITICAL,
            AlertSeverity.HIGH: logging.ERROR,
            AlertSeverity.MEDIUM: logging.WARNING,
            AlertSeverity.LOW: logging.INFO
        }.get(alert.severity, logging.WARNING)
        
        logger.log(
            log_level,
            f"PERFORMANCE ALERT: {alert.description}",
            extra={
                'category': LogCategory.MONITORING.value,
                'metadata': {
                    'alert_id': alert.alert_id,
                    'severity': alert.severity.value,
                    'agent_type': alert.agent_type.value if alert.agent_type else None,
                    'metric_name': alert.metric_name,
                    'current_value': alert.current_value,
                    'threshold_value': alert.threshold_value,
                    'recommendation': alert.recommendation
                }
            }
        )
    
    async def _update_dashboard_alert(self, alert: PerformanceAlert, rule: AlertRule):
        """Update dashboard with alert information"""
        # This would integrate with a real-time dashboard system
        logger.info(f"Dashboard alert updated: {alert.alert_id}")
    
    def add_alert_callback(self, callback: Callable):
        """Add callback for alert notifications"""
        self.alert_callbacks.append(callback)
    
    def add_custom_rule(self, rule: AlertRule):
        """Add custom alert rule"""
        self.alert_rules.append(rule)
        logger.info(f"Added custom alert rule: {rule.name}")
    
    def remove_rule(self, rule_id: str):
        """Remove alert rule"""
        self.alert_rules = [r for r in self.alert_rules if r.rule_id != rule_id]
        logger.info(f"Removed alert rule: {rule_id}")

# Global alert manager instance
_alert_manager = None

def get_alert_manager() -> AlertManager:
    """Get global alert manager instance"""
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager

async def init_alert_system():
    """Initialize the alert system"""
    alert_manager = get_alert_manager()
    await alert_manager.start_monitoring()
    logger.info("Alert system initialized and monitoring started")