"""
Real-Time Data Pipeline for Vidalytics
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
    
    def __init__(self, db_path: str = "Vidalytics.db"):
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
            # Enhanced error handling and fallback logic
            logger.info(f"🔄 Fetching real-time context for user {user_id}")
            
            # Get fresh performance summary with retry logic
            performance_summary = None
            max_retries = 2
            
            for attempt in range(max_retries):
                try:
                    performance_summary = await self.analytics_service.get_recent_performance_summary(user_id)
                    if performance_summary:
                        logger.info(f"✅ Got performance summary on attempt {attempt + 1}")
                        break
                    else:
                        logger.warning(f"⚠️ No performance summary on attempt {attempt + 1}")
                except Exception as retry_e:
                    logger.warning(f"⚠️ Performance summary attempt {attempt + 1} failed: {retry_e}")
                    if attempt == max_retries - 1:
                        raise retry_e
            
            if not performance_summary:
                # Try to get basic channel data as fallback
                logger.info(f"🔄 Attempting fallback to basic channel analytics for {user_id}")
                try:
                    basic_analytics = await self.analytics_service.get_channel_analytics(user_id, days=7)
                    if basic_analytics:
                        logger.info(f"✅ Got basic analytics fallback")
                        # Create minimal performance summary structure
                        performance_summary = {
                            'current_period': {
                                'views': basic_analytics.views,
                                'ctr': basic_analytics.ctr,
                                'average_view_percentage': basic_analytics.average_view_percentage,
                                'net_subscriber_change': basic_analytics.net_subscriber_change,
                                'traffic_source_youtube_search': basic_analytics.traffic_source_youtube_search,
                                'traffic_source_suggested_videos': basic_analytics.traffic_source_suggested_videos,
                                'traffic_source_external': basic_analytics.traffic_source_external,
                                'traffic_source_direct': basic_analytics.traffic_source_direct
                            },
                            'performance_changes': {},  # No comparison data in fallback
                            'top_insights': [f"Channel had {basic_analytics.views:,} views in the last 7 days"]
                        }
                    else:
                        logger.warning(f"❌ Both performance summary and basic analytics failed for {user_id}")
                        return self._create_empty_context_with_status(user_id, "analytics_unavailable")
                except Exception as fallback_e:
                    logger.error(f"❌ Fallback analytics also failed for {user_id}: {fallback_e}")
                    return self._create_empty_context_with_status(user_id, "all_analytics_failed")
            
            # Get recent alerts
            recent_alerts = []
            try:
                recent_alerts = await self._get_recent_alerts(user_id, hours=24)
                logger.info(f"📊 Got {len(recent_alerts)} recent alerts for {user_id}")
            except Exception as alert_e:
                logger.warning(f"Failed to get recent alerts for {user_id}: {alert_e}")
                # Continue without alerts rather than failing entirely
            
            # Build real-time context with enhanced error handling
            try:
                current_period = performance_summary.get('current_period', {})
                context = {
                    'last_updated': datetime.now().isoformat(),
                    'performance_summary': performance_summary,
                    'recent_alerts': [alert.__dict__ for alert in recent_alerts],
                    'key_metrics': {
                        'current_week_views': current_period.get('views', 0),
                        'current_week_ctr': current_period.get('ctr', 0.0),
                        'current_week_retention': current_period.get('average_view_percentage', 0.0),
                        'subscriber_change': current_period.get('net_subscriber_change', 0),
                        'top_traffic_source': self._get_top_traffic_source(current_period)
                    },
                    'performance_insights': performance_summary.get('top_insights', []),
                    'data_freshness': 'real-time',  # Indicates to agents this is fresh data
                    'context_quality': 'complete' if performance_summary.get('performance_changes') else 'basic_fallback'
                }
                
                # Add top video information if available
                if 'top_video' in performance_summary.get('current_period', {}):
                    context['top_video'] = performance_summary['current_period']['top_video']
                
                logger.info(f"✅ Successfully built real-time context for {user_id}")
                return context
                
            except Exception as context_e:
                logger.error(f"Failed to build context structure for {user_id}: {context_e}")
                return self._create_empty_context_with_status(user_id, "context_build_failed")
            
        except Exception as e:
            logger.error(f"💥 Critical error getting real-time context for {user_id}: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return self._create_empty_context_with_status(user_id, "critical_error")
    
    def _create_empty_context_with_status(self, user_id: str, error_type: str) -> Dict[str, Any]:
        """Create empty context with error status information"""
        return {
            'last_updated': datetime.now().isoformat(),
            'performance_summary': None,
            'recent_alerts': [],
            'key_metrics': {
                'current_week_views': 0,
                'current_week_ctr': 0.0,
                'current_week_retention': 0.0,
                'subscriber_change': 0,
                'top_traffic_source': 'Unknown'
            },
            'performance_insights': [],
            'data_freshness': 'unavailable',
            'context_quality': 'empty_fallback',
            'error_type': error_type,
            'user_id': user_id
        }
    
    async def force_refresh_user_data(self, user_id: str) -> bool:
        """Force immediate refresh of user data with enhanced monitoring"""
        try:
            logger.info(f"🚀 Force refresh requested for user {user_id}")
            
            if user_id in self.active_refreshes:
                logger.info(f"⏳ Refresh already in progress for user {user_id}, waiting...")
                
                # Wait up to 10 seconds for existing refresh to complete
                wait_time = 0
                while user_id in self.active_refreshes and wait_time < 10:
                    await asyncio.sleep(0.5)
                    wait_time += 0.5
                
                if user_id in self.active_refreshes:
                    logger.warning(f"⏰ Existing refresh for {user_id} taking too long, proceeding anyway")
                    return False
                else:
                    logger.info(f"✅ Previous refresh completed for {user_id}")
                    return True
            
            # Proceed with force refresh
            start_time = datetime.now()
            success = await self._refresh_user_data(user_id, force=True)
            duration = (datetime.now() - start_time).total_seconds()
            
            if success:
                logger.info(f"✅ Force refresh successful for {user_id} in {duration:.1f}s")
            else:
                logger.error(f"❌ Force refresh failed for {user_id} after {duration:.1f}s")
            
            return success
            
        except Exception as e:
            logger.error(f"💥 Critical error in force refresh for user {user_id}: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
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
        """Refresh data for a specific user with enhanced error handling"""
        if user_id in self.active_refreshes and not force:
            logger.info(f"Data refresh already in progress for {user_id}")
            return False
        
        self.active_refreshes.add(user_id)
        refresh_start_time = datetime.now()
        
        try:
            logger.info(f"🔄 Starting data refresh for user {user_id} (force={force})")
            
            # Check if user has valid OAuth token with detailed logging
            token = await self.oauth_manager.get_valid_token(user_id)
            if not token:
                oauth_status = self.oauth_manager.get_oauth_status(user_id)
                logger.warning(f"🔐 No valid OAuth token for user {user_id}")
                logger.info(f"OAuth status details: {oauth_status}")
                
                if user_id in self.user_activities:
                    self.user_activities[user_id].consecutive_errors += 1
                    
                    # If too many consecutive errors, reduce refresh frequency
                    if self.user_activities[user_id].consecutive_errors >= 3:
                        self.user_activities[user_id].refresh_priority = 'low'
                        logger.warning(f"Reduced refresh priority for {user_id} due to consecutive OAuth errors")
                
                return False
            
            logger.info(f"✅ OAuth token valid for {user_id}, proceeding with analytics fetch")
            
            # Try multiple analytics approaches with fallbacks
            refresh_success = False
            analytics_data = None
            
            # Approach 1: Try performance summary (most comprehensive)
            try:
                logger.info(f"📊 Attempting performance summary fetch for {user_id}")
                performance_summary = await self.analytics_service.get_recent_performance_summary(user_id)
                if performance_summary:
                    logger.info(f"✅ Performance summary successful for {user_id}")
                    analytics_data = performance_summary
                    refresh_success = True
                else:
                    logger.warning(f"⚠️ Performance summary returned None for {user_id}")
            except Exception as perf_e:
                logger.warning(f"⚠️ Performance summary failed for {user_id}: {perf_e}")
            
            # Approach 2: Fallback to basic channel analytics
            if not refresh_success:
                try:
                    logger.info(f"🔄 Attempting basic channel analytics for {user_id}")
                    channel_analytics = await self.analytics_service.get_channel_analytics(
                        user_id, days=7, force_refresh=force
                    )
                    if channel_analytics:
                        logger.info(f"✅ Basic channel analytics successful for {user_id}")
                        analytics_data = channel_analytics
                        refresh_success = True
                    else:
                        logger.warning(f"⚠️ Channel analytics returned None for {user_id}")
                except Exception as analytics_e:
                    logger.warning(f"⚠️ Channel analytics failed for {user_id}: {analytics_e}")
            
            # Update user activity based on results
            if user_id in self.user_activities:
                activity = self.user_activities[user_id]
                activity.last_refresh_time = datetime.now()
                
                if refresh_success:
                    activity.consecutive_errors = 0
                    # Restore normal priority if we were successful
                    if activity.refresh_priority == 'low':
                        activity.refresh_priority = 'normal'
                        logger.info(f"Restored normal refresh priority for {user_id}")
                else:
                    activity.consecutive_errors += 1
                    
                await self._store_user_activity(activity)
            
            refresh_duration = (datetime.now() - refresh_start_time).total_seconds()
            
            if refresh_success:
                logger.info(f"✅ Successfully refreshed data for user {user_id} in {refresh_duration:.1f}s")
                
                # Store success metrics
                if hasattr(analytics_data, 'views'):
                    logger.info(f"📈 Analytics summary for {user_id}: {analytics_data.views:,} views, {analytics_data.ctr:.1f}% CTR")
                elif isinstance(analytics_data, dict) and 'current_period' in analytics_data:
                    views = analytics_data['current_period'].get('views', 0)
                    ctr = analytics_data['current_period'].get('ctr', 0)
                    logger.info(f"📈 Performance summary for {user_id}: {views:,} views, {ctr:.1f}% CTR")
                
                return True
            else:
                logger.error(f"❌ Failed to refresh any analytics data for user {user_id} after {refresh_duration:.1f}s")
                return False
            
        except Exception as e:
            refresh_duration = (datetime.now() - refresh_start_time).total_seconds()
            logger.error(f"💥 Critical error refreshing data for user {user_id} after {refresh_duration:.1f}s: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            
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