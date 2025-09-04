"""
Optimized Video Data Service
Handles video storage, caching, and retrieval with intelligent tiered strategy
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class PerformanceTier(Enum):
    HOT = "HOT"      # Recent videos, high performers - cache 1 hour
    WARM = "WARM"    # Good performers, recent - cache 24 hours  
    COLD = "COLD"    # Older videos, low performers - cache 7 days

class SyncPriority(Enum):
    URGENT = 1    # New videos, trending content
    HIGH = 2      # Recent videos, good performers
    NORMAL = 3    # Regular content
    LOW = 4       # Old, low-performing content

@dataclass
class VideoMetadata:
    """Core video metadata - always cached"""
    id: str
    user_id: str
    youtube_video_id: str
    title: str
    description: Optional[str]
    published_at: datetime
    duration: int
    thumbnail_url: str
    pillar_id: Optional[str]
    category: Optional[str]
    tags: List[str]
    view_count: int
    like_count: int
    comment_count: int
    share_count: int
    performance_score: float
    performance_tier: str
    engagement_rate: float
    last_synced: Optional[datetime]
    sync_priority: int

@dataclass
class VideoAnalytics:
    """Detailed analytics - cached based on tier"""
    video_id: str
    watch_time_minutes: float
    average_view_duration: float
    retention_rate: float
    click_through_rate: float
    impressions: int
    traffic_sources: List[Dict[str, Any]]
    top_countries: List[Dict[str, Any]]
    age_demographics: List[Dict[str, Any]]
    gender_demographics: List[Dict[str, Any]]
    estimated_revenue: float
    cpm: float
    views_growth_rate: float
    subscriber_gain: int
    cached_at: datetime
    expires_at: datetime
    data_freshness: str

@dataclass
class PaginatedVideos:
    """Paginated video results"""
    videos: List[Dict[str, Any]]
    total_count: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

class VideoDataService:
    """Intelligent video data management service"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database with optimized schema"""
        try:
            # Run the migration to create tables
            migration_path = "backend/database/migrations/create_optimized_video_storage.sql"
            with open(migration_path, 'r') as f:
                migration_sql = f.read()
            
            with sqlite3.connect(self.db_path) as conn:
                conn.executescript(migration_sql)
                logger.info("Video storage database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing video database: {e}")
            raise
    
    def calculate_performance_tier(self, video: Dict[str, Any]) -> PerformanceTier:
        """Calculate appropriate performance tier for a video"""
        published_at = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
        days_old = (datetime.now() - published_at).days
        view_count = video.get('view_count', 0)
        performance_score = video.get('performance_score', 0)
        
        # HOT tier: Recent videos (< 30 days) OR high performers
        if days_old < 30 or performance_score > 80:
            return PerformanceTier.HOT
        
        # WARM tier: Decent performers or moderately recent
        if days_old < 90 and performance_score > 50:
            return PerformanceTier.WARM
        
        # COLD tier: Everything else
        return PerformanceTier.COLD
    
    def calculate_sync_priority(self, video: Dict[str, Any]) -> SyncPriority:
        """Calculate sync priority based on video characteristics"""
        published_at = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
        days_old = (datetime.now() - published_at).days
        performance_score = video.get('performance_score', 0)
        
        # Urgent: Very recent or trending
        if days_old < 7 or performance_score > 90:
            return SyncPriority.URGENT
        
        # High: Recent good performers
        if days_old < 30 and performance_score > 70:
            return SyncPriority.HIGH
        
        # Normal: Regular content
        if days_old < 90:
            return SyncPriority.NORMAL
        
        # Low: Old content
        return SyncPriority.LOW
    
    def get_cache_duration(self, tier: PerformanceTier) -> timedelta:
        """Get cache duration based on performance tier"""
        durations = {
            PerformanceTier.HOT: timedelta(hours=1),
            PerformanceTier.WARM: timedelta(hours=24),
            PerformanceTier.COLD: timedelta(days=7)
        }
        return durations[tier]
    
    async def store_video(self, user_id: str, video_data: Dict[str, Any]) -> str:
        """Store or update video with intelligent caching"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate performance metrics
                tier = self.calculate_performance_tier(video_data)
                priority = self.calculate_sync_priority(video_data)
                
                # Prepare video data
                video_id = video_data.get('id') or f"vid_{datetime.now().timestamp()}"
                tags_json = json.dumps(video_data.get('tags', []))
                
                # Insert or update video
                cursor.execute('''
                    INSERT OR REPLACE INTO videos (
                        id, user_id, youtube_video_id, title, description, published_at,
                        duration, thumbnail_url, pillar_id, category, tags,
                        view_count, like_count, comment_count, share_count,
                        performance_score, performance_tier, engagement_rate,
                        last_synced, sync_priority
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    video_id, user_id, video_data.get('youtube_video_id'),
                    video_data.get('title'), video_data.get('description'),
                    video_data.get('published_at'), video_data.get('duration'),
                    video_data.get('thumbnail_url'), video_data.get('pillar_id'),
                    video_data.get('category'), tags_json,
                    video_data.get('view_count', 0), video_data.get('like_count', 0),
                    video_data.get('comment_count', 0), video_data.get('share_count', 0),
                    video_data.get('performance_score', 0), tier.value,
                    video_data.get('engagement_rate', 0), datetime.now(), priority.value
                ))
                
                # Store analytics if provided and video qualifies for caching
                if tier in [PerformanceTier.HOT, PerformanceTier.WARM]:
                    await self._store_analytics(cursor, video_id, user_id, video_data, tier)
                
                conn.commit()
                logger.info(f"Stored video {video_id} with tier {tier.value}")
                return video_id
                
        except Exception as e:
            logger.error(f"Error storing video: {e}")
            raise
    
    async def _store_analytics(self, cursor: sqlite3.Cursor, video_id: str, 
                             user_id: str, video_data: Dict[str, Any], 
                             tier: PerformanceTier):
        """Store detailed analytics in cache"""
        try:
            cache_duration = self.get_cache_duration(tier)
            expires_at = datetime.now() + cache_duration
            
            analytics = video_data.get('detailedStats', {})
            
            cursor.execute('''
                INSERT OR REPLACE INTO video_analytics_cache (
                    video_id, user_id, watch_time_minutes, average_view_duration,
                    retention_rate, click_through_rate, impressions,
                    traffic_sources, top_countries, estimated_revenue, cpm,
                    views_growth_rate, subscriber_gain, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video_id, user_id,
                analytics.get('watchTime', 0), analytics.get('avgViewDuration', 0),
                analytics.get('retention', 0), analytics.get('ctr', 0),
                analytics.get('impressions', 0),
                json.dumps(analytics.get('trafficSources', [])),
                json.dumps(analytics.get('topCountries', [])),
                analytics.get('revenue', 0), analytics.get('cpm', 0),
                analytics.get('viewsGrowth', 0), analytics.get('subscriberGain', 0),
                expires_at
            ))
            
        except Exception as e:
            logger.error(f"Error storing analytics for video {video_id}: {e}")
    
    async def get_videos_paginated(self, user_id: str, page: int = 1, 
                                 per_page: int = 24, filters: Dict[str, Any] = None,
                                 sort_by: str = 'published_at', sort_order: str = 'DESC') -> PaginatedVideos:
        """Get paginated videos with intelligent loading"""
        try:
            filters = filters or {}
            offset = (page - 1) * per_page
            
            # Build WHERE clause
            where_conditions = ["v.user_id = ? AND v.is_deleted = FALSE"]
            params = [user_id]
            
            # Add filters
            if filters.get('search'):
                where_conditions.append("(v.title LIKE ? OR v.tags LIKE ?)")
                search_term = f"%{filters['search']}%"
                params.extend([search_term, search_term])
            
            if filters.get('pillar_id'):
                where_conditions.append("v.pillar_id = ?")
                params.append(filters['pillar_id'])
            
            if filters.get('performance_tier'):
                where_conditions.append("v.performance_tier = ?")
                params.append(filters['performance_tier'])
            
            if filters.get('date_from'):
                where_conditions.append("v.published_at >= ?")
                params.append(filters['date_from'])
            
            if filters.get('date_to'):
                where_conditions.append("v.published_at <= ?")
                params.append(filters['date_to'])
            
            where_clause = " AND ".join(where_conditions)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Get total count
                count_query = f"SELECT COUNT(*) FROM videos v WHERE {where_clause}"
                cursor.execute(count_query, params)
                total_count = cursor.fetchone()[0]
                
                # Get paginated results using the performance view
                query = f'''
                    SELECT * FROM video_performance_summary v
                    WHERE {where_clause}
                    ORDER BY v.{sort_by} {sort_order}
                    LIMIT ? OFFSET ?
                '''
                
                cursor.execute(query, params + [per_page, offset])
                rows = cursor.fetchall()
                
                # Convert to dictionaries and parse JSON fields
                videos = []
                for row in rows:
                    video = dict(row)
                    # Parse JSON fields
                    if video.get('tags'):
                        video['tags'] = json.loads(video['tags'])
                    videos.append(video)
                
                # Calculate pagination info
                total_pages = (total_count + per_page - 1) // per_page
                has_next = page < total_pages
                has_prev = page > 1
                
                return PaginatedVideos(
                    videos=videos,
                    total_count=total_count,
                    page=page,
                    per_page=per_page,
                    total_pages=total_pages,
                    has_next=has_next,
                    has_prev=has_prev
                )
                
        except Exception as e:
            logger.error(f"Error getting paginated videos: {e}")
            raise

    async def get_video_with_analytics(self, user_id: str, video_id: str) -> Optional[Dict[str, Any]]:
        """Get single video with analytics, fetching from API if cache is stale"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # Get video with analytics from performance view
                cursor.execute('''
                    SELECT * FROM video_performance_summary
                    WHERE user_id = ? AND id = ?
                ''', (user_id, video_id))

                row = cursor.fetchone()
                if not row:
                    return None

                video = dict(row)

                # Parse JSON fields
                if video.get('tags'):
                    video['tags'] = json.loads(video['tags'])

                # Check if we need to refresh analytics
                if video['analytics_status'] in ['stale', 'no_analytics']:
                    await self._queue_video_sync(video_id, user_id, 'analytics', SyncPriority.HIGH)

                return video

        except Exception as e:
            logger.error(f"Error getting video {video_id}: {e}")
            return None

    async def _queue_video_sync(self, video_id: str, user_id: str,
                              sync_type: str, priority: SyncPriority):
        """Queue video for background synchronization"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if already queued
                cursor.execute('''
                    SELECT id FROM video_sync_queue
                    WHERE video_id = ? AND status IN ('pending', 'processing')
                ''', (video_id,))

                if cursor.fetchone():
                    return  # Already queued

                # Add to sync queue
                cursor.execute('''
                    INSERT INTO video_sync_queue (
                        video_id, user_id, sync_type, priority, scheduled_at
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (video_id, user_id, sync_type, priority.value, datetime.now()))

                conn.commit()
                logger.info(f"Queued video {video_id} for {sync_type} sync with priority {priority.value}")

        except Exception as e:
            logger.error(f"Error queueing video sync: {e}")

    async def get_videos_needing_sync(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get videos that need synchronization, ordered by priority"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT sq.*, v.youtube_video_id, v.performance_tier
                    FROM video_sync_queue sq
                    JOIN videos v ON sq.video_id = v.id
                    WHERE sq.status = 'pending'
                    AND sq.attempts < sq.max_attempts
                    AND sq.scheduled_at <= datetime('now')
                    ORDER BY sq.priority ASC, sq.scheduled_at ASC
                    LIMIT ?
                ''', (limit,))

                return [dict(row) for row in cursor.fetchall()]

        except Exception as e:
            logger.error(f"Error getting videos needing sync: {e}")
            return []

    async def mark_sync_completed(self, sync_id: str):
        """Mark a sync job as completed"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE video_sync_queue
                    SET status = 'completed', updated_at = ?
                    WHERE id = ?
                ''', (datetime.now(), sync_id))
                conn.commit()

        except Exception as e:
            logger.error(f"Error marking sync completed: {e}")

    async def mark_sync_failed(self, sync_id: str, error_message: str):
        """Mark a sync job as failed"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE video_sync_queue
                    SET status = 'failed', last_error = ?, attempts = attempts + 1, updated_at = ?
                    WHERE id = ?
                ''', (error_message, datetime.now(), sync_id))
                conn.commit()

        except Exception as e:
            logger.error(f"Error marking sync failed: {e}")

    async def get_user_video_stats(self, user_id: str) -> Dict[str, Any]:
        """Get aggregated video statistics for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get basic stats
                cursor.execute('''
                    SELECT
                        COUNT(*) as total_videos,
                        SUM(view_count) as total_views,
                        SUM(like_count) as total_likes,
                        SUM(comment_count) as total_comments,
                        AVG(performance_score) as avg_performance,
                        AVG(engagement_rate) as avg_engagement,
                        COUNT(CASE WHEN performance_tier = 'HOT' THEN 1 END) as hot_videos,
                        COUNT(CASE WHEN performance_tier = 'WARM' THEN 1 END) as warm_videos,
                        COUNT(CASE WHEN performance_tier = 'COLD' THEN 1 END) as cold_videos
                    FROM videos
                    WHERE user_id = ? AND is_deleted = FALSE
                ''', (user_id,))

                stats = dict(cursor.fetchone()) if cursor.fetchone() else {}

                # Get recent performance (last 30 days)
                cursor.execute('''
                    SELECT
                        COUNT(*) as recent_videos,
                        SUM(view_count) as recent_views,
                        AVG(performance_score) as recent_avg_performance
                    FROM videos
                    WHERE user_id = ? AND is_deleted = FALSE
                    AND published_at >= datetime('now', '-30 days')
                ''', (user_id,))

                recent_stats = dict(cursor.fetchone()) if cursor.fetchone() else {}

                return {**stats, **recent_stats}

        except Exception as e:
            logger.error(f"Error getting user video stats: {e}")
            return {}

    async def cleanup_expired_cache(self):
        """Clean up expired analytics cache entries"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Delete expired cache entries
                cursor.execute('''
                    DELETE FROM video_analytics_cache
                    WHERE expires_at < datetime('now')
                ''')

                deleted_count = cursor.rowcount

                # Clean up old completed sync jobs
                cursor.execute('''
                    DELETE FROM video_sync_queue
                    WHERE status IN ('completed', 'failed')
                    AND updated_at < datetime('now', '-7 days')
                ''')

                conn.commit()
                logger.info(f"Cleaned up {deleted_count} expired cache entries")

        except Exception as e:
            logger.error(f"Error cleaning up cache: {e}")

    async def bulk_update_performance_tiers(self, user_id: str):
        """Recalculate performance tiers for all user videos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # Get all videos for user
                cursor.execute('''
                    SELECT id, published_at, view_count, performance_score
                    FROM videos WHERE user_id = ? AND is_deleted = FALSE
                ''', (user_id,))

                videos = cursor.fetchall()
                updates = []

                for video in videos:
                    video_dict = dict(video)
                    new_tier = self.calculate_performance_tier(video_dict)
                    new_priority = self.calculate_sync_priority(video_dict)

                    updates.append((new_tier.value, new_priority.value, video['id']))

                # Bulk update
                cursor.executemany('''
                    UPDATE videos
                    SET performance_tier = ?, sync_priority = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', updates)

                conn.commit()
                logger.info(f"Updated performance tiers for {len(updates)} videos")

        except Exception as e:
            logger.error(f"Error updating performance tiers: {e}")
