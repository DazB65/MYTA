"""
Security Monitoring Dashboard
Real-time security metrics and threat detection for MYTA application
"""

import time
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging
from threading import Lock
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class SecurityEvent:
    """Security event data structure"""
    timestamp: datetime
    event_type: str  # 'auth_failure', 'rate_limit', 'suspicious_request', 'token_blacklist'
    severity: str    # 'low', 'medium', 'high', 'critical'
    user_id: Optional[str]
    ip_address: str
    user_agent: str
    details: Dict[str, Any]
    resolved: bool = False

@dataclass
class SecurityMetrics:
    """Security metrics summary"""
    timestamp: datetime
    total_requests: int
    failed_auth_attempts: int
    rate_limited_requests: int
    suspicious_requests: int
    blocked_requests: int
    unique_ips: int
    auth_success_rate: float
    avg_response_time: float
    security_score: float

class SecurityMonitor:
    """Real-time security monitoring system"""
    
    def __init__(self, db_path: str = "security_monitoring.db"):
        self.db_path = db_path
        self.events_buffer = deque(maxlen=1000)  # Keep last 1000 events in memory
        self.metrics_cache = {}
        self.lock = Lock()
        self._init_database()
        
        # Threat detection thresholds
        self.thresholds = {
            'failed_auth_rate': 0.3,      # 30% failure rate
            'rate_limit_threshold': 100,   # requests per minute
            'suspicious_patterns': 5,      # suspicious requests per hour
            'unique_ip_threshold': 1000    # unique IPs per hour
        }
    
    def _init_database(self):
        """Initialize security monitoring database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS security_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        event_type TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        user_id TEXT,
                        ip_address TEXT NOT NULL,
                        user_agent TEXT,
                        details TEXT,
                        resolved BOOLEAN DEFAULT FALSE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS security_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        total_requests INTEGER,
                        failed_auth_attempts INTEGER,
                        rate_limited_requests INTEGER,
                        suspicious_requests INTEGER,
                        blocked_requests INTEGER,
                        unique_ips INTEGER,
                        auth_success_rate REAL,
                        avg_response_time REAL,
                        security_score REAL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes for performance
                conn.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON security_events(timestamp)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON security_events(event_type)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_events_ip ON security_events(ip_address)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON security_metrics(timestamp)")
                
                conn.commit()
                logger.info("Security monitoring database initialized")
        except Exception as e:
            logger.error(f"Failed to initialize security database: {e}")
    
    def log_security_event(self, event: SecurityEvent):
        """Log a security event"""
        try:
            with self.lock:
                # Add to memory buffer
                self.events_buffer.append(event)
                
                # Store in database
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        INSERT INTO security_events (
                            timestamp, event_type, severity, user_id, ip_address,
                            user_agent, details, resolved
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        event.timestamp, event.event_type, event.severity,
                        event.user_id, event.ip_address, event.user_agent,
                        json.dumps(event.details), event.resolved
                    ))
                    conn.commit()
                
                # Check for immediate threats
                self._check_threat_patterns(event)
                
                logger.info(f"Security event logged: {event.event_type} - {event.severity}")
        except Exception as e:
            logger.error(f"Failed to log security event: {e}")
    
    def _check_threat_patterns(self, event: SecurityEvent):
        """Check for threat patterns and trigger alerts"""
        try:
            # Check for brute force attacks
            if event.event_type == 'auth_failure':
                recent_failures = self._count_recent_events(
                    'auth_failure', 
                    minutes=5, 
                    ip_address=event.ip_address
                )
                if recent_failures >= 5:
                    self._trigger_alert('brute_force_detected', event.ip_address, {
                        'failed_attempts': recent_failures,
                        'time_window': '5 minutes'
                    })
            
            # Check for rate limiting abuse
            if event.event_type == 'rate_limit':
                recent_rate_limits = self._count_recent_events(
                    'rate_limit',
                    minutes=10,
                    ip_address=event.ip_address
                )
                if recent_rate_limits >= 10:
                    self._trigger_alert('rate_limit_abuse', event.ip_address, {
                        'rate_limit_hits': recent_rate_limits,
                        'time_window': '10 minutes'
                    })
        except Exception as e:
            logger.error(f"Failed to check threat patterns: {e}")
    
    def _count_recent_events(self, event_type: str, minutes: int, ip_address: str = None) -> int:
        """Count recent events of a specific type"""
        try:
            since_time = datetime.now() - timedelta(minutes=minutes)
            
            with sqlite3.connect(self.db_path) as conn:
                if ip_address:
                    cursor = conn.execute("""
                        SELECT COUNT(*) FROM security_events 
                        WHERE event_type = ? AND timestamp >= ? AND ip_address = ?
                    """, (event_type, since_time, ip_address))
                else:
                    cursor = conn.execute("""
                        SELECT COUNT(*) FROM security_events 
                        WHERE event_type = ? AND timestamp >= ?
                    """, (event_type, since_time))
                
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Failed to count recent events: {e}")
            return 0
    
    def _trigger_alert(self, alert_type: str, ip_address: str, details: Dict[str, Any]):
        """Trigger a security alert"""
        alert_event = SecurityEvent(
            timestamp=datetime.now(),
            event_type='security_alert',
            severity='high',
            user_id=None,
            ip_address=ip_address,
            user_agent='',
            details={
                'alert_type': alert_type,
                **details
            }
        )
        self.log_security_event(alert_event)
        logger.warning(f"Security alert triggered: {alert_type} for IP {ip_address}")
    
    def get_security_metrics(self, hours: int = 24) -> SecurityMetrics:
        """Get security metrics for the specified time period"""
        try:
            since_time = datetime.now() - timedelta(hours=hours)
            
            with sqlite3.connect(self.db_path) as conn:
                # Get basic counts
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total_events,
                        SUM(CASE WHEN event_type = 'auth_failure' THEN 1 ELSE 0 END) as failed_auth,
                        SUM(CASE WHEN event_type = 'rate_limit' THEN 1 ELSE 0 END) as rate_limited,
                        SUM(CASE WHEN event_type = 'suspicious_request' THEN 1 ELSE 0 END) as suspicious,
                        SUM(CASE WHEN event_type = 'blocked_request' THEN 1 ELSE 0 END) as blocked,
                        COUNT(DISTINCT ip_address) as unique_ips
                    FROM security_events 
                    WHERE timestamp >= ?
                """, (since_time,))
                
                result = cursor.fetchone()
                total_events, failed_auth, rate_limited, suspicious, blocked, unique_ips = result
                
                # Calculate success rate (assuming successful requests aren't logged as events)
                auth_success_rate = max(0, 1 - (failed_auth / max(total_events, 1)))
                
                # Calculate security score (0-100)
                security_score = self._calculate_security_score(
                    failed_auth, rate_limited, suspicious, blocked, unique_ips, hours
                )
                
                return SecurityMetrics(
                    timestamp=datetime.now(),
                    total_requests=total_events,
                    failed_auth_attempts=failed_auth,
                    rate_limited_requests=rate_limited,
                    suspicious_requests=suspicious,
                    blocked_requests=blocked,
                    unique_ips=unique_ips,
                    auth_success_rate=auth_success_rate,
                    avg_response_time=0.0,  # Would need to integrate with performance monitoring
                    security_score=security_score
                )
        except Exception as e:
            logger.error(f"Failed to get security metrics: {e}")
            return SecurityMetrics(
                timestamp=datetime.now(),
                total_requests=0, failed_auth_attempts=0, rate_limited_requests=0,
                suspicious_requests=0, blocked_requests=0, unique_ips=0,
                auth_success_rate=1.0, avg_response_time=0.0, security_score=100.0
            )
    
    def _calculate_security_score(self, failed_auth: int, rate_limited: int, 
                                 suspicious: int, blocked: int, unique_ips: int, hours: int) -> float:
        """Calculate overall security score (0-100)"""
        try:
            # Base score
            score = 100.0
            
            # Deduct points for security events
            score -= min(failed_auth * 2, 30)      # Max 30 points for auth failures
            score -= min(rate_limited * 1, 20)     # Max 20 points for rate limiting
            score -= min(suspicious * 3, 25)       # Max 25 points for suspicious activity
            score -= min(blocked * 1, 15)          # Max 15 points for blocked requests
            
            # Deduct points for too many unique IPs (potential bot activity)
            if unique_ips > self.thresholds['unique_ip_threshold']:
                score -= min((unique_ips - self.thresholds['unique_ip_threshold']) * 0.1, 10)
            
            return max(score, 0.0)
        except Exception as e:
            logger.error(f"Failed to calculate security score: {e}")
            return 50.0  # Default middle score on error

# Global security monitor instance
security_monitor = SecurityMonitor()

def log_auth_failure(user_id: str, ip_address: str, user_agent: str, details: Dict[str, Any]):
    """Helper function to log authentication failures"""
    event = SecurityEvent(
        timestamp=datetime.now(),
        event_type='auth_failure',
        severity='medium',
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details
    )
    security_monitor.log_security_event(event)

def log_rate_limit(ip_address: str, user_agent: str, details: Dict[str, Any]):
    """Helper function to log rate limiting events"""
    event = SecurityEvent(
        timestamp=datetime.now(),
        event_type='rate_limit',
        severity='low',
        user_id=None,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details
    )
    security_monitor.log_security_event(event)

def log_suspicious_request(ip_address: str, user_agent: str, details: Dict[str, Any]):
    """Helper function to log suspicious requests"""
    event = SecurityEvent(
        timestamp=datetime.now(),
        event_type='suspicious_request',
        severity='medium',
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
        user_id=None
    )
    security_monitor.log_security_event(event)
