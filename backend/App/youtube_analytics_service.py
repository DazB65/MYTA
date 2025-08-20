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
    performance_score: float = 0.0
    optimization_opportunities: List[str] = None
    trending_score: float = 0.0

@dataclass
class RealTimeInsights:
    """Real-time AI-powered insights"""
    performance_alerts: List[Dict[str, Any]] = None
    optimization_recommendations: List[Dict[str, Any]] = None
    trending_opportunities: List[Dict[str, Any]] = None
    competitive_insights: List[Dict[str, Any]] = None
    growth_predictions: Dict[str, Any] = None
    timestamp: datetime = None

@dataclass
class VideoPerformanceInsight:
    """Individual video performance with AI insights"""
    video_id: str
    title: str
    views: int
    ctr: float
    retention: float
    engagement_score: float
    optimization_score: float
    trending_potential: float
    recommended_actions: List[str] = None
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

        except Exception as e:
            logger.error(f"Error getting comprehensive analytics: {e}")
            return {"error": str(e)}

    async def get_real_time_insights(self, channel_id: str, access_token: str) -> RealTimeInsights:
        """Get real-time AI-powered insights and recommendations"""

        try:
            # Get current metrics
            current_metrics = await self.get_channel_analytics(channel_id, access_token, days=7)

            # Get performance trends
            performance_trends = await self._analyze_performance_trends(channel_id, access_token)

            # Generate AI insights
            insights = RealTimeInsights(
                performance_alerts=await self._generate_performance_alerts(current_metrics, performance_trends),
                optimization_recommendations=await self._generate_optimization_recommendations(current_metrics),
                trending_opportunities=await self._identify_trending_opportunities(channel_id, access_token),
                competitive_insights=await self._generate_competitive_insights(channel_id, access_token),
                growth_predictions=await self._predict_growth_trajectory(current_metrics, performance_trends),
                timestamp=datetime.now()
            )

            return insights

        except Exception as e:
            logger.error(f"Error generating real-time insights: {e}")
            return RealTimeInsights(
                performance_alerts=[],
                optimization_recommendations=[],
                trending_opportunities=[],
                competitive_insights=[],
                growth_predictions={},
                timestamp=datetime.now()
            )

    async def get_video_performance_insights(self, video_ids: List[str], access_token: str) -> List[VideoPerformanceInsight]:
        """Get AI-powered insights for specific videos"""

        try:
            insights = []

            for video_id in video_ids:
                try:
                    # Get video analytics
                    video_data = await self._get_video_analytics(video_id, access_token)

                    # Calculate AI scores
                    optimization_score = self._calculate_optimization_score(video_data)
                    trending_potential = self._calculate_trending_potential(video_data)
                    engagement_score = self._calculate_engagement_score(video_data)

                    # Generate recommendations
                    recommendations = self._generate_video_recommendations(video_data, optimization_score)

                    insight = VideoPerformanceInsight(
                        video_id=video_id,
                        title=video_data.get('title', 'Unknown'),
                        views=video_data.get('views', 0),
                        ctr=video_data.get('ctr', 0.0),
                        retention=video_data.get('retention', 0.0),
                        engagement_score=engagement_score,
                        optimization_score=optimization_score,
                        trending_potential=trending_potential,
                        recommended_actions=recommendations
                    )

                    insights.append(insight)

                except Exception as e:
                    logger.error(f"Error analyzing video {video_id}: {e}")

            return insights

        except Exception as e:
            logger.error(f"Error getting video performance insights: {e}")
            return []

    async def get_optimization_dashboard(self, channel_id: str, access_token: str) -> Dict[str, Any]:
        """Get comprehensive optimization dashboard data"""

        try:
            # Gather all data
            current_metrics = await self.get_channel_analytics(channel_id, access_token, days=30)
            real_time_insights = await self.get_real_time_insights(channel_id, access_token)
            recent_videos = await self._get_recent_video_performance(channel_id, access_token)

            # Calculate dashboard metrics
            dashboard = {
                "performance_overview": {
                    "current_metrics": current_metrics,
                    "performance_score": self._calculate_overall_performance_score(current_metrics),
                    "growth_trend": self._determine_growth_trend(current_metrics),
                    "health_status": self._assess_channel_health(current_metrics)
                },
                "real_time_insights": real_time_insights,
                "video_performance": recent_videos,
                "optimization_priorities": self._prioritize_optimizations(real_time_insights),
                "action_plan": self._generate_action_plan(real_time_insights, current_metrics),
                "benchmarks": self._get_performance_benchmarks(current_metrics),
                "predictions": {
                    "next_30_days": self._predict_30_day_performance(current_metrics),
                    "growth_milestones": self._predict_growth_milestones(current_metrics)
                },
                "timestamp": datetime.now().isoformat()
            }

            return dashboard

        except Exception as e:
            logger.error(f"Error generating optimization dashboard: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    # AI-powered analysis methods

    async def _generate_performance_alerts(self, metrics: Dict, trends: Dict) -> List[Dict[str, Any]]:
        """Generate performance alerts based on metrics and trends"""

        alerts = []

        try:
            # CTR alerts
            current_ctr = metrics.get('click_through_rate', 0)
            if current_ctr < 0.03:
                alerts.append({
                    "type": "critical",
                    "category": "ctr",
                    "title": "Low Click-Through Rate",
                    "message": f"CTR of {current_ctr:.1%} is below 3% threshold",
                    "impact": "High impact on video discovery",
                    "urgency": "high",
                    "recommended_action": "Optimize thumbnails and titles immediately"
                })
            elif current_ctr < 0.05:
                alerts.append({
                    "type": "warning",
                    "category": "ctr",
                    "title": "CTR Below Average",
                    "message": f"CTR of {current_ctr:.1%} could be improved",
                    "impact": "Moderate impact on growth",
                    "urgency": "medium",
                    "recommended_action": "A/B test thumbnail designs"
                })

            # Retention alerts
            current_retention = metrics.get('average_view_percentage', 0)
            if current_retention < 0.35:
                alerts.append({
                    "type": "critical",
                    "category": "retention",
                    "title": "Low Audience Retention",
                    "message": f"Retention of {current_retention:.1%} is critically low",
                    "impact": "Severe impact on algorithm performance",
                    "urgency": "high",
                    "recommended_action": "Improve video hooks and pacing"
                })

            # Growth alerts
            growth_rate = trends.get('subscriber_growth_rate', 0)
            if growth_rate < 0:
                alerts.append({
                    "type": "critical",
                    "category": "growth",
                    "title": "Negative Growth",
                    "message": "Channel is losing subscribers",
                    "impact": "Critical impact on channel health",
                    "urgency": "critical",
                    "recommended_action": "Immediate content strategy review needed"
                })

            return alerts

        except Exception as e:
            logger.error(f"Error generating performance alerts: {e}")
            return []

    async def _generate_optimization_recommendations(self, metrics: Dict) -> List[Dict[str, Any]]:
        """Generate AI-powered optimization recommendations"""

        recommendations = []

        try:
            # Thumbnail optimization
            ctr = metrics.get('click_through_rate', 0)
            if ctr < 0.06:
                recommendations.append({
                    "category": "thumbnails",
                    "priority": "high",
                    "title": "Optimize Thumbnail Strategy",
                    "description": "Your CTR suggests thumbnail improvements could significantly boost performance",
                    "specific_actions": [
                        "Use high contrast colors and bold text",
                        "Include faces with clear emotions",
                        "A/B test different thumbnail styles",
                        "Analyze competitor thumbnail strategies"
                    ],
                    "expected_impact": "15-25% CTR improvement",
                    "timeline": "1-2 weeks",
                    "difficulty": "medium"
                })

            # Content optimization
            retention = metrics.get('average_view_percentage', 0)
            if retention < 0.50:
                recommendations.append({
                    "category": "content",
                    "priority": "high",
                    "title": "Improve Content Structure",
                    "description": "Audience retention can be significantly improved with better content structure",
                    "specific_actions": [
                        "Create stronger hooks in first 15 seconds",
                        "Add pattern interrupts every 60-90 seconds",
                        "Improve pacing and remove dead time",
                        "Use preview techniques to maintain interest"
                    ],
                    "expected_impact": "10-20% retention improvement",
                    "timeline": "2-4 weeks",
                    "difficulty": "medium"
                })

            # SEO optimization
            views = metrics.get('views', 0)
            impressions = metrics.get('impressions', 1)
            if views / impressions < 0.05:
                recommendations.append({
                    "category": "seo",
                    "priority": "medium",
                    "title": "Enhance SEO Strategy",
                    "description": "Improve discoverability through better SEO optimization",
                    "specific_actions": [
                        "Research and use trending keywords",
                        "Optimize video descriptions with keywords",
                        "Create strategic playlists",
                        "Use relevant tags and categories"
                    ],
                    "expected_impact": "20-30% discovery improvement",
                    "timeline": "3-6 weeks",
                    "difficulty": "low"
                })

            return recommendations

        except Exception as e:
            logger.error(f"Error generating optimization recommendations: {e}")
            return []

    async def _identify_trending_opportunities(self, channel_id: str, access_token: str) -> List[Dict[str, Any]]:
        """Identify trending content opportunities"""

        try:
            opportunities = []

            # Mock trending analysis - in real implementation, analyze trending videos in niche
            opportunities.append({
                "type": "trending_topic",
                "title": "Capitalize on Trending Topics",
                "description": "Several topics in your niche are trending",
                "trending_topics": ["AI tools", "productivity hacks", "2024 trends"],
                "urgency": "high",
                "potential_impact": "30-50% view increase",
                "action_deadline": "next 7 days"
            })

            return opportunities

        except Exception as e:
            logger.error(f"Error identifying trending opportunities: {e}")
            return []

    async def _generate_competitive_insights(self, channel_id: str, access_token: str) -> List[Dict[str, Any]]:
        """Generate competitive insights"""

        try:
            insights = []

            # Mock competitive analysis
            insights.append({
                "type": "competitor_analysis",
                "title": "Competitor Performance Gap",
                "description": "Similar channels are outperforming in specific areas",
                "gap_areas": ["upload_frequency", "thumbnail_quality", "seo_optimization"],
                "recommended_actions": [
                    "Increase upload frequency to 2x per week",
                    "Invest in professional thumbnail design",
                    "Improve keyword research and optimization"
                ],
                "potential_impact": "25-40% growth acceleration"
            })

            return insights

        except Exception as e:
            logger.error(f"Error generating competitive insights: {e}")
            return []

    async def _predict_growth_trajectory(self, metrics: Dict, trends: Dict) -> Dict[str, Any]:
        """Predict growth trajectory based on current performance"""

        try:
            current_subs = metrics.get('subscriber_count', 1000)
            growth_rate = trends.get('subscriber_growth_rate', 0.05)

            predictions = {
                "next_30_days": {
                    "subscribers": int(current_subs * (1 + growth_rate)),
                    "confidence": "medium",
                    "factors": ["current_growth_rate", "content_consistency"]
                },
                "next_90_days": {
                    "subscribers": int(current_subs * (1 + growth_rate * 3)),
                    "confidence": "low",
                    "factors": ["algorithm_changes", "content_strategy", "market_trends"]
                },
                "milestones": {
                    "next_1k": self._calculate_milestone_timeline(current_subs, 1000, growth_rate),
                    "next_10k": self._calculate_milestone_timeline(current_subs, 10000, growth_rate),
                    "next_100k": self._calculate_milestone_timeline(current_subs, 100000, growth_rate)
                }
            }

            return predictions

        except Exception as e:
            logger.error(f"Error predicting growth trajectory: {e}")
            return {}

    def _calculate_optimization_score(self, video_data: Dict) -> float:
        """Calculate optimization score for a video"""

        try:
            score = 50  # Base score

            # Title optimization
            title = video_data.get('title', '')
            if 30 <= len(title) <= 60:
                score += 15
            if any(word in title.lower() for word in ['how', 'best', 'top', 'guide', 'tutorial']):
                score += 10

            # Performance metrics
            ctr = video_data.get('ctr', 0)
            if ctr > 0.06:
                score += 15
            elif ctr > 0.04:
                score += 10

            retention = video_data.get('retention', 0)
            if retention > 0.50:
                score += 10
            elif retention > 0.40:
                score += 5

            return min(score, 100)

        except Exception as e:
            logger.error(f"Error calculating optimization score: {e}")
            return 50.0

    def _calculate_trending_potential(self, video_data: Dict) -> float:
        """Calculate trending potential for a video"""

        try:
            views = video_data.get('views', 0)
            likes = video_data.get('likes', 0)
            comments = video_data.get('comments', 0)

            # Calculate engagement rate
            engagement_rate = (likes + comments * 2) / max(views, 1)

            # Calculate trending score
            trending_score = min(engagement_rate * 1000, 100)

            return trending_score

        except Exception as e:
            logger.error(f"Error calculating trending potential: {e}")
            return 0.0

    def _calculate_engagement_score(self, video_data: Dict) -> float:
        """Calculate engagement score for a video"""

        try:
            views = video_data.get('views', 0)
            likes = video_data.get('likes', 0)
            comments = video_data.get('comments', 0)
            shares = video_data.get('shares', 0)

            if views == 0:
                return 0.0

            # Weighted engagement calculation
            engagement = (likes + comments * 3 + shares * 5) / views
            return min(engagement * 100, 100)

        except Exception as e:
            logger.error(f"Error calculating engagement score: {e}")
            return 0.0

    def _generate_video_recommendations(self, video_data: Dict, optimization_score: float) -> List[str]:
        """Generate specific recommendations for a video"""

        recommendations = []

        try:
            # Title recommendations
            title = video_data.get('title', '')
            if len(title) < 30:
                recommendations.append("Expand title to 30-60 characters for better SEO")
            elif len(title) > 60:
                recommendations.append("Shorten title to under 60 characters")

            # Performance recommendations
            ctr = video_data.get('ctr', 0)
            if ctr < 0.04:
                recommendations.append("Create more compelling thumbnail to improve CTR")

            retention = video_data.get('retention', 0)
            if retention < 0.40:
                recommendations.append("Improve video hook and pacing to increase retention")

            # SEO recommendations
            if optimization_score < 70:
                recommendations.append("Optimize description with relevant keywords")
                recommendations.append("Add video to relevant playlists")

            return recommendations[:3]  # Top 3 recommendations

        except Exception as e:
            logger.error(f"Error generating video recommendations: {e}")
            return ["General optimization recommended"]

    def _calculate_overall_performance_score(self, metrics: Dict) -> float:
        """Calculate overall channel performance score"""

        try:
            # Weighted scoring
            ctr_score = min(metrics.get('click_through_rate', 0) / 0.06, 1.0) * 30
            retention_score = min(metrics.get('average_view_percentage', 0) / 0.50, 1.0) * 40
            growth_score = min(metrics.get('subscriber_growth_rate', 0) / 0.10, 1.0) * 30

            total_score = (ctr_score + retention_score + growth_score)
            return round(total_score, 1)

        except Exception as e:
            logger.error(f"Error calculating performance score: {e}")
            return 50.0

    def _determine_growth_trend(self, metrics: Dict) -> str:
        """Determine growth trend direction"""

        try:
            growth_rate = metrics.get('subscriber_growth_rate', 0)

            if growth_rate > 0.10:
                return "rapid_growth"
            elif growth_rate > 0.05:
                return "steady_growth"
            elif growth_rate > 0:
                return "slow_growth"
            elif growth_rate == 0:
                return "stagnant"
            else:
                return "declining"

        except Exception as e:
            logger.error(f"Error determining growth trend: {e}")
            return "unknown"

    def _assess_channel_health(self, metrics: Dict) -> str:
        """Assess overall channel health"""

        try:
            performance_score = self._calculate_overall_performance_score(metrics)

            if performance_score >= 80:
                return "excellent"
            elif performance_score >= 60:
                return "good"
            elif performance_score >= 40:
                return "fair"
            else:
                return "needs_improvement"

        except Exception as e:
            logger.error(f"Error assessing channel health: {e}")
            return "unknown"

    def _prioritize_optimizations(self, insights: RealTimeInsights) -> List[Dict[str, Any]]:
        """Prioritize optimization recommendations"""

        try:
            all_items = []

            # Add alerts as high priority
            for alert in insights.performance_alerts or []:
                all_items.append({
                    "type": "alert",
                    "priority": 1 if alert["urgency"] == "critical" else 2,
                    "item": alert
                })

            # Add recommendations
            for rec in insights.optimization_recommendations or []:
                priority = 1 if rec["priority"] == "high" else 2 if rec["priority"] == "medium" else 3
                all_items.append({
                    "type": "recommendation",
                    "priority": priority,
                    "item": rec
                })

            # Sort by priority
            return sorted(all_items, key=lambda x: x["priority"])[:5]

        except Exception as e:
            logger.error(f"Error prioritizing optimizations: {e}")
            return []

    def _generate_action_plan(self, insights: RealTimeInsights, metrics: Dict) -> Dict[str, Any]:
        """Generate actionable plan based on insights"""

        try:
            action_plan = {
                "immediate_actions": [],
                "this_week": [],
                "this_month": [],
                "long_term": []
            }

            # Process alerts for immediate actions
            for alert in insights.performance_alerts or []:
                if alert["urgency"] in ["critical", "high"]:
                    action_plan["immediate_actions"].append({
                        "action": alert["recommended_action"],
                        "reason": alert["message"],
                        "impact": alert["impact"]
                    })

            # Process recommendations by timeline
            for rec in insights.optimization_recommendations or []:
                timeline = rec.get("timeline", "this_month")
                if "week" in timeline:
                    action_plan["this_week"].append({
                        "action": rec["title"],
                        "description": rec["description"],
                        "expected_impact": rec.get("expected_impact", "Positive impact")
                    })
                elif "month" in timeline:
                    action_plan["this_month"].append({
                        "action": rec["title"],
                        "description": rec["description"],
                        "expected_impact": rec.get("expected_impact", "Positive impact")
                    })
                else:
                    action_plan["long_term"].append({
                        "action": rec["title"],
                        "description": rec["description"],
                        "expected_impact": rec.get("expected_impact", "Positive impact")
                    })

            return action_plan

        except Exception as e:
            logger.error(f"Error generating action plan: {e}")
            return {"immediate_actions": [], "this_week": [], "this_month": [], "long_term": []}

    def _get_performance_benchmarks(self, metrics: Dict) -> Dict[str, Any]:
        """Get performance benchmarks for comparison"""

        return {
            "ctr": {
                "your_value": metrics.get('click_through_rate', 0),
                "poor": 0.02,
                "average": 0.05,
                "good": 0.08,
                "excellent": 0.12
            },
            "retention": {
                "your_value": metrics.get('average_view_percentage', 0),
                "poor": 0.30,
                "average": 0.45,
                "good": 0.60,
                "excellent": 0.75
            },
            "growth_rate": {
                "your_value": metrics.get('subscriber_growth_rate', 0),
                "poor": 0.01,
                "average": 0.05,
                "good": 0.10,
                "excellent": 0.20
            }
        }

    def _predict_30_day_performance(self, metrics: Dict) -> Dict[str, Any]:
        """Predict 30-day performance"""

        try:
            current_views = metrics.get('views', 0)
            current_subs = metrics.get('subscriber_count', 0)
            growth_rate = metrics.get('subscriber_growth_rate', 0.05)

            return {
                "predicted_views": int(current_views * 1.2),  # Assume 20% growth
                "predicted_subscribers": int(current_subs * (1 + growth_rate)),
                "confidence": "medium",
                "factors": ["current_trends", "seasonal_patterns", "content_strategy"]
            }

        except Exception as e:
            logger.error(f"Error predicting 30-day performance: {e}")
            return {}

    def _predict_growth_milestones(self, metrics: Dict) -> Dict[str, Any]:
        """Predict when growth milestones will be reached"""

        try:
            current_subs = metrics.get('subscriber_count', 0)
            growth_rate = metrics.get('subscriber_growth_rate', 0.05)

            milestones = {}
            targets = [1000, 10000, 100000, 1000000]

            for target in targets:
                if current_subs < target:
                    months = self._calculate_milestone_timeline(current_subs, target, growth_rate)
                    milestones[f"{target:,}_subscribers"] = {
                        "timeline": months,
                        "confidence": "medium" if months < 24 else "low"
                    }
                    break

            return milestones

        except Exception as e:
            logger.error(f"Error predicting growth milestones: {e}")
            return {}

    def _calculate_milestone_timeline(self, current: int, target: int, growth_rate: float) -> str:
        """Calculate timeline to reach milestone"""

        try:
            if growth_rate <= 0 or current >= target:
                return "Unable to calculate"

            import math
            months = math.log(target / current) / math.log(1 + growth_rate)

            if months < 1:
                return "Less than 1 month"
            elif months < 12:
                return f"{int(months)} months"
            else:
                years = months / 12
                return f"{years:.1f} years"

        except Exception as e:
            logger.error(f"Error calculating milestone timeline: {e}")
            return "Unable to calculate"

    async def _get_video_analytics(self, video_id: str, access_token: str) -> Dict[str, Any]:
        """Get analytics for a specific video"""

        try:
            # Mock implementation - in real app, use YouTube Analytics API
            return {
                "video_id": video_id,
                "title": f"Video {video_id}",
                "views": 1000,
                "likes": 50,
                "comments": 10,
                "shares": 5,
                "ctr": 0.05,
                "retention": 0.45
            }
        except Exception as e:
            logger.error(f"Error getting video analytics: {e}")
            return {}

    async def _get_recent_video_performance(self, channel_id: str, access_token: str) -> List[VideoPerformanceInsight]:
        """Get recent video performance insights"""

        try:
            # Mock implementation
            recent_videos = ["video_1", "video_2", "video_3"]
            return await self.get_video_performance_insights(recent_videos, access_token)
        except Exception as e:
            logger.error(f"Error getting recent video performance: {e}")
            return []

    async def _analyze_performance_trends(self, channel_id: str, access_token: str) -> Dict[str, Any]:
        """Analyze performance trends over time"""

        try:
            # Mock implementation - in real app, analyze historical data
            return {
                "subscriber_growth_rate": 0.05,
                "view_growth_rate": 0.10,
                "engagement_trend": "increasing",
                "performance_trend": "stable"
            }
        except Exception as e:
            logger.error(f"Error analyzing performance trends: {e}")
            return {}
            
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