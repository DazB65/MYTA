"""
Real-Time Data Pipeline for CreatorMate
Handles background data refresh, monitoring, and intelligent caching
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
import json
import sqlite3
from contextlib import asynccontextmanager

from analytics_service import get_analytics_service, ChannelAnalytics
from oauth_manager import OAuthManager

logger = logging.getLogger(__name__)

@dataclass
class DataPipelineConfig:
    """Configuration for the data pipeline"""
    # Refresh intervals (in minutes)
    quick_refresh_interval: int = 15      # For active users
    normal_refresh_interval: int = 30     # For recently active users
    background_refresh_interval: int = 60  # For inactive users
    
    # Cache TTL settings
    performance_summary_ttl: int = 900    # 15 minutes
    channel_analytics_ttl: int = 1800     # 30 minutes
    video_analytics_ttl: int = 3600       # 1 hour
    
    # Monitoring thresholds
    significant_change_threshold: float = 20.0  # 20% change
    alert_worthy_threshold: float = 50.0        # 50% change
    
    # Pipeline settings
    max_concurrent_refreshes: int = 5
    batch_size: int = 10

@dataclass
class UserActivity:
    """Track user activity for smart refresh scheduling"""
    user_id: str
    last_chat_time: datetime
    last_refresh_time: datetime
    refresh_priority: str  # 'high', 'normal', 'low'
    is_active: bool
    consecutive_errors: int = 0

@dataclass
class PerformanceAlert:
    """Performance alert data structure"""
    user_id: str
    alert_type: str  # 'spike', 'drop', 'milestone', 'anomaly'
    metric: str      # 'views', 'ctr', 'retention', 'subscribers'
    current_value: float
    previous_value: float
    change_percentage: float
    significance: str  # 'high', 'medium', 'low'
    message: str
    created_at: datetime

class RealTimeDataPipeline:
    """Real-time data pipeline for YouTube analytics"""
    
    def __init__(self, db_path: str = "creatormate.db"):
        self.db_path = db_path
        self.config = DataPipelineConfig()
        self.analytics_service = get_analytics_service()
        self.oauth_manager = OAuthManager(db_path)
        
        # Runtime state
        self.user_activities: Dict[str, UserActivity] = {}
        self.active_refreshes: Set[str] = set()
        self.performance_alerts: List[PerformanceAlert] = []
        self.pipeline_running = False
        
        # Initialize database
        self._init_pipeline_database()
    
    def _init_pipeline_database(self):
        """Initialize pipeline-specific database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # User activity tracking
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_activity (
                        user_id TEXT PRIMARY KEY,
                        last_chat_time TEXT,
                        last_refresh_time TEXT,
                        refresh_priority TEXT DEFAULT 'normal',
                        is_active BOOLEAN DEFAULT 0,
                        consecutive_errors INTEGER DEFAULT 0
                    )
                """)
                
                # Performance alerts
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS performance_alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        alert_type TEXT,
                        metric TEXT,
                        current_value REAL,
                        previous_value REAL,
                        change_percentage REAL,
                        significance TEXT,
                        message TEXT,
                        created_at TEXT,
                        is_read BOOLEAN DEFAULT 0
                    )
                """)
                
                # Pipeline metrics cache
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS pipeline_cache (
                        cache_key TEXT PRIMARY KEY,
                        data TEXT,
                        created_at TEXT,
                        expires_at TEXT,
                        user_id TEXT
                    )
                """)
                
                conn.commit()
                logger.info("Pipeline database tables initialized")
                
        except Exception as e:
            logger.error(f"Failed to initialize pipeline database: {e}")
    
    async def start_pipeline(self):
        """Start the real-time data pipeline"""
        if self.pipeline_running:
            logger.warning("Pipeline is already running")
            return
        
        self.pipeline_running = True
        logger.info("🚀 Starting real-time data pipeline")
        
        # Start background tasks
        await asyncio.gather(
            self._background_refresh_scheduler(),
            self._performance_monitor(),
            self._cache_cleanup_task(),
            return_exceptions=True
        )
    
    async def stop_pipeline(self):
        """Stop the real-time data pipeline"""
        self.pipeline_running = False
        logger.info("⏹️ Stopping real-time data pipeline")
    
    async def register_user_activity(self, user_id: str, activity_type: str = "chat"):
        """Register user activity for smart refresh scheduling"""
        try:
            now = datetime.now()
            
            # Update user activity
            if user_id in self.user_activities:
                activity = self.user_activities[user_id]
                activity.last_chat_time = now
                activity.is_active = True
                activity.refresh_priority = self._calculate_refresh_priority(activity)
            else:
                activity = UserActivity(
                    user_id=user_id,
                    last_chat_time=now,
                    last_refresh_time=now - timedelta(hours=1),  # Force initial refresh
                    refresh_priority='high',
                    is_active=True
                )
                self.user_activities[user_id] = activity
            
            # Store in database
            await self._store_user_activity(activity)
            
            # Trigger immediate refresh for highly active users
            if activity.refresh_priority == 'high' and user_id not in self.active_refreshes:
                asyncio.create_task(self._refresh_user_data(user_id, force=False))
            
            logger.debug(f"Registered {activity_type} activity for user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to register user activity for {user_id}: {e}")
    
    async def get_real_time_context(self, user_id: str) -> Dict[str, Any]:
        """Get real-time context for user (for agent prompts)"""
        try:
            # Get fresh performance summary
            performance_summary = await self.analytics_service.get_recent_performance_summary(user_id)
            
            if not performance_summary:
                return {}
            
            # Get recent alerts
            recent_alerts = await self._get_recent_alerts(user_id, hours=24)
            
            # Build real-time context
            context = {
                'last_updated': datetime.now().isoformat(),
                'performance_summary': performance_summary,
                'recent_alerts': [alert.__dict__ for alert in recent_alerts],
                'key_metrics': {
                    'current_week_views': performance_summary['current_period']['views'],
                    'current_week_ctr': performance_summary['current_period']['ctr'],
                    'current_week_retention': performance_summary['current_period']['average_view_percentage'],
                    'subscriber_change': performance_summary['current_period']['net_subscriber_change'],
                    'top_traffic_source': self._get_top_traffic_source(performance_summary['current_period'])
                },
                'performance_insights': performance_summary.get('top_insights', []),
                'data_freshness': 'real-time'  # Indicates to agents this is fresh data
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to get real-time context for {user_id}: {e}")
            return {}
    
    async def force_refresh_user_data(self, user_id: str) -> bool:
        """Force immediate refresh of user data"""
        try:
            if user_id in self.active_refreshes:
                logger.info(f"Refresh already in progress for user {user_id}")
                return False
            
            success = await self._refresh_user_data(user_id, force=True)
            return success
            
        except Exception as e:
            logger.error(f"Failed to force refresh for user {user_id}: {e}")
            return False
    
    async def _background_refresh_scheduler(self):
        """Background task to schedule data refreshes"""
        while self.pipeline_running:
            try:
                # Load user activities from database
                await self._load_user_activities()
                
                # Determine which users need refreshing
                users_to_refresh = []
                now = datetime.now()
                
                for user_id, activity in self.user_activities.items():
                    if user_id in self.active_refreshes:
                        continue  # Skip if already refreshing
                    
                    # Calculate when user should be refreshed
                    time_since_refresh = now - activity.last_refresh_time
                    
                    if activity.refresh_priority == 'high':
                        should_refresh = time_since_refresh.total_seconds() >= (self.config.quick_refresh_interval * 60)
                    elif activity.refresh_priority == 'normal':
                        should_refresh = time_since_refresh.total_seconds() >= (self.config.normal_refresh_interval * 60)
                    else:  # low priority
                        should_refresh = time_since_refresh.total_seconds() >= (self.config.background_refresh_interval * 60)
                    
                    if should_refresh:
                        users_to_refresh.append(user_id)
                
                # Refresh users in batches
                if users_to_refresh:
                    logger.info(f"Scheduling refresh for {len(users_to_refresh)} users")
                    
                    # Limit concurrent refreshes
                    batch = users_to_refresh[:self.config.max_concurrent_refreshes]
                    
                    # Start refresh tasks
                    refresh_tasks = [
                        self._refresh_user_data(user_id, force=False)
                        for user_id in batch
                    ]
                    
                    await asyncio.gather(*refresh_tasks, return_exceptions=True)
                
                # Wait before next cycle
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in background refresh scheduler: {e}")
                await asyncio.sleep(30)  # Wait before retrying
    
    async def _performance_monitor(self):
        """Background task to monitor performance changes and generate alerts"""
        while self.pipeline_running:
            try:
                # Check for significant performance changes
                for user_id in self.user_activities:
                    try:
                        alerts = await self._detect_performance_changes(user_id)
                        
                        for alert in alerts:
                            await self._store_performance_alert(alert)
                            self.performance_alerts.append(alert)
                            
                            # Keep only recent alerts in memory
                            cutoff_time = datetime.now() - timedelta(hours=24)
                            self.performance_alerts = [
                                a for a in self.performance_alerts 
                                if a.created_at > cutoff_time
                            ]
                        
                    except Exception as e:
                        logger.error(f"Error monitoring performance for user {user_id}: {e}")
                
                # Wait before next monitoring cycle
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Error in performance monitor: {e}")
                await asyncio.sleep(60)
    
    async def _cache_cleanup_task(self):
        """Background task to clean up expired cache entries"""
        while self.pipeline_running:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    # Remove expired cache entries
                    now = datetime.now().isoformat()
                    conn.execute(
                        "DELETE FROM pipeline_cache WHERE expires_at < ?",
                        (now,)
                    )
                    conn.commit()
                
                # Clean up old alerts (keep 7 days)
                cutoff_date = (datetime.now() - timedelta(days=7)).isoformat()
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute(
                        "DELETE FROM performance_alerts WHERE created_at < ?",
                        (cutoff_date,)
                    )
                    conn.commit()
                
                # Wait before next cleanup
                await asyncio.sleep(3600)  # Clean every hour
                
            except Exception as e:
                logger.error(f"Error in cache cleanup: {e}")
                await asyncio.sleep(300)
    
    async def _refresh_user_data(self, user_id: str, force: bool = False) -> bool:
        """Refresh data for a specific user"""
        if user_id in self.active_refreshes and not force:
            return False
        
        self.active_refreshes.add(user_id)
        
        try:
            logger.info(f"🔄 Refreshing data for user {user_id}")
            
            # Check if user has valid OAuth token
            token = await self.oauth_manager.get_valid_token(user_id)
            if not token:
                logger.warning(f"No valid token for user {user_id}, skipping refresh")
                if user_id in self.user_activities:
                    self.user_activities[user_id].consecutive_errors += 1
                return False
            
            # Refresh channel analytics (7 days for quick context)
            channel_analytics = await self.analytics_service.get_channel_analytics(
                user_id, days=7, force_refresh=force
            )
            
            if channel_analytics:
                # Update user activity
                if user_id in self.user_activities:
                    activity = self.user_activities[user_id]
                    activity.last_refresh_time = datetime.now()
                    activity.consecutive_errors = 0
                    await self._store_user_activity(activity)
                
                logger.info(f"✅ Successfully refreshed data for user {user_id}")
                return True
            else:
                logger.warning(f"Failed to refresh channel analytics for user {user_id}")
                if user_id in self.user_activities:
                    self.user_activities[user_id].consecutive_errors += 1
                return False
            
        except Exception as e:
            logger.error(f"Error refreshing data for user {user_id}: {e}")
            if user_id in self.user_activities:
                self.user_activities[user_id].consecutive_errors += 1
            return False
        
        finally:
            self.active_refreshes.discard(user_id)
    
    async def _detect_performance_changes(self, user_id: str) -> List[PerformanceAlert]:
        """Detect significant performance changes and generate alerts"""
        try:
            alerts = []
            
            # Get current and previous week data
            current_week = await self.analytics_service.get_channel_analytics(user_id, days=7)
            if not current_week:
                return alerts
            
            # Get previous week data for comparison
            token = await self.oauth_manager.get_valid_token(user_id)
            if not token:
                return alerts
            
            # This is a simplified comparison - in production you'd want more sophisticated trend analysis
            performance_summary = await self.analytics_service.get_recent_performance_summary(user_id)
            if not performance_summary:
                return alerts
            
            changes = performance_summary.get('performance_changes', {})
            
            # Check for significant changes
            for metric, change_pct in changes.items():
                if abs(change_pct) >= self.config.significant_change_threshold:
                    alert_type = 'spike' if change_pct > 0 else 'drop'
                    significance = 'high' if abs(change_pct) >= self.config.alert_worthy_threshold else 'medium'
                    
                    # Create human-readable message
                    metric_name = metric.replace('_change', '').replace('_', ' ').title()
                    direction = 'increased' if change_pct > 0 else 'decreased'
                    message = f"{metric_name} {direction} by {abs(change_pct):.1f}% this week"
                    
                    alert = PerformanceAlert(
                        user_id=user_id,
                        alert_type=alert_type,
                        metric=metric.replace('_change', ''),
                        current_value=getattr(current_week, metric.replace('_change', ''), 0),
                        previous_value=0,  # Would need previous week data
                        change_percentage=change_pct,
                        significance=significance,
                        message=message,
                        created_at=datetime.now()
                    )
                    
                    alerts.append(alert)
            
            # Check for milestones
            if current_week.net_subscriber_change >= 100:
                alert = PerformanceAlert(
                    user_id=user_id,
                    alert_type='milestone',
                    metric='subscribers',
                    current_value=current_week.net_subscriber_change,
                    previous_value=0,
                    change_percentage=0,
                    significance='high',
                    message=f"Milestone: +{current_week.net_subscriber_change} subscribers this week!",
                    created_at=datetime.now()
                )
                alerts.append(alert)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error detecting performance changes for {user_id}: {e}")
            return []
    
    def _calculate_refresh_priority(self, activity: UserActivity) -> str:
        """Calculate refresh priority based on user activity"""
        now = datetime.now()
        time_since_chat = now - activity.last_chat_time
        
        # High priority: very recent activity
        if time_since_chat.total_seconds() < 300:  # 5 minutes
            return 'high'
        
        # Normal priority: recent activity
        elif time_since_chat.total_seconds() < 3600:  # 1 hour
            return 'normal'
        
        # Low priority: older activity or errors
        else:
            return 'low'
    
    def _get_top_traffic_source(self, period_data: Dict[str, Any]) -> str:
        """Get the top traffic source for a period"""
        traffic_sources = {
            'YouTube Search': period_data.get('traffic_source_youtube_search', 0),
            'Suggested Videos': period_data.get('traffic_source_suggested_videos', 0),
            'External': period_data.get('traffic_source_external', 0),
            'Direct/Other': period_data.get('traffic_source_direct', 0) + period_data.get('traffic_source_browse_features', 0)
        }
        
        return max(traffic_sources, key=traffic_sources.get) if traffic_sources else 'Unknown'
    
    async def _store_user_activity(self, activity: UserActivity):
        """Store user activity in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO user_activity 
                    (user_id, last_chat_time, last_refresh_time, refresh_priority, is_active, consecutive_errors)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    activity.user_id,
                    activity.last_chat_time.isoformat(),
                    activity.last_refresh_time.isoformat(),
                    activity.refresh_priority,
                    activity.is_active,
                    activity.consecutive_errors
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to store user activity: {e}")
    
    async def _load_user_activities(self):
        """Load user activities from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT user_id, last_chat_time, last_refresh_time, refresh_priority, is_active, consecutive_errors
                    FROM user_activity
                    WHERE last_chat_time > ?
                """, ((datetime.now() - timedelta(days=7)).isoformat(),))
                
                for row in cursor.fetchall():
                    user_id = row[0]
                    activity = UserActivity(
                        user_id=user_id,
                        last_chat_time=datetime.fromisoformat(row[1]),
                        last_refresh_time=datetime.fromisoformat(row[2]),
                        refresh_priority=row[3],
                        is_active=bool(row[4]),
                        consecutive_errors=row[5]
                    )
                    
                    # Update priority based on current time
                    activity.refresh_priority = self._calculate_refresh_priority(activity)
                    self.user_activities[user_id] = activity
                    
        except Exception as e:
            logger.error(f"Failed to load user activities: {e}")
    
    async def _store_performance_alert(self, alert: PerformanceAlert):
        """Store performance alert in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO performance_alerts 
                    (user_id, alert_type, metric, current_value, previous_value, change_percentage, significance, message, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert.user_id,
                    alert.alert_type,
                    alert.metric,
                    alert.current_value,
                    alert.previous_value,
                    alert.change_percentage,
                    alert.significance,
                    alert.message,
                    alert.created_at.isoformat()
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to store performance alert: {e}")
    
    async def _get_recent_alerts(self, user_id: str, hours: int = 24) -> List[PerformanceAlert]:
        """Get recent alerts for a user"""
        try:
            cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT user_id, alert_type, metric, current_value, previous_value, 
                           change_percentage, significance, message, created_at
                    FROM performance_alerts 
                    WHERE user_id = ? AND created_at > ?
                    ORDER BY created_at DESC
                    LIMIT 10
                """, (user_id, cutoff_time))
                
                alerts = []
                for row in cursor.fetchall():
                    alert = PerformanceAlert(
                        user_id=row[0],
                        alert_type=row[1],
                        metric=row[2],
                        current_value=row[3],
                        previous_value=row[4],
                        change_percentage=row[5],
                        significance=row[6],
                        message=row[7],
                        created_at=datetime.fromisoformat(row[8])
                    )
                    alerts.append(alert)
                
                return alerts
                
        except Exception as e:
            logger.error(f"Failed to get recent alerts for {user_id}: {e}")
            return []

# Global pipeline instance
_data_pipeline = None

def get_data_pipeline() -> RealTimeDataPipeline:
    """Get global data pipeline instance"""
    global _data_pipeline
    if _data_pipeline is None:
        _data_pipeline = RealTimeDataPipeline()
    return _data_pipeline

async def initialize_data_pipeline():
    """Initialize and start the data pipeline"""
    pipeline = get_data_pipeline()
    await pipeline.start_pipeline()
    logger.info("🚀 Real-time data pipeline initialized")

async def shutdown_data_pipeline():
    """Shutdown the data pipeline"""
    pipeline = get_data_pipeline()
    await pipeline.stop_pipeline()
    logger.info("⏹️ Real-time data pipeline shutdown")