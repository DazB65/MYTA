"""
Enhanced YouTube API Integration for CreatorMate Multi-Agent System
Provides comprehensive YouTube data with caching and quota management
"""

import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import re
import time
import hashlib
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from agent_cache import get_agent_cache
from oauth_manager import get_oauth_manager

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class YouTubeVideoMetrics:
    """Comprehensive video metrics"""
    video_id: str
    title: str
    description: str
    tags: List[str]
    published_at: str
    thumbnail_url: str
    duration: str
    view_count: int
    like_count: int
    comment_count: int
    definition: str
    category_id: str
    default_language: Optional[str] = None
    
    # Calculated metrics
    engagement_rate: float = 0.0
    ctr_estimate: float = 0.0
    retention_estimate: float = 0.0

@dataclass
class YouTubeChannelMetrics:
    """Comprehensive channel metrics"""
    channel_id: str
    title: str
    description: str
    custom_url: Optional[str]
    published_at: str
    thumbnail_url: str
    country: Optional[str]
    view_count: int
    subscriber_count: int
    video_count: int
    
    # Recent performance
    recent_videos: List[YouTubeVideoMetrics]
    avg_views_last_30: float = 0.0
    avg_engagement_last_30: float = 0.0
    upload_frequency: str = "unknown"

@dataclass
class YouTubeCommentData:
    """Comment data for sentiment analysis"""
    comment_id: str
    video_id: str
    author_name: str
    text: str
    like_count: int
    published_at: str
    reply_count: int = 0
    parent_id: Optional[str] = None

class YouTubeQuotaManager:
    """Manages YouTube API quota usage"""
    
    def __init__(self):
        self.daily_quota = 10000  # YouTube API default quota
        self.used_quota = 0
        self.quota_reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        self.operation_costs = {
            'videos.list': 1,
            'channels.list': 1,
            'search.list': 100,
            'commentThreads.list': 1,
            'playlists.list': 1,
            'playlistItems.list': 1
        }
    
    def check_quota(self, operation: str, estimated_calls: int = 1) -> bool:
        """Check if operation is within quota limits"""
        cost = self.operation_costs.get(operation, 1) * estimated_calls
        
        # Reset quota if new day
        if datetime.now() >= self.quota_reset_time:
            self.used_quota = 0
            self.quota_reset_time += timedelta(days=1)
        
        return (self.used_quota + cost) <= self.daily_quota
    
    def consume_quota(self, operation: str, actual_calls: int = 1):
        """Record quota usage"""
        cost = self.operation_costs.get(operation, 1) * actual_calls
        self.used_quota += cost
        logger.info(f"Quota used: {cost} units. Total: {self.used_quota}/{self.daily_quota}")
    
    def get_quota_status(self) -> Dict[str, Any]:
        """Get current quota status"""
        return {
            "daily_quota": self.daily_quota,
            "used_quota": self.used_quota,
            "remaining_quota": self.daily_quota - self.used_quota,
            "quota_reset_time": self.quota_reset_time.isoformat(),
            "usage_percentage": (self.used_quota / self.daily_quota) * 100
        }

def parse_duration(duration_str: str) -> str:
    """Convert YouTube duration format (PT4M47S) to readable format (4:47)"""
    if not duration_str:
        return "0:00"
    
    # Parse ISO 8601 duration
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return "0:00"
    
    hours, minutes, seconds = match.groups()
    hours = int(hours) if hours else 0
    minutes = int(minutes) if minutes else 0
    seconds = int(seconds) if seconds else 0
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


class YouTubeAPIIntegration:
    """Enhanced YouTube API integration with caching and quota management"""
    
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY") or os.getenv("YT_API_KEY")
        self.youtube = None
        self.simple_cache = {}  # Simple in-memory cache
        self.cache_ttl = {}  # Track TTL for cache entries
        self.quota_manager = YouTubeQuotaManager()
        self.oauth_manager = get_oauth_manager()
        
        # Initialize with API key (fallback for public data)
        if self.api_key:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                logger.info("YouTube API client initialized successfully with API key")
            except Exception as e:
                logger.error(f"Failed to initialize YouTube API client: {e}")
        else:
            logger.warning("YOUTUBE_API_KEY not found in environment variables")
    
    def _cache_get(self, key: str) -> Optional[Any]:
        """Get from simple cache if not expired"""
        if key in self.simple_cache and key in self.cache_ttl:
            if time.time() < self.cache_ttl[key]:
                return self.simple_cache[key]
            else:
                # Expired, remove from cache
                del self.simple_cache[key]
                del self.cache_ttl[key]
        return None
    
    def _cache_set(self, key: str, value: Any, ttl: int = 3600):
        """Set in simple cache with TTL"""
        self.simple_cache[key] = value
        self.cache_ttl[key] = time.time() + ttl
    
    async def get_authenticated_service(self, user_id: str, service_name: str = "youtube", version: str = "v3"):
        """Get authenticated YouTube service for a user"""
        try:
            service = await self.oauth_manager.get_youtube_service(user_id, service_name, version)
            if service:
                logger.info(f"Using OAuth-authenticated YouTube service for user {user_id}")
                return service
            else:
                logger.warning(f"No OAuth token available for user {user_id}, falling back to API key")
                return self.youtube
        except Exception as e:
            logger.error(f"Failed to get authenticated service for user {user_id}: {e}")
            return self.youtube
    
    def _generate_cache_key(self, method: str, **params) -> str:
        """Generate cache key for API request"""
        key_data = f"{method}_{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def get_channel_data(
        self, 
        channel_id: str, 
        include_recent_videos: bool = True,
        video_count: int = 20,
        user_id: Optional[str] = None
    ) -> Optional[YouTubeChannelMetrics]:
        """Get comprehensive channel data with caching"""
        
        cache_key = self._generate_cache_key(
            "channel_data", 
            channel_id=channel_id, 
            include_videos=include_recent_videos,
            video_count=video_count,
            user_id=user_id
        )
        
        # Check cache first
        cached_data = self._cache_get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for channel data: {channel_id}")
            return YouTubeChannelMetrics(**cached_data)
        
        # Get appropriate service (OAuth if available, otherwise API key)
        youtube_service = await self.get_authenticated_service(user_id) if user_id else self.youtube
        
        if not youtube_service:
            logger.error("YouTube API client not available")
            return None
        
        try:
            # Check quota
            if not self.quota_manager.check_quota('channels.list'):
                logger.error("YouTube API quota exceeded")
                return None
            
            # Get channel info
            channel_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: youtube_service.channels().list(
                    part='snippet,statistics,brandingSettings',
                    id=channel_id
                ).execute()
            )
            
            self.quota_manager.consume_quota('channels.list')
            
            if not channel_response.get('items'):
                logger.warning(f"Channel not found: {channel_id}")
                return None
            
            channel_info = channel_response['items'][0]
            snippet = channel_info['snippet']
            statistics = channel_info['statistics']
            
            # Get recent videos if requested
            recent_videos = []
            if include_recent_videos:
                recent_videos = await self.get_recent_videos(channel_id, video_count, user_id)
            
            # Calculate aggregated metrics
            avg_views_last_30 = 0.0
            avg_engagement_last_30 = 0.0
            upload_frequency = "unknown"
            
            if recent_videos:
                # Calculate average views
                recent_views = [video.view_count for video in recent_videos]
                avg_views_last_30 = sum(recent_views) / len(recent_views)
                
                # Calculate average engagement
                recent_engagement = [video.engagement_rate for video in recent_videos]
                avg_engagement_last_30 = sum(recent_engagement) / len(recent_engagement)
                
                # Estimate upload frequency
                upload_frequency = self._calculate_upload_frequency(recent_videos)
            
            # Create channel metrics object
            channel_metrics = YouTubeChannelMetrics(
                channel_id=channel_id,
                title=snippet.get('title', ''),
                description=snippet.get('description', ''),
                custom_url=snippet.get('customUrl'),
                published_at=snippet.get('publishedAt', ''),
                thumbnail_url=snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                country=snippet.get('country'),
                view_count=int(statistics.get('viewCount', 0)),
                subscriber_count=int(statistics.get('subscriberCount', 0)),
                video_count=int(statistics.get('videoCount', 0)),
                recent_videos=recent_videos,
                avg_views_last_30=avg_views_last_30,
                avg_engagement_last_30=avg_engagement_last_30,
                upload_frequency=upload_frequency
            )
            
            # Cache the result (4 hours TTL for channel data)
            self._cache_set(cache_key, asdict(channel_metrics), ttl=14400)
            
            return channel_metrics
            
        except HttpError as e:
            logger.error(f"YouTube API error getting channel data: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting channel data: {e}")
            return None
    
    async def get_recent_videos(
        self, 
        channel_id: str, 
        count: int = 20,
        user_id: Optional[str] = None
    ) -> List[YouTubeVideoMetrics]:
        """Get recent videos for a channel"""
        
        cache_key = self._generate_cache_key("recent_videos", channel_id=channel_id, count=count, user_id=user_id)
        
        # Check cache
        cached_data = self._cache_get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for recent videos: {channel_id}")
            return [YouTubeVideoMetrics(**video) for video in cached_data]
        
        # Get appropriate service (OAuth if available, otherwise API key)
        youtube_service = await self.get_authenticated_service(user_id) if user_id else self.youtube
        
        if not youtube_service:
            return []
        
        try:
            # Check quota for search
            if not self.quota_manager.check_quota('search.list'):
                logger.error("YouTube API quota exceeded for search")
                return []
            
            # Search for recent videos
            logger.info(f"Searching for videos from channel: {channel_id}, count: {min(count, 50)}")
            search_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: youtube_service.search().list(
                    part='id,snippet',
                    channelId=channel_id,
                    type='video',
                    order='date',
                    maxResults=min(count, 50)
                ).execute()
            )
            
            self.quota_manager.consume_quota('search.list')
            
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                logger.warning(f"No videos found for channel {channel_id}")
                return []
            
            # Get detailed video information
            videos = await self.get_video_details(video_ids, user_id)
            
            # Cache the result (2 hours TTL for recent videos)
            videos_dict = [asdict(video) for video in videos]
            self._cache_set(cache_key, videos_dict, ttl=7200)
            
            return videos
            
        except HttpError as e:
            logger.error(f"YouTube API error getting recent videos: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting recent videos: {e}")
            return []
    
    async def get_video_details(self, video_ids: List[str], user_id: Optional[str] = None) -> List[YouTubeVideoMetrics]:
        """Get detailed information for specific videos"""
        
        # Get appropriate service (OAuth if available, otherwise API key)
        youtube_service = await self.get_authenticated_service(user_id) if user_id else self.youtube
        
        if not youtube_service or not video_ids:
            return []
        
        try:
            # Check quota
            if not self.quota_manager.check_quota('videos.list'):
                logger.error("YouTube API quota exceeded for video details")
                return []
            
            # Get video details
            videos_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: youtube_service.videos().list(
                    part='snippet,statistics,contentDetails,status',
                    id=','.join(video_ids)
                ).execute()
            )
            
            self.quota_manager.consume_quota('videos.list')
            
            videos = []
            for video in videos_response.get('items', []):
                video_id = video['id']
                snippet = video['snippet']
                statistics = video['statistics']
                content_details = video['contentDetails']
                
                # Calculate engagement metrics
                view_count = int(statistics.get('viewCount', 0))
                like_count = int(statistics.get('likeCount', 0))
                comment_count = int(statistics.get('commentCount', 0))
                
                engagement_rate = 0.0
                if view_count > 0:
                    engagement_rate = ((like_count + comment_count) / view_count) * 100
                
                # Estimate CTR and retention (simplified)
                ctr_estimate = min(10.0, max(1.0, engagement_rate * 0.8))
                retention_estimate = min(90.0, max(20.0, 60 + (engagement_rate * 2)))
                
                video_metrics = YouTubeVideoMetrics(
                    video_id=video_id,
                    title=snippet.get('title', ''),
                    description=snippet.get('description', ''),
                    tags=snippet.get('tags', []),
                    published_at=snippet.get('publishedAt', ''),
                    thumbnail_url=snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    duration=parse_duration(content_details.get('duration', '')),
                    view_count=view_count,
                    like_count=like_count,
                    comment_count=comment_count,
                    definition=content_details.get('definition', 'hd'),
                    category_id=snippet.get('categoryId', ''),
                    default_language=snippet.get('defaultLanguage'),
                    engagement_rate=engagement_rate,
                    ctr_estimate=ctr_estimate,
                    retention_estimate=retention_estimate
                )
                
                videos.append(video_metrics)
            
            return videos
            
        except HttpError as e:
            logger.error(f"YouTube API error getting video details: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting video details: {e}")
            return []
    
    async def get_channel_analytics(
        self,
        channel_id: str,
        user_id: str,
        start_date: str = None,
        end_date: str = None,
        metrics: List[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get YouTube Analytics data for authenticated channel owner"""
        
        if not metrics:
            metrics = [
                'views', 'estimatedMinutesWatched', 'averageViewDuration',
                'subscribersGained', 'subscribersLost', 'likes', 'dislikes',
                'comments', 'shares'
            ]
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        cache_key = self._generate_cache_key(
            "channel_analytics",
            channel_id=channel_id,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            metrics=",".join(metrics)
        )
        
        # Check cache
        cached_data = self._cache_get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for channel analytics: {channel_id}")
            return cached_data
        
        try:
            # Get authenticated YouTube Analytics service
            analytics_service = await self.get_authenticated_service(user_id, "youtubeAnalytics", "v2")
            
            if not analytics_service:
                logger.error(f"No authenticated analytics service for user {user_id}")
                return None
            
            # Get analytics data
            analytics_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: analytics_service.reports().query(
                    ids=f"channel=={channel_id}",
                    startDate=start_date,
                    endDate=end_date,
                    metrics=",".join(metrics),
                    dimensions="day"
                ).execute()
            )
            
            # Process analytics data
            analytics_data = {
                "channel_id": channel_id,
                "start_date": start_date,
                "end_date": end_date,
                "metrics": metrics,
                "column_headers": analytics_response.get("columnHeaders", []),
                "rows": analytics_response.get("rows", []),
                "totals": {}
            }
            
            # Calculate totals
            if analytics_response.get("rows"):
                headers = [col["name"] for col in analytics_response.get("columnHeaders", [])]
                for i, metric in enumerate(metrics):
                    if metric in headers:
                        metric_index = headers.index(metric)
                        total = sum(row[metric_index] for row in analytics_response["rows"] if len(row) > metric_index)
                        analytics_data["totals"][metric] = total
            
            # Cache the result (4 hours TTL for analytics)
            self._cache_set(cache_key, analytics_data, ttl=14400)
            
            logger.info(f"Retrieved analytics data for channel {channel_id}")
            return analytics_data
            
        except Exception as e:
            logger.error(f"Error getting channel analytics: {e}")
            return None
    
    async def get_video_comments(
        self, 
        video_id: str, 
        max_results: int = 100
    ) -> List[YouTubeCommentData]:
        """Get comments for sentiment analysis"""
        
        cache_key = self._generate_cache_key("video_comments", video_id=video_id, max_results=max_results)
        
        # Check cache
        cached_data = self._cache_get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for video comments: {video_id}")
            return [YouTubeCommentData(**comment) for comment in cached_data]
        
        if not self.youtube:
            return []
        
        try:
            # Check quota
            if not self.quota_manager.check_quota('commentThreads.list'):
                logger.error("YouTube API quota exceeded for comments")
                return []
            
            # Get comment threads
            comments_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=min(max_results, 100),
                    order='relevance'
                ).execute()
            )
            
            self.quota_manager.consume_quota('commentThreads.list')
            
            comments = []
            for item in comments_response.get('items', []):
                top_comment = item['snippet']['topLevelComment']['snippet']
                
                comment_data = YouTubeCommentData(
                    comment_id=item['snippet']['topLevelComment']['id'],
                    video_id=video_id,
                    author_name=top_comment.get('authorDisplayName', ''),
                    text=top_comment.get('textDisplay', ''),
                    like_count=int(top_comment.get('likeCount', 0)),
                    published_at=top_comment.get('publishedAt', ''),
                    reply_count=item['snippet'].get('totalReplyCount', 0)
                )
                
                comments.append(comment_data)
                
                # Add replies if available
                if 'replies' in item:
                    for reply in item['replies']['comments']:
                        reply_snippet = reply['snippet']
                        reply_data = YouTubeCommentData(
                            comment_id=reply['id'],
                            video_id=video_id,
                            author_name=reply_snippet.get('authorDisplayName', ''),
                            text=reply_snippet.get('textDisplay', ''),
                            like_count=int(reply_snippet.get('likeCount', 0)),
                            published_at=reply_snippet.get('publishedAt', ''),
                            parent_id=comment_data.comment_id
                        )
                        comments.append(reply_data)
            
            # Cache comments (1 hour TTL)
            comments_dict = [asdict(comment) for comment in comments]
            self._cache_set(cache_key, comments_dict, ttl=3600)
            
            return comments
            
        except HttpError as e:
            logger.error(f"YouTube API error getting comments: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting comments: {e}")
            return []
    
    def _calculate_upload_frequency(self, videos: List[YouTubeVideoMetrics]) -> str:
        """Calculate upload frequency from recent videos"""
        if len(videos) < 2:
            return "unknown"
        
        try:
            # Parse publish dates
            dates = []
            for video in videos:
                date = datetime.fromisoformat(video.published_at.replace('Z', '+00:00'))
                dates.append(date)
            
            # Sort by date
            dates.sort()
            
            # Calculate average days between uploads
            intervals = []
            for i in range(1, len(dates)):
                interval = (dates[i] - dates[i-1]).days
                intervals.append(interval)
            
            if not intervals:
                return "unknown"
            
            avg_interval = sum(intervals) / len(intervals)
            
            # Categorize frequency
            if avg_interval <= 1.5:
                return "daily"
            elif avg_interval <= 4:
                return "2-3 times per week"
            elif avg_interval <= 8:
                return "weekly"
            elif avg_interval <= 15:
                return "bi-weekly"
            elif avg_interval <= 32:
                return "monthly"
            else:
                return "irregular"
                
        except Exception as e:
            logger.error(f"Error calculating upload frequency: {e}")
            return "unknown"
    
    async def search_competitor_channels(
        self, 
        query: str, 
        max_results: int = 10
    ) -> List[str]:
        """Search for competitor channels by keyword"""
        
        cache_key = self._generate_cache_key("competitor_search", query=query, max_results=max_results)
        
        # Check cache
        cached_data = self._cache_get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for competitor search: {query}")
            return cached_data
        
        if not self.youtube:
            return []
        
        try:
            # Check quota
            if not self.quota_manager.check_quota('search.list'):
                logger.error("YouTube API quota exceeded for competitor search")
                return []
            
            # Search for channels
            search_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.youtube.search().list(
                    part='id,snippet',
                    q=query,
                    type='channel',
                    maxResults=min(max_results, 25),
                    order='relevance'
                ).execute()
            )
            
            self.quota_manager.consume_quota('search.list')
            
            channel_ids = [item['id']['channelId'] for item in search_response.get('items', [])]
            
            # Cache results (24 hours TTL for competitor searches)
            self._cache_set(cache_key, channel_ids, ttl=86400)
            
            return channel_ids
            
        except HttpError as e:
            logger.error(f"YouTube API error searching competitors: {e}")
            return []
        except Exception as e:
            logger.error(f"Error searching competitors: {e}")
            return []
    
    def get_api_status(self) -> Dict[str, Any]:
        """Get YouTube API integration status"""
        return {
            "api_available": self.youtube is not None,
            "api_key_configured": self.api_key is not None,
            "quota_status": self.quota_manager.get_quota_status(),
            "cache_stats": {
                "size": len(self.simple_cache),
                "keys": list(self.simple_cache.keys())[:5]  # Show first 5 keys
            }
        }

# Global YouTube API integration instance
_youtube_integration = None

def get_youtube_integration() -> YouTubeAPIIntegration:
    """Get or create global YouTube API integration instance"""
    global _youtube_integration
    if _youtube_integration is None:
        _youtube_integration = YouTubeAPIIntegration()
    return _youtube_integration

async def get_channel_analytics(channel_id: str) -> Optional[YouTubeChannelMetrics]:
    """Convenience function to get channel analytics"""
    integration = get_youtube_integration()
    return await integration.get_channel_data(channel_id, include_recent_videos=True)

async def get_video_analytics(video_ids: List[str]) -> List[YouTubeVideoMetrics]:
    """Convenience function to get video analytics"""
    integration = get_youtube_integration()
    return await integration.get_video_details(video_ids)

async def get_comments_for_analysis(video_id: str, max_comments: int = 100) -> List[YouTubeCommentData]:
    """Convenience function to get comments for sentiment analysis"""
    integration = get_youtube_integration()
    return await integration.get_video_comments(video_id, max_comments)