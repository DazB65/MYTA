"""
YouTube Analytics API Service for Vidalytics
Comprehensive analytics data retrieval with proper error handling and caching
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib
import json
import asyncio
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
import sqlite3

try:
    from backend.App.config import get_settings
    from backend.App.oauth_manager import get_oauth_manager
    from backend.App.cache_service import get_cache_service, analytics_cached
except ImportError:
    # Fallback for direct execution
    from backend.App.config import get_settings
    from backend.App.oauth_manager import get_oauth_manager
    from backend.App.cache_service import get_cache_service, analytics_cached

logger = logging.getLogger(__name__)

@dataclass
class AnalyticsMetrics:
    """Structured analytics metrics data"""
    views: int = 0
    watch_time_minutes: float = 0.0
    average_view_duration: float = 0.0
    impressions: int = 0
    click_through_rate: float = 0.0
    subscribers_gained: int = 0
    subscribers_lost: int = 0
    revenue: float = 0.0
    cpm: float = 0.0
    estimated_minutes_watched: float = 0.0
    average_view_percentage: float = 0.0

@dataclass
class ChannelHealthMetrics:
    """Channel health analytics"""
    subscriber_growth_rate: float = 0.0
    view_velocity: float = 0.0
    engagement_rate: float = 0.0
    upload_consistency: float = 0.0
    audience_retention: float = 0.0
    click_through_rate: float = 0.0
    health_score: float = 0.0
    recommendations: List[str] = None

    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []

@dataclass
class RevenueMetrics:
    """Revenue analytics data"""
    total_revenue: float = 0.0
    ad_revenue: float = 0.0
    youtube_premium_revenue: float = 0.0
    super_chat_revenue: float = 0.0
    channel_memberships_revenue: float = 0.0
    merchandise_revenue: float = 0.0
    estimated_partner_revenue: float = 0.0
    rpm: float = 0.0  # Revenue per mille
    cpm: float = 0.0  # Cost per mille


class YouTubeAnalyticsService:
    """
    Comprehensive YouTube Analytics API service
    Handles all analytics data retrieval with proper authentication and caching
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.oauth_manager = get_oauth_manager()
        self.cache_duration = 3600  # 1 hour cache
        self.db_path = "Vidalytics.db"
        
        # Analytics API dimensions and metrics
        self.common_metrics = [
            'views', 'estimatedMinutesWatched', 'averageViewDuration',
            'subscribersGained', 'subscribersLost', 'videosAddedToPlaylists',
            'videosRemovedFromPlaylists', 'shares', 'comments', 'likes',
            'dislikes', 'estimatedRevenue', 'cpm'
        ]
        
        self.channel_metrics = [
            'views', 'estimatedMinutesWatched', 'averageViewDuration',
            'subscribersGained', 'subscribersLost', 'estimatedRevenue',
            'cpm', 'impressions', 'impressionClickThroughRate'
        ]
        
    def _get_service(self, user_id: str) -> Optional[Any]:
        """Get authenticated YouTube Analytics service"""
        try:
            credentials = self.oauth_manager.get_user_credentials(user_id)
            if not credentials:
                logger.warning(f"No credentials found for user {user_id}")
                return None
            
            service = build('youtubeAnalytics', 'v2', credentials=credentials)
            return service
            
        except Exception as e:
            logger.error(f"Failed to build YouTube Analytics service: {e}")
            return None
    
    def _get_youtube_service(self, user_id: str) -> Optional[Any]:
        """Get authenticated YouTube Data API service"""
        try:
            credentials = self.oauth_manager.get_user_credentials(user_id)
            if not credentials:
                return None
                
            service = build('youtube', 'v3', credentials=credentials)
            return service
            
        except Exception as e:
            logger.error(f"Failed to build YouTube Data service: {e}")
            return None
    
    def _get_channel_id(self, user_id: str) -> Optional[str]:
        """Get user's channel ID from database or API"""
        try:
            # First try database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT channel_id FROM oauth_tokens WHERE user_id = ?", 
                (user_id,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0]:
                return result[0]
            
            # If not in database, get from API
            youtube_service = self._get_youtube_service(user_id)
            if not youtube_service:
                return None
                
            response = youtube_service.channels().list(
                part='id',
                mine=True
            ).execute()
            
            if response.get('items'):
                channel_id = response['items'][0]['id']
                # Save to database
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE oauth_tokens SET channel_id = ? WHERE user_id = ?",
                    (channel_id, user_id)
                )
                conn.commit()
                conn.close()
                return channel_id
                
            return None
            
        except Exception as e:
            logger.error(f"Error getting channel ID for user {user_id}: {e}")
            return None
    
    def _generate_cache_key(self, user_id: str, endpoint: str, params: Dict) -> str:
        """Generate cache key for analytics data"""
        key_data = f"{user_id}:{endpoint}:{json.dumps(params, sort_keys=True)}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def _get_cached_data(self, cache_key: str) -> Optional[Dict]:
        """Get cached analytics data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT data, created_at FROM analytics_cache 
                WHERE cache_key = ? AND created_at > datetime('now', '-1 hour')
            """, (cache_key,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return json.loads(result[0])
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached data: {e}")
            return None
    
    def _cache_data(self, cache_key: str, data: Dict):
        """Cache analytics data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics_cache (
                    cache_key TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert or replace cached data
            cursor.execute("""
                INSERT OR REPLACE INTO analytics_cache (cache_key, data, created_at)
                VALUES (?, ?, datetime('now'))
            """, (cache_key, json.dumps(data)))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error caching data: {e}")
    
    @analytics_cached("channel_health")
    async def get_channel_health(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive channel health analytics"""
        cache_key = self._generate_cache_key(user_id, "channel_health", {"days": days})
        
        # Check cache first
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        try:
            analytics_service = self._get_service(user_id)
            channel_id = self._get_channel_id(user_id)
            
            if not analytics_service or not channel_id:
                return {
                    "status": "error",
                    "error": "YouTube Analytics access not available",
                    "data": None
                }
            
            # Calculate date range
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            # Get analytics data
            response = analytics_service.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date.isoformat(),
                endDate=end_date.isoformat(),
                metrics=','.join(self.channel_metrics),
                dimensions='day'
            ).execute()
            
            # Process the data
            health_data = self._process_channel_health_data(response)
            
            result = {
                "status": "success",
                "data": health_data,
                "metadata": {
                    "channel_id": channel_id,
                    "date_range": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat()
                    },
                    "retrieved_at": datetime.now().isoformat()
                }
            }
            
            # Cache the result
            self._cache_data(cache_key, result)
            return result
            
        except HttpError as e:
            logger.error(f"YouTube Analytics API error: {e}")
            return {
                "status": "error",
                "error": f"YouTube Analytics API error: {e.resp.status}",
                "data": None
            }
        except Exception as e:
            logger.error(f"Error getting channel health: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": None
            }
    
    def _process_channel_health_data(self, response: Dict) -> ChannelHealthMetrics:
        """Process raw analytics data into channel health metrics"""
        try:
            rows = response.get('rows', [])
            if not rows:
                return ChannelHealthMetrics()
            
            # Calculate metrics
            total_views = sum(int(row[1]) for row in rows if row[1] is not None)
            total_watch_time = sum(float(row[2]) for row in rows if row[2] is not None)
            subscribers_gained = sum(int(row[4]) for row in rows if row[4] is not None)
            subscribers_lost = sum(int(row[5]) for row in rows if row[5] is not None)
            
            # Calculate health metrics
            subscriber_growth_rate = (subscribers_gained - subscribers_lost) / len(rows) if rows else 0
            view_velocity = total_views / len(rows) if rows else 0
            average_watch_time = total_watch_time / total_views if total_views > 0 else 0
            
            # Get impressions and CTR if available
            impressions = 0
            ctr = 0.0
            if len(rows[0]) > 7:  # Check if impressions data is available
                impressions = sum(int(row[7]) for row in rows if len(row) > 7 and row[7] is not None)
                ctr = sum(float(row[8]) for row in rows if len(row) > 8 and row[8] is not None) / len(rows) if rows else 0
            
            # Calculate engagement rate (simplified)
            engagement_rate = (subscribers_gained / total_views * 100) if total_views > 0 else 0
            
            # Calculate overall health score (0-100)
            health_score = min(100, (
                (min(subscriber_growth_rate * 10, 25)) +  # 25% weight
                (min(view_velocity / 100, 25)) +          # 25% weight
                (min(engagement_rate * 5, 25)) +          # 25% weight
                (min(ctr * 500, 25))                      # 25% weight
            ))
            
            # Generate recommendations
            recommendations = []
            if subscriber_growth_rate < 1:
                recommendations.append("Focus on subscriber acquisition strategies")
            if ctr < 0.05:
                recommendations.append("Improve thumbnail and title optimization")
            if average_watch_time < 120:  # Less than 2 minutes
                recommendations.append("Work on audience retention and content engagement")
            if view_velocity < 100:
                recommendations.append("Increase content publishing frequency")
            
            return ChannelHealthMetrics(
                subscriber_growth_rate=subscriber_growth_rate,
                view_velocity=view_velocity,
                engagement_rate=engagement_rate,
                audience_retention=average_watch_time / 300 * 100,  # Assume 5min target
                click_through_rate=ctr,
                health_score=health_score,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error processing channel health data: {e}")
            return ChannelHealthMetrics()
    
    @analytics_cached("revenue")
    async def get_revenue_data(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get revenue analytics data"""
        cache_key = self._generate_cache_key(user_id, "revenue_data", {"days": days})
        
        # Check cache first
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        try:
            analytics_service = self._get_service(user_id)
            channel_id = self._get_channel_id(user_id)
            
            if not analytics_service or not channel_id:
                return {
                    "status": "error",
                    "error": "YouTube Analytics access not available",
                    "data": None
                }
            
            # Calculate date range
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            # Get revenue data
            response = analytics_service.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date.isoformat(),
                endDate=end_date.isoformat(),
                metrics='estimatedRevenue,cpm,playbackBasedCpm',
                dimensions='day'
            ).execute()
            
            revenue_data = self._process_revenue_data(response)
            
            result = {
                "status": "success",
                "data": asdict(revenue_data),
                "metadata": {
                    "channel_id": channel_id,
                    "date_range": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat()
                    },
                    "retrieved_at": datetime.now().isoformat()
                }
            }
            
            # Cache the result
            self._cache_data(cache_key, result)
            return result
            
        except HttpError as e:
            logger.error(f"YouTube Analytics API error: {e}")
            return {
                "status": "error",
                "error": f"YouTube Analytics API error: {e.resp.status}",
                "data": None
            }
        except Exception as e:
            logger.error(f"Error getting revenue data: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": None
            }
    
    def _process_revenue_data(self, response: Dict) -> RevenueMetrics:
        """Process raw revenue data"""
        try:
            rows = response.get('rows', [])
            if not rows:
                return RevenueMetrics()
            
            total_revenue = sum(float(row[1]) for row in rows if row[1] is not None)
            avg_cpm = sum(float(row[2]) for row in rows if row[2] is not None) / len(rows) if rows else 0
            avg_playback_cpm = sum(float(row[3]) for row in rows if len(row) > 3 and row[3] is not None) / len(rows) if rows else 0
            
            return RevenueMetrics(
                total_revenue=total_revenue,
                ad_revenue=total_revenue,  # Most revenue is typically ad revenue
                cpm=avg_cpm,
                rpm=avg_playback_cpm
            )
            
        except Exception as e:
            logger.error(f"Error processing revenue data: {e}")
            return RevenueMetrics()
    
    @analytics_cached("subscribers")
    async def get_subscriber_data(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get subscriber analytics data"""
        cache_key = self._generate_cache_key(user_id, "subscriber_data", {"days": days})
        
        # Check cache first
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        try:
            analytics_service = self._get_service(user_id)
            channel_id = self._get_channel_id(user_id)
            
            if not analytics_service or not channel_id:
                return {
                    "status": "error",
                    "error": "YouTube Analytics access not available",
                    "data": None
                }
            
            # Calculate date range
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            # Get subscriber data
            response = analytics_service.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date.isoformat(),
                endDate=end_date.isoformat(),
                metrics='subscribersGained,subscribersLost',
                dimensions='day'
            ).execute()
            
            subscriber_data = self._process_subscriber_data(response)
            
            result = {
                "status": "success",
                "data": subscriber_data,
                "metadata": {
                    "channel_id": channel_id,
                    "date_range": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat()
                    },
                    "retrieved_at": datetime.now().isoformat()
                }
            }
            
            # Cache the result
            self._cache_data(cache_key, result)
            return result
            
        except HttpError as e:
            logger.error(f"YouTube Analytics API error: {e}")
            return {
                "status": "error",
                "error": f"YouTube Analytics API error: {e.resp.status}",
                "data": None
            }
        except Exception as e:
            logger.error(f"Error getting subscriber data: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": None
            }
    
    def _process_subscriber_data(self, response: Dict) -> Dict[str, Any]:
        """Process subscriber analytics data"""
        try:
            rows = response.get('rows', [])
            if not rows:
                return {"daily_data": [], "summary": {"net_change": 0, "gained": 0, "lost": 0}}
            
            daily_data = []
            total_gained = 0
            total_lost = 0
            
            for row in rows:
                date_str = row[0]
                gained = int(row[1]) if row[1] is not None else 0
                lost = int(row[2]) if row[2] is not None else 0
                net_change = gained - lost
                
                daily_data.append({
                    "date": date_str,
                    "gained": gained,
                    "lost": lost,
                    "net_change": net_change
                })
                
                total_gained += gained
                total_lost += lost
            
            return {
                "daily_data": daily_data,
                "summary": {
                    "net_change": total_gained - total_lost,
                    "gained": total_gained,
                    "lost": total_lost,
                    "growth_rate": ((total_gained - total_lost) / len(rows)) if rows else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing subscriber data: {e}")
            return {"daily_data": [], "summary": {"net_change": 0, "gained": 0, "lost": 0}}
    
    @analytics_cached("content_performance")
    async def get_content_performance(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get content performance analytics"""
        cache_key = self._generate_cache_key(user_id, "content_performance", {"days": days})
        
        # Check cache first
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        try:
            analytics_service = self._get_service(user_id)
            youtube_service = self._get_youtube_service(user_id)
            channel_id = self._get_channel_id(user_id)
            
            if not analytics_service or not youtube_service or not channel_id:
                return {
                    "status": "error",
                    "error": "YouTube Analytics access not available",
                    "data": None
                }
            
            # Get recent videos first
            videos_response = youtube_service.search().list(
                part='id',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=10,
                publishedAfter=(datetime.now() - timedelta(days=days)).isoformat() + 'Z'
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in videos_response.get('items', [])]
            
            if not video_ids:
                return {
                    "status": "success",
                    "data": {"videos": [], "summary": {"total_videos": 0}},
                    "message": "No videos found in the specified date range"
                }
            
            # Get video details
            video_details = youtube_service.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids)
            ).execute()
            
            # Process video performance data
            video_performance = []
            for video in video_details.get('items', []):
                video_data = {
                    "video_id": video['id'],
                    "title": video['snippet']['title'],
                    "published_at": video['snippet']['publishedAt'],
                    "views": int(video['statistics'].get('viewCount', 0)),
                    "likes": int(video['statistics'].get('likeCount', 0)),
                    "comments": int(video['statistics'].get('commentCount', 0)),
                    "thumbnail": video['snippet']['thumbnails']['medium']['url']
                }
                video_performance.append(video_data)
            
            # Sort by performance
            video_performance.sort(key=lambda x: x['views'], reverse=True)
            
            result = {
                "status": "success",
                "data": {
                    "videos": video_performance,
                    "summary": {
                        "total_videos": len(video_performance),
                        "total_views": sum(v['views'] for v in video_performance),
                        "average_views": sum(v['views'] for v in video_performance) / len(video_performance) if video_performance else 0,
                        "total_engagement": sum(v['likes'] + v['comments'] for v in video_performance)
                    }
                },
                "metadata": {
                    "channel_id": channel_id,
                    "retrieved_at": datetime.now().isoformat()
                }
            }
            
            # Cache the result
            self._cache_data(cache_key, result)
            return result
            
        except HttpError as e:
            logger.error(f"YouTube Analytics API error: {e}")
            return {
                "status": "error",
                "error": f"YouTube Analytics API error: {e.resp.status}",
                "data": None
            }
        except Exception as e:
            logger.error(f"Error getting content performance: {e}")
            return {
                "status": "error",
                "error": str(e),
                "data": None
            }


# Singleton instance
_analytics_service = None

def get_youtube_analytics_service() -> YouTubeAnalyticsService:
    """Get singleton YouTube Analytics service instance"""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = YouTubeAnalyticsService()
    return _analytics_service