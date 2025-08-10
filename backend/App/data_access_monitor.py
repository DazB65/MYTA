"""
Data Access Chain Monitor for Vidalytics
Provides comprehensive debugging and monitoring for the data access pipeline
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import sqlite3
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

@dataclass
class DataAccessEvent:
    """Data access event for monitoring"""
    event_id: str
    user_id: str
    event_type: str  # 'oauth_check', 'database_read', 'analytics_fetch', 'context_build', 'error'
    component: str   # 'oauth_manager', 'database', 'analytics_service', 'enhanced_context', 'boss_agent'
    status: str      # 'start', 'success', 'failure', 'retry'
    timestamp: datetime
    duration_ms: Optional[float] = None
    details: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat(),
            'duration_ms': self.duration_ms
        }

@dataclass 
class UserDataAccessSummary:
    """Summary of user's data access health"""
    user_id: str
    oauth_status: str
    database_health: str
    analytics_health: str
    context_health: str
    last_successful_access: Optional[datetime]
    total_events: int
    error_count: int
    success_rate: float
    recent_errors: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            'last_successful_access': self.last_successful_access.isoformat() if self.last_successful_access else None
        }

class DataAccessMonitor:
    """Monitors and debugs the entire data access chain"""
    
    def __init__(self, db_path: str = "Vidalytics.db"):
        self.db_path = db_path
        self.events: List[DataAccessEvent] = []
        self.max_events_memory = 1000  # Keep last 1000 events in memory
        self._init_monitoring_database()
    
    def _init_monitoring_database(self):
        """Initialize monitoring database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Data access events table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS data_access_events (
                        event_id TEXT PRIMARY KEY,
                        user_id TEXT,
                        event_type TEXT,
                        component TEXT,
                        status TEXT,
                        timestamp TEXT,
                        duration_ms REAL,
                        details TEXT,
                        error_message TEXT
                    )
                ''')
                
                # Create index for efficient queries
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_data_access_user_time 
                    ON data_access_events(user_id, timestamp)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_data_access_component 
                    ON data_access_events(component, status)
                ''')
                
                conn.commit()
                logger.info("Data access monitoring database initialized")
                
        except Exception as e:
            logger.error(f"Failed to initialize monitoring database: {e}")
    
    async def log_event(
        self,
        user_id: str,
        event_type: str,
        component: str,
        status: str,
        details: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        duration_ms: Optional[float] = None
    ):
        """Log a data access event"""
        try:
            event_id = f"{user_id}_{component}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            event = DataAccessEvent(
                event_id=event_id,
                user_id=user_id,
                event_type=event_type,
                component=component,
                status=status,
                timestamp=datetime.now(),
                duration_ms=duration_ms,
                details=details,
                error_message=error_message
            )
            
            # Add to memory
            self.events.append(event)
            if len(self.events) > self.max_events_memory:
                self.events.pop(0)  # Remove oldest
            
            # Store in database
            await self._store_event(event)
            
            # Log important events
            if status == 'failure':
                logger.warning(f"📊 Data access failure: {component}.{event_type} for {user_id}: {error_message}")
            elif status == 'success' and duration_ms and duration_ms > 5000:  # > 5 seconds
                logger.warning(f"📊 Slow data access: {component}.{event_type} for {user_id}: {duration_ms:.1f}ms")
                
        except Exception as e:
            logger.error(f"Failed to log monitoring event: {e}")
    
    async def _store_event(self, event: DataAccessEvent):
        """Store event in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO data_access_events 
                    (event_id, user_id, event_type, component, status, timestamp, duration_ms, details, error_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    event.event_id,
                    event.user_id,
                    event.event_type,
                    event.component,
                    event.status,
                    event.timestamp.isoformat(),
                    event.duration_ms,
                    json.dumps(event.details) if event.details else None,
                    event.error_message
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to store monitoring event: {e}")
    
    @asynccontextmanager
    async def monitor_operation(
        self,
        user_id: str,
        event_type: str,
        component: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Context manager to monitor an operation"""
        start_time = datetime.now()
        
        # Log start
        await self.log_event(user_id, event_type, component, 'start', details)
        
        try:
            yield
            # Log success
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            await self.log_event(user_id, event_type, component, 'success', details, duration_ms=duration_ms)
            
        except Exception as e:
            # Log failure
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            await self.log_event(
                user_id, event_type, component, 'failure', 
                details, str(e), duration_ms
            )
            raise
    
    async def get_user_data_health(self, user_id: str) -> UserDataAccessSummary:
        """Get comprehensive data access health for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get events from last 24 hours
                since = (datetime.now() - timedelta(hours=24)).isoformat()
                cursor.execute('''
                    SELECT event_type, component, status, timestamp, error_message
                    FROM data_access_events 
                    WHERE user_id = ? AND timestamp > ?
                    ORDER BY timestamp DESC
                ''', (user_id, since))
                
                events = cursor.fetchall()
                
                # Analyze health by component
                oauth_events = [e for e in events if e[1] == 'oauth_manager']
                db_events = [e for e in events if e[1] == 'database']
                analytics_events = [e for e in events if e[1] == 'analytics_service']
                context_events = [e for e in events if e[1] == 'enhanced_context']
                
                total_events = len(events)
                error_events = [e for e in events if e[2] == 'failure']
                error_count = len(error_events)
                success_rate = ((total_events - error_count) / total_events * 100) if total_events > 0 else 0
                
                # Find last successful access
                success_events = [e for e in events if e[2] == 'success']
                last_success = datetime.fromisoformat(success_events[0][3]) if success_events else None
                
                # Recent errors
                recent_errors = [e[4] for e in error_events[:5] if e[4]]  # Last 5 errors
                
                return UserDataAccessSummary(
                    user_id=user_id,
                    oauth_status=self._assess_component_health(oauth_events),
                    database_health=self._assess_component_health(db_events),
                    analytics_health=self._assess_component_health(analytics_events),
                    context_health=self._assess_component_health(context_events),
                    last_successful_access=last_success,
                    total_events=total_events,
                    error_count=error_count,
                    success_rate=success_rate,
                    recent_errors=recent_errors
                )
                
        except Exception as e:
            logger.error(f"Failed to get user data health for {user_id}: {e}")
            return UserDataAccessSummary(
                user_id=user_id,
                oauth_status="unknown",
                database_health="unknown", 
                analytics_health="unknown",
                context_health="unknown",
                last_successful_access=None,
                total_events=0,
                error_count=0,
                success_rate=0,
                recent_errors=[str(e)]
            )
    
    def _assess_component_health(self, component_events: List[Tuple]) -> str:
        """Assess health of a specific component"""
        if not component_events:
            return "no_data"
        
        recent_events = component_events[:10]  # Last 10 events
        failures = [e for e in recent_events if e[2] == 'failure']
        
        failure_rate = len(failures) / len(recent_events)
        
        if failure_rate == 0:
            return "healthy"
        elif failure_rate < 0.3:
            return "warning"
        else:
            return "critical"
    
    async def debug_user_data_access(self, user_id: str) -> Dict[str, Any]:
        """Comprehensive debugging for user's data access"""
        debug_info = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "debug_results": {}
        }
        
        try:
            # 1. Check OAuth status
            debug_info["debug_results"]["oauth"] = await self._debug_oauth(user_id)
            
            # 2. Check database access
            debug_info["debug_results"]["database"] = await self._debug_database_access(user_id)
            
            # 3. Check analytics service
            debug_info["debug_results"]["analytics"] = await self._debug_analytics_service(user_id)
            
            # 4. Check enhanced context
            debug_info["debug_results"]["enhanced_context"] = await self._debug_enhanced_context(user_id)
            
            # 5. Get overall health summary
            debug_info["health_summary"] = await self.get_user_data_health(user_id)
            
            # 6. Provide recommendations
            debug_info["recommendations"] = self._generate_debug_recommendations(debug_info)
            
            logger.info(f"📊 Debug completed for user {user_id}")
            return debug_info
            
        except Exception as e:
            logger.error(f"Debug failed for user {user_id}: {e}")
            debug_info["debug_error"] = str(e)
            return debug_info
    
    async def _debug_oauth(self, user_id: str) -> Dict[str, Any]:
        """Debug OAuth status"""
        try:
            from backend.oauth_manager import get_oauth_manager
            oauth_manager = get_oauth_manager()
            
            async with self.monitor_operation(user_id, 'status_check', 'oauth_manager'):
                status = oauth_manager.get_oauth_status(user_id)
                token = await oauth_manager.get_valid_token(user_id)
                
                return {
                    "status": "success",
                    "oauth_status": status,
                    "has_valid_token": token is not None,
                    "token_expires_in": status.get('expires_in_seconds', 0) if status else 0
                }
                
        except Exception as e:
            await self.log_event(user_id, 'status_check', 'oauth_manager', 'failure', error_message=str(e))
            return {"status": "error", "error": str(e)}
    
    async def _debug_database_access(self, user_id: str) -> Dict[str, Any]:
        """Debug database access"""
        try:
            from backend.database import get_database_manager
            db_manager = get_database_manager()
            
            async with self.monitor_operation(user_id, 'user_context_read', 'database'):
                user_context = db_manager.get_user_context(user_id)
                integrity = db_manager.verify_database_integrity()
                
                return {
                    "status": "success",
                    "has_user_context": bool(user_context),
                    "channel_info_complete": bool(user_context.get('channel_info', {}).get('name', '') != 'Unknown'),
                    "database_integrity": integrity,
                    "conversation_history_count": len(user_context.get('conversation_history', []))
                }
                
        except Exception as e:
            await self.log_event(user_id, 'user_context_read', 'database', 'failure', error_message=str(e))
            return {"status": "error", "error": str(e)}
    
    async def _debug_analytics_service(self, user_id: str) -> Dict[str, Any]:
        """Debug analytics service access"""
        try:
            from backend.App.analytics_service import get_analytics_service
            analytics_service = get_analytics_service()
            
            async with self.monitor_operation(user_id, 'analytics_fetch', 'analytics_service'):
                # Try to get basic analytics
                analytics = await analytics_service.get_channel_analytics(user_id, days=7)
                summary = await analytics_service.get_recent_performance_summary(user_id)
                
                return {
                    "status": "success",
                    "has_analytics": analytics is not None,
                    "has_performance_summary": summary is not None,
                    "analytics_views": analytics.views if analytics else 0,
                    "analytics_date_range": analytics.date_range if analytics else "none"
                }
                
        except Exception as e:
            await self.log_event(user_id, 'analytics_fetch', 'analytics_service', 'failure', error_message=str(e))
            return {"status": "error", "error": str(e)}
    
    async def _debug_enhanced_context(self, user_id: str) -> Dict[str, Any]:
        """Debug enhanced context system"""
        try:
            from backend.App.enhanced_user_context import get_enhanced_context_manager
            context_manager = get_enhanced_context_manager()
            
            async with self.monitor_operation(user_id, 'context_build', 'enhanced_context'):
                enhanced_context = await context_manager.get_enhanced_context(user_id)
                
                return {
                    "status": "success",
                    "context_type": enhanced_context.get('context_type', 'unknown'),
                    "data_quality": enhanced_context.get('data_quality', 'unknown'),
                    "has_realtime_data": bool(enhanced_context.get('realtime_data')),
                    "has_intelligence": bool(enhanced_context.get('intelligence')),
                    "oauth_status_in_context": enhanced_context.get('oauth_status', {}).get('authenticated', False)
                }
                
        except Exception as e:
            await self.log_event(user_id, 'context_build', 'enhanced_context', 'failure', error_message=str(e))
            return {"status": "error", "error": str(e)}
    
    def _generate_debug_recommendations(self, debug_info: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on debug results"""
        recommendations = []
        results = debug_info.get("debug_results", {})
        
        # OAuth recommendations
        oauth = results.get("oauth", {})
        if oauth.get("status") == "error":
            recommendations.append("🔐 OAuth connection failed - user needs to reconnect YouTube account")
        elif not oauth.get("has_valid_token"):
            recommendations.append("🔄 OAuth token expired - user should refresh connection")
        
        # Database recommendations  
        database = results.get("database", {})
        if database.get("status") == "error":
            recommendations.append("💾 Database access failed - check database schema and permissions")
        elif not database.get("database_integrity", {}).get("required_columns_exist"):
            recommendations.append("🔧 Database schema needs migration - run database.migrate_database_if_needed()")
        
        # Analytics recommendations
        analytics = results.get("analytics", {})
        if analytics.get("status") == "error":
            recommendations.append("📊 Analytics service failed - check YouTube API quotas and OAuth permissions")
        elif not analytics.get("has_analytics"):
            recommendations.append("📈 No analytics data available - may need fresh OAuth token or API access")
        
        # Context recommendations
        context = results.get("enhanced_context", {})
        if context.get("status") == "error":
            recommendations.append("🧠 Enhanced context failed - check data pipeline and fallback mechanisms")
        elif context.get("data_quality") == "fallback":
            recommendations.append("⚠️ Using fallback data - real-time analytics may be unavailable")
        
        # Overall health recommendations
        health = debug_info.get("health_summary")
        if health and health.success_rate < 50:
            recommendations.append("🚨 Low success rate - investigate frequent failures in data access chain")
        
        return recommendations
    
    async def get_system_health_report(self) -> Dict[str, Any]:
        """Get overall system health report"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get events from last hour
                since = (datetime.now() - timedelta(hours=1)).isoformat()
                cursor.execute('''
                    SELECT component, status, COUNT(*)
                    FROM data_access_events 
                    WHERE timestamp > ?
                    GROUP BY component, status
                ''', (since,))
                
                component_stats = {}
                for component, status, count in cursor.fetchall():
                    if component not in component_stats:
                        component_stats[component] = {}
                    component_stats[component][status] = count
                
                # Calculate overall metrics
                cursor.execute('''
                    SELECT COUNT(*) as total,
                           SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) as failures,
                           AVG(duration_ms) as avg_duration
                    FROM data_access_events 
                    WHERE timestamp > ?
                ''', (since,))
                
                total, failures, avg_duration = cursor.fetchone()
                success_rate = ((total - (failures or 0)) / total * 100) if total > 0 else 100
                
                return {
                    "timestamp": datetime.now().isoformat(),
                    "time_period": "last_hour",
                    "overall_health": {
                        "total_events": total or 0,
                        "success_rate": success_rate,
                        "average_duration_ms": avg_duration or 0,
                        "failure_count": failures or 0
                    },
                    "component_health": component_stats,
                    "system_status": "healthy" if success_rate > 90 else "degraded" if success_rate > 70 else "unhealthy"
                }
                
        except Exception as e:
            logger.error(f"Failed to get system health report: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "system_status": "unknown"
            }

# Global monitor instance
_data_access_monitor = None

def get_data_access_monitor() -> DataAccessMonitor:
    """Get or create global data access monitor"""
    global _data_access_monitor
    if _data_access_monitor is None:
        _data_access_monitor = DataAccessMonitor()
    return _data_access_monitor

# Convenience functions
async def debug_user(user_id: str) -> Dict[str, Any]:
    """Debug a specific user's data access"""
    monitor = get_data_access_monitor()
    return await monitor.debug_user_data_access(user_id)

async def get_system_health() -> Dict[str, Any]:
    """Get system health report"""
    monitor = get_data_access_monitor()
    return await monitor.get_system_health_report()