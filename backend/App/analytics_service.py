"""
YouTube Analytics Service for Vidalytics
Provides real-time channel analytics and performance insights
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import from parent directory for production deployment
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from oauth_manager import OAuthManager

logger = logging.getLogger(__name__)

@dataclass
class ChannelAnalytics:
    """Channel-level analytics data"""
    channel_id: str
    date_range: str
    
    # Core metrics
    views: int
    watch_time_hours: float
    subscribers_gained: int
    subscribers_lost: int
    net_subscriber_change: int
    
    # Engagement metrics
    likes: int
    dislikes: int
    comments: int
    shares: int
    average_view_duration: float
    
    # Performance metrics
    ctr: float  # Click-through rate
    average_view_percentage: float  # Retention rate
    subscriber_conversion_rate: float
    
    # Revenue metrics (if monetized)
    estimated_revenue: Optional[float] = None
    rpm: Optional[float] = None  # Revenue per mille
    cpm: Optional[float] = None  # Cost per mille
    
    # Traffic sources
    traffic_source_youtube_search: float = 0.0
    traffic_source_external: float = 0.0
    traffic_source_suggested_videos: float = 0.0
    traffic_source_browse_features: float = 0.0
    traffic_source_direct: float = 0.0
    
    # Demographics
    audience_retention_graph: List[Dict[str, float]] = None
    top_countries: List[Dict[str, Any]] = None
    age_gender_breakdown: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

@dataclass
class VideoAnalytics:
    """Individual video analytics data"""
    video_id: str
    title: str
    published_at: str
    date_range: str
    
    # Core metrics
    views: int
    watch_time_hours: float
    likes: int
    dislikes: int
    comments: int
    shares: int
    
    # Performance metrics
    ctr: float
    average_view_duration: float
    average_view_percentage: float
    
    # Traffic and discovery
    impressions: int
    impressions_ctr: float
    traffic_sources: Dict[str, float]
    
    # Revenue (if monetized)
    estimated_revenue: Optional[float] = None
    rpm: Optional[float] = None
    
    # Retention data
    audience_retention: List[Dict[str, float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

class AnalyticsService:
    """YouTube Analytics API service"""
    
    def __init__(self, oauth_manager: OAuthManager):
        self.oauth_manager = oauth_manager
        self._analytics_cache: Dict[str, Any] = {}
        self._cache_ttl = 1800  # 30 minutes
    
    async def get_channel_analytics(
        self, 
        user_id: str, 
        days: int = 30,
        force_refresh: bool = False
    ) -> Optional[ChannelAnalytics]:
        """
        Get comprehensive channel analytics for the specified period
        
        Args:
            user_id: User ID
            days: Number of days to analyze (7, 30, 90)
            force_refresh: Force fresh data fetch
        """
        try:
            # Check cache first
            cache_key = f"channel_analytics_{user_id}_{days}"
            if not force_refresh and self._is_cache_valid(cache_key):
                cached_data = self._analytics_cache[cache_key]
                logger.info(f"Returning cached channel analytics for {user_id}")
                return ChannelAnalytics(**cached_data['data'])
            
            # Get valid OAuth token
            token = await self.oauth_manager.get_valid_token(user_id)
            if not token:
                logger.error(f"❌ No valid OAuth token for user {user_id} - analytics data unavailable")
                oauth_status = self.oauth_manager.get_oauth_status(user_id)
                logger.info(f"🔐 OAuth status: {oauth_status}")
                return None
            
            # Get channel ID
            channel_id = await self._get_channel_id(user_id, token)
            if not channel_id:
                logger.error(f"Could not get channel ID for user {user_id}")
                return None
            
            # Build services
            analytics = self._build_analytics_service(token)
            youtube = self._build_youtube_service(token)
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            date_range = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            
            # Fetch core analytics data
            core_metrics = await self._fetch_core_channel_metrics(
                analytics, channel_id, start_date, end_date
            )
            
            # Fetch traffic source data
            traffic_sources = await self._fetch_traffic_sources(
                analytics, channel_id, start_date, end_date
            )
            
            # Fetch demographics data
            demographics = await self._fetch_demographics(
                analytics, channel_id, start_date, end_date
            )
            
            # Fetch revenue data (if available)
            revenue_data = await self._fetch_revenue_data(
                analytics, channel_id, start_date, end_date
            )
            
            # Combine all data
            channel_analytics = ChannelAnalytics(
                channel_id=channel_id,
                date_range=date_range,
                **core_metrics,
                **traffic_sources,
                **demographics,
                **revenue_data
            )
            
            # Cache the result
            self._cache_analytics_data(cache_key, channel_analytics.to_dict())
            
            logger.info(f"✅ Fetched channel analytics for {user_id}: {core_metrics.get('views', 0)} views in {days} days")
            return channel_analytics
            
        except Exception as e:
            logger.error(f"Failed to get channel analytics for {user_id}: {e}")
            return None
    
    async def get_video_analytics(
        self, 
        user_id: str, 
        video_id: str,
        days: int = 30,
        force_refresh: bool = False
    ) -> Optional[VideoAnalytics]:
        """
        Get comprehensive analytics for a specific video
        
        Args:
            user_id: User ID
            video_id: YouTube video ID
            days: Number of days to analyze
            force_refresh: Force fresh data fetch
        """
        try:
            # Check cache first
            cache_key = f"video_analytics_{user_id}_{video_id}_{days}"
            if not force_refresh and self._is_cache_valid(cache_key):
                cached_data = self._analytics_cache[cache_key]
                logger.info(f"Returning cached video analytics for {video_id}")
                return VideoAnalytics(**cached_data['data'])
            
            # Get valid OAuth token
            token = await self.oauth_manager.get_valid_token(user_id)
            if not token:
                logger.error(f"❌ No valid OAuth token for user {user_id} - analytics data unavailable")
                oauth_status = self.oauth_manager.get_oauth_status(user_id)
                logger.info(f"🔐 OAuth status: {oauth_status}")
                return None
            
            # Build services
            analytics = self._build_analytics_service(token)
            youtube = self._build_youtube_service(token)
            
            # Get video details
            video_details = await self._get_video_details(youtube, video_id)
            if not video_details:
                logger.error(f"Could not get video details for {video_id}")
                return None
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            date_range = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            
            # Fetch video analytics
            video_metrics = await self._fetch_video_metrics(
                analytics, video_id, start_date, end_date
            )
            
            # Fetch traffic sources for video
            video_traffic = await self._fetch_video_traffic_sources(
                analytics, video_id, start_date, end_date
            )
            
            # Fetch retention data
            retention_data = await self._fetch_video_retention(
                analytics, video_id, start_date, end_date
            )
            
            # Combine all data
            video_analytics = VideoAnalytics(
                video_id=video_id,
                title=video_details['title'],
                published_at=video_details['published_at'],
                date_range=date_range,
                **video_metrics,
                traffic_sources=video_traffic,
                audience_retention=retention_data
            )
            
            # Cache the result
            self._cache_analytics_data(cache_key, video_analytics.to_dict())
            
            logger.info(f"✅ Fetched video analytics for {video_id}: {video_metrics.get('views', 0)} views")
            return video_analytics
            
        except Exception as e:
            logger.error(f"Failed to get video analytics for {video_id}: {e}")
            return None
    
    async def get_recent_performance_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a quick performance summary for the last 7 days vs previous 7 days
        Perfect for real-time chat context
        """
        try:
            # Get current week data
            current_week = await self.get_channel_analytics(user_id, days=7)
            if not current_week:
                return None
            
            # Get previous week data for comparison
            token = await self.oauth_manager.get_valid_token(user_id)
            if not token:
                return None
            
            channel_id = await self._get_channel_id(user_id, token)
            analytics = self._build_analytics_service(token)
            
            # Calculate date ranges
            end_date = datetime.now() - timedelta(days=7)
            start_date = end_date - timedelta(days=7)
            
            previous_metrics = await self._fetch_core_channel_metrics(
                analytics, channel_id, start_date, end_date
            )
            
            # Calculate percentage changes
            def calc_change(current, previous):
                if previous == 0:
                    return float('inf') if current > 0 else 0
                return ((current - previous) / previous) * 100
            
            # Calculate algorithm performance score
            algorithm_score = self.calculate_algorithm_performance_score(current_week)
            
            summary = {
                'current_period': current_week.to_dict(),
                'performance_changes': {
                    'views_change': calc_change(current_week.views, previous_metrics.get('views', 0)),
                    'watch_time_change': calc_change(current_week.watch_time_hours, previous_metrics.get('watch_time_hours', 0)),
                    'subscribers_change': calc_change(current_week.net_subscriber_change, previous_metrics.get('net_subscriber_change', 0)),
                    'ctr_change': calc_change(current_week.ctr, previous_metrics.get('ctr', 0)),
                    'retention_change': calc_change(current_week.average_view_percentage, previous_metrics.get('average_view_percentage', 0))
                },
                'algorithm_performance': algorithm_score,
                'top_insights': self._generate_performance_insights(current_week, previous_metrics)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get performance summary for {user_id}: {e}")
            return None
    
    def _generate_performance_insights(self, current: ChannelAnalytics, previous: Dict[str, Any]) -> List[str]:
        """Generate human-readable performance insights"""
        insights = []
        
        # Views insight
        views_change = ((current.views - previous.get('views', 0)) / previous.get('views', 1)) * 100 if previous.get('views', 0) > 0 else 0
        if views_change > 20:
            insights.append(f"🚀 Views are up {views_change:.1f}% this week!")
        elif views_change < -20:
            insights.append(f"📉 Views are down {abs(views_change):.1f}% this week")
        
        # CTR insight
        if current.ctr > 8:
            insights.append(f"🎯 Excellent CTR of {current.ctr:.1f}% - your thumbnails are working!")
        elif current.ctr < 3:
            insights.append(f"📸 CTR is {current.ctr:.1f}% - consider optimizing thumbnails")
        
        # Retention insight
        if current.average_view_percentage > 60:
            insights.append(f"⏱️ Great retention at {current.average_view_percentage:.1f}% - engaging content!")
        elif current.average_view_percentage < 30:
            insights.append(f"⏱️ Retention at {current.average_view_percentage:.1f}% - try shorter intros")
        
        # Subscriber insight
        if current.net_subscriber_change > 0:
            insights.append(f"👥 +{current.net_subscriber_change} net subscribers this week")
        
        # Traffic source insight
        if current.traffic_source_youtube_search > 50:
            insights.append("🔍 Most traffic from YouTube search - your SEO is strong!")
        elif current.traffic_source_suggested_videos > 50:
            insights.append("📺 Most traffic from suggested videos - algorithm loves your content!")
        
        return insights[:3]  # Return top 3 insights
    
    def calculate_algorithm_performance_score(self, analytics: ChannelAnalytics) -> Dict[str, Any]:
        """
        Calculate YouTube Algorithm Performance Score (0-100)
        Based on key metrics that influence algorithm recommendations
        """
        try:
            score_components = {}
            total_score = 0
            max_possible_score = 100
            
            # 1. Click-Through Rate (CTR) Score - 25 points max
            ctr_score = 0
            if analytics.ctr >= 10:
                ctr_score = 25  # Exceptional CTR
            elif analytics.ctr >= 8:
                ctr_score = 22  # Excellent CTR
            elif analytics.ctr >= 6:
                ctr_score = 18  # Very good CTR
            elif analytics.ctr >= 4:
                ctr_score = 14  # Good CTR
            elif analytics.ctr >= 2:
                ctr_score = 8   # Below average CTR
            else:
                ctr_score = 2   # Poor CTR
            
            score_components['ctr_score'] = ctr_score
            total_score += ctr_score
            
            # 2. Average View Percentage (Retention) Score - 25 points max
            retention_score = 0
            if analytics.average_view_percentage >= 70:
                retention_score = 25  # Exceptional retention
            elif analytics.average_view_percentage >= 60:
                retention_score = 22  # Excellent retention
            elif analytics.average_view_percentage >= 50:
                retention_score = 18  # Very good retention
            elif analytics.average_view_percentage >= 40:
                retention_score = 14  # Good retention
            elif analytics.average_view_percentage >= 30:
                retention_score = 8   # Below average retention
            else:
                retention_score = 2   # Poor retention
            
            score_components['retention_score'] = retention_score
            total_score += retention_score
            
            # 3. Engagement Rate Score - 20 points max
            # Calculate engagement rate from likes, comments, shares
            total_engagement = analytics.likes + analytics.comments + analytics.shares
            engagement_rate = (total_engagement / max(analytics.views, 1)) * 100
            
            engagement_score = 0
            if engagement_rate >= 8:
                engagement_score = 20  # Exceptional engagement
            elif engagement_rate >= 6:
                engagement_score = 17  # Excellent engagement
            elif engagement_rate >= 4:
                engagement_score = 14  # Very good engagement
            elif engagement_rate >= 2:
                engagement_score = 10  # Good engagement
            elif engagement_rate >= 1:
                engagement_score = 6   # Below average engagement
            else:
                engagement_score = 2   # Poor engagement
            
            score_components['engagement_score'] = engagement_score
            total_score += engagement_score
            
            # 4. Watch Time Score - 15 points max
            # Based on average view duration vs typical video length
            avg_duration_minutes = analytics.average_view_duration / 60
            watch_time_score = 0
            
            if avg_duration_minutes >= 8:
                watch_time_score = 15  # Exceptional watch time
            elif avg_duration_minutes >= 6:
                watch_time_score = 13  # Excellent watch time
            elif avg_duration_minutes >= 4:
                watch_time_score = 10  # Good watch time
            elif avg_duration_minutes >= 2:
                watch_time_score = 6   # Below average watch time
            else:
                watch_time_score = 2   # Poor watch time
            
            score_components['watch_time_score'] = watch_time_score
            total_score += watch_time_score
            
            # 5. Subscriber Growth Score - 15 points max
            subscriber_score = 0
            if analytics.net_subscriber_change >= 100:
                subscriber_score = 15  # Exceptional growth
            elif analytics.net_subscriber_change >= 50:
                subscriber_score = 13  # Excellent growth
            elif analytics.net_subscriber_change >= 20:
                subscriber_score = 10  # Good growth
            elif analytics.net_subscriber_change >= 5:
                subscriber_score = 6   # Moderate growth
            elif analytics.net_subscriber_change >= 0:
                subscriber_score = 3   # Stable
            else:
                subscriber_score = 0   # Declining
            
            score_components['subscriber_score'] = subscriber_score
            total_score += subscriber_score
            
            # Determine algorithm favorability
            if total_score >= 85:
                favorability = "Excellent"
                recommendation = "Your content is highly favored by the algorithm"
            elif total_score >= 70:
                favorability = "Very Good"
                recommendation = "Algorithm performance is strong with room for optimization"
            elif total_score >= 55:
                favorability = "Good"
                recommendation = "Solid algorithm performance, focus on retention and CTR"
            elif total_score >= 40:
                favorability = "Fair"
                recommendation = "Algorithm performance needs improvement in key areas"
            else:
                favorability = "Poor"
                recommendation = "Focus on fundamentals: thumbnails, hooks, and content quality"
            
            # Identify improvement areas
            improvement_areas = []
            if ctr_score < 15:
                improvement_areas.append("Thumbnail and title optimization")
            if retention_score < 15:
                improvement_areas.append("Content structure and hooks")
            if engagement_score < 12:
                improvement_areas.append("Audience engagement strategies")
            if watch_time_score < 8:
                improvement_areas.append("Content length and pacing")
            if subscriber_score < 8:
                improvement_areas.append("Subscriber conversion tactics")
            
            return {
                'overall_score': total_score,
                'favorability': favorability,
                'recommendation': recommendation,
                'score_components': score_components,
                'improvement_areas': improvement_areas,
                'metrics_breakdown': {
                    'ctr_rating': self._get_metric_rating(analytics.ctr, [(2, "Poor"), (4, "Fair"), (6, "Good"), (8, "Excellent"), (10, "Exceptional")]),
                    'retention_rating': self._get_metric_rating(analytics.average_view_percentage, [(30, "Poor"), (40, "Fair"), (50, "Good"), (60, "Excellent"), (70, "Exceptional")]),
                    'engagement_rating': self._get_metric_rating(engagement_rate, [(1, "Poor"), (2, "Fair"), (4, "Good"), (6, "Excellent"), (8, "Exceptional")]),
                    'watch_time_rating': self._get_metric_rating(avg_duration_minutes, [(2, "Poor"), (4, "Fair"), (6, "Good"), (8, "Excellent")]),
                    'growth_rating': self._get_metric_rating(analytics.net_subscriber_change, [(0, "Stable"), (5, "Fair"), (20, "Good"), (50, "Excellent"), (100, "Exceptional")])
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate algorithm performance score: {e}")
            return {
                'overall_score': 0,
                'favorability': 'Unknown',
                'recommendation': 'Unable to calculate algorithm performance score',
                'score_components': {},
                'improvement_areas': [],
                'metrics_breakdown': {}
            }
    
    def _get_metric_rating(self, value: float, thresholds: List[Tuple[float, str]]) -> str:
        """Get rating for a metric based on thresholds"""
        for threshold, rating in reversed(thresholds):
            if value >= threshold:
                return rating
        return thresholds[0][1] if thresholds else "Unknown"
    
    async def _get_channel_id(self, user_id: str, token) -> Optional[str]:
        """Get the user's channel ID"""
        try:
            # First check if we have it in user context
            from backend.ai_services import get_user_context
            context = get_user_context(user_id)
            channel_info = context.get('channel_info', {})

            if channel_info.get('channel_id'):
                return channel_info['channel_id']

            # If not, fetch from YouTube API
            youtube = self._build_youtube_service(token)
            channels_response = youtube.channels().list(
                part='id',
                mine=True
            ).execute()

            if channels_response['items']:
                channel_id = channels_response['items'][0]['id']

                # Store for future use
                channel_info['channel_id'] = channel_id
                from backend.ai_services import update_user_context
                update_user_context(user_id, "channel_info", channel_info)

                return channel_id
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get channel ID for {user_id}: {e}")
            return None
    
    def _build_analytics_service(self, token):
        """Build YouTube Analytics API service"""
        credentials = Credentials(
            token=token.access_token,
            refresh_token=token.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.oauth_manager.client_id,
            client_secret=self.oauth_manager.client_secret,
            scopes=token.scope.split()
        )
        
        return build('youtubeAnalytics', 'v2', credentials=credentials)
    
    def _build_youtube_service(self, token):
        """Build YouTube Data API service"""
        credentials = Credentials(
            token=token.access_token,
            refresh_token=token.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.oauth_manager.client_id,
            client_secret=self.oauth_manager.client_secret,
            scopes=token.scope.split()
        )
        
        return build('youtube', 'v3', credentials=credentials)
    
    async def _fetch_core_channel_metrics(self, analytics, channel_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Fetch core channel metrics from Analytics API"""
        try:
            # Core metrics query
            response = analytics.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='views,estimatedMinutesWatched,subscribersGained,subscribersLost,likes,dislikes,comments,shares,averageViewDuration',
                dimensions='day'
            ).execute()
            
            # Process results
            metrics = {
                'views': 0,
                'watch_time_hours': 0.0,
                'subscribers_gained': 0,
                'subscribers_lost': 0,
                'net_subscriber_change': 0,
                'likes': 0,
                'dislikes': 0,
                'comments': 0,
                'shares': 0,
                'average_view_duration': 0.0,
                'ctr': 0.0,
                'average_view_percentage': 0.0,
                'subscriber_conversion_rate': 0.0
            }
            
            if response.get('rows'):
                for row in response['rows']:
                    metrics['views'] += int(row[1] or 0)
                    metrics['watch_time_hours'] += float(row[2] or 0) / 60.0
                    metrics['subscribers_gained'] += int(row[3] or 0)
                    metrics['subscribers_lost'] += int(row[4] or 0)
                    metrics['likes'] += int(row[5] or 0)
                    metrics['dislikes'] += int(row[6] or 0)
                    metrics['comments'] += int(row[7] or 0)
                    metrics['shares'] += int(row[8] or 0)
                    if row[9]:
                        metrics['average_view_duration'] += float(row[9])
                
                # Calculate derived metrics
                metrics['net_subscriber_change'] = metrics['subscribers_gained'] - metrics['subscribers_lost']
                
                # Get CTR and retention data
                ctr_response = analytics.reports().query(
                    ids=f'channel=={channel_id}',
                    startDate=start_date.strftime('%Y-%m-%d'),
                    endDate=end_date.strftime('%Y-%m-%d'),
                    metrics='cardClickRate,averageViewPercentage'
                ).execute()
                
                if ctr_response.get('rows') and ctr_response['rows'][0]:
                    row = ctr_response['rows'][0]
                    metrics['ctr'] = float(row[0] or 0)
                    metrics['average_view_percentage'] = float(row[1] or 0)
                
                # Calculate conversion rate
                if metrics['views'] > 0:
                    metrics['subscriber_conversion_rate'] = (metrics['subscribers_gained'] / metrics['views']) * 100
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to fetch core channel metrics: {e}")
            return {}
    
    async def _fetch_traffic_sources(self, analytics, channel_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """Fetch traffic source breakdown"""
        try:
            response = analytics.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='views',
                dimensions='insightTrafficSourceType',
                sort='-views'
            ).execute()
            
            traffic_sources = {
                'traffic_source_youtube_search': 0.0,
                'traffic_source_external': 0.0,
                'traffic_source_suggested_videos': 0.0,
                'traffic_source_browse_features': 0.0,
                'traffic_source_direct': 0.0
            }
            
            total_views = 0
            traffic_mapping = {
                'YT_SEARCH': 'traffic_source_youtube_search',
                'EXT_URL': 'traffic_source_external',
                'RELATED_VIDEO': 'traffic_source_suggested_videos',
                'YT_CHANNEL': 'traffic_source_direct',
                'NOTIFICATION': 'traffic_source_direct'
            }
            
            if response.get('rows'):
                for row in response['rows']:
                    source_type = row[0]
                    views = int(row[1])
                    total_views += views
                
                # Calculate percentages
                for row in response['rows']:
                    source_type = row[0]
                    views = int(row[1])
                    percentage = (views / total_views * 100) if total_views > 0 else 0
                    
                    mapped_key = traffic_mapping.get(source_type)
                    if mapped_key:
                        traffic_sources[mapped_key] = percentage
            
            return traffic_sources
            
        except Exception as e:
            logger.error(f"Failed to fetch traffic sources: {e}")
            return {}
    
    async def _fetch_demographics(self, analytics, channel_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Fetch audience demographics"""
        try:
            # Get top countries
            countries_response = analytics.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='views',
                dimensions='country',
                sort='-views',
                maxResults=10
            ).execute()
            
            top_countries = []
            if countries_response.get('rows'):
                total_views = sum(int(row[1]) for row in countries_response['rows'])
                for row in countries_response['rows']:
                    country = row[0]
                    views = int(row[1])
                    percentage = (views / total_views * 100) if total_views > 0 else 0
                    top_countries.append({
                        'country': country,
                        'views': views,
                        'percentage': percentage
                    })
            
            # Get age/gender breakdown
            age_gender_response = analytics.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='viewerPercentage',
                dimensions='ageGroup,gender'
            ).execute()
            
            age_gender_breakdown = {}
            if age_gender_response.get('rows'):
                for row in age_gender_response['rows']:
                    age_group = row[0]
                    gender = row[1]
                    percentage = float(row[2])
                    key = f"{age_group}_{gender}"
                    age_gender_breakdown[key] = percentage
            
            return {
                'top_countries': top_countries,
                'age_gender_breakdown': age_gender_breakdown
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch demographics: {e}")
            return {'top_countries': [], 'age_gender_breakdown': {}}
    
    async def _fetch_revenue_data(self, analytics, channel_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Fetch revenue data (if available)"""
        try:
            response = analytics.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='estimatedRevenue,cpm,playbackBasedCpm'
            ).execute()
            
            revenue_data = {
                'estimated_revenue': None,
                'rpm': None,
                'cpm': None
            }
            
            if response.get('rows') and response['rows'][0]:
                row = response['rows'][0]
                revenue_data['estimated_revenue'] = float(row[0]) if row[0] else None
                revenue_data['cpm'] = float(row[1]) if row[1] else None
                revenue_data['rpm'] = float(row[2]) if row[2] else None
            
            return revenue_data
            
        except HttpError as e:
            # Revenue data might not be available for all channels
            logger.info(f"Revenue data not available for channel {channel_id}: {e}")
            return {'estimated_revenue': None, 'rpm': None, 'cpm': None}
        except Exception as e:
            logger.error(f"Failed to fetch revenue data: {e}")
            return {'estimated_revenue': None, 'rpm': None, 'cpm': None}
    
    async def _fetch_video_metrics(self, analytics, video_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Fetch metrics for a specific video"""
        try:
            response = analytics.reports().query(
                filters=f'video=={video_id}',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='views,estimatedMinutesWatched,likes,dislikes,comments,shares,averageViewDuration,averageViewPercentage'
            ).execute()
            
            metrics = {
                'views': 0,
                'watch_time_hours': 0.0,
                'likes': 0,
                'dislikes': 0,
                'comments': 0,
                'shares': 0,
                'average_view_duration': 0.0,
                'average_view_percentage': 0.0,
                'ctr': 0.0,
                'impressions': 0,
                'impressions_ctr': 0.0
            }
            
            if response.get('rows') and response['rows'][0]:
                row = response['rows'][0]
                metrics['views'] = int(row[0] or 0)
                metrics['watch_time_hours'] = float(row[1] or 0) / 60.0
                metrics['likes'] = int(row[2] or 0)
                metrics['dislikes'] = int(row[3] or 0)
                metrics['comments'] = int(row[4] or 0)
                metrics['shares'] = int(row[5] or 0)
                metrics['average_view_duration'] = float(row[6] or 0)
                metrics['average_view_percentage'] = float(row[7] or 0)
            
            # Get impressions and CTR
            impressions_response = analytics.reports().query(
                filters=f'video=={video_id}',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='cardImpressions,cardClickRate'
            ).execute()
            
            if impressions_response.get('rows') and impressions_response['rows'][0]:
                row = impressions_response['rows'][0]
                metrics['impressions'] = int(row[0] or 0)
                metrics['impressions_ctr'] = float(row[1] or 0)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to fetch video metrics for {video_id}: {e}")
            return {}
    
    async def _fetch_video_traffic_sources(self, analytics, video_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """Fetch traffic sources for a specific video"""
        try:
            response = analytics.reports().query(
                filters=f'video=={video_id}',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='views',
                dimensions='insightTrafficSourceType'
            ).execute()
            
            traffic_sources = {}
            total_views = 0
            
            if response.get('rows'):
                for row in response['rows']:
                    views = int(row[1])
                    total_views += views
                
                for row in response['rows']:
                    source_type = row[0]
                    views = int(row[1])
                    percentage = (views / total_views * 100) if total_views > 0 else 0
                    traffic_sources[source_type] = percentage
            
            return traffic_sources
            
        except Exception as e:
            logger.error(f"Failed to fetch video traffic sources: {e}")
            return {}
    
    async def _fetch_video_retention(self, analytics, video_id: str, start_date: datetime, end_date: datetime) -> List[Dict[str, float]]:
        """Fetch audience retention data for a video"""
        try:
            response = analytics.reports().query(
                filters=f'video=={video_id}',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='audienceRetentionForPlaybackLocation',
                dimensions='elapsedVideoTimeRatio'
            ).execute()
            
            retention_data = []
            if response.get('rows'):
                for row in response['rows']:
                    time_ratio = float(row[0])
                    retention = float(row[1])
                    retention_data.append({
                        'time_ratio': time_ratio,
                        'retention_percentage': retention
                    })
            
            return retention_data
            
        except Exception as e:
            logger.error(f"Failed to fetch video retention for {video_id}: {e}")
            return []
    
    async def _get_video_details(self, youtube, video_id: str) -> Optional[Dict[str, Any]]:
        """Get basic video details"""
        try:
            response = youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            
            if response['items']:
                video = response['items'][0]
                return {
                    'title': video['snippet']['title'],
                    'published_at': video['snippet']['publishedAt']
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get video details for {video_id}: {e}")
            return None
    
    def _cache_analytics_data(self, key: str, data: Dict[str, Any]):
        """Cache analytics data with timestamp"""
        self._analytics_cache[key] = {
            'data': data,
            'timestamp': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=self._cache_ttl)
        }
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self._analytics_cache:
            return False
        
        cache_entry = self._analytics_cache[key]
        return datetime.now() < cache_entry['expires_at']
    
    def clear_cache(self, user_id: Optional[str] = None):
        """Clear analytics cache for a user or all users"""
        if user_id:
            # Clear cache for specific user
            keys_to_remove = [k for k in self._analytics_cache.keys() if user_id in k]
            for key in keys_to_remove:
                del self._analytics_cache[key]
            logger.info(f"Cleared analytics cache for user {user_id}")
        else:
            # Clear all cache
            self._analytics_cache.clear()
            logger.info("Cleared all analytics cache")

# Global analytics service instance
_analytics_service = None

def get_analytics_service() -> AnalyticsService:
    """Get global analytics service instance"""
    global _analytics_service
    if _analytics_service is None:
        from backend.oauth_manager import get_oauth_manager
        oauth_manager = get_oauth_manager()  # Use global OAuth manager
        _analytics_service = AnalyticsService(oauth_manager)
    return _analytics_service